from app.services.diabetes_service import avaliar_dados_paciente
from app.services.email_service import enviar_email_para_medico
from fastapi import APIRouter, Query, HTTPException, Form, Body

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

@router.post("/enviar-email")
def enviar_email(
    body: dict = Body(...)
):
    nome = body.get("nome")
    idade = body.get("idade")
    glicose = body.get("glicose")
    imc = body.get("imc")
    pressao = body.get("pressao")
    avaliacao = body.get("avaliacao")
    email_medico = body.get("email_medico")

    sucesso = enviar_email_para_medico(nome, idade, glicose, imc, pressao, avaliacao, email_medico)
    if not sucesso:
        raise HTTPException(status_code=500, detail="Erro ao enviar e-mail para o médico.")
    return {"mensagem": "E-mail enviado com sucesso."}
