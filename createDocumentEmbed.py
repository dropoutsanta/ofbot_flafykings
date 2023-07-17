import openai
import os
import pinecone

pinecone.init(api_key="dfad2cf1-0731-415f-80dd-7e0588fb4c58", environment="asia-southeast1-gcp-free")

index = pinecone.Index("pictures")

openAIKey = os.environ.get('OPEN_AI_KEY')
openai.api_key = openAIKey

def getEmbeddings(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embeddings = response['data'][0]['embedding']
    return embeddings



with open('megan.txt', 'r') as file:
  data = file.read()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 600,
    chunk_overlap  = 20,
    length_function = len,
)
texts = text_splitter.create_documents([data])

count = 0
embeddings = []
for text in texts:
   
   count+=1
   embed = getEmbeddings(text.page_content)
   tupple = (str(count),embed,{"text": text.page_content})
   result = {
        'id': str(count),
        'values': embed,
        'metadata': {'text': text.page_content},
   }
   embeddings.append(result)



upsert_response = index.upsert(
    vectors=embeddings,
    namespace='example-namespace'
)


print(upsert_response)



