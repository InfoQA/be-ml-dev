# be-ml-dev
back-end api &amp; machine learning

### ⚙️ Prasyarat
- Python 3.9+
- pip

---

### 🚀 Cara Menjalankan Program
#### 1️⃣ Masuk ke folder project
```bash
  cd be-ml-dev
```
#### 2️⃣ Aktifkan virtual environment
```bash
  venv\Scripts\activate
```
Jika berhasil, terminal akan berubah menjadi :
```commandline
(venv) be-ml-dev>
```
#### 3️⃣ Install dependency (Jalankan sekali saja )
```bash
  pip install fastapi uvicorn
```
#### 4️⃣ Jalankan server FastAPI
```bash
  python -m uvicorn app.main:app --reload
```
Jika berhasil, akan muncul : 
```commandline
Uvicorn running on http://127.0.0.1:8000
```
---
### 🌐 Akses Halaman FastAPI
Fast  API tidak memiliki halaman wwebsite seperti Laravel atau Django. Yang tersedia adalah endpoint API dan halaman dokumentasi.

#### Dokumentasi API
```commandline
http://127.0.0.1:8000/docs
```
* Halaman utama FastAPI
* Bisa langsung test endpoint
* Digunakan untuk development

### Redoc
```commandline
http://127.0.0.1:8000/redoc
```
* Dokumentasi versi rapi 
* Hanya untuk membaca (read-only)