"""Benny - Wellness AI"""

import os, sys
from datetime import datetime
from typing import Dict, Optional
from enum import Enum
from pathlib import Path

from openai import AzureOpenAI
from dotenv import load_dotenv

# import db
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "bennyDB"))
import db_connector_real

# Load environment variables
load_dotenv()


class BennyMode(Enum):
    """Different response styles for Benny"""
    CHAT = "chat"
    RECOMMEND = "recommend"
 

class BennyWellnessAI:
    """Core Benny AI implementation"""

    # Base personality for all modes
    BASE_PERSONALITY = """ You are Benny, you a warm and
    motivational wellness coach who uses evidence-based
    research with psychology to provide education, motivation
    and encouragement. You have a strong knowledge of nutrition,
    exercise science, physiology, kinesiology, sleep science,
    behavioral psychology, and psychological wellness. You
    do not provide medical advice.
    """

    # Mode configurations
    MODE = {
        BennyMode.CHAT: {
            "prompt": """
            - Respond to their question, comment, or insight with curiosity,
            - motivation, or understanding
            - Provide 1 actionable recommendation
            - Give 1-2 reasons why this action works (research based,
            - but simple)
            - Keep responses to 150 words
            - Ask one thoughtful follow-up question
            - If user wants suggestions, give 1 or 2 max to keep chat shorter
            """,
            "max_tokens": 150,
            "temperature": 0.6
        },
        BennyMode.RECOMMEND: {
            "prompt": """
            - Analyze the daily check-in data
            (nutrition, fitness, stress, sleep)
            - Identify the area that needs the most improvement
            - Give exactly one sentence of actionable advice
            - include specific numbers, times, or techniques
            """,
            "max_tokens": 50,
            "temperature": 0.4,
        }
    }

    def __init__(self):
        """Initialize Benny with Azure OpenAI"""

        # Get configuration from environment
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")

        # Validate configuration
        if not self.endpoint or not self.api_key:
            raise ValueError("Missing Azure OpenAI credentials")
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version="2025-01-01-preview"
        )

        # conversation tracking
        self.conversation_history = []

        # db connection
        self.db = db_connector_real.wellness_ai_db()
        
        print("Benny initialized successful!")

    async def chat(self, message: str) -> Dict: 
        """
        Chat with Benny
        Args:
            message: User's message
        
        Returns: 
            Response dictionary with chat response
        """
        # Generate response
        response = await self._generate_response(
            message=message,
            mode=BennyMode.CHAT
        )
        # save chat to db
        if response["success"]:
            await self._save_chat_to_db(message, response["response"])

        return response
    
    async def _save_chat_to_db(self, user_message: str, benny_response: str):
        """Save chat to database"""
        try:
            today = datetime.now().strftime("%m/%d/%Y")

            # check if chat exists today, if not create
            existing_chat = self.db.fetch_main_chat_history_pk(today)
            if not existing_chat:
                self.db.insert_row_chat_history_main(today)
                # refetch
                existing_chat = self.db.fetch_main_chat_history_pk(today)
            
            # get number of entries
            existing_entries = self.db.fetch_chat_logs_by_date(today)
            seq_num = len(existing_entries) + 1

            self.db.add_chat_entry(today, seq_num, 0, user_message)
            self.db.add_chat_entry(today, seq_num + 1, 1, benny_response)
            print("Chat saved to Database")
        
        except Exception as e:
            print(f"Error saving to database: {e}")
    
    async def recommend(self, daily_checkin: Dict) -> Dict:
        """
        Get wellness recommendation based on daily check-in from user
        Args:
            daily_checkin: Dict with keys:
                nutrition, fitness, stress, sleep

        Returns: Response dictionary with one-sentence recommendation
        """
        checkin_message = self._format_checkin(daily_checkin)

        benny_prompt = f"""
        Here is today's check in Data: 
        {checkin_message}
        Do not repeat the checkin data to the user, instead
        respond with one simple, actionable goal that will
        make the biggest positive impact based on their response.
        If all areas are good, give one actionable goal to improve.
        Keep the suggestion short, to one actionable sentence and remain positive.
        """

        return await self._generate_response(
            message=benny_prompt,
            mode=BennyMode.RECOMMEND
        )
    
    def _format_checkin(self, daily_checkin: Dict) -> str:
        """Format daily checkin-data to send to ai"""
        message = ""

        for response in daily_checkin:
            if response == "nutrition":
                message += f"Today my nutrition was {daily_checkin[response]}. "
            elif response == "fitness":
                message += f"Was I able to complete my planned fitness: {daily_checkin[response]} "
            elif response == "stress":
                message += f"My stress was {daily_checkin[response]}. "
            elif response == "sleep":
                message += f"My sleep quality was {daily_checkin[response]}. "
        
        return message

    async def _generate_response(self, message: str, mode: BennyMode) -> Dict:
        """Internal method to generate response response"""

        try:
            # get the system prompt for this mode
            config = self.MODE[mode]
            system_prompt = self.BASE_PERSONALITY + config["prompt"]

            # Build messages for API call
            messages = [{"role": "system", "content": system_prompt}]

            # add convo history for conversational mode (10 tokens)
            if mode == BennyMode.CHAT and self.conversation_history:
                messages.extend(self.conversation_history[-10:])
            
            messages.append({"role": "user", "content": message})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                max_tokens=config["max_tokens"],
                temperature=config["temperature"],
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.2
            )
            
            benny_response = response.choices[0].message.content.strip()
            
            # Update conversation history
            if mode == BennyMode.CHAT:
                self.conversation_history.extend([
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": benny_response}
                ])
            
            return {
                "success": True,
                "response": benny_response,
                "mode": mode.value,
                "tokens_used": response.usage.total_tokens,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "mode": mode.value,
                "response": self._get_fallback_response(mode),
                "timestamp": datetime.now().isoformat()
            }
   
    def _get_fallback_response(self, mode: BennyMode) -> str:
        """default response for each mode"""

        fallbacks = {
            BennyMode.CHAT: """Benny: Taking a little break, please try
            again later.""",
            BennyMode.RECOMMEND: """Take a deep breath and try a 5-minute 
            walk outside."""
        }

        return fallbacks[mode]

    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        return {"success": True, "message": "Conversation history cleared"}