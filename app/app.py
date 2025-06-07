from fastapi import FastAPI, Request, HTTPException
from models import *
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.settings import Settings
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do modelo
Settings.llm = Ollama(model="gemma2:2b")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Carrega os dados vetorizados
documentos = SimpleDirectoryReader("data/dados_diabetes").load_data()
print(f"[INFO] {len(documentos)} documentos carregados.")

# Indexação
index = VectorStoreIndex.from_documents(documentos)
print("[INFO] Índice vetorial criado.")

# Motor de consulta
query_engine = index.as_query_engine()

# Modelo dos dados recebidos
class DadosPaciente(BaseModel):
    idade: int
    glicose: float
    imc: float
    pressao: int

# Rota de avaliação
@app.get("/avaliar")
def avaliar_diabetes(idade: int, glicose: float, imc: float, pressao: int):
    prompt = (
        "Com base no conhecimento disponível, avalie se o paciente pode ter diabetes.\n"
        "Responda apenas com uma das opções:\n"
        "1. 'Sim, é possível que o paciente tenha diabetes.'\n"
        "2. 'Não, é improvável que o paciente tenha diabetes.'\n\n"
        f"Idade: {idade}\n"
        f"Glicose: {glicose}\n"
        f"IMC: {imc}\n"
        f"Pressão arterial: {pressao}\n"
    )

    try:
        resposta = query_engine.query(prompt)
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="Tempo de resposta esgotado. Tente novamente.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

    return {
        "idade": idade,
        "glicose": glicose,
        "imc": imc,
        "pressao": pressao,
        "avaliacao": resposta.response.strip()
    }
