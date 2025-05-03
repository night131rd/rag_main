from pyalex import Works,config
from io import BytesIO
from text_handling import split_store
from chroma import list_jurnal
import pyalex
import fitz
import asyncio
import aiohttp
import uvloop


config.max_retries = 100
config.retry_backoff_factor = 0.1
config.retry_http_codes = [429, 500, 503]
pyalex.config.email = "ifanns2021@student.uns.ac.id"

count = 0
count_lock = asyncio.Lock()
stop_event = asyncio.Event()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())



list_database={
      md["title"] for md in list_jurnal.get()['metadatas']
}

def main():
      open_alex()

def open_alex(querry,year):
        search_works(querry,year)

def search_works(querry,year):
        w= Works().search(querry).filter(publication_year=f"{year}-",is_oa= True).get()
        print(f"MENDAPATKAN TOTAL {len(w)} PDF")
        asyncio.run(handle_pdf(w))
        return w    
    
async def handle_pdf(w):
     semaphore = asyncio.Semaphore(len(w))
     global count
     tasks = []
     time_out = aiohttp.ClientTimeout(total = 15)
     connector = aiohttp.TCPConnector(limit_per_host=5, ttl_dns_cache=300,ssl=False)
     async with aiohttp.ClientSession(connector=connector, timeout=time_out) as session:
        for paper in w:
            if count >= 4 or any(paper == p for p in w[-1]):
                break
            if str(paper.get('title','Unknown')).lower() in list_database:
                count +=1
                print(F"JURNAL DENGAN JUDUL {paper.get('title','Unknown').lower()} SUDAH ADA DI DATABASE")
                continue
            if paper.get('primary_location').get('pdf_url'):
                tasks.append(extract_text(paper,paper.get('primary_location').get('pdf_url'),session,semaphore))
        await asyncio.gather(*tasks)

def parse_pdf(content):
    doc = fitz.open(stream=BytesIO(content),filetype="pdf")
    pages = ([page.get_text() for page in doc])
    return "\n".join(pages)



      
async def extract_text(paper,pdf_url, session,semaphore):            
                async with semaphore:
                    try:
                        async with session.get(pdf_url,ssl =False) as response:
                                    content_type = response.headers.get("Content-Type","")
                                    print(response.status)
                                    if "pdf"  not in content_type:
                                        return
                                    if response.status == 200:
                                        async with count_lock:
                                            global count
                                            if count >= 4 :
                                                stop_event.set()
                                                return
                                            count += 1
                                            print(f"MENCOBA MENYIMPAN JURNAL KE- {count}")  
                                        content = await response.read()
                                        text = await asyncio.to_thread(parse_pdf, content)   
                                        print("BERHASIL EKSTRAK TEKS")    
                                        await asyncio.to_thread(
                                            split_store, text,
                                            paper.get('title','Unknown').lower(), 
                                            paper["publication_year"],
                                            ", ".join(a["author"]["display_name"] for a in paper["authorships"]),
                                            paper["primary_location"]["pdf_url"]) 
                    except asyncio.TimeoutError:
                          print(f" TIME OUT ERROR ")
                                                         
                    except Exception as e:
                        print(f"Error Happened {e}")


if __name__== "__main__":
        open_alex("Defisiensi nitrogen",2021)
    


