from fastapi import APIRouter
from app.services.diabetes_service import avaliar_dados_paciente

router = APIRouter()

@router.get("/avaliar")
def avaliar(idade: int, glicose: float, imc: float, pressao: int):
    resultado = avaliar_dados_paciente(idade, glicose, imc, pressao)
    return {
        "idade": idade,
        "glicose": glicose,
        "imc": imc,
        "pressao": pressao,
        "avaliacao": resultado
    }
