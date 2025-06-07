from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.settings import Settings

# Configuração dos modelos
Settings.llm = Ollama(model="gemma2:2b")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Carregamento e indexação dos documentos
folder_path = "app/data/dados_diabetes"
documentos = SimpleDirectoryReader(folder_path).load_data()
index = VectorStoreIndex.from_documents(documentos)
query_engine = index.as_query_engine(similarity_top_k=2)

def avaliar_dados_paciente_ia(idade: int, glicose: float, imc: float, pressao: int, insulina=None, espessura_pele=None, pedigree=None, gestacoes=None) -> str:
    prompt = (
        f"Paciente:\n"
        f"Idade: {idade}\n"
        f"Glicose: {glicose}\n"
        f"IMC: {imc}\n"
        f"Pressão arterial: {pressao}\n"
    )
    if insulina is not None:
        prompt += f"Insulina: {insulina}\n"
    if espessura_pele is not None:
        prompt += f"Espessura da pele: {espessura_pele}\n"
    if pedigree is not None:
        prompt += f"Função hereditária: {pedigree}\n"
    if gestacoes is not None:
        prompt += f"Número de gestações: {gestacoes}\n"
    prompt += ("\nCom base no conteúdo dos documentos, avalie se esse paciente pode estar com diabetes. "
               "Responda apenas com uma das opções: "
               "Sim, é possível que o paciente tenha diabetes. "
               "Não, é improvável que o paciente tenha diabetes. "
               "Responda 'Sim' se houver indícios razoáveis, caso contrário responda 'Não'.")

    resposta = query_engine.query(prompt)
    resposta_str = resposta.response.strip().lower()
    if resposta_str.startswith('sim'):
        return 'Sim, é possível que o paciente tenha diabetes.'
    elif resposta_str.startswith('não') or resposta_str.startswith('nao'):
        return 'Não, é improvável que o paciente tenha diabetes.'
    else:
        return resposta.response.strip()

