import time
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.primitives import serialization, hashes

def get_rsa_options():
    return ["RSA-2048", "RSA-3072", "RSA-4096"]

def get_ecc_options():
    return ["SECP256R1 (P-256)", "SECP384R1 (P-384)", "SECP521R1 (P-521)"]

def benchmark_rsa_kem(algo_name="RSA-2048", payload=None):
    size = int(algo_name.split("-")[1])
    
    t0 = time.perf_counter()
    priv = rsa.generate_private_key(public_exponent=65537, key_size=size)
    pub = priv.public_key()
    t_gen = (time.perf_counter() - t0) * 1000

    pk_bytes = pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    sk_bytes = priv.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())

    secret = b"x" * 32
    
    t0 = time.perf_counter()
    ct = pub.encrypt(
        secret,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    t_enc = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    _ = priv.decrypt(
        ct,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    t_dec = (time.perf_counter() - t0) * 1000

    return {
        "KeyGen (ms)": t_gen, 
        "Encaps (ms)": t_enc, 
        "Decaps (ms)": t_dec,
        "PK Size (B)": len(pk_bytes), 
        "SK Size (B)": len(sk_bytes), 
        "CT/Sig Size (B)": len(ct)
    }

def benchmark_ecdsa_sign(algo_name="SECP256R1 (P-256)", payload=b"test"):
    if "P-256" in algo_name:
        curve = ec.SECP256R1()
    elif "P-384" in algo_name:
        curve = ec.SECP384R1()
    else:
        curve = ec.SECP521R1()

    t0 = time.perf_counter()
    priv = ec.generate_private_key(curve)
    pub = priv.public_key()
    t_gen = (time.perf_counter() - t0) * 1000

    pk_bytes = pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    sk_bytes = priv.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())

    t0 = time.perf_counter()
    sig = priv.sign(payload, ec.ECDSA(hashes.SHA256()))
    t_sign = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    pub.verify(sig, payload, ec.ECDSA(hashes.SHA256()))
    t_vrfy = (time.perf_counter() - t0) * 1000

    return {
        "KeyGen (ms)": t_gen, 
        "Sign (ms)": t_sign, 
        "Verify (ms)": t_vrfy,
        "PK Size (B)": len(pk_bytes), 
        "SK Size (B)": len(sk_bytes), 
        "CT/Sig Size (B)": len(sig)
    }