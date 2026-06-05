# 🍽️ Restaurant Order Queue System

Sistem antrian pesanan restoran sederhana berbasis **FIFO (First In, First Out)** menggunakan Python + Streamlit.

---

## 📁 Struktur File

```
├── app.py          # Frontend (Streamlit UI)
├── backend.py      # Logic antrian & data
├── orders.json     # Database pesanan (auto-generated)
└── README.md
```

---

## ⚙️ Instalasi

### 1. Clone / Download project
```bash
git clone <repo-url>
cd restaurant-order-queue
```

### 2. Install dependencies
```bash
pip install streamlit
```

### 3. Jalankan aplikasi
```bash
streamlit run app.py
```

Buka browser di `http://localhost:8501`

---

## 🔄 Alur Pesanan

```
ENQUEUE                PROSES               DEQUEUE
─────────              ──────               ───────
Pelanggan     →   🔴 Antri   →   🔥 Diproses   →   ✅ Selesai (otomatis buang)
pesan
```

1. **Enqueue** — Kasir input nomor meja + pilih menu → klik **Tambah ke Antrian**
2. **Diproses** — Dapur klik tombol 🔥 **Proses** saat mulai masak
3. **Dequeue** — Klik ✅ **Selesai** → order otomatis dibuang dari antrian

---

## 📋 Menu yang Tersedia

| Menu | Harga |
|------|-------|
| Nasi Goreng | Rp 35.000 |
| Mie Goreng | Rp 30.000 |
| Soto Ayam | Rp 25.000 |
| Gado-Gado | Rp 20.000 |
| Lumpia | Rp 15.000 |
| Tahu Goreng | Rp 12.000 |
| Es Teh Manis | Rp 8.000 |
| Kopi | Rp 10.000 |

---

## 🧠 Konsep Antrian (Queue)

Sistem ini menggunakan struktur data **Queue FIFO murni**:

| Operasi | Method | Keterangan |
|---------|--------|------------|
| **Enqueue** | `q.enqueue(meja, items)` | Tambah order ke **belakang** antrian |
| **Dequeue** | `q.dequeue()` | Ambil & hapus order dari **depan** antrian |
| Lihat semua | `q.get_all()` | Tampilkan seluruh isi antrian |
| Update status | `q.update_status(id, status)` | Ubah status order |

### Contoh penggunaan backend langsung:
```python
from backend import OrderQueue

q = OrderQueue()

# Enqueue
q.enqueue("A1", [("Nasi Goreng", 2), ("Kopi", 1)])
q.enqueue("B3", [("Mie Goreng", 1)])

# Dequeue (ambil order paling depan)
order = q.dequeue()
print(order.meja)   # A1
```

---

## 💾 Penyimpanan Data

Semua pesanan disimpan otomatis ke `orders.json` setiap ada perubahan. File ini akan dibuat otomatis saat pertama kali ada pesanan masuk.

Contoh isi `orders.json`:
```json
[
  {
    "id": 1,
    "meja": "A1",
    "items": [
      {"nama": "Nasi Goreng", "harga": 35000, "qty": 2}
    ],
    "status": "diproses",
    "waktu": "10:30:00"
  }
]
```

---

## 🗂️ Penjelasan Kode

### `backend.py`
- **`MenuItem`** — dataclass untuk satu item menu (nama, harga, qty)
- **`Order`** — dataclass untuk satu pesanan (id, meja, items, status, waktu)
- **`OrderQueue`** — class utama pengelola antrian

### `app.py`
- **Sidebar** — Form input pesanan baru (enqueue)
- **Main area** — Tampilan antrian dengan tombol aksi per order

---

## 📦 Requirements

```
streamlit>=1.28.0
python>=3.8
```
