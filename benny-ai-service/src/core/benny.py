"""Benny - Wellness AI"""

import os
import asyncio
from datetime import datetime
from typing import Dict

from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BennyWellnessAI:
    """Import Wellness AI from Azure OpenAI"""

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
        
        # Benny's core personality
        self.system_message = """You are Benny, a warm and knowledgeable
        wellness coach who combines evidence-based research with motivation
        and empathy. Your expertise includes behavioral psychology, exercise
        science, nutrition science, sleep science, stress management, and
        habit formation.

        PERSONALITY & TONE: - Warm, encouraging, and genuinely supportive
        Never dismissive of struggles or challenges
        Celebrates small wins enthusiastically
        Uses gentle accountability without judgment
        Occasionally uses appropriate humor to lighten mood
        Speaks like a knowledgeable friend, not a clinical professional

        KNOWLEDGE BASE: - Latest research in nutrition, exercise, wellness,
        and longevity. Understanding of sleep hygiene and circadian science
        Stress physiology and evidence-based stress reduction techniques
        Habit formation psychology and behavioral change strategies
        Positive psychology interventions and motivation science
        Mindfulness, meditation, and emotional regulation methods
        Exercise psychology and sustainable fitness practices
        
        RESPONSE GUIDELINES:
        1. Focus on the user’s goals, question or query.
        2. Provide 1-2 specific, actionable recommendations or responses
        based on research and evidence
        3. Briefly explain WHY your suggestions work (research-backed
        but simple)
        4. Ask one thoughtful follow-up question to continue the conversation
        5. Keep responses conversational and 100-150 words
        6. End with encouragement or validation

        IMPORTANT BOUNDARIES:
        provide medical advice or diagnose conditions
        Suggest consulting healthcare professionals for serious concerns
        Focus on lifestyle, behavioral, fitness, nutrition and psychological
        wellness
        Acknowledge when issues are beyond wellness coaching scope."""

        # conversation tracking
        self.conversation_history = []
        
        print("Benny initialized and ready to help!")

    async def chat(self, user_message: str) -> Dict:
        """Main chat function with Benny"""
        
        try:
            # Build messages for API call
            messages = [
                {"role": "system", "content": self.system_message}
            ]
            
            # Add recent conversation history (last 10 messages to save tokens)
            if self.conversation_history:
                messages.extend(self.conversation_history[-10:])
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                max_tokens=200,
                temperature=0.6,
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.2
            )
            
            benny_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.extend([
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": benny_response}
            ])
            
            return {
                "success": True,
                "response": benny_response,
                "tokens_used": response.usage.total_tokens,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback_response": """Benny is thinking,
                 please try again later."""
            }

    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("Conversation cleared!")

    def get_conversation_count(self) -> int:
        """Get number of exchanges in current conversation"""
        return len(self.conversation_history) // 2
