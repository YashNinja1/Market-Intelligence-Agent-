from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.core.database import get_latest_stocks, get_stock_history
from app.models.schemas import StockResponse

router = APIRouter(prefix="/stocks", tags=["Stocks"])


@router.get("/", response_model=list[StockResponse])
async def get_all_stocks():
    """Get latest price for all tracked stocks."""
    stocks = get_latest_stocks()
    if not stocks:
        raise HTTPException(status_code=404, detail="No stock data found. Run a fetch first.")
    return stocks
from app.core.database import remove_stock, get_tracked_symbols


@router.delete("/remove/{symbol}")
async def remove_stock_endpoint(symbol: str):
    """Remove a stock and all its news from the database."""
    success = remove_stock(symbol.upper())
    if not success:
        raise HTTPException(status_code=500, detail=f"Failed to remove {symbol}")
    return {
        "status": "removed",
        "symbol": symbol.upper(),
        "message": f"{symbol.upper()} removed from tracking"
    }


@router.get("/tracked")
async def get_tracked():
    """Get all currently tracked symbols."""
    return {"symbols": get_tracked_symbols()}

@router.get("/{symbol}", response_model=list[StockResponse])
async def get_stock(symbol: str):
    """Get price history for a specific stock symbol."""
    history = get_stock_history(symbol.upper())
    if not history:
        raise HTTPException(status_code=404, detail=f"No data found for {symbol.upper()}")
    return history


from app.services.fetchers import resolve_symbol, fetch_all
from app.core.database import insert_all


@router.get("/search/{query}")
async def search_company(query: str):
    """
    Convert company name to stock symbol.
    Example: /stocks/search/tesla → { symbol: TSLA, name: Tesla }
    """
    result = resolve_symbol(query)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find a stock symbol for '{query}'"
        )
    return result


@router.post("/add/{company_name}")
async def add_company(company_name: str, background_tasks: BackgroundTasks):
    """
    Resolve company name → symbol, then fetch and store its data.
    Example: POST /stocks/add/tesla → fetches TSLA data
    """
    

    result = resolve_symbol(company_name)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Could not resolve '{company_name}' to a stock symbol"
        )

    symbol = result["symbol"]

    def fetch_and_store():
        data = fetch_all(symbols=[symbol])
        insert_all(data)

    background_tasks.add_task(fetch_and_store)

    return {
        "status": "fetching",
        "company": company_name,
        "symbol": symbol,
        "name": result["name"],
        "message": f"Fetching data for {result['name']} ({symbol})..."
    }