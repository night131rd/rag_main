from chroma import querry
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import getpass
import os


os.environ["GOOGLE_API_KEY"] = "AIzaSyCW48u86C518XxX2jD8YWw1kFcdGtblHNc"
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass(
        "AIzaSyCW48u86C518XxX2jD8YWw1kFcdGtblHNc"
    )

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def main():
    return


system_prompt = """"Anda adalah asisten pencarian akademik ahli yang menggunakan alur pemikiran terstruktur (chain of thought). Ikuti langkah-langkah berikut untuk input pengguna:

Langkah 1: Analisis Topik
- Identifikasi 1-2 topik utama dari paragraf  
- Contoh: "Dampak rokok dan upaya regulasi"
Langkah 2: Ekstraksi Kata Kunci 
- Daftarkan kata/frasa kunci (prioritaskan istilah ilmiah/medis)  
- Contoh: ["rokok", "kesehatan", "nikotin", "regulasi"]

Langkah 3: Formulasi Query
- Gabungkan 1-3 kata kunci terkuat menjadi query  
- Jika output hanya 1 kata kunci, tambahkan kata kunci yang relevan
- Contoh: "rokok  kesehatan regulasi"

Format Output Wajib:

hasil query dari Langkah 

Aturan Tambahan:
1. Abaikan tahun/lokasi/keterangan spesifik  
2. Gunakan akronim umum ( 
3. Fokus pada konsep yang dapat dicari di database akademik
4. Pastikan output dalam bahasa yang sama dengan input pengguna

Contoh Input-Output:

Input: "Rokok adalah produk yang terbuat dari tembakau yang digulung atau dipadatkan dalam kertas, biasanya digunakan dengan cara dibakar dan dihisap asapnya.
Rokok mengandung berbagai zat kimia berbahaya, termasuk nikotin, tar, dan karbon monoksida, yang dapat menyebabkan berbagai masalah kesehatan serius, seperti penyakit jantung,
kanker paru-paru, stroke, dan gangguan pernapasan.Selain berdampak buruk bagi perokok aktif, asap rokok juga berbahaya bagi perokok pasif 
(orang yang menghirup asap rokok dari lingkungan sekitar). Oleh karena itu, banyak negara telah menerapkan regulasi ketat terkait rokok, termasuk larangan merokok di tempat umum,
pembatasan iklan rokok, dan kampanye kesehatan untuk mengurangi konsumsi rokok."  
Output: rokok  kesehatan regulasi
Input: "Padi di Indonesia"
Output: Padi Indonesia
Input: "Factors Affecting Rice Grain Size and Weight"
Output: Rice Grain Size Weight
Input: "The Impact of Climate Change on Coral Reefs"
Output: Climate Change Coral Reefs

Berikan output  yang sesuai dengan aturan di atas.
hasil query dari Langkah 3
HANYA QUERY YANG PERLU ANDA BERIKAN!!!
"""
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant {system_prompt} .",
        ),
        ("human", "{input}"),
    ]
)
chain = prompt | llm


def llm_querry(querry):
    answer = chain.invoke(
        {
            "system_prompt": system_prompt,
            "input": querry,
        }
    )
    print(answer.content)
    return answer.content


system_prompt_answer = """
INSTRUKSI WAJIB - ATURAN SITASI AKADEMIK

Anda adalah seorang dosen peneliti yang sedang menulis paper akademik dengan standar tinggi.
"


============= VALIDASI SITASI =============
Untuk SETIAP sitasi yang Anda gunakan:
1. Ekstrak tahun dari sitasi (misalnya: dari "(Ahmad, 2020)" ekstrak "2020")
3. Jika YA: sitasi VALID dan BOLEH digunakan
4. Jika TIDAK: sitasi TIDAK VALID dan DILARANG digunakan!
=======================================



GAYA PENULISAN:
- Tulis seperti dosen peneliti yang sedang menulis paper ilmiah
- Gunakan bahasa akademik yang formal dan presisi
- Sajikan informasi dengan logis dan terstruktur

FORMAT OUTPUT:
1. Satu paragraf akademik (5-8 kalimat)
2. Minimal 4 sitasi dengan format (Nama, Tahun) 


CONTOH OUTPUT:
Rokok adalah produk olahan tembakau yang dikemas dalam bentuk silinder dari kertas dengan campuran cengkeh dan bahan tambahan lainnya yang diproduksi
oleh pabrik maupun dibuat sendiri, yang digunakan dengan cara dibakar pada salah satu ujungnya dan dibiarkan membara agar asapnya dapat dihirup melalui
mulut pada ujung lainnya. Kandungan berbahaya dalam rokok meliputi lebih dari 7.000 bahan kimia, termasuk nikotin yang bersifat adiktif, tar yang dapat
menyebabkan kanker, dan karbon monoksida yang mengganggu sistem peredaran darah (Samsuri et al., 2023). Dampak kesehatan yang ditimbulkan oleh rokok tidak hanya mempengaruhi 
perokok aktif tetapi juga perokok pasif yang terpapar asap rokok di lingkungannya. Konsumsi rokok merupakan salah satu penyebab utama kematian yang dapat
dicegah di seluruh dunia, dengan estimasi lebih dari 8 juta kematian setiap tahunnya (Kholis, 2024). Berbagai penelitian ilmiahtelah membuktikan bahwa
merokok secara signifikan meningkatkan risiko berbagai penyakit serius seperti kanker paru-paru, penyakit jantung koroner, stroke, dan penyakit
paru obstruktif kronik (PPOK)..



"""

prompt_context = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "  {system_prompt_answer} dan gunakan referensi ini sebagai jawaban, saya ulangi lagi hanya gunakan referensi dibawah ini, jangan membuat jawaban yang tidak bersumber dari referensi yang saya berikan {context}.",
        ),
        ("human", "{input}"),
    ]
)
chain_answer = prompt_context | llm


def answer(pencarian):
    context = querry(pencarian)
    if context is not None:
        content = chain_answer.invoke(
            {
                "system_prompt_answer": system_prompt_answer,
                "context": context,
                "input": pencarian,
            }
        )

    print("JAWABAN BERDASARKAN JURNAL    ", content.content)


if __name__ == "__main__":
    answer("Rokok")
