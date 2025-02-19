from fastapi import APIRouter, HTTPException
from app.utils.currency import get_exchange_rate

router = APIRouter(prefix="/currency", tags=["Currency"])

@router.get("/convert-currency/")
async def convert_currency(amount: float, from_currency: str, to_currency: str):
    try:
        exchange_rate = await get_exchange_rate(from_currency, to_currency)
        if exchange_rate is None:
            raise HTTPException(status_code=400, detail="Invalid currency codes")
        
        converted_amount = amount * exchange_rate
        return {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "exchange_rate": exchange_rate,
            "converted_amount": round(converted_amount, 2)
        }
    
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))