from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.settings import Settings

# Configura modelos
Settings.llm = Ollama(model="gemma2:2b")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Carrega e indexa documentos
documentos = SimpleDirectoryReader("app/data/dados_diabetes").load_data()
index = VectorStoreIndex.from_documents(documentos)
query_engine = index.as_query_engine()


def avaliar_dados_paciente(idade: int, glicose: float, imc: float, pressao: int) -> str:
    prompt = (
        f"Paciente:\n"
        f"Idade: {idade}\n"
        f"Glicose: {glicose}\n"
        f"IMC: {imc}\n"
        f"Pressão arterial: {pressao}\n\n"
        f"Com base no conteúdo dos documentos, avalie se esse paciente pode estar com diabetes. "
        f"Responda apenas com uma das opções: "
        f"1. 'Sim, é possível que o paciente tenha diabetes.' "
        f"2. 'Não, é improvável que o paciente tenha diabetes.'"
    )

    resposta = query_engine.query(prompt)
    return resposta.response.strip()
