from app.models.schemas import HealthResponse
from app.services.health import HealthService
from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=HealthResponse, summary="Simple health check")
async def health_check() -> HealthResponse:
    status = await HealthService().get_status()
    return HealthResponse(**status)
