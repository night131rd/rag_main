from chromadb.utils import embedding_functions
import uuid
import chromadb
import json 


emb_fn = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path="/home/nightbird/PROGRAMING/rag_langchain/rag_main/data")

list_jurnal = client.get_or_create_collection(name="jurnal_tes_v2", embedding_function=emb_fn)

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
    from text_handling import clean_pdf_text
    
    result = list_jurnal.query(
    query_texts=pencarian,
    n_results=50,
    include=["documents","metadatas","distances"],
    where={
        "year":{
            "$gte":2021
        }
    }
    )

    text = ""
    seen_journals = []

    # Ambil dokumen dan metadata secara berpasangan
    documents = result.get('documents')[0]  # Get the first list of documents
    metadatas = result.get('metadatas')[0]  # Get the first list of metadatas
    
    for doc, metadata in zip(documents, metadatas):
        print(len(seen_journals))
        if len(seen_journals) == 3:
            return text
            
        if metadata['title'] not in seen_journals:
            doc = clean_pdf_text(doc)
            text += f"\nJUDUL: {metadata['title']}\n"
            text += f"TAHUN: {metadata['year']}\n"
            text += f"PENULIS: {metadata['author']}\n"
            text += f"TEXT:\n{doc}\n"
            seen_journals.append(metadata['title'])

if __name__ == "__main__":
    querry("Budidaya pisang")