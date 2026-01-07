"""
Hybrid Encryption Module
Implements real file encryption combining KEM with AES-256-GCM
for benchmarking purposes.
"""

import time
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import classic_algo
import pqc_algo


def derive_aes_key(shared_secret, salt=None):
    """Derive AES-256 key from KEM shared secret using HKDF."""
    if salt is None:
        salt = b'\x00' * 16
    
    kdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b'hybrid-encryption-key',
    )
    return kdf.derive(shared_secret)


def benchmark_hybrid_encryption_rsa(algo_name, file_data):
    """
    Benchmark RSA-based hybrid encryption:
    1. RSA-OAEP for key encapsulation (32-byte secret)
    2. AES-256-GCM for file encryption
    """
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import serialization
    
    size = int(algo_name.split("-")[1])
    
    # Step 1: Key Generation
    t0 = time.perf_counter()
    priv = rsa.generate_private_key(public_exponent=65537, key_size=size)
    pub = priv.public_key()
    t_gen = (time.perf_counter() - t0) * 1000

    pk_bytes = pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    sk_bytes = priv.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())

    # Step 2: Generate and encapsulate random AES key
    aes_key = os.urandom(32)
    
    t0 = time.perf_counter()
    kem_ciphertext = pub.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    t_encaps = (time.perf_counter() - t0) * 1000

    # Step 3: Encrypt file data with AES-256-GCM
    nonce = os.urandom(12)
    aesgcm = AESGCM(aes_key)
    
    t0 = time.perf_counter()
    file_ciphertext = aesgcm.encrypt(nonce, file_data, None)
    t_aes_enc = (time.perf_counter() - t0) * 1000
    
    # Step 4: Decapsulate AES key
    t0 = time.perf_counter()
    recovered_key = priv.decrypt(
        kem_ciphertext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    t_decaps = (time.perf_counter() - t0) * 1000
    
    # Step 5: Decrypt file data
    t0 = time.perf_counter()
    recovered_data = aesgcm.decrypt(nonce, file_ciphertext, None)
    t_aes_dec = (time.perf_counter() - t0) * 1000
    
    assert recovered_key == aes_key
    assert recovered_data == file_data

    return {
        "KeyGen (ms)": t_gen,
        "KEM Encaps (ms)": t_encaps,
        "KEM Decaps (ms)": t_decaps,
        "AES Encrypt (ms)": t_aes_enc,
        "AES Decrypt (ms)": t_aes_dec,
        "Total Encrypt (ms)": t_encaps + t_aes_enc,
        "Total Decrypt (ms)": t_decaps + t_aes_dec,
        "Total Time (ms)": t_gen + t_encaps + t_decaps + t_aes_enc + t_aes_dec,
        "PK Size (B)": len(pk_bytes),
        "SK Size (B)": len(sk_bytes),
        "KEM CT Size (B)": len(kem_ciphertext),
        "File Size (B)": len(file_data),
        "Ciphertext Size (B)": len(file_ciphertext),
        "Total Overhead (B)": len(kem_ciphertext) + (len(file_ciphertext) - len(file_data)) + 12,  # +12 for nonce
        "Overhead (%)": ((len(file_ciphertext) - len(file_data) + len(kem_ciphertext) + 12) / len(file_data)) * 100 if len(file_data) > 0 else 0
    }


def benchmark_hybrid_encryption_pqc(algo_name, file_data):
    """
    Benchmark PQC-based hybrid encryption:
    1. PQC KEM for key encapsulation
    2. AES-256-GCM for file encryption
    """
    if not pqc_algo.OQS_AVAILABLE:
        raise RuntimeError("Liboqs not available")
    
    import oqs
    
    with oqs.KeyEncapsulation(algo_name) as client:
        with oqs.KeyEncapsulation(algo_name) as server:
            
            # Step 1: Key Generation
            t0 = time.perf_counter()
            public_key = client.generate_keypair()
            t_gen = (time.perf_counter() - t0) * 1000
            
            secret_key = client.export_secret_key()
            
            # Step 2: Encapsulation (generates shared secret)
            t0 = time.perf_counter()
            kem_ciphertext, shared_secret_server = server.encap_secret(public_key)
            t_encaps = (time.perf_counter() - t0) * 1000
            
            # Derive AES key from shared secret
            aes_key = derive_aes_key(shared_secret_server)
            
            # Step 3: Encrypt file data with AES-256-GCM
            nonce = os.urandom(12)
            aesgcm = AESGCM(aes_key)
            
            t0 = time.perf_counter()
            file_ciphertext = aesgcm.encrypt(nonce, file_data, None)
            t_aes_enc = (time.perf_counter() - t0) * 1000
            
            # Step 4: Decapsulation
            t0 = time.perf_counter()
            shared_secret_client = client.decap_secret(kem_ciphertext)
            t_decaps = (time.perf_counter() - t0) * 1000
            
            # Derive same AES key
            recovered_aes_key = derive_aes_key(shared_secret_client)
            
            # Step 5: Decrypt file data
            t0 = time.perf_counter()
            recovered_data = aesgcm.decrypt(nonce, file_ciphertext, None)
            t_aes_dec = (time.perf_counter() - t0) * 1000
            
            assert shared_secret_client == shared_secret_server
            assert recovered_aes_key == aes_key
            assert recovered_data == file_data

            return {
                "KeyGen (ms)": t_gen,
                "KEM Encaps (ms)": t_encaps,
                "KEM Decaps (ms)": t_decaps,
                "AES Encrypt (ms)": t_aes_enc,
                "AES Decrypt (ms)": t_aes_dec,
                "Total Encrypt (ms)": t_encaps + t_aes_enc,
                "Total Decrypt (ms)": t_decaps + t_aes_dec,
                "Total Time (ms)": t_gen + t_encaps + t_decaps + t_aes_enc + t_aes_dec,
                "PK Size (B)": len(public_key),
                "SK Size (B)": len(secret_key),
                "KEM CT Size (B)": len(kem_ciphertext),
                "File Size (B)": len(file_data),
                "Ciphertext Size (B)": len(file_ciphertext),
                "Total Overhead (B)": len(kem_ciphertext) + (len(file_ciphertext) - len(file_data)) + 12,
                "Overhead (%)": ((len(file_ciphertext) - len(file_data) + len(kem_ciphertext) + 12) / len(file_data)) * 100 if len(file_data) > 0 else 0
            }


def benchmark_hybrid_encryption(algo_name, file_data):
    """Unified interface for benchmarking hybrid encryption."""
    if "RSA" in algo_name:
        return benchmark_hybrid_encryption_rsa(algo_name, file_data)
    else:
        return benchmark_hybrid_encryption_pqc(algo_name, file_data)
