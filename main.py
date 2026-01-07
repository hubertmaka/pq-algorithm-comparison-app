import os
import tempfile
import json

# Use home directory instead of /tmp to avoid "No space left on device" in Docker
try:
    mpl_config_dir = os.path.join(os.path.expanduser('~'), '.matplotlib_cache')
    os.environ['MPLCONFIGDIR'] = mpl_config_dir
    os.makedirs(mpl_config_dir, exist_ok=True)
except OSError:
    # If can't create matplotlib cache, continue anyway (matplotlib will use default)
    pass

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
import classic_algo
import pqc_algo
import hybrid_encryption
import scenarios
import statistics_utils
import export_utils
import analysis_utils
import translations

st.set_page_config(page_title="PQC vs Classic Crypto Benchmark", layout="wide", page_icon="🔐")

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Get translations
t = translations.get_all_texts(st.session_state.language)

if not pqc_algo.OQS_AVAILABLE:
    st.error(f"⚠️ {t['error_liboqs']}")
    st.info(t['error_liboqs_help'])
    st.stop()

# Header with system info and language selector
col_header1, col_header2, col_header3 = st.columns([3, 1, 1])
with col_header1:
    st.title(t['title'])
    st.caption(t['subtitle'])

with col_header2:
    try:
        sys_info = export_utils.get_system_info()
        st.metric(t['system'], sys_info.get('platform', 'Unknown'))
        st.caption(f"{sys_info.get('cpu_brand', 'Unknown CPU')[:30]}")
    except:
        pass

with col_header3:
    lang_options = {'English': 'en', 'Polski': 'pl'}
    selected_lang = st.selectbox(
        "Language / Język",
        options=list(lang_options.keys()),
        index=0 if st.session_state.language == 'en' else 1,
        key='lang_selector'
    )
    if lang_options[selected_lang] != st.session_state.language:
        st.session_state.language = lang_options[selected_lang]
        st.rerun()

st.divider()

# ========== SIDEBAR CONFIGURATION ==========
st.sidebar.header(t['configuration'])

# Mode Selection
mode_map = {
    t['mode_kem']: "KEM (Key Exchange Only)",
    t['mode_signatures']: "Digital Signatures",
    t['mode_hybrid']: "Hybrid Encryption (KEM+AES)",
    t['mode_scenarios']: "Real-World Scenarios"
}

mode_display = st.sidebar.radio(
    t['test_scenario'],
    list(mode_map.keys()),
    help=t['select_scenario']
)
mode = mode_map[mode_display]

st.sidebar.divider()

# Input configuration based on mode
payload_bytes = b""

if mode == "KEM (Key Exchange Only)":
    st.sidebar.info(t['mode_kem_desc'])
    payload_bytes = b"x" * 32  # Fixed size for KEM
    
elif mode == "Digital Signatures":
    st.sidebar.subheader(t['message_config'])
    data_source = st.sidebar.radio(t['message_source'], [t['random_generated'], t['upload_file']])
    
    if data_source == t['random_generated']:
        size_kb = st.sidebar.slider(t['message_size_kb'], 1, 1024, 10)
        payload_bytes = os.urandom(size_kb * 1024)
        st.sidebar.success(f"{t['generated']} {size_kb} KB")
    else:
        uploaded_file = st.sidebar.file_uploader(t['upload_file_sign'], type=None)
        if uploaded_file is not None:
            payload_bytes = uploaded_file.read()
            st.sidebar.success(f"{t['loaded']} {len(payload_bytes)/1024:.2f} KB")
        else:
            st.sidebar.warning(f"{t['no_file_uploaded']} 1KB")
            payload_bytes = os.urandom(1024)
            
elif mode == "Hybrid Encryption (KEM+AES)":
    st.sidebar.info(t['mode_hybrid_desc'])
    
    data_source = st.sidebar.radio(t['file_source'], [t['random_generated'], t['upload_file']])
    
    if data_source == t['random_generated']:
        size_options = [1, 10, 100, 500, 1024, 5120, 10240]
        size_kb = st.sidebar.select_slider(t['file_size_kb'], options=size_options, value=100)
        payload_bytes = os.urandom(size_kb * 1024)
        st.sidebar.success(f"{t['generated']} {size_kb} KB")
    else:
        uploaded_file = st.sidebar.file_uploader(t['upload_file_encrypt'], type=None)
        if uploaded_file is not None:
            payload_bytes = uploaded_file.read()
            st.sidebar.success(f"{t['loaded']} {len(payload_bytes)/1024:.2f} KB")
        else:
            st.sidebar.warning(f"{t['no_file_uploaded']} 100KB")
            payload_bytes = os.urandom(102400)
            
elif mode == "Real-World Scenarios":
    st.sidebar.info(t['mode_scenarios_desc'])
    
    scenario_map = {
        t['scenario_tls']: "TLS 1.3 Handshake",
        t['scenario_email']: "Secure Email (S/MIME)",
        t['scenario_vpn']: "VPN Session",
        t['scenario_code']: "Code Signing"
    }
    
    scenario_display = st.sidebar.selectbox(
        t['select_scenario'] + ":",
        list(scenario_map.keys())
    )
    scenario = scenario_map[scenario_display]
    
    if scenario == "Secure Email (S/MIME)":
        msg_size = st.sidebar.slider(t['email_size'], 1, 1024, 10)
        payload_bytes = os.urandom(msg_size * 1024)
    elif scenario == "Code Signing":
        file_size_mb = st.sidebar.slider(t['file_size_mb'], 1, 100, 1)
        payload_bytes = os.urandom(file_size_mb * 1024 * 1024)
    else:
        payload_bytes = os.urandom(1024)

st.sidebar.divider()

# Algorithm Selection
st.sidebar.subheader(t['algo_selection'])

iterations = st.sidebar.number_input(t['iterations'], 5, 500, 20, 
                                     help=t['iterations_help'])

selected_algos = []
selected_kem = []
selected_sig = []

if mode == "Real-World Scenarios":
    st.sidebar.markdown(f"**{t['classic_kem']}**")
    classic_kem = classic_algo.get_rsa_options()
    sel_classic_kem = st.sidebar.multiselect(t['classic_kem'], classic_kem, default=["RSA-2048"])
    
    pqc_kem = pqc_algo.get_available_kem()
    sel_pqc_kem = st.sidebar.multiselect(t['pqc_kem'], pqc_kem, default=pqc_kem[:2] if pqc_kem else [])
    
    selected_kem = sel_classic_kem + sel_pqc_kem
    
    st.sidebar.markdown(f"**{t['classic_sig']}**")
    classic_sig = classic_algo.get_ecc_options()
    sel_classic_sig = st.sidebar.multiselect(t['classic_sig'], classic_sig, default=["SECP256R1 (P-256)"])
    
    pqc_sig = pqc_algo.get_available_sig()
    sel_pqc_sig = st.sidebar.multiselect(t['pqc_sig'], pqc_sig, default=pqc_sig[:2] if pqc_sig else [])
    
    selected_sig = sel_classic_sig + sel_pqc_sig
    
elif mode.startswith("KEM") or mode.startswith("Hybrid"):
    st.sidebar.markdown(f"**{t['classic_kem']}**")
    classic_opts = classic_algo.get_rsa_options()
    sel_classic = st.sidebar.multiselect(t['rsa_sizes'], classic_opts, default=["RSA-2048"])
    
    st.sidebar.markdown(f"**{t['pqc_kem']}**")
    pqc_opts = pqc_algo.get_available_kem()
    default_pqc = pqc_opts[:3] if len(pqc_opts) >= 3 else pqc_opts
    sel_pqc = st.sidebar.multiselect(t['pqc_kems'], pqc_opts, default=default_pqc)
    
    selected_algos = sel_classic + sel_pqc
else:  # Digital Signatures
    st.sidebar.markdown(f"**{t['classic_sig']}**")
    classic_opts = classic_algo.get_ecc_options()
    sel_classic = st.sidebar.multiselect(t['ecc_curves'], classic_opts, default=["SECP256R1 (P-256)"])
    
    st.sidebar.markdown(f"**{t['pqc_sig']}**")
    pqc_opts = pqc_algo.get_available_sig()
    default_pqc = pqc_opts[:3] if len(pqc_opts) >= 3 else pqc_opts
    sel_pqc = st.sidebar.multiselect(t['pqc_signatures'], pqc_opts, default=default_pqc)
    
    selected_algos = sel_classic + sel_pqc

st.sidebar.divider()

# Run button
run_button = st.sidebar.button(t['run_benchmark'], type="primary", use_container_width=True)

# ========== MAIN CONTENT ==========

if run_button:
    # Validate selection
    if mode == "Real-World Scenarios":
        if not selected_kem or not selected_sig:
            st.error(t['error_select_kem_sig'])
            st.stop()
    else:
        if not selected_algos:
            st.error(t['error_select_algos'])
            st.stop()
    
    # Progress tracking
    st.header(t['running_benchmarks'])
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    raw_measurements = {}  # For statistical analysis
    
    # Run benchmarks based on mode
    if mode == "Real-World Scenarios":
        total_tests = len(selected_kem) * len(selected_sig)
        idx = 0
        
        for kem in selected_kem:
            for sig in selected_sig:
                idx += 1
                status_text.text(f"{t['testing']} {idx}/{total_tests}: {kem} + {sig}")
                
                try:
                    if scenario == "TLS 1.3 Handshake":
                        result = scenarios.benchmark_tls_handshake(kem, sig)
                    elif scenario == "Secure Email (S/MIME)":
                        result = scenarios.benchmark_secure_email(sig, kem, len(payload_bytes))
                    elif scenario == "VPN Session":
                        result = scenarios.benchmark_vpn_session(kem, sig, 100)
                    elif scenario == "Code Signing":
                        result = scenarios.benchmark_code_signing(sig, len(payload_bytes))
                    else:
                        result = scenarios.benchmark_tls_handshake(kem, sig)
                    
                    # Add combined Algorithm column for visualization
                    if "KEM Algorithm" in result and "Signature Algorithm" in result:
                        result["Algorithm"] = f"{result['KEM Algorithm']} + {result['Signature Algorithm']}"
                    elif "Signature Algorithm" in result:
                        result["Algorithm"] = result["Signature Algorithm"]
                    else:
                        result["Algorithm"] = kem if kem else sig
                    
                    # Add Family for color coding
                    is_pqc = any(pqc in kem for pqc in ["Kyber", "ML-KEM", "Dilithium", "ML-DSA", "Falcon", "SPHINCS"]) if kem else False
                    is_pqc = is_pqc or (any(pqc in sig for pqc in ["Dilithium", "ML-DSA", "Falcon", "SPHINCS"]) if sig else False)
                    result["Family"] = "Post-Quantum" if is_pqc else "Classic"
                    
                    results.append(result)
                except Exception as e:
                    st.warning(f"{t['failed_to_test']} {kem} + {sig}: {e}")
                
                progress_bar.progress(idx / total_tests)
    
    else:
        # Regular benchmarks with multiple iterations
        op_labels = ["Encaps", "Decaps"] if mode.startswith("KEM") or mode.startswith("Hybrid") else ["Sign", "Verify"]
        
        for idx, algo in enumerate(selected_algos):
            status_text.text(f"{t['testing']} {idx+1}/{len(selected_algos)}: {algo} ({iterations} {t['iterations'].lower()})")
            
            is_rsa = "RSA" in algo
            is_ecc = "SECP" in algo
            
            acc = {"KG": [], "OP1": [], "OP2": []}
            if mode.startswith("Hybrid"):
                acc["AES_ENC"] = []
                acc["AES_DEC"] = []
            
            meta = {}
            
            try:
                for iter_num in range(iterations):
                    if mode == "Hybrid Encryption (KEM+AES)":
                        res = hybrid_encryption.benchmark_hybrid_encryption(algo, payload_bytes)
                        acc["KG"].append(res["KeyGen (ms)"])
                        acc["OP1"].append(res["KEM Encaps (ms)"])
                        acc["OP2"].append(res["KEM Decaps (ms)"])
                        acc["AES_ENC"].append(res["AES Encrypt (ms)"])
                        acc["AES_DEC"].append(res["AES Decrypt (ms)"])
                        
                        meta = {
                            "PK Size": res["PK Size (B)"],
                            "SK Size": res["SK Size (B)"],
                            "KEM CT Size": res["KEM CT Size (B)"],
                            "File Size": res["File Size (B)"],
                            "Ciphertext Size": res["Ciphertext Size (B)"],
                            "Total Overhead": res["Total Overhead (B)"],
                            "Overhead %": res["Overhead (%)"]
                        }
                    elif is_rsa:
                        res = classic_algo.benchmark_rsa_kem(algo, payload_bytes)
                        acc["KG"].append(res["KeyGen (ms)"])
                        acc["OP1"].append(res[f"{op_labels[0]} (ms)"])
                        acc["OP2"].append(res[f"{op_labels[1]} (ms)"])
                        meta = {
                            "PK Size": res["PK Size (B)"],
                            "SK Size": res["SK Size (B)"],
                            "Output Size": res["CT/Sig Size (B)"]
                        }
                    elif is_ecc:
                        res = classic_algo.benchmark_ecdsa_sign(algo, payload_bytes)
                        acc["KG"].append(res["KeyGen (ms)"])
                        acc["OP1"].append(res[f"{op_labels[0]} (ms)"])
                        acc["OP2"].append(res[f"{op_labels[1]} (ms)"])
                        meta = {
                            "PK Size": res["PK Size (B)"],
                            "SK Size": res["SK Size (B)"],
                            "Output Size": res["CT/Sig Size (B)"]
                        }
                    elif mode.startswith("KEM") or mode.startswith("Hybrid"):
                        res = pqc_algo.benchmark_pqc_kem(algo, payload_bytes)
                        acc["KG"].append(res["KeyGen (ms)"])
                        acc["OP1"].append(res[f"{op_labels[0]} (ms)"])
                        acc["OP2"].append(res[f"{op_labels[1]} (ms)"])
                        meta = {
                            "PK Size": res["PK Size (B)"],
                            "SK Size": res["SK Size (B)"],
                            "Output Size": res["CT/Sig Size (B)"]
                        }
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
                
                # Calculate statistics
                kg_stats = statistics_utils.compute_statistics(acc["KG"])
                op1_stats = statistics_utils.compute_statistics(acc["OP1"])
                op2_stats = statistics_utils.compute_statistics(acc["OP2"])
                
                avg_res = {
                    "Algorithm": algo,
                    "Family": "Classic" if (is_rsa or is_ecc) else "Post-Quantum",
                    "KeyGen (ms)": kg_stats["mean"],
                    f"{op_labels[0]} (ms)": op1_stats["mean"],
                    f"{op_labels[1]} (ms)": op2_stats["mean"],
                    "Total Time (ms)": kg_stats["mean"] + op1_stats["mean"] + op2_stats["mean"],
                }
                
                if mode.startswith("Hybrid"):
                    aes_enc_stats = statistics_utils.compute_statistics(acc["AES_ENC"])
                    aes_dec_stats = statistics_utils.compute_statistics(acc["AES_DEC"])
                    avg_res["AES Encrypt (ms)"] = aes_enc_stats["mean"]
                    avg_res["AES Decrypt (ms)"] = aes_dec_stats["mean"]
                    avg_res["Total Encrypt (ms)"] = op1_stats["mean"] + aes_enc_stats["mean"]
                    avg_res["Total Decrypt (ms)"] = op2_stats["mean"] + aes_dec_stats["mean"]
                    avg_res["Total Time (ms)"] = (kg_stats["mean"] + op1_stats["mean"] + 
                                                  op2_stats["mean"] + aes_enc_stats["mean"] + 
                                                  aes_dec_stats["mean"])
                
                # Add statistical metrics
                avg_res["KeyGen StdDev"] = kg_stats["std"]
                avg_res["KeyGen P95"] = kg_stats["p95"]
                avg_res["Consistency Score"] = statistics_utils.calculate_consistency_score(acc["KG"])
                
                # Add metadata
                avg_res.update(meta)
                
                # Calculate bandwidth
                if mode.startswith("Hybrid"):
                    # For hybrid, Total Overhead (B) is already in meta from benchmark_hybrid_encryption
                    # Use it if available, otherwise calculate from components
                    if "Total Overhead (B)" in meta:
                        avg_res["Total Bandwidth (B)"] = meta["Total Overhead (B)"]
                    else:
                        # Fallback: PK Size + KEM CT Size
                        avg_res["Total Bandwidth (B)"] = meta.get("PK Size", 0) + meta.get("KEM CT Size", 0)
                else:
                    avg_res["Total Bandwidth (B)"] = meta.get("PK Size", 0) + meta.get("Output Size", 0)
                
                results.append(avg_res)
                raw_measurements[algo] = acc
                
            except Exception as e:
                st.warning(f"{t['failed_to_benchmark']} {algo}: {e}")
            
            progress_bar.progress((idx + 1) / len(selected_algos))
    
    status_text.text(t['benchmark_complete'])
    progress_bar.empty()
    status_text.empty()
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    if len(df) == 0:
        st.error(t['error_no_results'])
        st.stop()
    
    # Store results in session state for export
    st.session_state['benchmark_results'] = df
    st.session_state['raw_measurements'] = raw_measurements
    st.session_state['config'] = {
        'mode': mode,
        'iterations': iterations,
        'payload_size': len(payload_bytes)
    }
    
    st.success(f"{t['benchmark_success']} {len(df)} {t['algo_configs']}")
    
    # ========== RESULTS VISUALIZATION ==========
    
    st.header(t['tab_results'].replace("Table", ""))
    
    # Create tabs based on mode
    if mode == "Real-World Scenarios":
        tab_names = [t['tab_results'], t['tab_perf_analysis'], t['tab_export']]
    else:
        tab_names = [t['tab_performance'], t['tab_size'], t['tab_tradeoff'], t['tab_statistics'], 
                     t['tab_analysis'], t['tab_recommendations'], t['tab_export']]
    
    tabs = st.tabs(tab_names)
    
    # Tab 0: Performance / Results Table
    with tabs[0]:
        if mode == "Real-World Scenarios":
            st.subheader(f"{scenario} {t['tab_results']}")
            st.dataframe(df.style.format(precision=3), use_container_width=True)
        else:
            st.subheader(t['performance_metrics'])
            st.caption(t['perf_caption'])
            st.info(t['metrics_performance_desc'])
            
            # Performance bar chart
            perf_cols = [c for c in df.columns if 'ms)' in c and 'StdDev' not in c and 'P95' not in c]
            if len(perf_cols) > 0:
                df_long = df.melt(id_vars=["Algorithm", "Family"], 
                                  value_vars=perf_cols,
                                  var_name="Operation", value_name="Time (ms)")
                
                fig_time = px.bar(df_long, x="Algorithm", y="Time (ms)", color="Operation",
                                 title=t.get('exec_time_breakdown', 'Execution Time Breakdown'),
                                 height=500, barmode='group')
                fig_time.update_xaxes(tickangle=45)
                st.plotly_chart(fig_time, use_container_width=True)
            else:
                st.warning(t.get('no_perf_data', 'No performance data available for visualization'))
            
            # Summary table
            st.subheader(t['summary_table'])
            st.info(t['metrics_summary_table_desc'])
            # Show all time columns, not just total
            time_cols = [c for c in df.columns if 'ms)' in c and 'StdDev' not in c and 'P95' not in c]
            display_cols = ["Algorithm", "Family"] + time_cols
            if "Total Bandwidth (B)" in df.columns:
                display_cols.append("Total Bandwidth (B)")
            if "Consistency Score" in df.columns:
                display_cols.append("Consistency Score")
            st.dataframe(df[display_cols].style.format(precision=2).background_gradient(
                subset=[c for c in time_cols if c in df.columns], cmap="RdYlGn_r"), use_container_width=True)
    
    # Tab 1: Performance Analysis for Real-World Scenarios
    if mode == "Real-World Scenarios" and len(tabs) > 1:
        with tabs[1]:
            st.subheader(t['tab_perf_analysis'])
            st.info(t['metrics_scenarios_desc'])
            
            if len(df) > 0:
                # Performance comparison chart - use Total Time (ms) which should always exist
                if 'Total Time (ms)' in df.columns or 'Total Session Setup (ms)' in df.columns:
                    time_col = 'Total Time (ms)' if 'Total Time (ms)' in df.columns else 'Total Session Setup (ms)'
                    
                    fig_scenario = px.bar(df, x='Algorithm', 
                                         y=time_col,
                                         color='Family',
                                         title=f"{scenario} - {t['performance_metrics']}",
                                         height=500)
                    fig_scenario.update_xaxes(tickangle=45)
                    fig_scenario.update_yaxes(title="Time (ms)")
                    st.plotly_chart(fig_scenario, use_container_width=True)
                    
                    # Detailed metrics table
                    st.subheader(t['summary_table'])
                    st.dataframe(df.style.format(precision=3), use_container_width=True)
                else:
                    st.warning(t.get('no_perf_data', 'No performance data available'))
            else:
                st.warning(t.get('no_perf_data', 'No performance data available'))
    
    # Tab 1: Size Analysis (for non-scenario modes)
    if mode != "Real-World Scenarios" and len(tabs) > 1:
        with tabs[1]:
            st.subheader(t['crypto_sizes'])
            st.caption(t['sizes_caption'])
            st.info(t['metrics_size_desc'])
            
            # Check for size columns with actual data
            size_cols = []
            for col in ["PK Size", "SK Size", "Output Size"]:
                if col in df.columns:
                    size_cols.append(col)
            
            if len(size_cols) > 0:
                df_size = df.melt(id_vars=["Algorithm", "Family"],
                                  value_vars=size_cols,
                                  var_name=t['artifact'], value_name=t['size_bytes'])
                
                fig_size = px.bar(df_size, x="Algorithm", y=t['size_bytes'], color=t['artifact'],
                                 barmode="group", log_y=True,
                                 title=t['key_output_sizes'],
                                 height=500)
                fig_size.update_xaxes(tickangle=45)
                st.plotly_chart(fig_size, use_container_width=True)
                
                # Size comparison table
                st.subheader(t['size_comparison'])
                if "Family" in df.columns:
                    size_summary = df.groupby("Family")[size_cols].mean().round(0).astype(int)
                    st.dataframe(size_summary, use_container_width=True)
            else:
                st.warning(t['no_size_data'])
    
    # Tab 2: Trade-off Analysis
    if mode != "Real-World Scenarios" and len(tabs) > 2:
        with tabs[2]:
            st.subheader(t['tradeoff_title'])
            st.caption(t['tradeoff_caption'])
            st.info(t['metrics_tradeoff_desc'])
            
            if "Total Bandwidth (B)" in df.columns and "Total Time (ms)" in df.columns:
                # Use text instead of hover for better visibility
                fig_scatter = px.scatter(
                    df,
                    x="Total Bandwidth (B)",
                    y="Total Time (ms)",
                    color="Family",
                    symbol="Family",
                    text="Algorithm",
                    title=t['efficiency_frontier'],
                    height=600
                )
                
                # Better text positioning
                fig_scatter.update_traces(textposition='top center', textfont_size=9)
                
                # Fixed axis ranges for better readability - use linear scale instead of log for better control
                # Determine reasonable ranges based on data
                min_bw = df["Total Bandwidth (B)"].min()
                max_bw = df["Total Bandwidth (B)"].max()
                min_time = df["Total Time (ms)"].min()
                max_time = df["Total Time (ms)"].max()
                
                # Add 20% padding
                bw_padding = (max_bw - min_bw) * 0.2
                time_padding = (max_time - min_time) * 0.2
                
                fig_scatter.update_xaxes(
                    range=[max(0, min_bw - bw_padding), max_bw + bw_padding],
                    title="Total Bandwidth (Bytes)"
                )
                fig_scatter.update_yaxes(
                    range=[max(0, min_time - time_padding), max_time + time_padding],
                    title="Total Time (ms)"
                )
                
                # Add quadrant lines
                median_bw = df["Total Bandwidth (B)"].median()
                median_time = df["Total Time (ms)"].median()
                
                fig_scatter.add_hline(y=median_time, line_dash="dash", line_color="gray", opacity=0.5,
                                     annotation_text=t['median_time'], annotation_position="right")
                fig_scatter.add_vline(x=median_bw, line_dash="dash", line_color="gray", opacity=0.5,
                                     annotation_text=t['median_size'], annotation_position="top")
                
                st.plotly_chart(fig_scatter, use_container_width=True)
                
                # Calculate efficiency scores
                df_with_score = statistics_utils.calculate_efficiency_score(
                    df, "Total Time (ms)", "Total Bandwidth (B)"
                )
                
                st.subheader(t['efficiency_rankings'])
                st.caption(t['efficiency_caption'])
                top_efficient = df_with_score.nsmallest(10, "Efficiency Score")[
                    ["Algorithm", "Family", "Total Time (ms)", "Total Bandwidth (B)", "Efficiency Score"]
                ]
                st.dataframe(top_efficient.style.format(precision=2).background_gradient(
                    subset=["Efficiency Score"], cmap="RdYlGn_r"), use_container_width=True)
    
    # Tab 3: Statistics
    if mode != "Real-World Scenarios" and len(tabs) > 3:
        with tabs[3]:
            st.subheader(t['detailed_stats'])
            st.info(t['metrics_stats_desc'])
            
            # Consistency analysis
            st.markdown(f"### {t['consistency_scores_title']}")
            st.caption(t['consistency_caption'])
            
            if "Consistency Score" in df.columns:
                fig_consistency = px.bar(df, x="Algorithm", y="Consistency Score",
                                        color="Family", title=t['algo_consistency_title'],
                                        height=400)
                fig_consistency.add_hline(y=80, line_dash="dash", line_color="orange",
                                         annotation_text=t['acceptable_threshold'])
                fig_consistency.update_xaxes(tickangle=45)
                st.plotly_chart(fig_consistency, use_container_width=True)
            else:
                st.warning(t['no_perf_data'])
            
            # Statistical summary
            st.markdown(f"### {t['statistical_summary']}")
            stats_cols = [c for c in df.columns if any(x in c for x in ["mean", "StdDev", "P95", "Consistency"])]
            if len(stats_cols) > 0:
                st.dataframe(df[["Algorithm", "Family"] + stats_cols].style.format(precision=3),
                           use_container_width=True)
            
            # Outlier detection
            if raw_measurements:
                st.markdown(f"### {t['outlier_analysis']}")
                outlier_data = []
                for algo, measurements in raw_measurements.items():
                    for metric, values in measurements.items():
                        outliers = statistics_utils.detect_outliers(values)
                        if outliers['count'] > 0:
                            outlier_data.append({
                                t['algorithm']: algo,
                                t['metric']: metric,
                                t['outliers']: outliers['count'],
                                t['percentage']: f"{outliers['percentage']:.1f}%"
                            })
                
                if outlier_data:
                    st.dataframe(pd.DataFrame(outlier_data), use_container_width=True)
                else:
                    st.success(t['no_outliers'])
    
    # Tab 4: Analysis
    if mode != "Real-World Scenarios" and len(tabs) > 4:
        with tabs[4]:
            st.subheader(t['comparative_analysis'])
            
            # Analyze classical algorithms
            classic_analysis = analysis_utils.analyze_classic_algorithms(df)
            if "error" not in classic_analysis:
                st.markdown(f"### {t['classic_algos']}")
                col1, col2, col3 = st.columns(3)
                
                if "performance" in classic_analysis:
                    with col1:
                        st.metric(t['fastest_classic'],
                                classic_analysis["performance"]["fastest"]["algorithm"],
                                f"{classic_analysis['performance']['fastest']['time_ms']:.2f} ms")
                    with col2:
                        st.metric(t['average_time'],
                                f"{classic_analysis['performance']['average_time_ms']:.2f} ms")
                
                if "bandwidth" in classic_analysis:
                    with col3:
                        st.metric(t['smallest_classic'],
                                classic_analysis["bandwidth"]["smallest"]["algorithm"],
                                f"{classic_analysis['bandwidth']['smallest']['bytes']:,} B")
                
                # Insights
                if "insights" in classic_analysis:
                    for insight in classic_analysis["insights"]:
                        with st.expander(f"{insight['category']} {t['analysis']}"):
                            st.write(f"**{t['observation']}:** {insight['observation']}")
                            st.info(f"**{t['recommendation']}:** {insight['recommendation']}")
            
            st.divider()
            
            # Analyze PQC algorithms
            pqc_analysis = analysis_utils.analyze_pqc_algorithms(df)
            if "error" not in pqc_analysis:
                st.markdown(f"### {t['pqc_algos']}")
                col1, col2, col3 = st.columns(3)
                
                if "performance" in pqc_analysis:
                    with col1:
                        st.metric(t['fastest_pqc'],
                                pqc_analysis["performance"]["fastest"]["algorithm"],
                                f"{pqc_analysis['performance']['fastest']['time_ms']:.2f} ms")
                    with col2:
                        st.metric(t['average_time'],
                                f"{pqc_analysis['performance']['average_time_ms']:.2f} ms")
                
                if "bandwidth" in pqc_analysis:
                    with col3:
                        st.metric(t['smallest_pqc'],
                                pqc_analysis["bandwidth"]["smallest"]["algorithm"],
                                f"{pqc_analysis['bandwidth']['smallest']['bytes']:,} B")
                
                # NIST Status
                if "nist_status" in pqc_analysis:
                    st.success(f"{t['nist_standardized']} {', '.join(pqc_analysis['nist_status']['standardized'])}")
                    st.caption(pqc_analysis['nist_status']['note'])
            
            st.divider()
            
            # Comparison
            comparison = analysis_utils.compare_classic_vs_pqc(df)
            if "error" not in comparison:
                st.markdown(f"### {t['classic_vs_pqc']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"#### {t['performance']}")
                    if "performance" in comparison:
                        perf = comparison["performance"]
                        st.metric(t['classic_average'], f"{perf['classic_avg_ms']:.2f} ms")
                        st.metric(t['pqc_average'], f"{perf['pqc_avg_ms']:.2f} ms",
                                delta=f"{((perf['pqc_avg_ms'] - perf['classic_avg_ms']) / perf['classic_avg_ms'] * 100):.1f}%",
                                delta_color="inverse")
                        st.caption(perf['verdict'])
                
                with col2:
                    st.markdown(f"#### {t['bandwidth']}")
                    if "bandwidth" in comparison:
                        bw = comparison["bandwidth"]
                        st.metric(t['classic_average'], f"{bw['classic_avg_bytes']:,} B")
                        st.metric(t['pqc_average'], f"{bw['pqc_avg_bytes']:,} B",
                                delta=f"{((bw['pqc_avg_bytes'] - bw['classic_avg_bytes']) / bw['classic_avg_bytes'] * 100):.1f}%",
                                delta_color="inverse")
                        st.caption(bw['verdict'])
    
    # Tab 5: Recommendations
    if mode != "Real-World Scenarios" and len(tabs) > 5:
        with tabs[5]:
            st.subheader(t['recommendations_title'])
            
            use_case_options = [
                t['usecase_general'],
                t['usecase_iot'],
                t['usecase_server'],
                t['usecase_mobile'],
                t['usecase_security']
            ]
            
            use_case = st.selectbox(t['select_use_case'], use_case_options)
            
            use_case_map = {
                t['usecase_general']: "general",
                t['usecase_iot']: "iot",
                t['usecase_server']: "server",
                t['usecase_mobile']: "mobile",
                t['usecase_security']: "high_security"
            }
            
            recommendations = analysis_utils.generate_recommendations(df, use_case_map[use_case])
            
            st.markdown(f"### {t['recommended_algos']}")
            for rec in recommendations.get("recommendations", []):
                with st.expander(f"{rec['category']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**{t['classical']}**")
                        st.code(rec.get('classic', 'N/A'))
                    with col2:
                        st.markdown(f"**{t['post_quantum']}**")
                        st.code(rec.get('pqc', 'N/A'))
                    with col3:
                        st.markdown(f"**{t['hybrid']}**")
                        st.info(rec.get('hybrid', rec.get('note', t['recommended'])))
            
            # Best performers from data
            if "data_driven" in recommendations:
                st.markdown(f"### {t['best_performers']}")
                dd = recommendations["data_driven"]
                
                col1, col2 = st.columns(2)
                if "fastest_overall" in dd:
                    with col1:
                        st.success(f"**{t['fastest']}** {dd['fastest_overall']['algorithm']}")
                        st.metric(t['time'], f"{dd['fastest_overall']['time_ms']:.2f} ms")
                
                if "smallest_overhead" in dd:
                    with col2:
                        st.success(f"**{t['smallest']}** {dd['smallest_overhead']['algorithm']}")
                        st.metric(t['bandwidth'], f"{dd['smallest_overhead']['bytes']:,} B")
            
            # Migration strategy
            st.markdown(f"### {t['migration_strategy']}")
            if "migration_strategy" in recommendations:
                strategy = recommendations["migration_strategy"]
                for i, (phase, description) in enumerate(strategy.items()):
                    if phase != "timeline":
                        st.markdown(f"**{phase.replace('_', ' ').title()}:** {description}")
                st.info(f"**{t['recommended_timeline']}** {strategy.get('timeline', '2024-2030')}")
    
    # Last Tab: Export
    export_tab_idx = len(tabs) - 1
    with tabs[export_tab_idx]:
        st.subheader(t['export_results'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=t['export_csv'],
                    data=csv_data,
                    file_name="benchmark_results.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key='download_csv'
                )
            except Exception as e:
                st.error(f"{t['export_failed']} {e}")
        
        with col2:
            try:
                metadata = export_utils.create_metadata(
                    st.session_state.get('config', {}),
                    export_utils.get_system_info()
                )
                export_data = {
                    "timestamp": pd.Timestamp.now().isoformat(),
                    "metadata": metadata,
                    "results": df.to_dict('records')
                }
                json_data = json.dumps(export_data, indent=2).encode('utf-8')
                st.download_button(
                    label=t['export_json'],
                    data=json_data,
                    file_name="benchmark_results.json",
                    mime="application/json",
                    use_container_width=True,
                    key='download_json'
                )
            except Exception as e:
                st.error(f"{t['export_failed']} {e}")

else:
    # Initial welcome screen
    st.header(t['welcome'])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {t['what_does']}")
        st.markdown(t['what_desc'])
        
        st.markdown(f"### {t['quick_start']}")
        st.markdown(t['quick_start_steps'])
        
        st.markdown(f"### {t['test_scenarios']}")
        st.markdown(t['test_scenarios_desc'])
    
    with col2:
        st.info(f"**{t['why_pqc']}**\n\n{t['why_pqc_desc']}")
        
        st.success(f"**{t['available_algos']}**\n\n{t['available_algos_desc']}")
    
    st.divider()
    
    # Example results
    st.subheader(t['example_title'])
    
    example_data = {
        'Algorithm': ['RSA-2048', 'ECDSA P-256', 'Kyber768', 'Dilithium3'],
        'Family': ['Classic', 'Classic', 'Post-Quantum', 'Post-Quantum'],
        'Total Time (ms)': [45.2, 2.1, 0.8, 3.5],
        'Total Bandwidth (B)': [512, 128, 2400, 4800]
    }
    example_df = pd.DataFrame(example_data)
    
    fig_example = px.scatter(example_df, x='Total Bandwidth (B)', y='Total Time (ms)',
                            color='Family', text='Algorithm',
                            title=t['example_tradeoff'],
                            log_x=True, log_y=True)
    fig_example.update_traces(textposition='top center')
    st.plotly_chart(fig_example, use_container_width=True)
    
    st.caption(t['example_caption'])

# Footer
st.divider()
st.caption(f"{t['footer']} | [{t['documentation']}](https://github.com/open-quantum-safe/liboqs) | {t['version']} | © 2026")
