from chroma import querry
import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel,Field

os.environ["GOOGLE_API_KEY"] = "AIzaSyCW48u86C518XxX2jD8YWw1kFcdGtblHNc"
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass(
        "AIzaSyCW48u86C518XxX2jD8YWw1kFcdGtblHNc"
    )



llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=2,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)





def main():
    return 

system_prompt ="""
You are a professional content analyzer, and your primary role is to identify and extract the most relevant keywords from a given article. Your goal is to focus on the main ideas, themes, and key phrases that best represent the input.

I will send a text .

Please follow these steps:

1. Carefully read the  text to understand its core topics and main ideas.

2. Extract relevant keywords or key phrases that accurately reflect the key concepts discussed. Focus on terms that someone might use to search for this type of content online.

3. If the text is too short add synonym or relevant topics for better search

4. Avoid common stop words like "the", "and", or "with". Also, avoid overly generic terms unless they are critical to the topic.

5. Prioritize phrases over single words where it makes sense, especially if the phrase better captures a core idea (e.g., "artificial intelligence" instead of just "intelligence").

6. Make sure the output language is the same as the input

7. Make sure the output in one sentence maximal 3 words




Your goal is to deliver a keywords in one sentece that captures the essence of the text in a way that would be useful for JournalArticle query or content categorization.

"""



prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            " {system_prompt} .",
        ),
        ("human", "{input}"),
    ]
)
chain = prompt | llm


def llm_querry(querry):
    answer= chain.invoke(
    {
        "system_prompt": system_prompt,
        "input": querry,
    }
    )
    print(answer.content)
    return answer.content

    
example = """
Contoh 1:
Exposure to secondhand smoke significantly impacts children under 5 years old, increasing their risk of severe respiratory infections. 
Studies show a strong correlation between parental smoking and the occurrence of severe pneumonia in children under 5 (Stefani & Setiawan, 2021). 
Infants aged 0-1 are particularly vulnerable, with smoke exposure interfering with respiratory tract development and increasing the risk of bronchopneumonia (Palaguna, 2023). 
Despite awareness of smoking's consequences, many parents continue the habit, exposing their children to harmful substances like nicotine and carbon monoxide (Ramdani et al., 2019). 
Research indicates that parental knowledge about the dangers of secondhand smoke is often insufficient, with 66 percent of parents having only moderate understanding of how it can trigger acute respiratory infections in children aged 0-5 (Zara, 2021). 
These findings emphasize the need for increased education and awareness about the risks of secondhand smoke exposure to young children.

Contoh 2:
Nitrogen is a crucial nutrient for plant growth and development, playing a vital role in protein, DNA, and RNA synthesis (Sari & Prayudyaningsih, 2015).
While abundant in the atmosphere, plants cannot directly utilize atmospheric nitrogen. 
Rhizobium bacteria can fix atmospheric nitrogen through symbiosis with legumes, converting it into plant-available forms (Meitasari & Wicaksono, 2018).
Proper nitrogen management is essential, as excess can lead to increased susceptibility to pests and diseases, while deficiency results in stunted growth and yellowing leaves (Erythrina, 2016).
The Leaf Color Chart is an effective tool for optimizing nitrogen application in rice cultivation. 
For crops like kailan, appropriate nitrogen dosage and plant density can significantly improve growth and yield (Pramitasari et al., 2016).
In soybean cultivation, a combination of Rhizobium inoculation and balanced nitrogen fertilization can enhance various growth parameters and yield components (Dwi, 2018).

Contoh 3:
Klorofil adalah pigmen hijau yang berperan penting dalam fotosintesis, ditemukan dalam membran tilakoid dan kloroplas (Juandaet al., 2020). 
ungsi utamanya meliputi pemanfaatan energi matahari, fiksasi CO2, dan penyediaan energi bagi ekosistem (Aulia Juanda Djs et al., 2020).
Klorofil memiliki manfaat sebagai antioksidan, antiinflamasi, antimutagenik, dan antikanker (Anies Chamidah et al., 2024). 
Kandungan klorofil dapat digunakan sebagai indikator kesehatan tanaman, dengan tanaman sehat memiliki jumlah klorofil lebih besar (Sukmono et al., 2012). 
Klorofil dapat diisolasi dari berbagai sumber, termasuk mikroalga dan daun tanaman seperti singkong ( Winasih, 2020). 
Pengembangan klorofil sebagai pewarna makanan alami menghadapi tantangan stabilitas warna terhadap pH, oksidasi, dan pemanasan (Rachmawati, 2020). 
Estimasi kandungan klorofil dapat dilakukan menggunakan algoritma khusus dengan data airborne hyperspectral (Abdi et al., 2012).







"""

citation_rules = f"""
1. Dilarang melakukan kutipan pada kalimat yang juga hasil mengutip.
    Contoh:  Dampak rokok pada anak dibawah umur adalah buruk(Penulis,Tahun).
    Hal ini karena kutipan format APA 7 melarang hal tersebut
2. Cara menulis kutipan:
    Menggunakan nama akhir penulis.
    Nama: Ahmad Budi
    Tahun: 2021
    Contoh dua Penulis: 
    Kutipan: Teks kutipan(Budi,2021)
    Contoh satu Penulis:
    Kutipan: Teks kutipan( Budi dan Ilyas,Tahun)
    Contoh penulis lebih dari dua:
    Kutipan: Teks kutipan(Tegar et al., Tahun)
3. Pada satu referensi hanya boleh mengutip dari satu jurnal, jangan mengutip jurnal hingga dua kali
4. Tidak boleh mengarang, hana lakukan kutipan berdasarkan referensi teks yang diberikan

Contoh Kutipan Benar:
Beberapa jenis kacang yang populer antara lain kacang tanah (*Arachis hypogaea*), kacang kedelai (*Glycine max*), kacang hijau (*Vigna radiata*) (Ilyas dan Hakim, 2021)

Contoh Kutipan Salah:
Menurut Ilyas dan Hakim Beberapa jenis kacang yang populer antara lain kacang tanah (*Arachis hypogaea*), kacang kedelai (*Glycine max*), kacang hijau (*Vigna radiata*).
"""

writing_rules="""
1. Buatlah paragraft berdasarkan input pengguna
2. Paragraft harus berisi minimal 5 dan maksimal 6 kalimat yang menjawab, menjelaskan, dan mengembangkan input
3. Paragraft harus berisi minimal 2 kutipan dari referensi, dan tidak ada duplikat kutipan.



"""

prompt_context = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Kamu adalah Profesor penulis jurnal ilmiah dengan format APA7,\n
            Jawab input ini {input}\n
            Ini adalah referensi untuk menjawab pertanyaan:\n {context}\n
            Jika referensi tidak cukup untuk menjawab pertanyaan cukup katakan informasi yang diperlukan tidak cukup.\n
            Jangan mengarang jawaban yang tidak berasal dari referensi. Aku ulangi, jangan membuat kalimat yang tidak berdasarkan pada referensi.
            Tugasmu adalah \n {writing_rules} \n  ,Panduan kutipan adalah \n {citation_rules} \n
            Contoh jawaban yang benar adalah seperti ini:\n
            {example}
            ."""
        ),
        ("human", 
         """Tolong ikuti intruksi ini saat menjawab input.
            1. Baca dan pahami input
            2. Liat contoh jawaban yang benar
            3. Pahami aturan kepenulisan dan cara mengutip
            4. Hasilkan paragraft seperti intruksi 
         """),
    ]
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature =0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

chain_answer = prompt_context | llm
def answer(pencarian):
    context = querry(pencarian)
    if context is not None:
        print(context)
        content = chain_answer.invoke(
            {
                "writing_rules":writing_rules,
                "citation_rules":citation_rules,
                "context":context,
                "input":pencarian,
                "example":example,
            }
        )

  
    print("JAWABAN BERDASARKAN JURNAL    " ,content.content)
   
if __name__ == "__main__":
    #llm_querry("jelaskan pengertian nitrogen untuk tanaman")
    answer("Jelaskan cara budidaya pisang")
