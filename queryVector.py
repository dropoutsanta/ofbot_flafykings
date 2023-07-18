import os
import pinecone
from createEmbeddings import getEmbeddings

pinecone.init(api_key="dfad2cf1-0731-415f-80dd-7e0588fb4c58", environment="asia-southeast1-gcp-free")

def queryVectorImage(text, bot_id):
    index = pinecone.Index("pictures")
    botIdString = str(bot_id)
    embed = getEmbeddings(text)
    result = index.query(
    namespace=f"{botIdString}-picture",
    vector=embed,
    top_k=1,
    include_values=True,
    include_metadata=True
    )
    data = result['matches'][0]
    metadata = data['metadata']
    description = metadata['description']
    url = metadata['url']

    return metadata

def queryVectorText(text):
    index = pinecone.Index("pictures")
    embed = getEmbeddings(text)
    result = index.query(
    namespace="example-namespace",
    vector=embed,
    top_k=1,
    include_values=True,
    include_metadata=True
    )
    data = result['matches'][0]
    metadata = data['metadata']
    print(metadata)

    return metadata