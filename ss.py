from io import BytesIO
from text_handling import split_store
from chroma import list_jurnal
from semanticscholar import SemanticScholar
import fitz
import asyncio
import aiohttp
import uvloop



sch = SemanticScholar()
count = 0
count_lock = asyncio.Lock()
stop_event = asyncio.Event()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
semaphore = asyncio.Semaphore(5)

                                    


list_database={
      md["title"] for md in list_jurnal.get()['metadatas']
}

def main():
    semantic()

def semantic(querry,year):
    search_semantic(querry,year)

def search_semantic(querry,year):
        w = sch.search_paper(query=querry,year=f"{year}-2025",publication_types=['JournalArticle'],open_access_pdf=True,limit=50)
        print(f"MENDAPATKAN {w.total} PDF")
        asyncio.run(handle_pdf(w))
        return w    
    
async def handle_pdf(w):
     global count
     tasks = []
     connector = aiohttp.TCPConnector(limit_per_host=20, ttl_dns_cache=300, )
     async with aiohttp.ClientSession(connector=connector,) as session:
        for paper in w:
            if count >= 5 or paper == w.total:
                break
            if paper['title'].lower() in list_database:
                print(F"JURNAL KE {count} DENGAN JUDUL {paper['title'].lower()} SUDAH ADA DI DATABASE")
                continue
            if paper['openAccessPdf'].get('url'):
               tasks.append(extract_text(paper,paper['openAccessPdf'].get('url'),session))
        print("ASYNCIO RUN")
        await asyncio.gather(*tasks)

def parse_pdf(content):
    doc = fitz.open(stream=BytesIO(content),filetype="pdf")
    pages = ([page.get_text() for page in doc])
    return "\n".join(pages)



      
async def extract_text(paper,pdf_url, session):
                async with semaphore:
                    try:
                        async with session.get(pdf_url) as response:
                                    content_type = response.headers.get("Content-Type","")
                                    if "pdf"  not in content_type:
                                        return
                                    if response.status == 200:
                                        print(2)
                                        async with count_lock:
                                            global count
                                            if count >= 5 :
                                                stop_event.set()
                                                return
                                            count += 1
                                            print(f"MENCOBA MENYIMPAN JURNAL KE- {count}")  
                                        content = await response.read()
                                        text = await asyncio.to_thread(parse_pdf, content)   
                                        print("BERHASIL EKSTRAK TEKS")    
                                        await asyncio.to_thread(
                                            split_store, text,
                                            paper['title'].lower(), 
                                            paper['year'],
                                            ", ".join(author['name'] for author in paper['authors']),
                                            paper['openAccessPdf'].get('url') 
                                        )
                                       
                    except Exception as e:
                        print(f"Error Happened {e}")


if __name__== "__main__":
        search_semantic("rokok",2021)
    


