import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

def hitung_eoq(D, S, H):
    """
    Fungsi untuk menghitung Economic Order Quantity (EOQ).
    """
    if D <= 0 or S <= 0 or H <= 0:
        return None, None, None, "Nilai permintaan tahunan, biaya pemesanan, dan biaya penyimpanan harus lebih besar dari nol."
    
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
    page_icon="�",
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

        st.markdown("---")
        st.header("Visualisasi Biaya Persediaan")

        # Generate data for the plot
        # Create a range of order quantities around the EOQ
        min_q = max(1, int(eoq_result * 0.1))
        max_q = int(eoq_result * 2.0) + 1
        q_values = np.linspace(min_q, max_q, 500)

        # Calculate ordering cost, holding cost, and total cost for each Q
        ordering_costs = (permintaan_tahunan / q_values) * biaya_pemesanan
        holding_costs = (q_values / 2) * biaya_penyimpanan
        total_costs = ordering_costs + holding_costs

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(q_values, ordering_costs, label='Biaya Pemesanan (D/Q * S)', color='red')
        ax.plot(q_values, holding_costs, label='Biaya Penyimpanan (Q/2 * H)', color='green')
        ax.plot(q_values, total_costs, label='Total Biaya Persediaan', color='blue', linewidth=2)

        # Mark the EOQ point
        ax.axvline(eoq_result, color='purple', linestyle='--', label=f'EOQ = {eoq_result:,.2f}')
        ax.plot(eoq_result, total_cost_result, 'o', color='purple', markersize=8) # Mark the EOQ point

        ax.set_title('Kurva Biaya Persediaan vs. Kuantitas Pesanan')
        ax.set_xlabel('Kuantitas Pesanan (Q)')
        ax.set_ylabel('Biaya (Rp)')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_ylim(bottom=0) # Ensure y-axis starts from 0
        ax.set_xlim(left=0) # Ensure x-axis starts from 0

        st.pyplot(fig)
        st.markdown("""
        Grafik di atas menunjukkan bagaimana total biaya persediaan berubah
        seiring dengan perubahan kuantitas pesanan. Titik terendah pada kurva
        Total Biaya Persediaan adalah Economic Order Quantity (EOQ).
        """)
    else:
        st.warning("Silakan masukkan nilai yang valid untuk semua parameter.")

st.markdown("---")
