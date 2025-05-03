from openalex import open_alex
from llm import llm_querry, answer


while True:
    input_user = input("Masukkan querry . . .")
    tahun = input ("Masukkan tahun maksimal . . .")
    print("Memulai pencarian")
    list_pencarian = llm_querry(input_user)
    open_alex(list_pencarian,tahun)
    print("Memulai memuat jawaban")
    answer(input_user,list_pencarian)














