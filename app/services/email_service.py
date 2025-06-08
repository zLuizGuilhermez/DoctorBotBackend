import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.ia.ia_logica import justificar_avaliacao_ia
import traceback

def enviar_email_para_medico(nome: str, idade: int, glicose: float, imc: float, pressao: int, avaliacao: str, email_medico: str):
    justificativa = justificar_avaliacao_ia(idade, glicose, imc, pressao, avaliacao)
    remetente = 'iadoctorbot@gmail.com'
    senha = 'aqds vjee cvpt vnrz'
    assunto = f'Avaliação aprofundada do paciente {nome}'
    corpo = (
        f"Dados da consulta:\n"
        f"Nome: {nome}\n"
        f"Idade: {idade}\nGlicose: {glicose}\nIMC: {imc}\nPressão arterial: {pressao}\n"
        f"\nResultado da avaliação: {avaliacao}\n"
        f"\nJustificativa do modelo:\n{justificativa}"
    )
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = email_medico
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.sendmail(remetente, email_medico, msg.as_string())
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        traceback.print_exc()
        return False
