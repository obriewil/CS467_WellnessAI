"""Benny - Wellness AI"""

import os
import asyncio
from datetime import datetime
from typing import Dict
from enum import Enum

from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BennyMode(Enum):
    """Different response styles for Benny"""
    CONVERSATIONAL = "conversational"
    RECOMMENDATIONS = "recommendations"


class BennyPrompts:
    """Prompt templates for different Benny Modes"""

    @staticmethod
    def get_system_prompt(mode: BennyMode) -> str:
        """Get the system prompt for the chosen mode"""

        base_personality = """
            You are Benny, a warm and knowledgeable
            wellness coach who combines evidence-based research with motivation
            and empathy. Your expertise includes behavioral psychology, exercise
            science, nutrition science, sleep science, stress management, and
            habit formation.

            KNOWLEDGE BASE: - Latest research in nutrition, exercise, wellness,
            and longevity. Understanding of sleep hygiene and circadian science
            Stress physiology and evidence-based stress reduction techniques
            Habit formation psychology and behavioral change strategies
            Positive psychology interventions and motivation science
            Mindfulness, meditation, and emotional regulation methods
            Exercise psychology and sustainable fitness practices

            IMPORTANT BOUNDARIES:
            do not provide medical advice or diagnose conditions
            Suggest consulting healthcare professionals for serious concerns
            Focus on lifestyle, behavioral, fitness, nutrition and psychological
            wellness
            Acknowledge when issues are beyond wellness coaching scope.
        """

        prompts = {
            BennyMode.CONVERSATIONAL:
            f"""{base_personality}
            CONVERSATIONAL MODE:
            - Warm, encouraging, motivational personality
            - Focus on the question asked, give direct 1-2 sentence response
            based on evidence but is simple terms
            - Offer guidance and accountability with focus on progress
            - Keep Responses to 150-200 words

            RESPONSE STYLE:
            1. Acknowledge question or feelings first
            2. Provide 1-2 specific actionable recommendations
            3. Simply explain why suggestion works
            4. Ask one thoughtful follow up question""",

            BennyMode.RECOMMENDATIONS:
            f"""{base_personality}
            - Give EXACTLY ONE SENTENCE of wellness advice
            - Be encouraging but brief and direct
            - Focus on actionable, specific guidance
            - NO follow-up questions - just the recommendation

            RESPONSE STYLE:
            - ONE sentence only
            - Actionable advice
            - Encouraging tone
            """
            }
        
        return prompts[mode]


class BennyWellnessAI:
    """Multi-Mode Benny implementation"""

    def __init__(self):
        """Initialize Benny with Azure OpenAI"""

        # Get configuration from environment
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")

        # Validate configuration
        if not self.endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT not found in environment")
        if not self.api_key:
            raise ValueError("AZURE_OPENAI_API_KEY not found in environment")
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version="2025-01-01-preview"
        )

        # conversation tracking
        self.conversation_history = []
        
        print("Benny initialized and ready to help!")

    async def chat(self, user_message: str, mode: BennyMode =BennyMode.CONVERSATIONAL, user_id: str=None) -> Dict:
        """Main chat function with Benny"""
        
        try:
            # get the system prompt for this mode
            system_prompt = BennyPrompts.get_system_prompt(mode)

            # Build messages for API call
            messages = [{"role": "system", "content": system_prompt}]

            # add convo history for conversational mode (10 tokens)
            if mode == BennyMode.CONVERSATIONAL and self.conversation_history:
                messages.extend(self.conversation_history[-10:])
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Set parameters for mode
            params = self._get_mode_parameters(mode)
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                **params
            )
            
            benny_response = response.choices[0].message.content
            
            # Update conversation history
            if mode == BennyMode.CONVERSATIONAL:
                self.conversation_history.extend([
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": benny_response}
                ])
            
            return {
                "success": True,
                "response": benny_response,
                "tokens_used": response.usage.total_tokens,
                "mode": mode.value,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback_response": self._get_fallback_response(mode),
                "mode": mode.value,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id
            }
    
    def _get_mode_parameters(self, mode: BennyMode) -> Dict:
        """Get API params for each mode"""

        mode_params = {
            BennyMode.CONVERSATIONAL: {
                "max_tokens": 250,
                "temperature": 0.6,
                "top_p": 0.9,
                "frequency_penalty": 0.3,
                "presence_penalty": 0.2
            },
            BennyMode.RECOMMENDATIONS: {
                "max_tokens": 50,
                "temperature": 0.4,
                "top_p": 0.9,
                "frequency_penalty": 0.3,
                "presence_penalty": 0.2
            }
        }

        return mode_params[mode]
    
    def _get_fallback_response(self, mode: BennyMode) -> str:
        """default response for each mode"""

        fallbacks = {
            BennyMode.CONVERSATIONAL: "Benny: Taking a little break, please try again later.",
            BennyMode.RECOMMENDATIONS: "Take a deep breath and try a 5-minute walk outside."
        }

        return fallbacks[mode]

    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("Conversation cleared!")

    def get_conversation_count(self) -> int:
        """Get number of exchanges in current conversation"""
        return len(self.conversation_history) // 2
