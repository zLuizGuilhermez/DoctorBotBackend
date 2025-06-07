from pydantic import BaseModel

class DadosPaciente(BaseModel):
    idade: int
    glicose: float
    imc: float
    pressao: int