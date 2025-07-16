"""
Test script for Multi-Mode Benny
Run this to verify all modes work properly
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from core.benny import BennyWellnessAI, BennyMode

async def test_mode_comparison():
    """Test the same message in different modes to see the difference"""
    
    print("Test Benny Modes")
    print("=" * 60)
    
    benny = BennyWellnessAI()
    test_message = "How can I eat more fiber?"
    
    print(f"Test Message: '{test_message}'\n")
    
    # Test different modes
    modes_to_test = [
        (BennyMode.CONVERSATIONAL, "💬 Conversational Mode"),
        (BennyMode.RECOMMENDATIONS, "🎯 Recommendation Mode")
    ]
    
    for mode, mode_name in modes_to_test:
        print(f"{mode_name}")
        print("-" * 40)
        
        result = await benny.chat(test_message, mode)
        
        if result["success"]:
            print(f"Benny: {result['response']}")
            print(f"Tokens: {result['tokens_used']} | Mode: {result['mode']}")
        else:
            print(f"Error: {result.get('error')}")
            print(f"Fallback: {result.get('fallback_response')}")
        
        print("\n")


async def main():
    """Run all tests"""
    
    print("Starting Multi-Mode Benny Tests\n")
    
    try:
        await test_mode_comparison()
        
    except Exception as e:
        print(f" Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())