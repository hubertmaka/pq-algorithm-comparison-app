# 📘 User Guide - PQC vs Classic Crypto Benchmark Tool

## Spis treści

1. [Wprowadzenie](#wprowadzenie)
2. [Instalacja](#instalacja)
3. [Uruchomienie](#uruchomienie)
4. [Scenariusze testowe](#scenariusze-testowe)
5. [Konfiguracja testów](#konfiguracja-testów)
6. [Interpretacja wyników](#interpretacja-wyników)
7. [Eksport wyników](#eksport-wyników)
8. [Najlepsze praktyki](#najlepsze-praktyki)
9. [Rozwiązywanie problemów](#rozwiązywanie-problemów)

---

## Wprowadzenie

### Co to jest PQC Benchmark Tool?

Narzędzie do kompleksowego porównania wydajności algorytmów kryptograficznych:

- **Klasycznych** (RSA, ECDSA) - obecnie używanych powszechnie
- **Postkwantowych** (Kyber, Dilithium, SPHINCS+) - odpornych na ataki komputerów kwantowych

### Dlaczego to jest ważne?

W ciągu najbliższych 5-10 lat komputery kwantowe mogą złamać obecne algorytmy szyfrowania (RSA, ECC). NIST (National Institute of Standards and Technology) wystandaryzował nowe algorytmy postkwantowe, które są odporne na ataki kwantowe.

### Kluczowe możliwości

✅ **4 tryby testowania**

- Wymiana kluczy (KEM)
- Podpisy cyfrowe
- Szyfrowanie plików (hybrid encryption)
- Symulacje rzeczywistych scenariuszy

✅ **Kompleksowa analiza**

- Pomiar czasu operacji
- Pomiar rozmiarów kluczy i szyfrogramów
- Analiza statystyczna (odchylenie std, percentyle)
- Porównanie classic vs PQC

✅ **Wizualizacje i raporty**

- Interaktywne wykresy
- Tabele porównawcze
- Eksport do CSV, JSON, PDF

---

## Instalacja

### Opcja 1: Docker (zalecana)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/PQC-Project
cd PQC-Project

# 2. Build Docker image (zajmie ~10-15 minut przy pierwszym budowaniu)
docker build -t pqc-benchmark:latest .

# 3. Uruchom kontener
docker run --rm -p 8501:8501 pqc-benchmark:latest

# 4. Otwórz w przeglądarce
# http://localhost:8501
```

### Opcja 2: Instalacja lokalna

**Wymagania:**

- Python 3.10+
- liboqs (biblioteka C dla PQC)
- cmake, build-essential

**Kroki instalacji (Ubuntu/Debian):**

```bash
# 1. Zainstaluj zależności systemowe
sudo apt-get update
sudo apt-get install -y build-essential cmake libssl-dev python3-venv

# 2. Zainstaluj liboqs
git clone https://github.com/open-quantum-safe/liboqs
cd liboqs
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr/local ..
make -j4
sudo make install
sudo ldconfig
cd ../..

# 3. Zainstaluj liboqs-python
git clone https://github.com/open-quantum-safe/liboqs-python
cd liboqs-python
pip install .
cd ..

# 4. Zainstaluj pozostałe zależności projektu
cd PQC-Project
pip install -r requirements.txt

# 5. Uruchom aplikację
streamlit run main.py
```

**Kroki instalacji (macOS):**

```bash
# Użyj Homebrew
brew install cmake openssl
# Następnie postępuj jak w instrukcji powyżej
```

---

## Uruchomienie

### Uruchomienie aplikacji

**Docker:**

```bash
docker run --rm -p 8501:8501 pqc-benchmark:latest
```

**Lokalne:**

```bash
streamlit run main.py
```

### Pierwsze kroki

1. **Otwórz aplikację** w przeglądarce: `http://localhost:8501`
2. **Wybierz scenariusz testowy** z panelu bocznego
3. **Skonfiguruj parametry** (algorytmy, iteracje, rozmiar danych)
4. **Uruchom benchmark** przyciskiem "🚀 Run Comprehensive Benchmark"
5. **Analizuj wyniki** w zakładkach

---

## Scenariusze testowe

### 1️⃣ KEM (Key Exchange Only)

**Cel:** Test czystej wymiany kluczy - jak szybko algorytmy mogą ustanowić wspólny tajny klucz.

**Zastosowanie:**

- Ustanawianie sesji szyfrowanych (TLS/SSL)
- Wymiana kluczy w protokołach komunikacyjnych
- Kryptografia hybrydowa

**Co jest mierzone:**

- Czas generowania pary kluczy
- Czas enkapsulacji (tworzenie wspólnego sekretu)
- Czas dekapsulacji (odzyskanie wspólnego sekretu)
- Rozmiar klucza publicznego
- Rozmiar szyfrotekstu KEM

**Przykład użycia:**

```
1. Wybierz: "KEM (Key Exchange Only)"
2. Algorytmy: RSA-2048, Kyber768, Kyber1024
3. Iteracje: 20
4. Uruchom test
```

**Interpretacja:**

- ✅ Kyber768: ~0.1-0.5ms, klucz publiczny ~1KB, CT ~1KB
- ⚠️ RSA-2048: ~20-50ms, klucz publiczny ~0.5KB, CT ~0.5KB
- 📊 Wynik: Kyber jest 50-100x szybszy, ale ma większe klucze

---

### 2️⃣ Digital Signatures

**Cel:** Test podpisywania i weryfikacji wiadomości.

**Zastosowanie:**

- Podpisy dokumentów
- Uwierzytelnianie wiadomości
- Code signing (podpisywanie oprogramowania)
- Certyfikaty cyfrowe

**Co jest mierzone:**

- Czas generowania klucza
- Czas podpisywania
- Czas weryfikacji podpisu
- Rozmiar klucza publicznego
- Rozmiar podpisu

**Przykład użycia:**

```
1. Wybierz: "Digital Signatures"
2. Message Source: "Random Generated"
3. Message Size: 10 KB
4. Algorytmy: ECDSA P-256, Dilithium3, SPHINCS+-128f
5. Iteracje: 20
6. Uruchom test
```

**Interpretacja:**

- ✅ ECDSA P-256: bardzo szybka (~1ms), mały podpis (~64B)
- ✅ Dilithium3: szybka (~2-5ms), większy podpis (~3KB)
- ⚠️ SPHINCS+-128f: wolniejsza (~100ms+), duży podpis (~17KB), ale stateless

**Kiedy używać każdego:**

- **ECDSA**: gdy liczy się rozmiar i wydajność (obecnie)
- **Dilithium**: uniwersalny PQC, dobry balans (przyszłość)
- **SPHINCS+**: gdy potrzebny stateless (nie wymaga stanu)

---

### 3️⃣ Hybrid Encryption (KEM+AES)

**Cel:** Test faktycznego szyfrowania plików - najbliższy rzeczywistym zastosowaniom.

**Jak działa:**

1. KEM generuje wspólny sekret
2. Sekret jest używany jako klucz AES-256-GCM
3. AES szyfruje faktyczne dane pliku

**Zastosowanie:**

- Szyfrowanie plików
- Bezpieczne przesyłanie danych
- Backup szyfrowany
- Szyfrowanie email attachments

**Co jest mierzone:**

- Czas KEM (encaps/decaps)
- Czas szyfrowania AES
- Czas deszyfrowania AES
- Całkowity czas szyfrowania/deszyfrowania
- Overhead (jak dużo większy jest zaszyfrowany plik)

**Przykład użycia:**

```
1. Wybierz: "Hybrid Encryption (KEM+AES)"
2. File Source: "Random Generated"
3. File Size: 1 MB
4. Algorytmy: RSA-2048, Kyber768, Kyber1024
5. Iteracje: 10 (mniej, bo test trwa dłużej)
6. Uruchom test
```

**Interpretacja dla 1MB pliku:**

- **RSA-2048:**

  - KEM: ~30ms
  - AES: ~2ms
  - Całość: ~32ms
  - Overhead: ~512B (klucz KEM)

- **Kyber768:**
  - KEM: ~0.3ms
  - AES: ~2ms
  - Całość: ~2.3ms
  - Overhead: ~2KB (klucz + CT)

**Wniosek:** KEM ma niewielki wpływ na całkowity czas, AES dominuje dla dużych plików. Overhead PQC to tylko ~0.2% dla 1MB pliku.

---

### 4️⃣ Real-World Scenarios

**Cel:** Symulacja kompletnych, rzeczywistych aplikacji kryptograficznych.

#### a) TLS 1.3 Handshake

Symuluje nawiązanie bezpiecznego połączenia HTTPS.

**Fazy:**

1. Server generuje certyfikat i go podpisuje
2. Client weryfikuje certyfikat
3. Client i Server wykonują wymianę kluczy (KEM)
4. Gotowe do przesyłania danych

**Mierzone metryki:**

- Całkowity czas handshake
- Ilość przesłanych danych (bandwidth)
- Czas poszczególnych faz

**Przykład:**

```
Algorytmy KEM: RSA-2048, Kyber768
Algorytmy Signature: ECDSA P-256, Dilithium3

Kombinacje testowane:
- RSA + ECDSA (obecny standard)
- Kyber + ECDSA (hybrid)
- Kyber + Dilithium (pełny PQC)
```

**Wyniki typowe:**

- RSA + ECDSA: ~50ms, ~1.5KB danych
- Kyber + ECDSA: ~5ms, ~3KB danych
- Kyber + Dilithium: ~8ms, ~7KB danych

**Wnioski:**

- Pełny PQC jest ~6x szybszy niż obecny standard
- Kosztem ~5x większej ilości przesłanych danych
- Dla współczesnych sieci różnica jest akceptowalna

#### b) Secure Email (S/MIME-like)

Symuluje wysłanie zaszyfrowanego i podpisanego emaila.

**Kroki:**

1. Nadawca podpisuje wiadomość
2. Nadawca szyfruje (wiadomość + podpis) kluczem odbiorcy
3. Odbiorca deszyfruje
4. Odbiorca weryfikuje podpis

**Przykład:**

```
Email Size: 10 KB
Signature: Dilithium3
KEM: Kyber768
```

**Typowe wyniki:**

- Sign + Encrypt: ~5ms
- Decrypt + Verify: ~5ms
- Overhead: ~15% (email 10KB → 11.5KB)

#### c) VPN Session

Symuluje nawiązanie sesji VPN z okresowym re-keyingiem.

**Fazy:**

1. Autentykacja (podpisy)
2. Wymiana klucza początkowego (KEM)
3. Okresowa wymiana kluczy co N pakietów

**Parametry:**

- Session Packets: 100 (domyślnie)
- Re-key co 20 pakietów

**Wyniki typowe:**

- Initial handshake: ~10ms
- Re-key overhead: ~0.5ms per 20 packets
- Łącznie: ~12ms dla 100 pakietów

#### d) Code Signing

Symuluje podpisanie i weryfikację pliku wykonywalnego.

**Parametry:**

- File Size: 1-100 MB

**Zastosowanie:**

- Podpisywanie aplikacji
- Weryfikacja integralności oprogramowania

**Wyniki dla 10MB pliku:**

- ECDSA P-256: Sign ~50ms, Verify ~50ms
- Dilithium3: Sign ~100ms, Verify ~80ms
- SPHINCS+-128f: Sign ~2000ms, Verify ~50ms

---

## Konfiguracja testów

### Wybór algorytmów

#### Klasyczne algorytmy

**RSA (Key Exchange):**

- **RSA-2048:** Standard na dziś, bezpieczny do ~2030
- **RSA-3072:** Wyższa ochrona, wolniejszy
- **RSA-4096:** Maksymalna ochrona klasyczna, znacznie wolniejszy

**ECDSA (Signatures):**

- **SECP256R1 (P-256):** Najbardziej popularny, ~128-bit security
- **SECP384R1 (P-384):** Wyższe bezpieczeństwo, ~192-bit
- **SECP521R1 (P-521):** Najwyższe, ~256-bit security

#### Postkwantowe algorytmy

**KEM (Key Exchange):**

| Algorytm                | Security Level | Uwagi                      |
| ----------------------- | -------------- | -------------------------- |
| Kyber512 / ML-KEM-512   | NIST Level 1   | Najszybszy, IoT            |
| Kyber768 / ML-KEM-768   | NIST Level 3   | ⭐ Zalecany, standardowy   |
| Kyber1024 / ML-KEM-1024 | NIST Level 5   | Maksymalne bezpieczeństwo  |
| BIKE L1/L3              | Varies         | Code-based, większe klucze |
| HQC-128/192/256         | Varies         | Code-based                 |

**Signatures:**

| Algorytm               | Security Level | Uwagi                     |
| ---------------------- | -------------- | ------------------------- |
| Dilithium2 / ML-DSA-44 | NIST Level 2   | Mały, szybki              |
| Dilithium3 / ML-DSA-65 | NIST Level 3   | ⭐ Zalecany               |
| Dilithium5 / ML-DSA-87 | NIST Level 5   | Maksymalne bezpieczeństwo |
| Falcon-512             | NIST Level 1   | Najmniejsze podpisy       |
| Falcon-1024            | NIST Level 5   | Mały ale wolniejszy       |
| SPHINCS+-128f/s        | NIST Level 1   | Stateless, duże podpisy   |
| SPHINCS+-256f/s        | NIST Level 5   | Bardzo bezpieczny         |

**Wybór zalecany dla różnych zastosowań:**

```
📱 IoT / Embedded:
   KEM: Kyber512
   Sig: Dilithium2 lub Falcon-512

💻 General Purpose:
   KEM: Kyber768 (ML-KEM-768) ⭐
   Sig: Dilithium3 (ML-DSA-65) ⭐

🖥️ Server / High Performance:
   KEM: Kyber768 lub Kyber1024
   Sig: Dilithium3 lub Dilithium5

🔒 Maximum Security:
   KEM: Kyber1024 (ML-KEM-1024)
   Sig: Dilithium5 lub SPHINCS+-256s
```

### Parametry testów

#### Iteracje

**Wartość:** 5-500 (zalecane: 20-50)

**Wpływ:**

- Więcej iteracji = lepsza dokładność statystyczna
- Mniej iteracji = szybsze zakończenie testu

**Zalecenia:**

- Quick test: 5-10 iteracji
- Standard: 20-30 iteracji
- Dokładna analiza: 50-100 iteracji
- Publikacja naukowa: 100-500 iteracji

#### Rozmiar danych

**Digital Signatures:**

- Small messages: 1-10 KB (typowe komunikaty)
- Documents: 10-100 KB
- Files: 100-1024 KB

**Hybrid Encryption:**

- Small files: 1-10 KB
- Documents: 100 KB - 1 MB
- Large files: 1-100 MB
- Very large: 100+ MB (może trwać długo)

**Wpływ rozmiaru:**

- KEM: rozmiar nie ma wpływu (zawsze 32B secret)
- Signatures: wpływ liniowy na czas
- Hybrid: AES dominuje dla dużych plików

---

## Interpretacja wyników

### Zakładka: Performance

**Metryki:**

- **KeyGen (ms):** Czas generowania pary kluczy
- **Encaps/Sign (ms):** Czas operacji nadawcy
- **Decaps/Verify (ms):** Czas operacji odbiorcy
- **Total Time (ms):** Suma wszystkich operacji

**Jak czytać wykresy:**

- Słupki: niższe = lepsze (szybsze)
- Porównaj między "Classic" i "Post-Quantum"
- Sprawdź proporcje: czy KeyGen dominuje? Czy Sign/Verify?

**Typowe wzorce:**

- **RSA:** KeyGen bardzo kosztowny (~50ms), encrypt szybszy
- **ECDSA:** Wszystkie operacje szybkie (~1-5ms)
- **Kyber:** Bardzo szybki we wszystkim (~0.1-1ms)
- **Dilithium:** Szybki (~2-10ms)
- **SPHINCS+:** Sign wolny (~100-1000ms), Verify szybki

### Zakładka: Size Analysis

**Metryki:**

- **PK Size:** Rozmiar klucza publicznego
- **SK Size:** Rozmiar klucza prywatnego
- **Output Size:** Rozmiar CT (ciphertext) lub Signature

**Skala logarytmiczna:**

- Wykresy używają log scale, bo różnice są rzędu 10-100x
- Każdy "stopień" na osi Y to 10x więcej

**Typowe rozmiary:**

```
Klasyczne:
  RSA-2048: PK ~256B, CT ~256B
  ECDSA P-256: PK ~64B, Sig ~64B

PQC KEM:
  Kyber768: PK ~1184B, CT ~1088B (10-20x większe)

PQC Signatures:
  Dilithium3: PK ~1952B, Sig ~3293B (50x większe)
  Falcon-512: PK ~897B, Sig ~666B (10x większe)
  SPHINCS+: PK ~32B, Sig ~17KB (270x większe!)
```

**Znaczenie:**

- Dla większości aplikacji 1-5KB overhead jest OK
- Dla IoT z ograniczonym bandwidth może być problem
- Falcon ma najmniejsze podpisy PQC

### Zakładka: Trade-off

**Wykres Scatter (Log-Log):**

- Oś X: Total Bandwidth (rozmiar)
- Oś Y: Total Time (czas)
- **Idealny algorytm:** lewy dolny róg (szybki I mały)

**Linie mediany:**

- Pozioma: mediana czasu
- Pionowa: mediana rozmiaru
- Dzielą wykres na 4 kwadranty

**Kwadranty:**

1. **Lewy dolny:** BEST (szybki i mały) ✅
2. **Lewy górny:** mały ale wolny
3. **Prawy dolny:** szybki ale duży
4. **Prawy górny:** WORST (wolny i duży) ❌

**Efficiency Score:**

- Syntetyczna miara łącząca czas i rozmiar
- Niższy = lepszy
- Top 10 pokazuje najbardziej zbalansowane algorytmy

### Zakładka: Statistics

**Consistency Score:**

- 100 = idealna powtarzalność
- 90-100 = bardzo dobra
- 80-90 = akceptowalna
- <80 = duża zmienność (uwaga!)

**Znaczenie:**

- Wysoka zmienność może wskazywać na problemy
- W środowisku produkcyjnym ważna jest przewidywalność
- Algorytmy PQC zwykle bardziej konsekwentne niż RSA

**Outliers:**

- Pomiary znacząco odbiegające od normy
- Mogą wskazywać na:
  - Obciążenie systemu podczas testu
  - Problemy z implementacją
  - Garbage collection (Python)

### Zakładka: Analysis

**Classical Algorithms Analysis:**

- Podsumowanie wyników klasycznych
- Best performers
- Insights i zalecenia

**Post-Quantum Analysis:**

- Podsumowanie PQC
- Kategorie (KEM vs Signatures)
- Status NIST

**Classic vs PQC Comparison:**

- Bezpośrednie porównanie średnich
- Trade-offs każdej rodziny
- Advantages i Disadvantages

**Kluczowe wnioski:**

✅ **PQC Advantages:**

- Quantum-resistant
- Kyber/Dilithium są bardzo wydajne
- NIST standardization complete

⚠️ **PQC Disadvantages:**

- Większe klucze i podpisy (2-50x)
- Mniej dojrzałe implementacje
- Ograniczone wsparcie hardware

### Zakładka: Recommendations

**Use Case Selection:**
Wybierz swój przypadek użycia, otrzymasz konkretne zalecenia

**Hybrid Mode:**

- Zalecany podczas migracji (2024-2027)
- Używa BOTH classic AND PQC
- Jeśli jeden zostanie złamany, drugi chroni

**Migration Strategy:**

- **Faza 1 (2024-2025):** Ocena i planowanie
- **Faza 2 (2025-2027):** Wdrożenie hybrid
- **Faza 3 (2027-2030):** Stopniowe przechodzenie na pełny PQC
- **Faza 4 (2030+):** Full PQC deployment

---

## Eksport wyników

### Format CSV

**Kiedy używać:**

- Analiza w Excel/Google Sheets
- Import do innych narzędzi
- Proste archiwum wyników

**Zawartość:**

- Wszystkie kolumny DataFrame
- Łatwy do filtrowania i sortowania

### Format JSON

**Kiedy używać:**

- Integracja z innymi systemami
- Programatyczna analiza
- Długoterminowe archiwum

**Zawartość:**

- Wyniki + metadata
- System info (CPU, OS)
- Konfiguracja testu
- Timestamp

**Przykład struktury:**

```json
{
  "timestamp": "2026-01-07T10:30:00",
  "metadata": {
    "version": "1.0",
    "benchmark_config": {
      "mode": "Hybrid Encryption",
      "iterations": 20,
      "payload_size": 102400
    },
    "system_info": {
      "platform": "Darwin",
      "cpu_brand": "Apple M1",
      "architecture": "arm64"
    }
  },
  "results": [
    {
      "Algorithm": "Kyber768",
      "Total Time (ms)": 2.45,
      ...
    }
  ]
}
```

### Format PDF

**Kiedy używać:**

- Prezentacje dla stakeholders
- Dokumentacja projektów
- Archiwum czytelne dla ludzi

**Zawartość:**

- Executive Summary
- Results Table (top 20)
- Analysis and Recommendations
- Metadata

**Przykładowa struktura:**

1. Strona tytułowa z datą
2. Executive Summary
3. Tabela wyników
4. Analiza i wnioski
5. Rekomendacje

### Export All Formats

Wygeneruje wszystkie 3 formaty jednocześnie:

- `benchmark_results.csv`
- `benchmark_results.json`
- `benchmark_report.pdf`

Zalecane dla kompletnej dokumentacji projektu.

---

## Najlepsze praktyki

### Przed testem

1. **Zamknij inne aplikacje** - aby uniknąć zakłóceń
2. **Stabilne środowisko** - nie przeprowadzaj testów na przeciążonym systemie
3. **Wybierz odpowiednią liczbę iteracji** - minimum 20 dla wiarygodnych statystyk
4. **Zacznij od małych testów** - przetestuj na 1-2 algorytmach, potem rozszerz

### Podczas testu

1. **Nie przerywaj testów** - poczekaj aż się zakończą
2. **Obserwuj Consistency Score** - jeśli <80, może być problem
3. **Dokumentuj konfigurację** - zapisz parametry testów

### Po teście

1. **Zapisz wyniki** - wyeksportuj przed uruchomieniem nowego testu
2. **Porównaj z baseline** - ustal baseline (np. RSA-2048) i porównuj
3. **Sprawdź outliers** - jeśli jest dużo outlierów, powtórz test
4. **Analizuj kontekst** - nie tylko liczby, ale też use case

### Porównywanie wyników

**Między uruchomieniami:**

- Używaj tego samego sprzętu
- Ta sama liczba iteracji
- Te same algorytmy

**Między systemami:**

- Zanotuj różnice w CPU/OS
- Normalizuj do baseline
- Uwzględnij różnice w implementacji

### Interpretacja różnic

**Różnica <10%:**

- Prawdopodobnie noise, nieistotna statystycznie

**Różnica 10-50%:**

- Zauważalna, ale może być przez różnice w systemie

**Różnica >50%:**

- Znacząca różnica
- Sprawdź przyczynę (inny CPU? optymalizacje?)

---

## Rozwiązywanie problemów

### Problem: "liboqs not available"

**Przyczyna:** Brak biblioteki liboqs

**Rozwiązanie Docker:**

```bash
# Upewnij się że build się zakończył prawidłowo
docker build -t pqc-benchmark:latest . --no-cache
```

**Rozwiązanie lokalne:**

```bash
# Sprawdź czy liboqs jest zainstalowana
ldconfig -p | grep liboqs

# Jeśli nie ma, zainstaluj ponownie
# (patrz sekcja Instalacja)
```

### Problem: Test trwa bardzo długo

**Przyczyny:**

- Za dużo iteracji
- Za duży plik w hybrid encryption
- Algorytm SPHINCS+ (naturalnie wolny)

**Rozwiązanie:**

- Zmniejsz iteracje do 10-20
- Zmniejsz rozmiar pliku
- Wyklucz SPHINCS+ z szybkich testów

### Problem: Wysokie odchylenie standardowe

**Przyczyny:**

- Obciążenie systemu
- Za mała liczba iteracji
- Garbage collection Python

**Rozwiązanie:**

- Zamknij inne aplikacje
- Zwiększ iteracje do 50+
- Uruchom test ponownie

### Problem: Wyniki różnią się od oczekiwanych

**Sprawdź:**

- Typ CPU (ARM vs x86 mają duże różnice)
- Dostępne instrukcje (AVX2, AVX-512)
- System operacyjny
- Wersja liboqs

**Normalizacja:**

- Porównuj względem RSA-2048 jako baseline
- Używaj "speedup" zamiast absolutnych wartości

### Problem: Export PDF nie działa

**Przyczyna:** Brak biblioteki fpdf2

**Rozwiązanie:**

```bash
pip install fpdf2
```

### Problem: Brak niektórych algorytmów PQC

**Przyczyna:** liboqs został zbudowany bez tych algorytmów

**Rozwiązanie:**

```bash
# Rebuild liboqs z wszystkimi algorytmami
cmake -DOQS_ENABLE_KEM_<alg>=ON ...
```

---

## FAQ

### Q: Który algorytm PQC powinienem używać?

**A:** Dla większości zastosowań:

- **KEM:** ML-KEM-768 (Kyber768) - NIST standardized
- **Signature:** ML-DSA-65 (Dilithium3) - NIST standardized

### Q: Czy powinienem już teraz przejść na PQC?

**A:** Zalecany plan:

- **2024-2025:** Testowanie i planowanie
- **2025-2027:** Hybrid mode (Classic + PQC)
- **2027-2030:** Stopniowe przejście na pełny PQC

### Q: Czy PQC jest gotowe do produkcji?

**A:**

- ✅ NIST standardization zakończona (2024)
- ✅ Implementacje dostępne (liboqs, BoringSSL, etc.)
- ⚠️ Wsparcie hardware nadal się rozwija
- ✅ Zalecane: hybrid mode podczas przejścia

### Q: Jak duży jest overhead PQC?

**A:**

- **Czas:** Kyber/Dilithium często SZYBSZE niż RSA
- **Rozmiar:** 2-20x większe klucze/podpisy
- **Sieć:** Dla typowych aplikacji overhead <1% przepustowości

### Q: Co to jest "hybrid mode"?

**A:** Użycie BOTH klasycznego i PQC algorytmu jednocześnie:

```
Hybrid = Classic_KEM + PQC_KEM
Benefit: Bezpieczny nawet jeśli jeden algorytm zostanie złamany
```

### Q: Czy mogę zaufać wynikom z tego narzędzia?

**A:**

- ✅ Używa oficjalnych implementacji (liboqs)
- ✅ Pomiary z time.perf_counter() (precyzyjny)
- ⚠️ Benchmark to nie produkcja - różne warunki
- ✅ Użyteczne do porównań względnych

### Q: Jak często powinienem testować?

**A:**

- Po zmianach w infrastrukturze
- Przed wdrożeniem nowych algorytmów
- Co 6-12 miesięcy (nowe wersje liboqs)
- Po aktualizacjach systemu operacyjnego

---

## Zasoby dodatkowe

### Oficjalna dokumentacja

- **NIST PQC:** https://csrc.nist.gov/projects/post-quantum-cryptography
- **liboqs:** https://github.com/open-quantum-safe/liboqs
- **Open Quantum Safe:** https://openquantumsafe.org/

### Standardy i RFC

- **FIPS 203 (ML-KEM):** https://csrc.nist.gov/pubs/fips/203/final
- **FIPS 204 (ML-DSA):** https://csrc.nist.gov/pubs/fips/204/final
- **FIPS 205 (SLH-DSA):** https://csrc.nist.gov/pubs/fips/205/final

### Narzędzia i biblioteki

- **liboqs-python:** https://github.com/open-quantum-safe/liboqs-python
- **OQS-OpenSSL:** https://github.com/open-quantum-safe/openssl
- **PQClean:** https://github.com/PQClean/PQClean

### Społeczność

- **PQC Forum:** https://groups.google.com/a/list.nist.gov/g/pqc-forum
- **GitHub Issues:** https://github.com/open-quantum-safe/liboqs/issues

---

## Słownik pojęć

**KEM (Key Encapsulation Mechanism):**
Mechanizm bezpiecznego ustanawiania wspólnego klucza symetrycznego.

**Hybrid Encryption:**
Połączenie KEM (dla wymiany klucza) + AES (dla danych).

**NIST PQC:**
Program NIST do standaryzacji algorytmów postkwantowych.

**Security Level:**

- Level 1: równoważny AES-128
- Level 3: równoważny AES-192
- Level 5: równoważny AES-256

**Lattice-based:**
Algorytmy oparte na problemach kratowych (Kyber, Dilithium).

**Code-based:**
Algorytmy oparte na kodach korekcji błędów (BIKE, HQC).

**Hash-based:**
Algorytmy oparte na funkcjach haszujących (SPHINCS+).

**Stateless signatures:**
Podpisy nie wymagające zapamiętywania stanu (SPHINCS+).

**Encapsulation:**
Proces tworzenia wspólnego sekretu w KEM.

**Decapsulation:**
Proces odzyskiwania wspólnego sekretu w KEM.

---

## Kontakt i wsparcie

**Problemy z narzędziem:**

- GitHub Issues: [link do repo]

**Pytania ogólne o PQC:**

- Open Quantum Safe community
- NIST PQC forum

**Wkład w projekt:**

- Pull requests welcome!
- Sugestie ulepszeń w Issues

---

**Wersja dokumentacji:** 2.0  
**Data:** 7 stycznia 2026  
**Autor:** PQC Benchmark Tool Team
