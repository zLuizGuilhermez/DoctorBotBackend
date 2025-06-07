
from app.services.diabetes_service import avaliar_dados_paciente
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/avaliar")
def avaliar(
    idade: int = Query(...),
    glicose: float = Query(...),
    imc: float = Query(...),
    pressao: int = Query(...)
):
    resultado = avaliar_dados_paciente(idade, glicose, imc, pressao)
    return {
        "idade": idade,
        "glicose": glicose,
        "imc": imc,
        "pressao": pressao,
        "avalicao": resultado
    }
