from semanticscholar import SemanticScholar
import time

sch = SemanticScholar(timeout=5)
time_before = time.time()
paper = sch.search_paper(query="padi",year="2023-2025",publication_types=['JournalArticle'],open_access_pdf=True,limit=50)
print(time_before-time.time())

for i, p in enumerate(paper):
    print(f"\n Paper {i+1}: ")
    print(f"Title: {p['url']}")
    print(p['year'])