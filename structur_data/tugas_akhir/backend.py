import json
from pathlib import Path
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Dict

# Menu makanan yang tersedia
MENU = {
    "Nasi Goreng": 35000,
    "Mie Goreng": 30000,
    "Soto Ayam": 25000,
    "Gado-Gado": 20000,
    "Lumpia": 15000,
    "Tahu Goreng": 12000,
    "Es Teh Manis": 8000,
    "Kopi": 10000,
}

@dataclass
class MenuItem:
    nama: str
    harga: int
    qty: int = 1
    
    def total_harga(self):
        return self.harga * self.qty

@dataclass
class Order:
    id: int
    nomor_meja: str
    items: List[MenuItem] = field(default_factory=list)
    status: str = "pending"  # pending, sedang_masak, siap, selesai
    created_at: str = ""
    waktu_selesai: str = ""
    catatan: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().strftime("%H:%M:%S")
    
    def total_harga(self):
        return sum(item.total_harga() for item in self.items)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nomor_meja": self.nomor_meja,
            "items": [{"nama": i.nama, "harga": i.harga, "qty": i.qty} for i in self.items],
            "status": self.status,
            "created_at": self.created_at,
            "waktu_selesai": self.waktu_selesai,
            "catatan": self.catatan
        }
    
    @classmethod
    def from_dict(cls, data):
        items = [MenuItem(i["nama"], i["harga"], i["qty"]) for i in data["items"]]
        return cls(
            id=data["id"],
            nomor_meja=data["nomor_meja"],
            items=items,
            status=data["status"],
            created_at=data["created_at"],
            waktu_selesai=data.get("waktu_selesai", ""),
            catatan=data.get("catatan", "")
        )

class OrderQueue:
    def __init__(self, file_path: str = "orders.json"):
        self.file_path = Path(file_path)
        self.orders = self._load_orders()
        self.next_id = max([o.id for o in self.orders], default=0) + 1
    
    def _load_orders(self) -> List[Order]:
        """Load orders dari file JSON"""
        if not self.file_path.exists():
            return []
        
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            return [Order.from_dict(order) for order in data]
    
    def _save_orders(self):
        """Simpan orders ke file JSON"""
        with open(self.file_path, 'w') as f:
            json.dump([o.to_dict() for o in self.orders], f, indent=2, ensure_ascii=False)
    
    def add_order(self, nomor_meja: str, items_list: List[tuple], catatan: str = "") -> Order:
        """
        Tambah order baru
        items_list: list of (nama_menu, qty)
        """
        items = []
        for nama, qty in items_list:
            if nama in MENU:
                items.append(MenuItem(nama, MENU[nama], qty))
        
        order = Order(
            id=self.next_id,
            nomor_meja=nomor_meja,
            items=items,
            catatan=catatan
        )
        self.orders.append(order)
        self.next_id += 1
        self._save_orders()
        return order
    
    def get_all_orders(self) -> List[Order]:
        """Dapatkan semua orders"""
        return self.orders
    
    def get_pending_orders(self) -> List[Order]:
        """Dapatkan orders yang pending (belum dimasak)"""
        return [o for o in self.orders if o.status == "pending"]
    
    def get_active_orders(self) -> List[Order]:
        """Dapatkan orders yang aktif (pending & sedang dimasak)"""
        return [o for o in self.orders if o.status in ["pending", "sedang_masak"]]
    
    def get_ready_orders(self) -> List[Order]:
        """Dapatkan orders yang sudah siap"""
        return [o for o in self.orders if o.status == "siap"]
    
    def update_status(self, order_id: int, status: str) -> bool:
        """Update status order"""
        for order in self.orders:
            if order.id == order_id:
                order.status = status
                if status == "siap":
                    order.waktu_selesai = datetime.now().strftime("%H:%M:%S")
                self._save_orders()
                return True
        return False
    
    def delete_order(self, order_id: int) -> bool:
        """Hapus order"""
        self.orders = [o for o in self.orders if o.id != order_id]
        self._save_orders()
        return True
    
    def get_stats(self) -> dict:
        """Dapatkan statistik restoran"""
        active = len(self.get_active_orders())
        ready = len(self.get_ready_orders())
        completed = len([o for o in self.orders if o.status == "selesai"])
        total_revenue = sum(o.total_harga() for o in self.orders if o.status == "selesai")
        
        return {
            "aktif": active,
            "siap": ready,
            "selesai": completed,
            "pendapatan": total_revenue
        }
