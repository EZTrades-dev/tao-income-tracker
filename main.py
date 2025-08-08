from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from typing import Dict, Any, Optional, List
import time
from collections import deque
from datetime import datetime, timedelta

app = FastAPI(title="Tao Income Tracking API", version="1.0.0")

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting setup
class RateLimiter:
    def __init__(self, max_calls: int = 10, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
    
    def can_make_call(self) -> bool:
        now = time.time()
        # Remove calls older than the time window
        while self.calls and self.calls[0] < now - self.time_window:
            self.calls.popleft()
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

rate_limiter = RateLimiter()

# Configuration
TAO_API_KEY = "2a2fae0b63c6850ace6abee0ccbd5ab6d3dc56a83556cb5115b68d3e1fa0f694"
TAO_API_BASE_URL = "https://api.tao.app/api/beta"

async def make_tao_api_call(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make a call to the tao.app API with rate limiting"""
    if not rate_limiter.can_make_call():
        raise HTTPException(
            status_code=429, 
            detail="Rate limit exceeded. Maximum 10 calls per minute."
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{TAO_API_BASE_URL}{endpoint}",
                headers={
                    "accept": "application/json",
                    "X-API-Key": TAO_API_KEY
                },
                params=params,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "rate_limit_info": {
                        "calls_made": len(rate_limiter.calls),
                        "calls_remaining": rate_limiter.max_calls - len(rate_limiter.calls)
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Tao API returned status code {response.status_code}",
                    "response_text": response.text
                }
                
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request to Tao API failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Tao Income Tracking API",
        "version": "1.0.0",
        "endpoints": {
            "/status": "Check API status and rate limit info",
            "/current": "Get current tao.app data",
            "/subnets": "Get all subnets information",
            "/subnet/{netuid}": "Get specific subnet information",
            "/subnet-screener": "Get subnet screener data",
            "/fear-greed": "Get fear & greed index data",
            "/fear-greed/current": "Get current fear & greed index",
            "/price-sustainability": "Get price sustainability data",
            "/apy/root": "Get estimated root APY",
            "/apy/alpha/{netuid}": "Get alpha APY for subnet",
            "/subnet-holders/{netuid}": "Get subnet holders",
            "/subnet-transactions/{netuid}": "Get subnet transactions",
            "/subnet-ohlc/{netuid}": "Get subnet OHLC data",
            "/subnet-valuation/{netuid}": "Get subnet valuation data",
            "/subnet-metagraph/{netuid}": "Get subnet metagraph",
            "/subnet-tags": "Get subnet tags",
            "/validator-identities": "Get validator identities",
            "/portfolio/balance": "Get current portfolio balance",
            "/portfolio/balance-history": "Get portfolio balance history",
            "/portfolio/events": "Get portfolio events",
            "/docs": "API documentation"
        }
    }

@app.get("/status")
async def get_status():
    """Check API status and rate limit information"""
    return {
        "api_status": "running",
        "rate_limit": {
            "max_calls": rate_limiter.max_calls,
            "time_window_seconds": rate_limiter.time_window,
            "calls_made": len(rate_limiter.calls),
            "calls_remaining": rate_limiter.max_calls - len(rate_limiter.calls)
        },
        "tao_api_key_configured": bool(TAO_API_KEY)
    }

@app.get("/current")
async def get_current_data():
    """Get current data from tao.app API"""
    return await make_tao_api_call("/current")

@app.get("/subnets")
async def get_all_subnets():
    """Get all subnets information"""
    return await make_tao_api_call("/analytics/subnets/info")

@app.get("/subnet/{netuid}")
async def get_subnet_info(netuid: int):
    """Get specific subnet information"""
    return await make_tao_api_call(f"/analytics/subnets/info/{netuid}")

@app.get("/subnet-screener")
async def get_subnet_screener():
    """Get subnet screener data"""
    return await make_tao_api_call("/subnet_screener")

@app.get("/fear-greed")
async def get_fear_greed_index(
    start: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end: Optional[str] = Query(None, description="End date in YYYY-MM-DD format")
):
    """Get fear & greed index data"""
    params = {}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    return await make_tao_api_call("/analytics/macro/fear_greed", params)

@app.get("/fear-greed/current")
async def get_current_fear_greed():
    """Get current fear & greed index"""
    return await make_tao_api_call("/analytics/macro/fear_greed/current")

@app.get("/price-sustainability")
async def get_price_sustainability(netuid: Optional[int] = Query(None, description="Subnet ID to filter results")):
    """Get price sustainability data"""
    params = {}
    if netuid is not None:
        params["netuid"] = netuid
    return await make_tao_api_call("/price-sustainability", params)

@app.get("/apy/root")
async def get_root_apy(
    start: Optional[str] = Query(None, description="Start of the data range"),
    end: Optional[str] = Query(None, description="End of the data range"),
    interval: str = Query("1hour", description="Time interval for data aggregation"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(100, description="Number of items per page")
):
    """Get estimated root APY"""
    params = {
        "interval": interval,
        "page": page,
        "page_size": page_size
    }
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    return await make_tao_api_call("/apy/root", params)

@app.get("/apy/alpha/{netuid}")
async def get_alpha_apy(
    netuid: int,
    start: Optional[str] = Query(None, description="Start of the data range"),
    end: Optional[str] = Query(None, description="End of the data range"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(100, description="Number of items per page")
):
    """Get alpha APY for specific subnet"""
    params = {
        "netuid": netuid,
        "page": page,
        "page_size": page_size
    }
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    return await make_tao_api_call("/apy/alpha", params)

@app.get("/subnet-holders/{netuid}")
async def get_subnet_holders(netuid: int):
    """Get subnet holders information"""
    params = {"netuid": netuid}
    return await make_tao_api_call("/analytics/subnets/holders", params)

@app.get("/subnet-transactions/{netuid}")
async def get_subnet_transactions(
    netuid: int,
    coldkey: Optional[str] = Query(None, description="Coldkey to filter results"),
    start: Optional[str] = Query(None, description="Start of the data range"),
    end: Optional[str] = Query(None, description="End of the data range"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(100, description="Number of items per page")
):
    """Get subnet transactions"""
    params = {
        "netuid": netuid,
        "page": page,
        "page_size": page_size
    }
    if coldkey:
        params["coldkey"] = coldkey
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    return await make_tao_api_call("/analytics/subnets/transactions", params)

@app.get("/subnet-ohlc/{netuid}")
async def get_subnet_ohlc(
    netuid: int,
    start: str = Query(..., description="Start of the data range"),
    end: str = Query(..., description="End of the data range"),
    interval_minutes: int = Query(15, description="Interval of the data in minute(s)")
):
    """Get subnet OHLC data"""
    params = {
        "netuid": netuid,
        "start": start,
        "end": end,
        "interval_minutes": interval_minutes
    }
    return await make_tao_api_call("/subnets/ohlc", params)

@app.get("/subnet-valuation/{netuid}")
async def get_subnet_valuation(
    netuid: int,
    start: Optional[str] = Query(None, description="Start of the data range"),
    end: Optional[str] = Query(None, description="End of the data range"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(100, description="Number of items per page")
):
    """Get subnet valuation data"""
    params = {
        "netuid": netuid,
        "page": page,
        "page_size": page_size
    }
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    return await make_tao_api_call("/analytics/subnets/valuation", params)

@app.get("/subnet-metagraph/{netuid}")
async def get_subnet_metagraph(
    netuid: int,
    timestamp: Optional[str] = Query(None, description="UTC timestamp of a historical metagraph")
):
    """Get subnet metagraph"""
    params = {}
    if timestamp:
        params["timestamp"] = timestamp
    return await make_tao_api_call(f"/analytics/subnets/metagraph/{netuid}", params)

@app.get("/subnet-tags")
async def get_subnet_tags():
    """Get subnet tags"""
    return await make_tao_api_call("/subnet_tags")

@app.get("/validator-identities")
async def get_validator_identities():
    """Get validator identities"""
    return await make_tao_api_call("/validator_identities")

@app.get("/portfolio/balance")
async def get_portfolio_balance(
    coldkey: str = Query(..., description="Coldkey of the user")
):
    """Get current portfolio balance"""
    params = {
        "coldkey": coldkey
    }
    return await make_tao_api_call("/portfolio/balance", params)

@app.get("/portfolio/balance-history")
async def get_portfolio_balance_history(
    coldkey: str = Query(..., description="Coldkey of the user"),
    start: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(1000, description="Number of items per page")
):
    """Get portfolio balance history"""
    params = {
        "coldkey": coldkey,
        "page": page,
        "page_size": page_size
    }
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    return await make_tao_api_call("/accounting/balance-history", params)

@app.get("/portfolio/events")
async def get_portfolio_events(
    coldkey: str = Query(..., description="Coldkey of the user"),
    start_block: Optional[int] = Query(None, description="Start block"),
    end_block: Optional[int] = Query(None, description="End block"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(1000, description="Number of items per page")
):
    """Get portfolio events"""
    params = {
        "coldkey": coldkey,
        "page": page,
        "page_size": page_size
    }
    if start_block:
        params["start_block"] = start_block
    if end_block:
        params["end_block"] = end_block
    return await make_tao_api_call("/accounting/events", params)

@app.get("/macro-analytics")
async def get_macro_analytics(
    interval: str = Query("5min", description="Time interval for data aggregation"),
    start: Optional[str] = Query(None, description="Start of the data range"),
    end: Optional[str] = Query(None, description="End of the data range"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(100, description="Number of items per page")
):
    """Get macro analytics aggregated data"""
    params = {
        "interval": interval,
        "page": page,
        "page_size": page_size
    }
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    return await make_tao_api_call("/analytics/macro/aggregated", params)

@app.get("/subnet-analytics")
async def get_subnet_analytics(
    interval: str = Query("15min", description="Time interval for data aggregation"),
    netuid: Optional[int] = Query(None, description="Subnet ID to filter results"),
    start: Optional[str] = Query(None, description="Start of the data range"),
    end: Optional[str] = Query(None, description="End of the data range"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(100, description="Number of items per page")
):
    """Get subnet analytics aggregated data"""
    params = {
        "interval": interval,
        "page": page,
        "page_size": page_size
    }
    if netuid is not None:
        params["netuid"] = netuid
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    return await make_tao_api_call("/analytics/subnets/aggregated", params)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
