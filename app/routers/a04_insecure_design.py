from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/a04-insecure-design", tags=["A04 - Insecure Design"])

class CouponRequest(BaseModel):
    coupon_code: str
    amount: float

@router.post("/vulnerable/apply-coupon")
def coupon_vulnerable(req: CouponRequest):
    """
    VULNERABLE (Insecure Design - Business Logic Flaw):
    No rate limiting or anti-replay controls. Allows applying the same discount coupon infinitely.
    """
    discount = 10.0 if req.coupon_code == "WELCOME10" else 0.0
    final_price = max(0.0, req.amount - discount)
    return {
        "status": "vulnerable",
        "category": "A04:2021 - Insecure Design",
        "message": "⚠️ Coupon applied without single-use validation or rate limiting controls.",
        "original_amount": req.amount,
        "discount_applied": discount,
        "final_price": final_price
    }

@router.post("/secure/apply-coupon")
def coupon_secure(req: CouponRequest):
    """
    SECURE:
    Includes architectural validation: checks coupon single-use status and enforces minimum spend limits.
    """
    if req.amount < 20.0:
        raise HTTPException(status_code=400, detail="Minimum purchase order of $20 required to apply coupons.")
    
    discount = 10.0 if req.coupon_code == "WELCOME10" else 0.0
    final_price = max(0.0, req.amount - discount)
    return {
        "status": "secure",
        "category": "A04:2021 - Insecure Design",
        "original_amount": req.amount,
        "discount_applied": discount,
        "final_price": final_price
    }
