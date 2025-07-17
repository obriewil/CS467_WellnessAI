"""Simple unit tests for Benny Wellness AI"""

import unittest
import asyncio
from src.core.benny import BennyWellnessAI


class TestBennyWelness(unittest.TestCase):
    """Test cases for Benny Wellness AI"""

    @classmethod
    def setUpClass(cls):
        """Initialize Benny for all test"""
        try:
            cls.benny = BennyWellnessAI()
            cls.setup_success = True
        except Exception as e:
            print(f"Setup failed: {e}")
            cls.setup_success = False

    def setUp(self):
        """Check benny is initialized"""
        if not self.setup_success:
            self.skipTest("Benny initialization failed")

    def test_1_init(self):
        """Test Benny Initialized Correctly"""
        self.assertIsNotNone(self.benny)
        self.assertIsNotNone(self.benny.client)
        print("Initialization test passed")
        print("=============================\n")

    def test_2_chat_simple(self):
        """Test Chat Intro"""
        message = "Hello Benny"
        result = asyncio.run(self.benny.chat(message))

        self.assertTrue(result["success"])
        self.assertIn("response", result)
        self.assertGreater(len(result["response"]), 0)
        self.assertGreater(result["tokens_used"], 0)

        print("\n=============================\n")
        print(f"User: {message}")
        print(f"\n Benny: {result['response']}")
        print("Chat Test Passed")
        print("=============================\n")

    def test_3_wellness_chat(self):
        """Test Chat with Wellness Topic"""
        message = "How can I improve my endurance?"
        result = asyncio.run(self.benny.chat(message))
        
        self.assertTrue(result["success"])
        self.assertIn("response", result)
        
        print("\n=============================\n")
        print(f"User: {message}")
        print(f"Benny: {result['response']}")
        print("Wellness Chat Test Passed")
        print("=============================\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)