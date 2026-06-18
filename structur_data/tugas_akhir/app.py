import streamlit as st
from backend import OrderQueue, MENU

st.set_page_config(page_title="Order Queue", layout="wide")

st.title("🍽️ Order Queue")

if "q" not in st.session_state:
    st.session_state.q = OrderQueue()

q = st.session_state.q

# ── SIDEBAR: Pesan (Enqueue) ──────────────────────────────
with st.sidebar:
    st.header("➕ Pesan")
    meja = st.text_input("Nomor Meja")
    pilihan = {}
    for nama, harga in MENU.items():
        qty = st.number_input(f"{nama} — Rp{harga:,}", min_value=0, max_value=20, value=0)
        if qty:
            pilihan[nama] = qty

    if st.button("Tambah ke Antrian", type="primary", use_container_width=True):
        if not meja.strip():
            st.error("Isi nomor meja!")
        elif not pilihan:
            st.error("Pilih minimal 1 menu!")
        else:
            q.enqueue(meja, list(pilihan.items()))
            st.success(f"Meja {meja} masuk antrian!")
            st.rerun()

# ── MAIN: Antrian ─────────────────────────────────────────
orders = q.get_all()

if not orders:
    st.info("Antrian kosong.")
else:
    for idx, order in enumerate(orders): # Tambahin idx di sini pakai enumerate
        with st.container(border=True): 
            c1, c2, c3 = st.columns([2, 3, 2]) 

            with c1:
                badge = {"antri": "🔴 Antri", "diproses": "🔥 Diproses", "selesai": "✅ Selesai"} 
                st.markdown(f"### Meja {order.meja}  `#{order.id}`") 
                st.write(badge[order.status], "·", order.waktu) 

            with c2:
                for item in order.items: 
                    st.write(f"- {item.nama} x{item.qty} = Rp{item.total():,}")
                st.markdown(f"**Total: Rp{order.total():,}**")

            with c3:
                # `if idx == 0:` supaya tombol cuma muncul di antrian paling atas
                if idx == 0:
                    if order.status == "antri": 
                        if st.button("🔥 Proses", key=f"p{order.id}", use_container_width=True): 
                            q.update_status(order.id, "diproses") 
                            st.rerun()

                    if order.status == "diproses": 
                        if st.button("✅ Selesai", key=f"s{order.id}", use_container_width=True, type="primary"):
                            q.dequeue()  
                            st.success(f"Meja {order.meja} selesai & dibuang dari antrian!")
                            st.rerun()


