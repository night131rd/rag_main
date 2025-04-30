from chromadb.utils import embedding_functions
import uuid
import chromadb


emb_fn = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path=".\data")

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


def stores_data(doc, title, year, author, url):
    list_jurnal.add(
        documents=doc,
        metadatas=[
            {"title": title, "year": year, "author": author, "url": url} for _ in doc
        ],
        ids=[str(uuid.uuid4()) for _ in doc],
    )


def querry(pencarian):
    context = " REFERENSI \n\n"
    print_text = context
    seen_titles = set()
    result = list_jurnal.query(
        query_texts=pencarian,
        n_results=100,
        include=["documents", "metadatas", "distances"],
        where={"year": {"$gte": 2021}},
    )
    from text_handling import clean_pdf_text

    count = 0
    for doc, meta in zip(result["documents"][0], result["metadatas"][0]):
        count += 1
        print(f"MEMULAI KE {count}")
        if meta["title"] in seen_titles:
            continue
        if len(seen_titles) >= 4:
            break
        doc = clean_pdf_text(doc)
        seen_titles.add(meta["title"])
        context += f"\n-------------------------------------\n TEXT: {doc}\n"
        context += f"JUDUL: {meta['title']}\n"
        context += f"TAHUN: {meta['year']}\n"
        context += f"AUTHOR: {meta['author']}\n"
        print_text += f"URL: {meta['url']}\n"

    print(context)
    return context


if __name__ == "__main__":
    querry("Nitrogen")
