"""
AI Service - Content generation, sentiment analysis, and more
Port: 8011
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

app = FastAPI(
    title="AI Service",
    version="1.0.0",
    description="AI-powered content generation, sentiment analysis, and more"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI integration
try:
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY', '')
    OPENAI_AVAILABLE = bool(openai.api_key)
except:
    OPENAI_AVAILABLE = False

# Schemas
class ContentGenerationRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.7

class SentimentAnalysisRequest(BaseModel):
    text: str

class ContentGenerationResponse(BaseModel):
    generated_text: str
    tokens_used: int

class SentimentAnalysisResponse(BaseModel):
    sentiment: str  # positive, negative, neutral
    confidence: float
    scores: dict

@app.get("/")
async def root():
    return {
        "service": "AI Service",
        "status": "running",
        "version": "1.0.0",
        "openai_available": OPENAI_AVAILABLE
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "openai_available": OPENAI_AVAILABLE}

@app.post("/generate/content", response_model=ContentGenerationResponse)
async def generate_content(request: ContentGenerationRequest):
    """Generate content using AI"""
    if not OPENAI_AVAILABLE:
        # Placeholder response
        return ContentGenerationResponse(
            generated_text=f"Generated content for: {request.prompt}",
            tokens_used=100
        )
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return ContentGenerationResponse(
            generated_text=response.choices[0].text.strip(),
            tokens_used=response.usage.total_tokens
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

@app.post("/analyze/sentiment", response_model=SentimentAnalysisResponse)
async def analyze_sentiment(request: SentimentAnalysisRequest):
    """Analyze sentiment of text"""
    # TODO: Use actual sentiment analysis model (VADER, TextBlob, or ML model)
    # For now, simple placeholder
    
    text_lower = request.text.lower()
    positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'happy']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'sad', 'disappointed']
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = "positive"
        confidence = min(0.9, 0.5 + (positive_count * 0.1))
    elif negative_count > positive_count:
        sentiment = "negative"
        confidence = min(0.9, 0.5 + (negative_count * 0.1))
    else:
        sentiment = "neutral"
        confidence = 0.5
    
    return SentimentAnalysisResponse(
        sentiment=sentiment,
        confidence=confidence,
        scores={
            "positive": positive_count,
            "negative": negative_count,
            "neutral": 1 - abs(positive_count - negative_count) / max(len(text_lower.split()), 1)
        }
    )

@app.post("/generate/product-description")
async def generate_product_description(
    product_name: str,
    category: str,
    features: List[str]
):
    """Generate product description using AI"""
    prompt = f"Write a compelling product description for {product_name} in the {category} category. Features: {', '.join(features)}"
    
    if not OPENAI_AVAILABLE:
        return {
            "description": f"Discover {product_name}, a premium {category} product featuring {', '.join(features)}. Perfect for your needs!"
        }
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        
        return {
            "description": response.choices[0].text.strip()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Description generation failed: {str(e)}")

@app.post("/generate/post-caption")
async def generate_post_caption(
    image_description: Optional[str] = None,
    mood: Optional[str] = "casual"
):
    """Generate social media post caption"""
    prompt = f"Generate a {mood} social media post caption"
    if image_description:
        prompt += f" for an image showing: {image_description}"
    
    if not OPENAI_AVAILABLE:
        return {
            "caption": "Check out this amazing product! #socialcommerce #shopping"
        }
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.8
        )
        
        return {
            "caption": response.choices[0].text.strip()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Caption generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
