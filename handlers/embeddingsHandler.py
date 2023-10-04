
import openai
from variables.apiKeys import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def getEmbeddings(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embeddings = response['data'][0]['embedding']
    return embeddings