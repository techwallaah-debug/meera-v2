"""
Search Service - Handles full-text search with Elasticsearch
Port: 8005
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from shared.database.connection import get_db
from shared.auth.jwt import verify_token
from fastapi.security import OAuth2PasswordBearer

# Elasticsearch
try:
    from elasticsearch import Elasticsearch
    es_client = Elasticsearch(
        [os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')],
        timeout=30,
        max_retries=10,
        retry_on_timeout=True
    )
    ES_ENABLED = True
except:
    ES_ENABLED = False

app = FastAPI(
    title="Search Service",
    version="1.0.0",
    description="Full-text search with Elasticsearch"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize Elasticsearch indices
if ES_ENABLED:
    try:
        # Create products index if not exists
        if not es_client.indices.exists(index="products"):
            es_client.indices.create(
                index="products",
                body={
                    "mappings": {
                        "properties": {
                            "id": {"type": "integer"},
                            "title": {"type": "text", "analyzer": "standard"},
                            "description": {"type": "text", "analyzer": "standard"},
                            "category": {"type": "keyword"},
                            "price": {"type": "float"},
                            "seller_id": {"type": "integer"},
                        }
                    }
                }
            )
        
        # Create posts index if not exists
        if not es_client.indices.exists(index="posts"):
            es_client.indices.create(
                index="posts",
                body={
                    "mappings": {
                        "properties": {
                            "id": {"type": "integer"},
                            "caption": {"type": "text", "analyzer": "standard"},
                            "user_id": {"type": "integer"},
                            "created_at": {"type": "date"},
                        }
                    }
                }
            )
    except Exception as e:
        print(f"Elasticsearch initialization error: {e}")

# Schemas
class SearchResult(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    score: Optional[float] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    took: int

# Helper to get current user ID
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Get current user ID from JWT token"""
    payload = verify_token(token)
    return int(payload.get("sub"))

# Routes
@app.get("/")
async def root():
    return {
        "service": "Search Service",
        "status": "running",
        "version": "1.0.0",
        "elasticsearch": "enabled" if ES_ENABLED else "disabled"
    }

@app.get("/health")
async def health_check():
    if ES_ENABLED:
        try:
            health = es_client.cluster.health()
            return {
                "status": "healthy",
                "elasticsearch": health.get("status", "unknown")
            }
        except:
            return {"status": "unhealthy", "elasticsearch": "connection failed"}
    return {"status": "healthy", "elasticsearch": "disabled"}

@app.get("/search/products", response_model=SearchResponse)
async def search_products(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Search products using Elasticsearch"""
    if not ES_ENABLED:
        # Fallback to database search
        raise HTTPException(status_code=503, detail="Search service unavailable")
    
    try:
        # Build Elasticsearch query
        query_body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": q,
                                "fields": ["title^3", "description"],
                                "type": "best_fields",
                                "fuzziness": "AUTO"
                            }
                        }
                    ]
                }
            },
            "from": skip,
            "size": limit
        }
        
        # Add filters
        filters = []
        if category:
            filters.append({"term": {"category": category.lower()}})
        if min_price is not None:
            filters.append({"range": {"price": {"gte": min_price}}})
        if max_price is not None:
            filters.append({"range": {"price": {"lte": max_price}}})
        
        if filters:
            query_body["query"]["bool"]["filter"] = filters
        
        # Execute search
        response = es_client.search(index="products", body=query_body)
        
        results = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            results.append(SearchResult(
                id=source.get("id"),
                title=source.get("title", ""),
                description=source.get("description"),
                category=source.get("category"),
                price=source.get("price"),
                score=hit.get("_score")
            ))
        
        return SearchResponse(
            results=results,
            total=response["hits"]["total"]["value"],
            took=response["took"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/search/posts", response_model=SearchResponse)
async def search_posts(
    q: str = Query(..., description="Search query"),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Search posts using Elasticsearch"""
    if not ES_ENABLED:
        raise HTTPException(status_code=503, detail="Search service unavailable")
    
    try:
        query_body = {
            "query": {
                "match": {
                    "caption": {
                        "query": q,
                        "fuzziness": "AUTO"
                    }
                }
            },
            "from": skip,
            "size": limit,
            "sort": [{"created_at": {"order": "desc"}}]
        }
        
        response = es_client.search(index="posts", body=query_body)
        
        results = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            results.append(SearchResult(
                id=source.get("id"),
                title=source.get("caption", ""),
                score=hit.get("_score")
            ))
        
        return SearchResponse(
            results=results,
            total=response["hits"]["total"]["value"],
            took=response["took"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/autocomplete")
async def autocomplete(
    q: str = Query(..., min_length=1),
    limit: int = Query(5, le=10)
):
    """Get autocomplete suggestions"""
    if not ES_ENABLED:
        return {"suggestions": []}
    
    try:
        query_body = {
            "suggest": {
                "product-suggest": {
                    "prefix": q,
                    "completion": {
                        "field": "title_suggest",
                        "size": limit
                    }
                }
            }
        }
        
        # This requires a completion suggester in the mapping
        # For now, return simple prefix match
        response = es_client.search(
            index="products",
            body={
                "query": {
                    "prefix": {"title": q}
                },
                "size": limit
            }
        )
        
        suggestions = [
            hit["_source"]["title"]
            for hit in response["hits"]["hits"][:limit]
        ]
        
        return {"suggestions": suggestions}
    except:
        return {"suggestions": []}

@app.post("/index/product")
async def index_product(
    product: dict,
    db: Session = Depends(get_db)
):
    """Index a product in Elasticsearch"""
    if not ES_ENABLED:
        return {"message": "Elasticsearch not available"}
    
    try:
        es_client.index(
            index="products",
            id=product.get("id"),
            body=product
        )
        return {"message": "Product indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")

@app.post("/index/post")
async def index_post(
    post: dict,
    db: Session = Depends(get_db)
):
    """Index a post in Elasticsearch"""
    if not ES_ENABLED:
        return {"message": "Elasticsearch not available"}
    
    try:
        es_client.index(
            index="posts",
            id=post.get("id"),
            body=post
        )
        return {"message": "Post indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005, reload=True)
