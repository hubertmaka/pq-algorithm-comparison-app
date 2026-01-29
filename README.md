# 🔐 PQC vs Classic Crypto Benchmark Tool

**Comprehensive Performance Analysis of Classical and Post-Quantum Cryptographic Algorithms**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen.svg)](Dockerfile)

---

## 📋 Overview

This project provides a comprehensive benchmarking tool for comparing the performance of:

- **Classical cryptographic algorithms** (RSA, ECDSA)
- **Post-quantum cryptographic algorithms** (Kyber, Dilithium, SPHINCS+, BIKE, Falcon, and more)

### 🎯 Key Features

✅ **Multiple Test Scenarios**

- Key Exchange (KEM - Key Encapsulation Mechanisms)
- Digital Signatures
- Hybrid Encryption (KEM + AES-256-GCM)
- Real-world scenarios (TLS handshake, Secure Email, VPN, Code Signing)

✅ **Comprehensive Metrics**

- Execution time (key generation, encryption/signing, decryption/verification)
- Key and ciphertext/signature sizes
- Statistical analysis (standard deviation, percentiles, consistency scores)
- Performance vs size trade-off analysis

✅ **Advanced Visualization**

- Interactive charts (Plotly)
- Performance comparisons
- Trade-off analysis
- Statistical distributions

✅ **Export & Reporting**

- CSV, JSON, PDF export
- Executive summaries
- Algorithm recommendations
- Migration strategies

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/PQC-Project
cd PQC-Project

# Build the Docker image (takes ~10-15 minutes on first build)
docker build -t pqc-benchmark:latest .

# Run the container
docker run --rm -p 8501:8501 pqc-benchmark:latest

# Open in browser
# http://localhost:8501
```

### Option 2: Local Installation

**Prerequisites:**

- Python 3.10 or higher
- liboqs C library
- cmake, build-essential

**Installation steps:**

```bash
# 1. Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y build-essential cmake libssl-dev python3-venv

# 2. Install liboqs
git clone https://github.com/open-quantum-safe/liboqs
cd liboqs
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr/local ..
make -j4
sudo make install
sudo ldconfig
cd ../..

# 3. Install liboqs-python
git clone https://github.com/open-quantum-safe/liboqs-python
cd liboqs-python
pip install .
cd ..

# 4. Install project dependencies
cd PQC-Project
pip install -r requirements.txt

# 5. Run the application
streamlit run main.py
```

---

## 📖 Documentation

- **[User Guide](USER_GUIDE.md)** - Comprehensive usage guide with examples
- **[Analysis Report](ANALIZA_I_ULEPSZENIA.md)** - Detailed analysis and improvements (Polish)

---

## 🧪 Test Scenarios

### 1️⃣ KEM (Key Exchange Only)

Tests pure key encapsulation/decapsulation performance.

**Use cases:**

- TLS/SSL session establishment
- Secure communication key exchange
- Hybrid cryptography

**Algorithms tested:**

- Classic: RSA-2048, RSA-3072, RSA-4096
- PQC: Kyber (ML-KEM), BIKE, HQC, FrodoKEM

### 2️⃣ Digital Signatures

Tests signing and verification performance.

**Use cases:**

- Document signing
- Code signing
- Certificate generation
- Message authentication

**Algorithms tested:**

- Classic: ECDSA (P-256, P-384, P-521)
- PQC: Dilithium (ML-DSA), Falcon, SPHINCS+ (SLH-DSA)

### 3️⃣ Hybrid Encryption (KEM + AES)

Tests real file encryption combining KEM with AES-256-GCM.

**Use cases:**

- File encryption
- Secure data transmission
- Encrypted backups
- Email attachments

**Process:**

1. KEM generates shared secret
2. AES-256-GCM encrypts actual data
3. Measures total time and overhead

### 4️⃣ Real-World Scenarios

Simulates complete cryptographic applications.

**Available scenarios:**

- **TLS 1.3 Handshake:** Full HTTPS connection establishment
- **Secure Email (S/MIME):** Sign + encrypt email workflow
- **VPN Session:** Authentication + key exchange with re-keying
- **Code Signing:** Sign and verify executable files

---

## 📊 Supported Algorithms

### Classical Algorithms

| Category       | Algorithms                   | Security Level            |
| -------------- | ---------------------------- | ------------------------- |
| **KEM**        | RSA-2048, RSA-3072, RSA-4096 | 112-bit, 128-bit, 152-bit |
| **Signatures** | ECDSA P-256, P-384, P-521    | 128-bit, 192-bit, 256-bit |

### Post-Quantum Algorithms

| Category       | Algorithms                  | NIST Status                |
| -------------- | --------------------------- | -------------------------- |
| **KEM**        | ML-KEM-512/768/1024 (Kyber) | ✅ Standardized (FIPS 203) |
|                | BIKE L1/L3/L5               | 🔬 Round 4                 |
|                | HQC-128/192/256             | 🔬 Round 4                 |
|                | FrodoKEM-640/976/1344       | 🔬 Alternative             |
| **Signatures** | ML-DSA-44/65/87 (Dilithium) | ✅ Standardized (FIPS 204) |
|                | SLH-DSA (SPHINCS+)          | ✅ Standardized (FIPS 205) |
|                | Falcon-512/1024             | 🔬 Under consideration     |

---

## 🎨 Application Interface

### Main Sections

1. **Configuration Panel (Sidebar)**

   - Test scenario selection
   - Algorithm selection
   - Parameter configuration
   - System information

2. **Results Visualization (Main Area)**

   - Performance charts
   - Size analysis
   - Trade-off analysis
   - Statistical details
   - Comparative analysis
   - Recommendations

3. **Export Options**
   - CSV export
   - JSON export with metadata

### Example Workflow

```
1. Select scenario: "Hybrid Encryption (KEM+AES)"
2. Choose algorithms:
   - Classic: RSA-2048
   - PQC: ML-KEM-768, ML-KEM-1024
3. Set parameters:
   - File size: 1 MB
   - Iterations: 20
4. Run benchmark
5. Analyze results in tabs:
   - Performance: Time breakdown
   - Size Analysis: Overhead comparison
   - Trade-off: Speed vs size
   - Statistics: Consistency scores
   - Analysis: Classic vs PQC comparison
   - Recommendations: Based on use case
6. Export results (CSV/JSON)
```

---

**Key Insights:**

- ✅ PQC (Kyber, Dilithium) are often **faster** than RSA
- ⚠️ PQC have **larger** keys/signatures (2-30x)
- 💡 For most applications, the size overhead is **acceptable**
- 🎯 Falcon offers the best size/performance trade-off for signatures

---

## 🧠 Use Case Recommendations

### General Purpose Applications

**Recommended:**

- **KEM:** ML-KEM-768 (Kyber768) - NIST standardized, excellent performance
- **Signature:** ML-DSA-65 (Dilithium3) - NIST standardized, balanced

**Why:**

- Fast enough for real-time applications
- Reasonable bandwidth overhead
- Officially standardized
- Strong security guarantees

### IoT / Embedded Devices

**Recommended:**

- **KEM:** ML-KEM-512 or Kyber512
- **Signature:** ML-DSA-44 or Falcon-512

**Why:**

- Smallest PQC variants
- Lower memory requirements
- Still quantum-resistant

### High-Security / Long-Term Storage

**Recommended:**

- **KEM:** ML-KEM-1024
- **Signature:** ML-DSA-87 or SPHINCS+-256s

**Why:**

- Maximum security level
- Suitable for data protected beyond 2050
- SPHINCS+ is stateless (no key state management)

### Servers / High-Throughput

**Recommended:**

- **KEM:** ML-KEM-768 or ML-KEM-1024
- **Signature:** ML-DSA-65 or ML-DSA-87

**Why:**

- Servers can handle larger sizes
- Future-proofing investment
- Best performance among high-security options

---

## 🗺️ Migration Strategy

### Phase 1: Assessment (2024-2025)

- ✅ Evaluate current cryptographic usage
- ✅ Identify quantum-vulnerable systems
- ✅ Test PQC algorithms (use this tool!)
- ✅ Plan migration timeline

### Phase 2: Hybrid Deployment (2025-2027)

- 🔄 Implement hybrid mode (Classic + PQC)
- 🔄 Update critical systems first
- 🔄 Monitor performance impact
- 🔄 Train teams on PQC

### Phase 3: PQC Transition (2027-2030)

- ⏩ Increase PQC usage
- ⏩ New systems: PQC by default
- ⏩ Legacy systems: maintain hybrid
- ⏩ Deprecate pure classical crypto

### Phase 4: Full PQC (2030+)

- 🎯 Complete PQC deployment
- 🎯 Remove classical algorithms
- 🎯 Continuous monitoring
- 🎯 Prepare for algorithm agility

**Why Hybrid Mode?**

```
Hybrid = Classical_Algorithm + PQC_Algorithm

Benefits:
✅ Protected against current threats (classical)
✅ Protected against quantum threats (PQC)
✅ Safe even if one algorithm is broken
✅ Smooth transition period
```

---

## 📦 Dependencies

### Core Libraries

- **streamlit** - Web application framework
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **plotly** - Interactive visualizations
- **cryptography** - Classical cryptographic operations
- **liboqs-python** - Post-quantum cryptographic operations

### Additional Libraries

- **fpdf2** - PDF report generation
- **py-cpuinfo** - CPU information detection

### System Requirements

- **Python** 3.10+
- **liboqs** C library (installed via Docker or manually)
- **cmake** (for building liboqs)
- **OpenSSL** development files

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

### Areas for Contribution

- Additional algorithms support
- New test scenarios
- Performance optimizations
- Documentation improvements
- Bug fixes

---

## 📚 References and Resources

### NIST PQC Standardization

- [NIST PQC Project](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [FIPS 203 - ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- [FIPS 204 - ML-DSA](https://csrc.nist.gov/pubs/fips/204/final)
- [FIPS 205 - SLH-DSA](https://csrc.nist.gov/pubs/fips/205/final)

### Libraries and Tools

- [liboqs](https://github.com/open-quantum-safe/liboqs) - C library for quantum-safe cryptography
- [liboqs-python](https://github.com/open-quantum-safe/liboqs-python) - Python wrapper
- [Open Quantum Safe](https://openquantumsafe.org/) - Project homepage

### Academic Papers

- Kyber: [CRYSTALS-Kyber](https://pq-crystals.org/kyber/)
- Dilithium: [CRYSTALS-Dilithium](https://pq-crystals.org/dilithium/)
- SPHINCS+: [SPHINCS+ Specification](https://sphincs.org/)
- Falcon: [Falcon Specification](https://falcon-sign.info/)

---

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support

- **Documentation:** [User Guide](USER_GUIDE.md)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Built with ❤️ for the post-quantum era**

_Stay quantum-safe!_ 🔐🚀
