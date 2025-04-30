from openalex import open_alex
from llm import llm_querry, answer

while True:
    pencarian_awal = input("Masukkan querry . . .")
    tahun = input("Masukkan tahun maksimal . . .")
    print("Memulai pencarian")
    pencarian = llm_querry(pencarian_awal)
    open_alex(pencarian, tahun)
    print("Memulai memuat jawaban")
    if open_alex is not None:
        answer(pencarian_awal)
