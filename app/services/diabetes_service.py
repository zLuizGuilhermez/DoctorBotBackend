from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.settings import Settings
from app.ia.ia_logica import avaliar_dados_paciente_ia

def binarizar(resposta: str) -> int:
    resposta = resposta.strip().lower()
    if resposta.startswith("sim"):
        return 1
    elif resposta.startswith("não") or resposta.startswith("nao"):
        return 0
    else:
        return 0


def avaliar_dados_paciente(idade: int, glicose: float, imc: float, pressao: int, insulina=None, espessura_pele=None, pedigree=None, gestacoes=None) -> str:
    return avaliar_dados_paciente_ia(idade, glicose, imc, pressao, insulina, espessura_pele, pedigree, gestacoes)
