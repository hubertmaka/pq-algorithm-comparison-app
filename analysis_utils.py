"""
Analysis utilities for cryptographic benchmark results.
Generates insights, comparisons, and recommendations.
"""

import pandas as pd
import numpy as np


def analyze_classic_algorithms(df):
    """
    Analyze classical cryptographic algorithms (RSA, ECC).
    
    Args:
        df: DataFrame with benchmark results
        
    Returns:
        Dictionary with analysis results and insights
    """
    classic_df = df[df['Family'] == 'Classic'].copy() if 'Family' in df.columns else df.copy()
    
    if len(classic_df) == 0:
        return {"error": "No classic algorithms found in dataset"}
    
    analysis = {
        "title": "Classical Algorithms Analysis",
        "algorithms_tested": classic_df['Algorithm'].tolist(),
        "count": len(classic_df),
    }
    
    # Performance analysis
    if 'Total Time (ms)' in classic_df.columns:
        analysis["performance"] = {
            "fastest": {
                "algorithm": classic_df.loc[classic_df['Total Time (ms)'].idxmin(), 'Algorithm'],
                "time_ms": float(classic_df['Total Time (ms)'].min())
            },
            "slowest": {
                "algorithm": classic_df.loc[classic_df['Total Time (ms)'].idxmax(), 'Algorithm'],
                "time_ms": float(classic_df['Total Time (ms)'].max())
            },
            "average_time_ms": float(classic_df['Total Time (ms)'].mean())
        }
    
    # Size analysis
    if 'Total Bandwidth (B)' in classic_df.columns:
        analysis["bandwidth"] = {
            "smallest": {
                "algorithm": classic_df.loc[classic_df['Total Bandwidth (B)'].idxmin(), 'Algorithm'],
                "bytes": int(classic_df['Total Bandwidth (B)'].min())
            },
            "largest": {
                "algorithm": classic_df.loc[classic_df['Total Bandwidth (B)'].idxmax(), 'Algorithm'],
                "bytes": int(classic_df['Total Bandwidth (B)'].max())
            },
            "average_bytes": int(classic_df['Total Bandwidth (B)'].mean())
        }
    
    # Insights
    insights = []
    
    # RSA analysis
    rsa_algos = classic_df[classic_df['Algorithm'].str.contains('RSA', na=False)]
    if len(rsa_algos) > 0:
        insights.append({
            "category": "RSA",
            "observation": f"Tested {len(rsa_algos)} RSA variants. "
                          f"Larger key sizes provide higher security but increase computation time significantly.",
            "recommendation": "RSA-2048 offers good balance for most applications. "
                            "RSA-3072+ recommended for long-term security (beyond 2030)."
        })
    
    # ECC analysis
    ecc_algos = classic_df[classic_df['Algorithm'].str.contains('SECP|ECC', na=False)]
    if len(ecc_algos) > 0:
        insights.append({
            "category": "ECC/ECDSA",
            "observation": f"Tested {len(ecc_algos)} elliptic curve variants. "
                          f"ECC provides equivalent security to RSA with much smaller keys.",
            "recommendation": "P-256 (SECP256R1) is widely supported and efficient. "
                            "P-384 recommended for high-security applications."
        })
    
    analysis["insights"] = insights
    
    return analysis


def analyze_pqc_algorithms(df):
    """
    Analyze post-quantum cryptographic algorithms.
    
    Args:
        df: DataFrame with benchmark results
        
    Returns:
        Dictionary with analysis results and insights
    """
    pqc_df = df[df['Family'] == 'Post-Quantum'].copy() if 'Family' in df.columns else df.copy()
    
    if len(pqc_df) == 0:
        return {"error": "No PQC algorithms found in dataset"}
    
    analysis = {
        "title": "Post-Quantum Algorithms Analysis",
        "algorithms_tested": pqc_df['Algorithm'].tolist(),
        "count": len(pqc_df),
    }
    
    # Performance analysis
    if 'Total Time (ms)' in pqc_df.columns:
        analysis["performance"] = {
            "fastest": {
                "algorithm": pqc_df.loc[pqc_df['Total Time (ms)'].idxmin(), 'Algorithm'],
                "time_ms": float(pqc_df['Total Time (ms)'].min())
            },
            "slowest": {
                "algorithm": pqc_df.loc[pqc_df['Total Time (ms)'].idxmax(), 'Algorithm'],
                "time_ms": float(pqc_df['Total Time (ms)'].max())
            },
            "average_time_ms": float(pqc_df['Total Time (ms)'].mean())
        }
    
    # Size analysis
    if 'Total Bandwidth (B)' in pqc_df.columns:
        analysis["bandwidth"] = {
            "smallest": {
                "algorithm": pqc_df.loc[pqc_df['Total Bandwidth (B)'].idxmin(), 'Algorithm'],
                "bytes": int(pqc_df['Total Bandwidth (B)'].min())
            },
            "largest": {
                "algorithm": pqc_df.loc[pqc_df['Total Bandwidth (B)'].idxmax(), 'Algorithm'],
                "bytes": int(pqc_df['Total Bandwidth (B)'].max())
            },
            "average_bytes": int(pqc_df['Total Bandwidth (B)'].mean())
        }
    
    # Category analysis
    insights = []
    
    # KEM analysis (Kyber, BIKE, etc.)
    kem_categories = ['Kyber', 'ML-KEM', 'BIKE', 'HQC', 'Frodo']
    for category in kem_categories:
        cat_algos = pqc_df[pqc_df['Algorithm'].str.contains(category, na=False)]
        if len(cat_algos) > 0:
            insights.append({
                "category": f"{category} (KEM)",
                "count": len(cat_algos),
                "observation": f"Found {len(cat_algos)} {category} variant(s). "
                              f"Average time: {cat_algos['Total Time (ms)'].mean():.2f}ms" 
                              if 'Total Time (ms)' in cat_algos.columns else ""
            })
    
    # Signature analysis (Dilithium, Falcon, SPHINCS+)
    sig_categories = ['Dilithium', 'ML-DSA', 'Falcon', 'SPHINCS', 'SLH-DSA']
    for category in sig_categories:
        cat_algos = pqc_df[pqc_df['Algorithm'].str.contains(category, na=False)]
        if len(cat_algos) > 0:
            insights.append({
                "category": f"{category} (Signature)",
                "count": len(cat_algos),
                "observation": f"Found {len(cat_algos)} {category} variant(s). "
                              f"Average time: {cat_algos['Total Time (ms)'].mean():.2f}ms"
                              if 'Total Time (ms)' in cat_algos.columns else ""
            })
    
    analysis["insights"] = insights
    
    # NIST recommendations
    analysis["nist_status"] = {
        "standardized": ["ML-KEM (Kyber)", "ML-DSA (Dilithium)", "SLH-DSA (SPHINCS+)"],
        "note": "NIST has standardized ML-KEM and ML-DSA for general use. "
                "Falcon may be standardized for specific use cases."
    }
    
    return analysis


def compare_classic_vs_pqc(df):
    """
    Compare classical vs post-quantum algorithms.
    
    Args:
        df: DataFrame with benchmark results
        
    Returns:
        Dictionary with comparison results
    """
    if 'Family' not in df.columns:
        return {"error": "Family column not found"}
    
    classic_df = df[df['Family'] == 'Classic']
    pqc_df = df[df['Family'] == 'Post-Quantum']
    
    if len(classic_df) == 0 or len(pqc_df) == 0:
        return {"error": "Need both Classic and PQC algorithms for comparison"}
    
    comparison = {
        "title": "Classic vs Post-Quantum Comparison",
        "summary": {
            "classic_count": len(classic_df),
            "pqc_count": len(pqc_df)
        }
    }
    
    # Performance comparison
    if 'Total Time (ms)' in df.columns:
        classic_avg_time = classic_df['Total Time (ms)'].mean()
        pqc_avg_time = pqc_df['Total Time (ms)'].mean()
        
        comparison["performance"] = {
            "classic_avg_ms": float(classic_avg_time),
            "pqc_avg_ms": float(pqc_avg_time),
            "speedup_factor": float(classic_avg_time / pqc_avg_time) if pqc_avg_time > 0 else 0,
            "verdict": "Classic algorithms are faster on average" if classic_avg_time < pqc_avg_time 
                      else "PQC algorithms are competitive in performance"
        }
    
    # Bandwidth comparison
    if 'Total Bandwidth (B)' in df.columns:
        classic_avg_bw = classic_df['Total Bandwidth (B)'].mean()
        pqc_avg_bw = pqc_df['Total Bandwidth (B)'].mean()
        
        comparison["bandwidth"] = {
            "classic_avg_bytes": int(classic_avg_bw),
            "pqc_avg_bytes": int(pqc_avg_bw),
            "size_ratio": float(pqc_avg_bw / classic_avg_bw) if classic_avg_bw > 0 else 0,
            "verdict": "Classic algorithms have smaller key/signature sizes on average"
                      if classic_avg_bw < pqc_avg_bw else "PQC has comparable size overhead"
        }
    
    # Trade-off analysis
    comparison["trade_offs"] = {
        "classic_advantages": [
            "Mature and well-tested",
            "Smaller key and signature sizes (typically)",
            "Hardware acceleration widely available",
            "Better understood security proofs"
        ],
        "classic_disadvantages": [
            "Vulnerable to quantum computers (Shor's algorithm)",
            "RSA becoming impractical for high security levels",
            "No future-proof quantum resistance"
        ],
        "pqc_advantages": [
            "Quantum-resistant security",
            "Future-proof for post-quantum era",
            "Some algorithms (Kyber, Dilithium) are very efficient",
            "NIST standardization complete"
        ],
        "pqc_disadvantages": [
            "Generally larger public keys and ciphertexts",
            "Less mature implementations",
            "Limited hardware acceleration currently",
            "Some algorithms (SPHINCS+) have performance trade-offs"
        ]
    }
    
    return comparison


def generate_recommendations(df, use_case="general"):
    """
    Generate algorithm recommendations based on benchmark results and use case.
    
    Args:
        df: DataFrame with benchmark results
        use_case: 'general', 'iot', 'server', 'mobile', 'high_security'
        
    Returns:
        Dictionary with recommendations
    """
    recommendations = {
        "use_case": use_case,
        "timestamp": pd.Timestamp.now().isoformat(),
        "recommendations": []
    }
    
    if use_case == "general":
        recommendations["recommendations"].extend([
            {
                "category": "Key Exchange (KEM)",
                "classic": "RSA-2048 or ECDH P-256",
                "pqc": "ML-KEM-768 (Kyber768) - NIST standardized, good balance",
                "hybrid": "Recommended: Use both classic and PQC in hybrid mode for transition"
            },
            {
                "category": "Digital Signatures",
                "classic": "ECDSA P-256 or RSA-2048",
                "pqc": "ML-DSA-65 (Dilithium3) - NIST standardized",
                "hybrid": "Consider hybrid signatures for critical applications"
            }
        ])
    
    elif use_case == "iot":
        recommendations["recommendations"].extend([
            {
                "category": "Constrained Devices",
                "classic": "ECDSA P-256 (smallest keys)",
                "pqc": "Kyber512 or Dilithium2 (smallest PQC variants)",
                "note": "Consider hybrid with preference for classic when bandwidth is critical"
            }
        ])
    
    elif use_case == "server":
        recommendations["recommendations"].extend([
            {
                "category": "High-Throughput Server",
                "classic": "ECDSA P-256 with hardware acceleration",
                "pqc": "ML-KEM-1024 and ML-DSA-87 for maximum security",
                "note": "Servers can handle larger key sizes and benefit from future-proofing"
            }
        ])
    
    elif use_case == "mobile":
        recommendations["recommendations"].extend([
            {
                "category": "Mobile Applications",
                "classic": "ECDSA P-256",
                "pqc": "Kyber768 and Dilithium3 (balanced)",
                "note": "Balance between security and battery/bandwidth consumption"
            }
        ])
    
    elif use_case == "high_security":
        recommendations["recommendations"].extend([
            {
                "category": "High Security / Long-Term",
                "classic": "Not recommended (quantum vulnerability)",
                "pqc": "ML-KEM-1024 + ML-DSA-87 or SPHINCS+-256f",
                "note": "Use highest security PQC variants. Consider SPHINCS+ for stateless signatures."
            }
        ])
    
    # Best performers from actual data
    if len(df) > 0:
        if 'Total Time (ms)' in df.columns:
            fastest = df.loc[df['Total Time (ms)'].idxmin()]
            recommendations["data_driven"] = {
                "fastest_overall": {
                    "algorithm": fastest['Algorithm'],
                    "time_ms": float(fastest['Total Time (ms)']),
                    "family": fastest.get('Family', 'Unknown')
                }
            }
        
        if 'Total Bandwidth (B)' in df.columns:
            smallest = df.loc[df['Total Bandwidth (B)'].idxmin()]
            if "data_driven" not in recommendations:
                recommendations["data_driven"] = {}
            recommendations["data_driven"]["smallest_overhead"] = {
                "algorithm": smallest['Algorithm'],
                "bytes": int(smallest['Total Bandwidth (B)']),
                "family": smallest.get('Family', 'Unknown')
            }
    
    # Migration strategy
    recommendations["migration_strategy"] = {
        "phase_1": "Assess current crypto usage and quantum risk timeline",
        "phase_2": "Implement hybrid mode (Classic + PQC) for critical systems",
        "phase_3": "Gradually increase PQC usage as implementations mature",
        "phase_4": "Full PQC deployment for new systems, maintain hybrid for legacy",
        "timeline": "2024-2030 (NIST recommendation)"
    }
    
    return recommendations


def generate_executive_summary(df, classic_analysis, pqc_analysis, comparison):
    """
    Generate executive summary for benchmark report.
    
    Args:
        df: DataFrame with results
        classic_analysis: Classical algorithms analysis
        pqc_analysis: PQC algorithms analysis
        comparison: Comparison results
        
    Returns:
        Formatted executive summary text
    """
    summary = []
    
    summary.append("=" * 80)
    summary.append("EXECUTIVE SUMMARY: CRYPTOGRAPHIC ALGORITHM BENCHMARK")
    summary.append("=" * 80)
    summary.append("")
    
    summary.append(f"Total Algorithms Tested: {len(df)}")
    summary.append(f"- Classical: {classic_analysis.get('count', 0)}")
    summary.append(f"- Post-Quantum: {pqc_analysis.get('count', 0)}")
    summary.append("")
    
    summary.append("KEY FINDINGS:")
    summary.append("-" * 80)
    
    # Performance findings
    if 'performance' in comparison:
        perf = comparison['performance']
        summary.append(f"1. Performance: {perf.get('verdict', 'N/A')}")
        summary.append(f"   - Classic average: {perf.get('classic_avg_ms', 0):.2f} ms")
        summary.append(f"   - PQC average: {perf.get('pqc_avg_ms', 0):.2f} ms")
        summary.append("")
    
    # Bandwidth findings
    if 'bandwidth' in comparison:
        bw = comparison['bandwidth']
        summary.append(f"2. Bandwidth: {bw.get('verdict', 'N/A')}")
        summary.append(f"   - Classic average: {bw.get('classic_avg_bytes', 0):,} bytes")
        summary.append(f"   - PQC average: {bw.get('pqc_avg_bytes', 0):,} bytes")
        summary.append(f"   - PQC overhead: {((bw.get('size_ratio', 1) - 1) * 100):.1f}%")
        summary.append("")
    
    summary.append("3. Best Performers:")
    if 'performance' in classic_analysis:
        summary.append(f"   - Fastest Classic: {classic_analysis['performance']['fastest']['algorithm']} "
                      f"({classic_analysis['performance']['fastest']['time_ms']:.2f} ms)")
    if 'performance' in pqc_analysis:
        summary.append(f"   - Fastest PQC: {pqc_analysis['performance']['fastest']['algorithm']} "
                      f"({pqc_analysis['performance']['fastest']['time_ms']:.2f} ms)")
    summary.append("")
    
    summary.append("RECOMMENDATIONS:")
    summary.append("-" * 80)
    summary.append("• Short-term (2024-2025): Begin hybrid deployments (Classic + PQC)")
    summary.append("• Medium-term (2025-2027): Increase PQC adoption, especially for new systems")
    summary.append("• Long-term (2027+): Full PQC deployment for quantum resistance")
    summary.append("")
    summary.append("• Recommended PQC algorithms:")
    summary.append("  - KEM: ML-KEM-768 (Kyber) - NIST standardized")
    summary.append("  - Signatures: ML-DSA-65 (Dilithium3) - NIST standardized")
    summary.append("  - Stateless signatures: SLH-DSA (SPHINCS+) - For specific use cases")
    summary.append("")
    
    summary.append("=" * 80)
    
    return "\n".join(summary)


def create_comparison_table(df):
    """
    Create formatted comparison table for display.
    
    Args:
        df: DataFrame with benchmark results
        
    Returns:
        Formatted DataFrame for display
    """
    if len(df) == 0:
        return df
    
    display_df = df.copy()
    
    # Round numeric columns
    numeric_cols = display_df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if 'ms' in col.lower():
            display_df[col] = display_df[col].round(3)
        elif 'B)' in col or 'Size' in col:
            display_df[col] = display_df[col].astype(int)
        else:
            display_df[col] = display_df[col].round(2)
    
    return display_df
