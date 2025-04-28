from chromadb.utils import embedding_functions
import uuid
import chromadb
import json 


emb_fn = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path="/home/nightbird/PROGRAMING/rag_langchain/rag_main/data")

list_jurnal = client.get_collection(name="jurnal_list", embedding_function=emb_fn)

def main():
    stores_data()

def cek_database(title):
    results = list_jurnal.get(
        where={
            "title": title,
        }
    )
    if results and results.get("documents"):
        print(f"JURNAL DENGAN JUDUL {title}  SUDAH ADA DI DATABASE")
        return True
    return False
        
    
def stores_data(doc,title,year,author,url):
    list_jurnal.add(
        documents=doc,
        metadatas=[{"title":title,"year":year,"author":author,"url":url} for _ in doc],
        ids=[str(uuid.uuid4())for _ in doc]
    )

def querry(pencarian):
    result = list_jurnal.query(
    query_texts=pencarian,
    n_results=4,
    include=["documents","metadatas","distances"],
    where={
        "year":{
            "$gte":2021
        }
    }
    )

    return result.get("documents","metadatas")

if __name__ == "__main__":
    querry("Nitrogen")