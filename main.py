import os
import tempfile

os.environ['MPLCONFIGDIR'] = os.path.join(tempfile.gettempdir(), 'matplotlib_config')
os.makedirs(os.environ['MPLCONFIGDIR'], exist_ok=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import classic_algo
import pqc_algo

st.set_page_config(page_title="Advanced Crypto Lab", layout="wide", page_icon="🛡️")

if not pqc_algo.OQS_AVAILABLE:
    st.error("Error: liboqs python wrapper not found. Please install proper dependencies.")
    st.stop()

st.title("🛡️ Quantum vs Classic: Advanced Benchmark")


mode = st.sidebar.radio(
    "1. Operation Mode", 
    ["KEM (Key Exchange)", "Digital Signatures"]
)

data_source = st.sidebar.radio(
    "2. Input Source", 
    ["Random Generated", "Upload File"]
)

payload_bytes = b""
if data_source == "Random Generated":
    size_kb = st.sidebar.slider("Payload Size (KB):", 1, 1024, 5)
    payload_bytes = os.urandom(size_kb * 1024)
else:
    uploaded_file = st.sidebar.file_uploader("Upload a file to test:", type=None)
    if uploaded_file is not None:
        payload_bytes = uploaded_file.read()
        st.sidebar.success(f"Loaded {len(payload_bytes)/1024:.2f} KB")
    else:
        st.sidebar.warning("No file uploaded, using 1KB dummy.")
        payload_bytes = os.urandom(1024)

st.sidebar.divider()
st.sidebar.markdown("**3. Algorithm Selection**")
iterations = st.sidebar.number_input("Iterations:", 10, 500, 20)

selected_algos = []

if mode.startswith("KEM"):
    op_labels = ["Encaps", "Decaps"]
    
    st.sidebar.subheader("Classic KEM (RSA)")
    classic_opts = classic_algo.get_rsa_options()
    sel_classic = st.sidebar.multiselect("Select RSA sizes:", classic_opts, default=["RSA-2048"])
    
    st.sidebar.subheader("Post-Quantum KEM")
    pqc_opts = pqc_algo.get_available_kem()
    default_pqc = pqc_opts[:2] if pqc_opts else []
    sel_pqc = st.sidebar.multiselect("Select PQC KEMs:", pqc_opts, default=default_pqc)
    
    selected_algos = sel_classic + sel_pqc

else:
    op_labels = ["Sign", "Verify"]
    
    st.sidebar.subheader("Classic Sign (ECDSA)")
    classic_opts = classic_algo.get_ecc_options()
    sel_classic = st.sidebar.multiselect("Select Curves:", classic_opts, default=["SECP256R1 (P-256)"])
    
    st.sidebar.subheader("Post-Quantum Sign")
    pqc_opts = pqc_algo.get_available_sig()
    default_pqc = pqc_opts[:2] if pqc_opts else []
    sel_pqc = st.sidebar.multiselect("Select PQC Sigs:", pqc_opts, default=default_pqc)
    
    selected_algos = sel_classic + sel_pqc


if st.sidebar.button("🚀 Run Comprehensive Test"):
    if not selected_algos:
        st.error("Please select at least one algorithm.")
        st.stop()

    results = []
    progress_bar = st.progress(0)
    
    for idx, algo in enumerate(selected_algos):
        is_rsa = "RSA" in algo
        is_ecc = "SECP" in algo
        
        acc = {"KG": [], "OP1": [], "OP2": []}
        meta = {}
        
        for _ in range(iterations):
            if is_rsa:
                res = classic_algo.benchmark_rsa_kem(algo, payload_bytes)
            elif is_ecc:
                res = classic_algo.benchmark_ecdsa_sign(algo, payload_bytes)
            elif mode.startswith("KEM"):
                res = pqc_algo.benchmark_pqc_kem(algo, payload_bytes)
            else:
                res = pqc_algo.benchmark_pqc_sign(algo, payload_bytes)
            
            acc["KG"].append(res["KeyGen (ms)"])
            acc["OP1"].append(res[f"{op_labels[0]} (ms)"])
            acc["OP2"].append(res[f"{op_labels[1]} (ms)"])
            
            meta = {
                "PK Size": res["PK Size (B)"],
                "SK Size": res["SK Size (B)"],
                "Output Size": res["CT/Sig Size (B)"]
            }
        
        avg_res = {
            "Algorithm": algo,
            "Family": "Classic" if (is_rsa or is_ecc) else "Post-Quantum",
            "KeyGen (ms)": sum(acc["KG"]) / iterations,
            f"{op_labels[0]} (ms)": sum(acc["OP1"]) / iterations,
            f"{op_labels[1]} (ms)": sum(acc["OP2"]) / iterations,
            "Total Time (ms)": (sum(acc["KG"]) + sum(acc["OP1"]) + sum(acc["OP2"])) / iterations,
            "Total Bandwidth (B)": meta["PK Size"] + meta["Output Size"]
        }
        avg_res.update(meta)
        results.append(avg_res)
        progress_bar.progress((idx + 1) / len(selected_algos))

    df = pd.DataFrame(results)

    tab1, tab2, tab3 = st.tabs(["Performance", "Data Sizes", "Trade-off Analysis"])

    def draw_chart(fig):
        try:
            st.plotly_chart(fig, on_select="ignore", selection_mode="points") 
        except TypeError:
             st.plotly_chart(fig)

    with tab1:
        st.subheader("Time Complexity Comparison")
        st.caption("Lower is better.")
        
        df_long = df.melt(id_vars=["Algorithm", "Family"], 
                          value_vars=["KeyGen (ms)", f"{op_labels[0]} (ms)", f"{op_labels[1]} (ms)"], 
                          var_name="Operation", value_name="Time (ms)")
        
        fig_time = px.bar(df_long, x="Algorithm", y="Time (ms)", color="Operation", 
                          facet_col="Family", title="Execution Time per Operation")
        st.plotly_chart(fig_time)

    with tab2:
        st.subheader("Memory & Bandwidth Overhead")
        st.caption("Lower is better. Note the Logarithmic Scale.")
        
        df_size = df.melt(id_vars=["Algorithm", "Family"], 
                          value_vars=["PK Size", "SK Size", "Output Size"], 
                          var_name="Artifact", value_name="Size (Bytes)")
        
        fig_size = px.bar(df_size, x="Algorithm", y="Size (Bytes)", color="Artifact", 
                          barmode="group", log_y=True, title="Key & Signature/Ciphertext Sizes")
        st.plotly_chart(fig_size)

    with tab3:
        st.subheader("Efficiency Trade-off: Speed vs Size")
        
        st.caption("The 'Sweet Spot' is the bottom-left corner (Fast & Small).")
        
        fig_scatter = px.scatter(
            df, 
            x="Total Bandwidth (B)", 
            y="Total Time (ms)", 
            color="Family", 
            symbol="Family",
            hover_data=["Algorithm"],
            log_x=True, 
            log_y=True,
            size_max=60,
            title="Total Time vs Total Network Overhead (Log-Log Scale)"
        )
        st.plotly_chart(fig_scatter)

    st.divider()
    st.subheader("📄 Raw Data")
    st.dataframe(df.style.format(precision=3).background_gradient(subset=["Total Time (ms)"], cmap="RdYlGn_r"))
