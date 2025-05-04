from chromadb.utils import embedding_functions
import uuid
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import getpass
import os

# Simpler but less secure
os.environ["GOOGLE_API_KEY"] = "AIzaSyAXCkXcahKwW6S4OlsiuEcJQhZ1-k5dWyE"
if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")




vector_store = Chroma(
    collection_name="example_collection_gemini",
    create_collection_if_not_exists=True,
    embedding_function=embeddings,
    persist_directory="/home/nightbird/PROGRAMING/rag_langchain/rag_main/data",  # Where to save data locally, remove if not necessary
)



def main():
    stores_data()

    
def stores_data(doc,title,year,author,url):
    vector_store.add_texts(
        texts=doc,
        metadatas=[{"title":title,"year":year,"author":author,"url":url} for _ in doc],
        ids=[str(uuid.uuid4())for _ in doc]
    )


def querry(pencarian):
    
    result = vector_store.similarity_search_with_relevance_scores(
    query=pencarian,
    k = 30,
    )
    count = 0
    text = ""
    seen_journals = []
    for documents in result:
        document = documents[0]
        metadata = document.metadata
        result_text = document.page_content
        count += 1
  
        if metadata['title'] not in seen_journals:
                
                seen_journals.append(metadata['title'])
                
                text += f"\nJUDUL: {metadata['title']}\n"
                text += f"TAHUN: {metadata['year']}\n"
                text += f"PENULIS: {metadata['author']}\n"
                text += f"TEXT:\n{result_text}\n"


        if len(seen_journals) == 8:
                print(text)
                return text
    
    print(text)
    return text
                

if __name__ == "__main__":
    text = """
Pada tahap awal budidaya pisang, persiapan lahan sangat penting untuk menjamin pertumbuhan optimal tanaman. Pilihlah lokasi dengan ketinggian 0–800 meter di atas permukaan laut, tanah gembur yang kaya bahan organik, serta pH antara 5,5–7. Bersihkan lahan dari gulma dan bebatuan, lalu olah tanah hingga gembur dengan cangkul atau bajak. Buat bedengan selebar sekitar 1–1,2 meter dan atur jarak tanam antar pohon sejauh 2–3 meter. Untuk bibit, gunakan anakan pisang unggul seperti Raja Bulu, Barangan, atau Ambon yang memiliki perakaran sehat, batang primer sempurna, serta bebas hama dan penyakit.
Setelah lahan siap, lakukan penanaman dengan hati-hati agar akar bibit tidak rusak. Gali lubang berdiameter dan kedalaman sekitar 30–40 cm, kemudian campur tanah galian dengan pupuk kandang seberat 5–10 kilogram guna menyediakan nutrisi awal yang cukup. Tanam bibit pada posisi tegak, timbun kembali lubang, dan padatkan sedikit untuk menjaga kestabilan batang. Siram segera setelah penanaman, kemudian lanjutkan penyiraman secara rutin dua hingga tiga kali per minggu, terutama pada musim kemarau. Pemupukan susulan dengan NPK 15-15-15 sebanyak 100–150 gram per tanaman setiap dua bulan sekali akan merangsang pertumbuhan daun dan batang, ditambah aplikasi pupuk organik cair dapat meningkatkan produktivitas.
Dalam pemeliharaan lanjutan, perhatikan gejala hama dan penyakit seperti ulat penggerek pelepah dan kutu sisik yang sering menyerang pisang. Kendalikan hama secara ramah lingkungan dengan insektisida nabati—misalnya ekstrak tembakau—atau gunakan pestisida sesuai dosis jika serangan berat. Rutin cabut anakan liar yang tidak perlu untuk mengurangi kompetisi nutrisi dan menjaga jarak ideal antar pohon. Buah pisang umumnya siap panen antara sembilan hingga dua belas bulan setelah tanam, ditandai dengan sisik buah yang mulai mengering dan permukaan kulit yang berangsur kekuningan. Panenlah menggunakan pisau tajam, lalu simpan tandan di tempat teduh untuk menstabilkan suhu buah sebelum didistribusikan agar mutu dan rasanya terjaga.
"""
    #vector_store.add_texts(text)
    querry("defisiensi nitrogen")