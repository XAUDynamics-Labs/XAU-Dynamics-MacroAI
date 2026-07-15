import asyncio
import os
import json
from datetime import datetime
from pydantic import BaseModel, Field
from openai import AsyncAzureOpenAI
import aiohttp

# Ensure required environment variables for Cloud/Azure deployment
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://xau-dynamics-ai.openai.azure.com/")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "dummy_key_for_local_testing")
TRADEBRIDGE_API_URL = os.getenv("TRADEBRIDGE_API_URL", "http://tradebridge:8000/api/v1/alerts/news")

# Initialize Azure OpenAI Async Client (Targeting Microsoft Infrastructure)
client = AsyncAzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-15-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

class TradingDirective(BaseModel):
    event_id: str = Field(..., description="UUID of the macroeconomic event")
    sentiment_score: float = Field(..., description="Sentiment score from -1.0 (Extreme Bearish) to 1.0 (Extreme Bullish)")
    market_impact: str = Field(..., description="Expected impact: HIGH, MEDIUM, LOW")
    action: str = Field(..., description="Strict directive: BUY, SELL, HOLD, HALT_TRADING")
    confidence: float = Field(..., description="AI confidence level in the analysis (0.0 to 1.0)")
    reasoning: str = Field(..., description="Brief 1-sentence explanation of the AI decision")

async def analyze_macroeconomic_text(event_id: str, raw_text: str) -> TradingDirective:
    """
    Sends raw macroeconomic text to the Azure OpenAI model to determine market sentiment 
    and generate a strict JSON trading directive for XAUUSD.
    """
    system_prompt = """
    You are an elite quantitative analyst specializing in Gold (XAUUSD). 
    Analyze the provided macroeconomic data/speech. 
    Respond ONLY in strict JSON matching the requested schema. 
    Focus on liquidity risks and institutional order flow implications.
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo", # Targeted deployment name
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Event ID: {event_id}\nRaw Data: {raw_text}"}
            ],
            temperature=0.1, # Low temperature for deterministic financial output
            max_tokens=250
        )
        
        # Parse output directly into our strict Pydantic model
        result_dict = json.loads(response.choices[0].message.content)
        directive = TradingDirective(**result_dict)
        return directive
        
    except Exception as e:
        print(f"[{datetime.utcnow()}] CRITICAL AI FAILURE: {e}")
        # Fail-safe mechanism: Halt trading if AI engine fails
        return TradingDirective(
            event_id=event_id,
            sentiment_score=0.0,
            market_impact="HIGH",
            action="HALT_TRADING",
            confidence=0.0,
            reasoning="AI Engine latency or failure. Triggering defensive halt."
        )

async def push_to_tradebridge(directive: TradingDirective):
    """Pushes the computed directive to the TradeBridge API Gateway."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(TRADEBRIDGE_API_URL, json=directive.model_dump()) as response:
                if response.status == 201:
                    print(f"[{datetime.utcnow()}] SUCCESS: Directive pushed to TradeBridge -> {directive.action}")
                else:
                    print(f"[{datetime.utcnow()}] BRIDGE ERROR: Status {response.status}")
        except Exception as e:
            print(f"[{datetime.utcnow()}] NETWORK ERROR: Cannot reach TradeBridge API -> {e}")

# Example execution flow for demonstration purposes
async def main():
    print(f"[{datetime.utcnow()}] Starting XAU Dynamics - MacroAI Engine...")
    sample_news = "US Non-Farm Payrolls absolutely crushed expectations, coming in at 353K vs 180K expected. Wage growth also surged."
    
    print(f"[{datetime.utcnow()}] Analyzing incoming data stream...")
    directive = await analyze_macroeconomic_text("NFP-FEB-2026", sample_news)
    
    print(f"[{datetime.utcnow()}] Analysis Complete. Action: {directive.action}, Confidence: {directive.confidence}")
    await push_to_tradebridge(directive)

if __name__ == "__main__":
    asyncio.run(main())
