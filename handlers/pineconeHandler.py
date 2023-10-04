from handlers.embeddingsHandler import getEmbeddings
import pinecone
import PyPDF2
from variables.apiKeys import PINECONE_API_KEY
from langchain.text_splitter import RecursiveCharacterTextSplitter

pinecone.init(api_key=PINECONE_API_KEY, environment="asia-southeast1-gcp-free")

pineconeDatabase = pinecone.Index("document")

def upsertPDFDocument(botId, document):
    pdfReader = PyPDF2.PdfReader(document)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 600,
        chunk_overlap  = 20,
        length_function = len,
    )
    chunks = text_splitter.create_documents([page.extract_text() for page in pdfReader.pages])

    embeddedPages = []
    for index, page in enumerate(chunks):
        embeddedPages.append({
            'id': str(index),
            'values': getEmbeddings(page.page_content),
        })

    botName = "document-" + botId

    pineconeDatabase.delete(deleteAll='true', namespace=botName)
    pineconeDatabase.upsert(
        vectors=embeddedPages,
        namespace=botName
    )