# app.py

import streamlit as st
import math

def hitung_eoq(D, S, H):
    """
    Fungsi untuk menghitung Economic Order Quantity (EOQ).
    """
    if D <= 0 or S <= 0 or H <= 0:
        return None, "Nilai permintaan tahunan, biaya pemesanan, dan biaya penyimpanan harus lebih besar dari nol."
    
    eoq = math.sqrt((2 * D * S) / H)
    
    # Hitung jumlah pesanan per tahun
    jumlah_pesanan = D / eoq if eoq > 0 else 0
    
    # Hitung total biaya persediaan
    # Biaya pemesanan total = (D/eoq) * S
    # Biaya penyimpanan total = (eoq/2) * H
    total_biaya_persediaan = (D / eoq) * S + (eoq / 2) * H if eoq > 0 else 0
    
    return eoq, jumlah_pesanan, total_biaya_persediaan, None

# --- Judul dan Deskripsi Aplikasi ---
st.set_page_config(
    page_title="Kalkulator EOQ Interaktif",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Kalkulator Economic Order Quantity (EOQ)")
st.markdown("""
Aplikasi ini membantu Anda menghitung jumlah pesanan ekonomis (EOQ) 
untuk meminimalkan total biaya persediaan, serta informasi terkait lainnya.
""")

st.markdown("---")

# --- Input Pengguna ---
st.header("Masukkan Parameter Persediaan")

col1, col2, col3 = st.columns(3)

with col1:
    permintaan_tahunan = st.number_input(
        "Permintaan Tahunan (D - unit)", 
        min_value=0.0, 
        value=1000.0, 
        step=10.0,
        help="Total unit produk yang dibutuhkan dalam setahun."
    )

with col2:
    biaya_pemesanan = st.number_input(
        "Biaya Pemesanan per Pesanan (S - Rp)", 
        min_value=0.0, 
        value=50000.0, 
        step=1000.0,
        help="Biaya tetap yang dikeluarkan setiap kali melakukan pemesanan (misal: biaya administrasi, pengiriman)."
    )

with col3:
    biaya_penyimpanan = st.number_input(
        "Biaya Penyimpanan per Unit per Tahun (H - Rp)", 
        min_value=0.0, 
        value=10000.0, 
        step=500.0,
        help="Biaya untuk menyimpan satu unit produk di gudang selama satu tahun (misal: sewa, asuransi, depresiasi)."
    )

# --- Tombol Hitung ---
if st.button("Hitung EOQ"):
    eoq_result, num_orders_result, total_cost_result, error_msg = hitung_eoq(
        permintaan_tahunan, biaya_pemesanan, biaya_penyimpanan
    )

    if error_msg:
        st.error(f"⚠️ Error: {error_msg}")
    elif eoq_result is not None:
        st.markdown("---")
        st.header("Hasil Perhitungan EOQ")
        
        st.info(f"**Economic Order Quantity (EOQ):** `{eoq_result:,.2f}` unit")
        st.markdown(f"""
        Ini adalah jumlah unit ideal yang harus Anda pesan setiap kali
        untuk meminimalkan total biaya persediaan Anda.
        """)

        st.subheader("Detail Biaya dan Pesanan")
        st.write(f"**Jumlah Pesanan per Tahun:** `{num_orders_result:,.2f}` kali")
        st.write(f"**Total Biaya Persediaan (Minimal):** `Rp {total_cost_result:,.2f}` per tahun")
        
        st.markdown("""
        **Penjelasan:**
        - **Jumlah Pesanan per Tahun:** Berapa kali Anda perlu melakukan pemesanan dalam setahun berdasarkan EOQ.
        - **Total Biaya Persediaan:** Jumlah dari biaya pemesanan total dan biaya penyimpanan total pada tingkat EOQ.
        """)
    else:
        st.warning("Silakan masukkan nilai yang valid untuk semua parameter.")

st.markdown("---")
st.markdown("Dibuat dengan cinta untuk tugas Matematika Terapan.")