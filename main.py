# import package
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel # untuk membuat parent class untuk schema di parent body 
import pandas as pd
from datetime import datetime # untuk mendapatkan waktu terkini 

# Membuat objek FastAPI
app = FastAPI()

# akan selalu menggunakan definsi variabel app = fast api -> app bebas pendefinisiannya

# membuat endpoint -> ketentuan untuk client membuat request
# function (get, put, post, delete)
# url (/...)


# memasukkan functionnya apa (get dkk) kemudian url (/)
# endpoint pertama/root  untuk mendapatkan pesan "Selamat Datang"
@app.get("/")
def getWelcome(): #function untuk menghandle endpoint 
    return {
        "msg": "Selamat Datamg!"
    }

# syarat membuat endpoint, mendefine endpoint -> mendefine function untuk endpoint, tiap endpoint akan ada function tersendiri. 
# ketika client mengirim request akan dibaca oleh api 
# application start up complete -> menandakan computer kita sudah menjadi API, tapi juga menjadi Client 
# Ketika menjadi API akan freeze, ketika ingin balik ke terimnal biasa harus mematikan FASTAPI, dengan mengklik ctrl + C u/ keluar dari fast api

# fastapi hanya berlaku kalau nama filenya main, kalo namanya app harus ditambahkan nama cth : fastapi dev app.py 

# buka di chrome -> localhost:8000 ketika di komputer sendiri ketika ditambahkan docs diakhir 8000-> akan membuka dokumentasi
# maskud dokumentasi semacam buku manual, cara penggunaan namanya Swagger -> API Documentation
# API Doc juga bisa menguji coba, bisa menguji API yang kita buat 


# Membuat endpoint baru untuk menampilkan semua isi dataset
@app.get("/data")
def getData():
    # melakukan proses pengambilan data dari csv 
    df = pd.read_csv("dataset.csv")

    # mengembalikan response isi dateset -> format df harus diganti ke dict / json -> () adalah method 
    # to_dict punya parameter namanya orient-> orient punya banyak variabel salah satunya records
    return df.to_dict(orient='records')

# ketika ada lebih dari 1 baris, akan banyak dict

# 
# routing/path parameter -> url dinamis -> menyeusaikan dengan data yang ada di server 
# parameter url 

# endpoint untuk menampilkan data sesuai dengan lokasi 
# misal ingin mengambil data dari rusia -> /data/Russia

# supaya tipe data tidak macem macem -> menentukan sebagai string 

@app.get("/data/{location}")
def getData(location: str):

    # melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")

    #filter data berdasarkan parameter menggunakan [] 
    result = df[df.location == location]

    # validate hasil ada dengan menggunakan logika if
    if len(result) == 0:
        # Menampilkan pesan error -> data tidak ditemukan
        raise HTTPException(status_code=404, detail="Data error tidak ditemukan bray!") 
    # RETURN KETIKA RESPON BERHASIL, KETIKA ERROR MENGGUNAKAN RAISE 

    # HTTPExecption hanya berfungsi untuk menampilkan error 


    # mengembalikan response isi dataset 
    return result.to_dict(orient='records')

password = "kopiluwak"

# Endpoint untuk menghapus data berdasarkan id 
@app.delete("/data/{id}") # karena parameter id maka def function akan id juga
def deleteData(id: int, api_key: str = Header(None)): # ketika client meminta request akan menampilakn header 
    # proses Authentication 
    if api_key == None or api_key != password:
        # kalau tidak ada kasih pesan error -> tidak ada akses
        raise HTTPException(status_code=401, detail= "you dont have accses!")


    # melakukan proses pengambilan data dari csv 
    df = pd.read_csv("dataset.csv")

    # cek apakah datanya ada
    result = df[df.id == id]

    # untuk cek apakah data itu ada atau tidak menggunakan if 
    if len(result) == 0:
        # Menampilkan pesan error -> data tidak ditemukan
        raise HTTPException(status_code=404, detail="Data error tidak ditemukan bray!") 
    
    # proses penghapusan data
    # condition
    result = df[df.id != id]

    # Untuk mengupdate csv
    result.to_csv("dataset.csv", index=False)

    # message after delete data -> wajib diberi return agar bisa menampilkan 
    return {
        "msg": "Data has been deleted!"
    }

# SKEMA/ model untuk request body 
class Profile(BaseModel): 
    id: int
    name: str
    age: int
    location: str


# endpoint untuk menambahkan data baru
@app.post("/data") # ketika pakai post, di fastapi bisa membuat skema
# perlu ada request body 
# untuk membuat request body harus membuat skema/model terlebih dahulu
def createData(profile: Profile):
    # melakukan proses pengambilan data dari csv 
    df = pd.read_csv("dataset.csv")

    # proses menambah baris data
    # untuk menambahkan data menggunakan concat
    # membuat df baru 
    newData = pd.DataFrame({
            'id': [profile.id],
            'name': [profile.name],
            'age': [profile.age],
            'location ': [profile.location],
            'created_at': [datetime.now().date()], # tanggal terkini 
    })

    # concat
    df = pd.concat([df, newData])

    # Untuk mengupdate csv
    df.to_csv("dataset.csv", index=False)


    # return harus dictionary agar bisa diproses menjadi json 
    return {
        "msg": "Data has been created!!!!!!"
    } 


