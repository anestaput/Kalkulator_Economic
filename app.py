import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# 🟢 Konfigurasi halaman
st.set_page_config(
    page_title="Kalkulator EOQ Profesional",
    layout="centered"
)

# 🟢 Header
st.markdown(
    """
    <h1 style='text-align: center; color: #2c3e50;'>📦 EOQ (Economic Order Quantity)</h1>
    <p style='text-align: center; font-size:18px;'>Hitung jumlah pemesanan optimal & visualisasi grafik biaya persediaan</p>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

# 🟢 Input form
col1, col2, col3 = st.columns(3)
with col1:
    D = st.number_input("📈 Permintaan Tahunan (D)", min_value=1.0, format="%.2f")
with col2:
    S = st.number_input("💰 Biaya Pemesanan (S)", min_value=1.0, format="%.2f")
with col3:
    H = st.number_input("🏬 Biaya Penyimpanan per Unit (H)", min_value=1.0, format="%.2f")

# 🟢 Proses hitung EOQ
if st.button("🚀 Hitung EOQ"):
    EOQ = np.sqrt((2 * D * S) / H)
    N = D / EOQ
    TC = (D / EOQ) * S + (EOQ / 2) * H

    # 🟢 Tampilkan hasil
    st.success("✅ Perhitungan Selesai!")
    st.markdown(f"""
    - 📦 *EOQ:* {EOQ:.2f} unit  
    - 🔁 *Jumlah Pesanan per Tahun:* {N:.2f} kali  
    - 💸 *Total Biaya Persediaan:* Rp {TC:,.2f}
    """)
    st.markdown("---")

    # 🟢 Simulasi animasi pemesanan
    st.subheader("🎬 Simulasi Proses Pemesanan")
    progress = st.progress(0)
    status = st.empty()
    steps = min(10, int(N))
    for i in range(steps):
        status.text(f"📦 Pemesanan ke-{i+1} sedang diproses...")
        time.sleep(0.3)
        progress.progress((i+1)/steps)
    status.text("✅ Semua pemesanan selesai diproses!")
    st.markdown("---")

    # 🟢 Grafik EOQ Profesional (Q vs Cost)
    st.subheader("📈 Grafik EOQ vs Biaya")

    Q = np.linspace(5, EOQ * 2, 200)  # start dari 5 agar tidak meleyot
    ordering_cost = (D / Q) * S
    holding_cost = (Q / 2) * H
    total_cost = ordering_cost + holding_cost

    fig, ax = plt.subplots(figsize=(9,6))
    ax.plot(Q, ordering_cost, label="Ordering Costs", color="dodgerblue", linewidth=2)
    ax.plot(Q, holding_cost, label="Holding Costs", color="black", linewidth=2)
    ax.plot(Q, total_cost, label="Total Cost", color="red", linewidth=2)

    # Garis vertikal EOQ + titik EOQ
    ax.axvline(EOQ, color="gray", linestyle="--", linewidth=1)
    ax.scatter([EOQ], [TC], color="gold", edgecolor="black", s=100, zorder=5)

    # Label dan layout
    ax.set_title("EOQ vs Komponen Biaya", fontsize=14, fontweight='bold')
    ax.set_xlabel("Re-Order Quantity (Q)")
    ax.set_ylabel("Annual Cost")
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.6)

    st.pyplot(fig)
    st.info("📌 EOQ optimal terjadi saat Total Cost minimum (titik kuning).")
else:
    st.info("Masukkan nilai D, S, dan H lalu klik *Hitung EOQ*.")
