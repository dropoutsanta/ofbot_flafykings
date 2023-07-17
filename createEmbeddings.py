import openai
import os
import pinecone
from getImages import getSFW

pinecone.init(api_key="dfad2cf1-0731-415f-80dd-7e0588fb4c58", environment="asia-southeast1-gcp-free")

index = pinecone.Index("pictures")

openAIKey = os.environ.get('OPEN_AI_KEY')
openai.api_key = openAIKey

items = [
       
        
    {"image_id": "img1", "description_text": "This is a selfie of me where we can see my boobs.", "url": "https://citeifmttmdotbcsotyh.supabase.co/storage/v1/object/public/media/ThierryTest/312137161_794085781868198_1815158447240693747_n.jpg?t=2023-07-16T03%3A36%3A09.231Z"},
    {"image_id": "img2", "description_text": "This is a picture of me wearing a bikini in a dogystyle position to arouse you", "url": "https://citeifmttmdotbcsotyh.supabase.co/storage/v1/object/public/media/ThierryTest/360081665_2280490219005403_4351657794535008494_n.jpg?t=2023-07-16T03%3A37%3A50.301Z"},
    {"image_id": "img3", "description_text": "This is a picture of me in a classy look.", "url": "https://citeifmttmdotbcsotyh.supabase.co/storage/v1/object/public/media/ThierryTest/310065513_518689866757647_4478844671022099818_n.jpg"},
]




def getEmbeddings(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embeddings = response['data'][0]['embedding']
    return embeddings

def uploadImagesToVDB(bot_id):
    count = 0
    embeddings = []
    idToString = str(bot_id)
    index.delete(deleteAll='true', namespace=f'{idToString}-picture')
    imagesData = getSFW(bot_id)

    for text in imagesData:
        count+=1
        if text['description']:
                print(text['description'])
                embed = getEmbeddings(text['description'])
                result = {
                'id': str(text['id']),
                'values': embed,
                'metadata': {'description': text['description'], "url": text['url']},
        }
                embeddings.append(result)
        else:
                print("No value")
    
    upsert_response = index.upsert(
        vectors=embeddings,
        namespace=f'{idToString}-picture'
    )
    return "Done"






