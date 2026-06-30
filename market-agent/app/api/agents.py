import httpx
from fastapi import APIRouter, HTTPException
from app.agents.orchestrator import MarketOrchestrator

router = APIRouter(prefix="/agents", tags=["Agents"])

orchestrator = MarketOrchestrator()


@router.get("/health")
async def ollama_health():
    """Check if Ollama is running locally."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:11434/api/tags",
                timeout=3.0
            )
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            mistral_ready = any("mistral" in m for m in model_names)
            return {
                "ollama": "running",
                "mistral": "ready" if mistral_ready else "not downloaded",
                "available_models": model_names
            }
    except Exception:
        return {
            "ollama": "not running",
            "mistral": "unavailable",
            "fix": "Run 'ollama serve' in a separate terminal"
        }


@router.post("/run")
async def run_agents():
    """Run all agents and return full intelligence report."""
    result = orchestrator.run()
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/analyze/{symbol}")
async def analyze_symbol(symbol: str):
    """Run all agents for a single stock symbol."""
    from app.core.database import get_latest_stocks
    stocks = get_latest_stocks()
    stock = next((s for s in stocks if s["symbol"] == symbol.upper()), None)
    if not stock:
        raise HTTPException(status_code=404, detail=f"No data for {symbol}")
    return orchestrator.analyze_symbol(stock)