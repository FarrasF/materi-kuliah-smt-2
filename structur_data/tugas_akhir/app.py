import streamlit as st
from backend import OrderQueue, MENU
import time

# Setup page
st.set_page_config(
    page_title="Restaurant Order Queue",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; 
        padding: 20px; 
        border-radius: 10px;
        text-align: center;
    }
    .order-pending { border-left: 5px solid #FFA500; }
    .order-masak { border-left: 5px solid #FF6B6B; }
    .order-siap { border-left: 5px solid #51CF66; }
    .order-selesai { border-left: 5px solid #868E96; }
</style>
""", unsafe_allow_html=True)

st.title("🍽️ Restaurant Order Queue System")
st.caption("Sistem Manajemen Pesanan Restoran Real-time")

# Initialize queue
if "queue" not in st.session_state:
    st.session_state.queue = OrderQueue()

# SIDEBAR - Input Order Baru
with st.sidebar:
    st.header("➕ Pesanan Baru")
    
    col1, col2 = st.columns(2)
    with col1:
        nomor_meja = st.text_input("Nomor Meja", placeholder="Contoh: A1, B3")
    with col2:
        catatan = st.text_input("Catatan", placeholder="Misal: Tidak pedas")
    
    st.subheader("📋 Pilih Menu")
    selected_items = {}
    
    # Buat kolom untuk pilih item
    for menu_name, price in MENU.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            qty = st.number_input(
                f"{menu_name} (Rp{price:,})",
                min_value=0,
                max_value=20,
                value=0,
                label_visibility="visible"
            )
            if qty > 0:
                selected_items[menu_name] = qty
    
    if st.button("✅ Tambah Pesanan", use_container_width=True, type="primary"):
        if not nomor_meja.strip():
            st.error("⚠️ Masukkan nomor meja!")
        elif not selected_items:
            st.error("⚠️ Pilih minimal 1 menu!")
        else:
            items_list = list(selected_items.items())
            st.session_state.queue.add_order(nomor_meja, items_list, catatan)
            st.success(f"✅ Pesanan meja {nomor_meja} ditambahkan!")
            st.rerun()

# MAIN CONTENT
# Stats cards
col1, col2, col3, col4 = st.columns(4)
stats = st.session_state.queue.get_stats()

with col1:
    st.metric("⏳ Aktif", stats["aktif"])
with col2:
    st.metric("🔔 Siap Diantar", stats["siap"])
with col3:
    st.metric("✅ Selesai", stats["selesai"])
with col4:
    st.metric("💰 Pendapatan", f"Rp{stats['pendapatan']:,}")

st.divider()

# TABS
tab1, tab2, tab3 = st.tabs(["⏳ Pending & Sedang Dimasak", "🔔 Siap Diantar", "📊 Semua Pesanan"])

# TAB 1 - Pending & Sedang Masak
with tab1:
    st.subheader("Pesanan yang Sedang Diproses")
    active = st.session_state.queue.get_active_orders()
    
    if active:
        for order in active:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 2, 1.5])
                
                with col1:
                    status_badge = "🔴 Pending" if order.status == "pending" else "🔥 Sedang Dimasak"
                    st.markdown(f"### Meja {order.nomor_meja} | #{order.id}")
                    st.markdown(f"**{status_badge}** | {order.created_at}")
                    
                    if order.catatan:
                        st.info(f"📝 Catatan: {order.catatan}")
                
                with col2:
                    st.write("**Pesanan:**")
                    for item in order.items:
                        st.write(f"- {item.nama} x{item.qty} = Rp{item.total_harga():,}")
                    st.markdown(f"**Total: Rp{order.total_harga():,}**")
                
                with col3:
                    st.write("**Aksi:**")
                    if order.status == "pending":
                        if st.button("🔥 Masak", key=f"masak_{order.id}", use_container_width=True):
                            st.session_state.queue.update_status(order.id, "sedang_masak")
                            st.rerun()
                    
                    if st.button("✅ Siap", key=f"siap_{order.id}", use_container_width=True):
                        st.session_state.queue.update_status(order.id, "siap")
                        st.balloons()
                        st.success(f"Pesanan meja {order.nomor_meja} siap diantar!")
                        st.rerun()
                    
                    if st.button("🗑️ Hapus", key=f"delete_active_{order.id}", use_container_width=True):
                        st.session_state.queue.delete_order(order.id)
                        st.rerun()
    else:
        st.info("✨ Tidak ada pesanan aktif")

# TAB 2 - Siap Diantar
with tab2:
    st.subheader("🔔 Pesanan Siap Diantar")
    ready = st.session_state.queue.get_ready_orders()
    
    if ready:
        for order in ready:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 2, 1.5])
                
                with col1:
                    st.markdown(f"### 🎉 Meja {order.nomor_meja} | #{order.id}")
                    st.markdown(f"**✅ Siap** | Dibuat: {order.created_at} | Siap: {order.waktu_selesai}")
                    
                with col2:
                    st.write("**Pesanan:**")
                    for item in order.items:
                        st.write(f"- {item.nama} x{item.qty}")
                    st.markdown(f"**Total: Rp{order.total_harga():,}**")
                
                with col3:
                    st.write("**Aksi:**")
                    if st.button("🛎️ Antar", key=f"antar_{order.id}", use_container_width=True, type="primary"):
                        st.session_state.queue.update_status(order.id, "selesai")
                        st.success(f"Pesanan diantar ke meja {order.nomor_meja}!")
                        st.rerun()
                    
                    if st.button("🗑️ Hapus", key=f"delete_ready_{order.id}", use_container_width=True):
                        st.session_state.queue.delete_order(order.id)
                        st.rerun()
    else:
        st.info("📭 Tidak ada pesanan yang siap")

# TAB 3 - Semua Pesanan
with tab3:
    st.subheader("📊 Riwayat Semua Pesanan")
    all_orders = st.session_state.queue.get_all_orders()
    
    if all_orders:
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            filter_status = st.multiselect(
                "Filter Status",
                ["pending", "sedang_masak", "siap", "selesai"],
                default=["pending", "sedang_masak", "siap", "selesai"]
            )
        
        filtered = [o for o in all_orders if o.status in filter_status]
        
        # Display filtered orders
        for order in reversed(filtered):
            status_map = {
                "pending": "🔴 Pending",
                "sedang_masak": "🔥 Sedang Dimasak",
                "siap": "🟢 Siap",
                "selesai": "✅ Selesai"
            }
            
            with st.expander(f"Meja {order.nomor_meja} | {status_map[order.status]} | Rp{order.total_harga():,}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**ID Pesanan:** #{order.id}")
                    st.write(f"**Waktu Pesan:** {order.created_at}")
                    if order.waktu_selesai:
                        st.write(f"**Waktu Selesai:** {order.waktu_selesai}")
                    if order.catatan:
                        st.write(f"**Catatan:** {order.catatan}")
                
                with col2:
                    st.write("**Items:**")
                    for item in order.items:
                        st.write(f"- {item.nama} x{item.qty} = Rp{item.total_harga():,}")
                
                if st.button("🗑️ Hapus Pesanan", key=f"delete_history_{order.id}"):
                    st.session_state.queue.delete_order(order.id)
                    st.rerun()
    else:
        st.info("📭 Tidak ada pesanan")

# Footer
st.divider()
st.caption("Restaurant Order Queue System v1.0 | Data tersimpan otomatis")
