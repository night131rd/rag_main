from openalex import open_alex
from llm import llm_querry, answer
import json

while True:
    pencarian = input("Masukkan querry . . .")
    tahun = input ("Masukkan tahun maksimal . . .")
    print("Memulai pencarian")
    pencarian = llm_querry(pencarian)
    open_alex(pencarian,tahun)
    print("Memulai memuat jawaban")
    answer(pencarian)












