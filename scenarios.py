"""
Real-world scenario simulations for cryptographic benchmarking.
Includes TLS handshake, secure email, VPN session, etc.
"""

import time
import classic_algo
import pqc_algo


def benchmark_tls_handshake(kem_algo, sig_algo, payload_size=1024):
    """
    Simulate TLS 1.3 handshake:
    1. Server generates signature keypair (for certificate)
    2. Client generates KEM keypair
    3. Server signs its certificate
    4. Client verifies signature
    5. Client encapsulates session key (KEM)
    6. Server decapsulates session key
    
    Returns comprehensive timing and bandwidth metrics.
    """
    is_rsa_kem = "RSA" in kem_algo
    is_ecc_sig = "SECP" in sig_algo
    
    # Phase 1: Certificate generation and signing
    if is_ecc_sig:
        cert_result = classic_algo.benchmark_ecdsa_sign(sig_algo, b"server-certificate-data")
    else:  # PQC signature
        cert_result = pqc_algo.benchmark_pqc_sign(sig_algo, b"server-certificate-data")
    
    t_cert_gen = cert_result["KeyGen (ms)"]
    t_cert_sign = cert_result["Sign (ms)"]
    t_cert_verify = cert_result["Verify (ms)"]
    cert_pk_size = cert_result["PK Size (B)"]
    cert_sig_size = cert_result["CT/Sig Size (B)"]
    
    # Phase 2: Key exchange (KEM)
    if is_rsa_kem:
        kem_result = classic_algo.benchmark_rsa_kem(kem_algo, None)
    else:  # PQC KEM
        kem_result = pqc_algo.benchmark_pqc_kem(kem_algo, None)
    
    t_kem_gen = kem_result["KeyGen (ms)"]
    t_encaps = kem_result["Encaps (ms)"]
    t_decaps = kem_result["Decaps (ms)"]
    kem_pk_size = kem_result["PK Size (B)"]
    kem_ct_size = kem_result["CT/Sig Size (B)"]
    
    # Calculate total metrics
    total_time = t_cert_gen + t_kem_gen + t_cert_sign + t_cert_verify + t_encaps + t_decaps
    
    # ClientHello: KEM public key
    client_hello_size = kem_pk_size + 100  # +100 for TLS overhead
    
    # ServerHello: Certificate (sig PK + signature) + KEM ciphertext
    server_hello_size = cert_pk_size + cert_sig_size + kem_ct_size + 200  # +200 for TLS overhead
    
    # Client final: verification complete
    client_final_size = 50  # Minimal ACK
    
    total_bandwidth = client_hello_size + server_hello_size + client_final_size
    
    return {
        "Scenario": "TLS 1.3 Handshake",
        "KEM Algorithm": kem_algo,
        "Signature Algorithm": sig_algo,
        "Total Time (ms)": total_time,
        "Server Cert Gen (ms)": t_cert_gen,
        "Client KEM Gen (ms)": t_kem_gen,
        "Cert Sign (ms)": t_cert_sign,
        "Cert Verify (ms)": t_cert_verify,
        "Encapsulate (ms)": t_encaps,
        "Decapsulate (ms)": t_decaps,
        "ClientHello Size (B)": client_hello_size,
        "ServerHello Size (B)": server_hello_size,
        "Total Handshake Bandwidth (B)": total_bandwidth,
        "Handshake RTT": 1.5,  # Typical: 1.5 round trips
        "Ready for Data Transfer (ms)": total_time
    }


def benchmark_secure_email(sig_algo, kem_algo, message_size=10240):
    """
    Simulate S/MIME-like secure email:
    1. Sender signs message
    2. Sender encrypts message with recipient's public key (hybrid encryption)
    3. Recipient decrypts message
    4. Recipient verifies signature
    """
    import os
    from hybrid_encryption import benchmark_hybrid_encryption
    
    message = os.urandom(message_size)
    
    is_ecc_sig = "SECP" in sig_algo
    
    # Phase 1: Sign message
    if is_ecc_sig:
        sig_result = classic_algo.benchmark_ecdsa_sign(sig_algo, message)
    else:
        sig_result = pqc_algo.benchmark_pqc_sign(sig_algo, message)
    
    t_sign = sig_result["Sign (ms)"]
    t_verify = sig_result["Verify (ms)"]
    sig_size = sig_result["CT/Sig Size (B)"]
    
    # Phase 2: Hybrid encryption of message + signature
    signed_message = message + b"|SIGNATURE|" + os.urandom(sig_size)
    
    enc_result = benchmark_hybrid_encryption(kem_algo, signed_message)
    
    total_time = sig_result["KeyGen (ms)"] + enc_result["KeyGen (ms)"] + t_sign + enc_result["Total Encrypt (ms)"] + enc_result["Total Decrypt (ms)"] + t_verify
    
    encrypted_email_size = enc_result["KEM CT Size (B)"] + enc_result["Ciphertext Size (B)"] + 12  # +12 nonce
    
    return {
        "Scenario": "Secure Email (S/MIME-like)",
        "Message Size (KB)": message_size / 1024,
        "Signature Algorithm": sig_algo,
        "KEM Algorithm": kem_algo,
        "Total Time (ms)": total_time,
        "Sign (ms)": t_sign,
        "Encrypt (ms)": enc_result["Total Encrypt (ms)"],
        "Decrypt (ms)": enc_result["Total Decrypt (ms)"],
        "Verify (ms)": t_verify,
        "Original Message Size (B)": message_size,
        "Encrypted Email Size (B)": encrypted_email_size,
        "Overhead (%)": ((encrypted_email_size - message_size) / message_size) * 100
    }


def benchmark_vpn_session(kem_algo, sig_algo, session_duration_pkts=100):
    """
    Simulate VPN session establishment:
    1. Initial authentication (signatures)
    2. Key exchange (KEM)
    3. Optional: periodic re-keying
    """
    is_ecc_sig = "SECP" in sig_algo
    is_rsa_kem = "RSA" in kem_algo
    
    # Phase 1: Authentication
    if is_ecc_sig:
        auth_result = classic_algo.benchmark_ecdsa_sign(sig_algo, b"vpn-auth-challenge")
    else:
        auth_result = pqc_algo.benchmark_pqc_sign(sig_algo, b"vpn-auth-challenge")
    
    # Phase 2: Key exchange
    if is_rsa_kem:
        kem_result = classic_algo.benchmark_rsa_kem(kem_algo, None)
    else:
        kem_result = pqc_algo.benchmark_pqc_kem(kem_algo, None)
    
    # Initial handshake time
    handshake_time = (auth_result["KeyGen (ms)"] + auth_result["Sign (ms)"] + 
                      auth_result["Verify (ms)"] + kem_result["KeyGen (ms)"] + 
                      kem_result["Encaps (ms)"] + kem_result["Decaps (ms)"])
    
    # Simulate periodic re-keying (every 20 packets)
    rekey_count = session_duration_pkts // 20
    rekey_time = rekey_count * (kem_result["Encaps (ms)"] + kem_result["Decaps (ms)"])
    
    total_time = handshake_time + rekey_time
    
    return {
        "Scenario": "VPN Session",
        "KEM Algorithm": kem_algo,
        "Signature Algorithm": sig_algo,
        "Session Packets": session_duration_pkts,
        "Initial Handshake (ms)": handshake_time,
        "Re-key Count": rekey_count,
        "Re-key Overhead (ms)": rekey_time,
        "Total Session Setup (ms)": total_time,
        "Avg Time per Packet (ms)": total_time / session_duration_pkts if session_duration_pkts > 0 else 0
    }


def benchmark_code_signing(sig_algo, file_size=1048576):
    """
    Simulate code signing scenario:
    1. Generate signature keypair
    2. Sign executable/package
    3. Distribute with signature
    4. Verify signature
    """
    import os
    
    code_data = os.urandom(file_size)
    
    is_ecc_sig = "SECP" in sig_algo
    
    if is_ecc_sig:
        sig_result = classic_algo.benchmark_ecdsa_sign(sig_algo, code_data)
    else:
        sig_result = pqc_algo.benchmark_pqc_sign(sig_algo, code_data)
    
    return {
        "Scenario": "Code Signing",
        "Signature Algorithm": sig_algo,
        "File Size (MB)": file_size / (1024 * 1024),
        "KeyGen (ms)": sig_result["KeyGen (ms)"],
        "Sign (ms)": sig_result["Sign (ms)"],
        "Verify (ms)": sig_result["Verify (ms)"],
        "Signature Size (B)": sig_result["CT/Sig Size (B)"],
        "Public Key Size (B)": sig_result["PK Size (B)"],
        "Distribution Overhead (%)": (sig_result["CT/Sig Size (B)"] / file_size) * 100
    }


def get_available_scenarios():
    """Return list of available real-world scenarios."""
    return [
        "TLS 1.3 Handshake",
        "Secure Email (S/MIME)",
        "VPN Session",
        "Code Signing",
        "Secure Messaging"
    ]
