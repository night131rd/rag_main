import re
import unicodedata
import ftfy
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chroma import stores_data


_HYPHEN_RE = re.compile(r"(\w+)-\n(\w+)")
_PAGE_NO_RE = re.compile(r"\n?\s*\d{1,3}\s*\n")
_HEADER_RE = re.compile(r"\n.*(Journal|Vol\.?|No\.?|ISSN).*?\n", flags=re.IGNORECASE)
_FIGCAP_RE = re.compile(r"\nFigure\s*\d+[:\.\s].*?(\n|$)", flags=re.IGNORECASE)
_REFS_RE = re.compile(r"(References|Daftar Pustaka)\s*[\s\S]+$", flags=re.IGNORECASE)
_SPACE_RE = re.compile(r"\s+")
_SENTENCE_RE = re.compile(r"\.([A-Za-z])")


def main():
    clean_pdf_text()


def clean_pdf_text(text):
    text = ftfy.fix_text(text)
    text = unicodedata.normalize("NFKC", text)
    text = _HYPHEN_RE.sub(r"\1\2", text)
    text = _PAGE_NO_RE.sub("\n", text)
    text = _HEADER_RE.sub("\n", text)
    text = _FIGCAP_RE.sub("\n", text)
    text = _REFS_RE.sub("", text)
    text = _SPACE_RE.sub(" ", text).strip()
    return _SENTENCE_RE.sub(r". \1", text)


def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    all_split = text_splitter.split_text(text)
    return all_split


def split_store(text, title, year, author, url):
    "PRINT MEMULAI MELAKUKAN SPLIT"
    text = clean_pdf_text(text)
    docs = split_text(text)
    print("BERHASIL MELAKUKAN SPLIT")
    if docs:
        title = title.lower()
        stores_data(docs, title, year, author, url)
    print(f"BERHASIL MENYIMPAN JURNAL DENGAN JUDUL {title}")


if __name__ == "__main__":
    text = "Rokok adalah produk olahan tembakau yang dikemas dalam bentuk silinder dari kertas dengan campuran cengkeh dan bahan tambahan lainnya yang diproduksi oleh pabrik maupun dibuat sendiri, yang digunakan dengan cara dibakar pada salah satu ujungnya dan dibiarkan membara agar asapnya dapat dihirup melalui mulut pada ujung lainnya. Kandungan berbahaya dalam rokok meliputi lebih dari 7.000 bahan kimia, termasuk nikotin yang bersifat adiktif, tar yang dapat menyebabkan kanker, dan karbon monoksida yang mengganggu sistem peredaran darah (Samsuri et al., 2023). Dampak kesehatan yang ditimbulkan oleh rokok tidak hanya mempengaruhi perokok aktif tetapi juga perokok pasif yang terpapar asap rokok di lingkungannya. Konsumsi rokok merupakan salah satu penyebab utama kematian yang dapat dicegah di seluruh dunia, dengan estimasi lebih dari 8 juta kematian setiap tahunnya (Kholis, 2024). Berbagai penelitian ilmiahtelah membuktikan bahwa merokok secara signifikan meningkatkan risiko berbagai penyakit serius seperti kanker paru-paru, penyakit jantung koroner, stroke, dan penyakit paru obstruktif kronik (PPOK).."

    # split_store("text", "judul", "tahun", "author", "url")
