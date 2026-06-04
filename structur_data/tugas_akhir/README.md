# 🍽️ Restaurant Order Queue System

Sistem manajemen pesanan restoran berbasis Python Streamlit. Kelola pesanan dengan mudah dari intake hingga delivery!

## ✨ Fitur

- ✅ **Tambah Pesanan** - Input pesanan dengan nomor meja & menu
- ✅ **Tracking Status** - Pending → Sedang Dimasak → Siap → Selesai
- ✅ **Menu Management** - 8 menu dengan harga yang dapat dikustomisasi
- ✅ **Real-time Stats** - Tampilan statistik pesanan aktif, siap, & pendapatan
- ✅ **Riwayat Lengkap** - Lihat semua pesanan dengan filter status
- ✅ **Catatan Khusus** - Tambah instruksi khusus per pesanan (misal: tidak pedas)
- ✅ **Auto Calculation** - Hitung otomatis total harga per item & pesanan
- ✅ **Persistent Storage** - Data disimpan ke JSON, tidak hilang saat refresh
- ✅ **Responsive UI** - Interface yang user-friendly & mudah dipahami

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install streamlit
```

### 2. Jalankan Aplikasi
```bash
streamlit run app.py
```

App akan otomatis buka di `http://localhost:8501`

## 📁 Struktur File

```
├── app.py              # Frontend Streamlit (UI/UX)
├── backend.py          # Backend OrderQueue (Logic)
├── orders.json         # Database pesanan (auto-created)
└── README.md          # File ini
```

## 🎯 Cara Penggunaan

### Menambah Pesanan Baru
1. Di sidebar kiri, masukkan **Nomor Meja** (A1, B3, dll)
2. Pilih menu dengan mengganti quantity (0 = tidak pesan)
3. (Optional) Tambah catatan khusus
4. Klik **✅ Tambah Pesanan**

### Update Status Pesanan
1. **Pending → Masak**: Klik tombol **🔥 Masak** untuk mulai masak
2. **Masak → Siap**: Klik **✅ Siap** ketika makanan sudah jadi
3. **Siap → Selesai**: Klik **🛎️ Antar** ketika diantar ke meja

### Melihat Riwayat
- Tab **Semua Pesanan** untuk melihat semua dengan filter status
- Expand detail pesanan untuk lihat info lengkap

## 📊 Menu Default (Bisa Diubah di backend.py)

| Menu | Harga |
|------|-------|
| Nasi Goreng | Rp35.000 |
| Mie Goreng | Rp30.000 |
| Soto Ayam | Rp25.000 |
| Gado-Gado | Rp20.000 |
| Lumpia | Rp15.000 |
| Tahu Goreng | Rp12.000 |
| Es Teh Manis | Rp8.000 |
| Kopi | Rp10.000 |

## 🔧 Customization

### Tambah Menu Baru
Edit `MENU` di `backend.py`:
```python
MENU = {
    "Nasi Goreng": 35000,
    "Menu Baru": 50000,  # Tambah baris ini
    ...
}
```

### Ubah Nama Restoran
Edit title di `app.py`:
```python
st.title("🍽️ Nama Restoran Anda")
```

### Ubah Warna & Style
Edit CSS di `app.py` bagian `st.markdown("""<style>...`

## 📈 Backend Explanation

### Class `MenuItem`
- Menyimpan nama menu, harga, & qty
- Method `total_harga()` = harga × qty

### Class `Order`
- Menyimpan data pesanan lengkap
- Status: pending → sedang_masak → siap → selesai
- Method `total_harga()` = sum semua items
- Auto timestamp untuk created_at & waktu_selesai

### Class `OrderQueue`
- Main manager untuk semua pesanan
- `add_order()` - Tambah pesanan baru
- `update_status()` - Update status pesanan
- `get_*_orders()` - Filter pesanan per status
- `get_stats()` - Hitung statistik
- `_save_orders()` & `_load_orders()` - Manage JSON storage

## 💾 Data Storage

Semua pesanan disimpan di `orders.json`. Format:
```json
[
  {
    "id": 1,
    "nomor_meja": "A1",
    "items": [
      {"nama": "Nasi Goreng", "harga": 35000, "qty": 1}
    ],
    "status": "siap",
    "created_at": "14:30:00",
    "waktu_selesai": "14:45:00",
    "catatan": "Tidak pedas"
  }
]
```

## 🌐 Deploy ke Cloud

Bisa di-deploy gratis ke **Streamlit Cloud**:
1. Push code ke GitHub
2. Pergi ke https://share.streamlit.io
3. Connect GitHub repo
4. Deploy!

## 📝 Tips & Tricks

- **Balloons Effect**: Muncul otomatis ketika pesanan siap 🎉
- **Real-time Update**: Refresh otomatis ketika ada perubahan status
- **Filter**: Tab "Semua Pesanan" bisa difilter per status
- **Mobile Friendly**: Responsif di semua ukuran layar

## 🆘 Troubleshooting

**Port 8501 sudah terpakai?**
```bash
streamlit run app.py --server.port 8502
```

**Data hilang setelah refresh?**
Pastikan ada file `orders.json` di folder yang sama dengan app.py

**Nomor meja tidak bisa input?**
Pastikan Streamlit versi terbaru: `pip install --upgrade streamlit`

## 📞 Support

Jika ada error atau pertanyaan, cek:
1. Semua file di folder yang sama
2. Python versi 3.8+
3. Streamlit versi terbaru

---

**Happy Serving! 🍽️✨**

Dibuat dengan ❤️ menggunakan Streamlit
