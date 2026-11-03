from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    temperatura_ar_k: float = Field(..., ge=250, le=350, description="Temperatura do ar (K)")
    temperatura_processo_k: float = Field(..., ge=250, le=350, description="Temperatura do processo (K)")
    velocidade_rotacao_rpm: float = Field(..., ge=0, le=5000, description="Velocidade de rotação (RPM)")
    torque_nm: float = Field(..., ge=0, le=200, description="Torque (Nm)")
    desgaste_ferramenta_min: float = Field(..., ge=0, le=500, description="Desgaste da ferramenta (min)")

class PredictResponse(BaseModel):
    falha_prevista: int = Field(..., ge=0, le=1, description="0 = Normal, 1 = Falha")
    probabilidade: float = Field(..., ge=0.0, le=1.0, description="Probabilidade de falha")

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool