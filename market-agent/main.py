from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import stocks, news, analysis,agents
from app.core.database import test_connection

app = FastAPI(
    title="Market Intelligence Agent API",
    description="Real-time stock data, news sentiment, and market signals",
    version="1.0.0"
)

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register all routers
app.include_router(stocks.router)
app.include_router(news.router)
app.include_router(analysis.router)

app.include_router(agents.router)  


@app.on_event("startup")
async def startup():
    if test_connection():
        print("Database connected successfully")
    else:
        print("WARNING: Database connection failed")


@app.get("/")
async def root():
    return {
        "app": "Market Intelligence Agent",
        "version": "1.0.0",
        "endpoints": ["/stocks", "/news", "/analysis/sentiment", "/analysis/signals"]
    }


@app.get("/health")
async def health():
    db_ok = test_connection()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "disconnected"
    }