from datetime import datetime
from decimal import Decimal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from restaurant_service.application.register_dinner import RegisterDinnerUseCase
from restaurant_service.domain.model.dinner import Dinner


class DinnerRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)
    card_number: str = Field(..., min_length=1)
    restaurant_code: str = Field(..., min_length=1)
    occurred_at: datetime


def create_app(use_case: RegisterDinnerUseCase) -> FastAPI:
    app = FastAPI(title="Restaurant Service")

    @app.post("/dinners", status_code=202)
    def register_dinner(request: DinnerRequest) -> dict:
        try:
            dinner = Dinner(
                amount=request.amount,
                card_number=request.card_number,
                restaurant_code=request.restaurant_code,
                occurred_at=request.occurred_at,
            )
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        use_case.execute(dinner)
        return {"status": "accepted"}

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app
