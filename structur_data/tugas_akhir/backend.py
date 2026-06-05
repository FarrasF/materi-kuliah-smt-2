import json
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

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

    def total(self):
        return self.harga * self.qty

@dataclass
class Order:
    id: int
    meja: str
    items: List[MenuItem] = field(default_factory=list)
    status: str = "antri"   # antri → diproses → selesai
    waktu: str = ""

    def __post_init__(self):
        if not self.waktu:
            self.waktu = datetime.now().strftime("%H:%M:%S")

    def total(self):
        return sum(i.total() for i in self.items)

    def to_dict(self):
        return {
            "id": self.id, "meja": self.meja,
            "items": [{"nama": i.nama, "harga": i.harga, "qty": i.qty} for i in self.items],
            "status": self.status, "waktu": self.waktu
        }

    @classmethod
    def from_dict(cls, d):
        items = [MenuItem(i["nama"], i["harga"], i["qty"]) for i in d["items"]]
        return cls(id=d["id"], meja=d["meja"], items=items, status=d["status"], waktu=d["waktu"])


class OrderQueue:
    def __init__(self, file_path="orders.json"):
        self.file_path = Path(file_path)
        self.queue: List[Order] = self._load()
        self.next_id = max((o.id for o in self.queue), default=0) + 1

    def _load(self):
        if not self.file_path.exists():
            return []
        with open(self.file_path) as f:
            return [Order.from_dict(d) for d in json.load(f)]

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump([o.to_dict() for o in self.queue], f, indent=2, ensure_ascii=False)

    # ENQUEUE — tambah order ke belakang antrian
    def enqueue(self, meja: str, items_list: List[tuple]) -> Order:
        items = [MenuItem(nama, MENU[nama], qty) for nama, qty in items_list if nama in MENU]
        order = Order(id=self.next_id, meja=meja, items=items)
        self.queue.append(order)
        self.next_id += 1
        self._save()
        return order

    # DEQUEUE — buang order paling depan (sudah selesai)
    def dequeue(self) -> Order:
        if not self.queue:
            return None
        order = self.queue.pop(0)
        self._save()
        return order

    def update_status(self, order_id: int, status: str):
        for o in self.queue:
            if o.id == order_id:
                o.status = status
                self._save()
                return True
        return False

    def get_all(self):
        return self.queue
