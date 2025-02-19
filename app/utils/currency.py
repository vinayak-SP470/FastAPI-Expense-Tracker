from fastapi import HTTPException
import httpx
from app.config import EXCHANGE_RATE_API_KEY, BASE_URL

async def get_exchange_rate(from_currency: str, to_currency: str):
    url = f"{BASE_URL}/{EXCHANGE_RATE_API_KEY}/pair/{from_currency}/{to_currency}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Invalid currency codes. Check the currency codes and try again."
        )
    
    data = response.json()
    return data.get("conversion_rate")
