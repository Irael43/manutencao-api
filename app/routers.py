from fastapi import APIRouter, HTTPException
from app.schemas import PredictRequest, PredictResponse, HealthResponse
from app.services import predict_failure, get_model

router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["Monitoramento"])
def health_check():
    try:
        get_model()
        return HealthResponse(status="ok", model_loaded=True)
    except Exception:
        return HealthResponse(status="error", model_loaded=False)

@router.post("/predict", response_model=PredictResponse, tags=["Inferência"])
def predict(payload: PredictRequest):
    try:
        data = payload.model_dump()
        falha, prob = predict_failure(data)
        return PredictResponse(falha_prevista=falha, probabilidade=prob)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na inferência: {str(e)}")