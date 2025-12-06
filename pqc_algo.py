import time
import sys

# Global flag to check library availability
OQS_AVAILABLE = False

try:
    import oqs
    OQS_AVAILABLE = True
except ImportError:
    OQS_AVAILABLE = False

def get_available_kem():
    """Returns a list of enabled PQC Key Encapsulation Mechanisms."""
    if not OQS_AVAILABLE:
        return []

    if hasattr(oqs, "get_enabled_kem_mechanisms"):
        all_kems = oqs.get_enabled_kem_mechanisms()
    elif hasattr(oqs, "get_enabled_KEM_mechanisms"):
        all_kems = oqs.get_enabled_KEM_mechanisms()
    else:
        try:
            all_kems = oqs.KeyEncapsulation.get_enabled_mechanisms()
        except AttributeError:
            return []

    priority_list = ["Kyber", "ML-KEM", "BIKE", "HQC", "FrodoKEM"] 
    filtered = [alg for alg in all_kems if any(p in alg for p in priority_list)]
    return filtered if filtered else all_kems

def get_available_sig():
    """Returns a list of enabled PQC Digital Signature algorithms."""
    if not OQS_AVAILABLE:
        return []
    
    if hasattr(oqs, "get_enabled_sig_mechanisms"):
        all_sigs = oqs.get_enabled_sig_mechanisms()
    elif hasattr(oqs, "get_enabled_sig_mechanisms"):
        all_sigs = oqs.get_enabled_sig_mechanisms()
    else:
        try:
            all_sigs = oqs.Signature.get_enabled_mechanisms()
        except AttributeError:
            return []

    priority_list = ["Dilithium", "ML-DSA", "Falcon", "SPHINCS", "SLH-DSA"]
    filtered = [alg for alg in all_sigs if any(p in alg for p in priority_list)]
    return filtered if filtered else all_sigs

def benchmark_pqc_kem(algo_name, payload=None):
    """
    Benchmarks Post-Quantum Key Encapsulation.
    """
    if not OQS_AVAILABLE:
        raise RuntimeError("Liboqs not available")

    results = {}
    
    # Context manager ensures memory is freed
    with oqs.KeyEncapsulation(algo_name) as client:
        with oqs.KeyEncapsulation(algo_name) as server:
            
            # 1. Key Generation
            t0 = time.perf_counter()
            public_key = client.generate_keypair()
            t_gen = (time.perf_counter() - t0) * 1000
            
            secret_key = client.export_secret_key()
            
            # 2. Encapsulation
            t0 = time.perf_counter()
            ciphertext, shared_secret_client = server.encap_secret(public_key)
            t_enc = (time.perf_counter() - t0) * 1000
            
            # 3. Decapsulation
            t0 = time.perf_counter()
            shared_secret_server = client.decap_secret(ciphertext)
            t_dec = (time.perf_counter() - t0) * 1000
            
            assert shared_secret_client == shared_secret_server
            
            results = {
                "KeyGen (ms)": t_gen,
                "Encaps (ms)": t_enc,
                "Decaps (ms)": t_dec,
                "PK Size (B)": len(public_key),
                "SK Size (B)": len(secret_key),
                "CT/Sig Size (B)": len(ciphertext)
            }

    return results

def benchmark_pqc_sign(algo_name, payload):
    """
    Benchmarks Post-Quantum Digital Signatures.
    """
    if not OQS_AVAILABLE:
        raise RuntimeError("Liboqs not available")
    
    results = {}
    
    # Ensure payload is bytes
    if isinstance(payload, str):
        payload = payload.encode()
        
    with oqs.Signature(algo_name) as signer:
        with oqs.Signature(algo_name) as verifier:
            
            # 1. Key Generation
            t0 = time.perf_counter()
            public_key = signer.generate_keypair()
            t_gen = (time.perf_counter() - t0) * 1000
            
            secret_key = signer.export_secret_key()
            
            # 2. Signing
            t0 = time.perf_counter()
            signature = signer.sign(payload)
            t_sign = (time.perf_counter() - t0) * 1000
            
            # 3. Verifying
            t0 = time.perf_counter()
            is_valid = verifier.verify(payload, signature, public_key)
            t_vrfy = (time.perf_counter() - t0) * 1000
            
            results = {
                "KeyGen (ms)": t_gen,
                "Sign (ms)": t_sign,
                "Verify (ms)": t_vrfy,
                "PK Size (B)": len(public_key),
                "SK Size (B)": len(secret_key),
                "CT/Sig Size (B)": len(signature)
            }
            
    return results