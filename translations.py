"""
Internationalization support for PQC Benchmark Tool
Supported languages: English (en), Polish (pl)
"""

TRANSLATIONS = {
    "en": {
        # General
        "title": "Post-Quantum vs Classical Cryptography Benchmark",
        "subtitle": "Comprehensive performance analysis and comparison tool",
        "system": "System",
        "version": "Version 2.0",
        
        # Sidebar
        "configuration": "Configuration",
        "test_scenario": "Test Scenario",
        "select_scenario": "Select the type of cryptographic operation to benchmark",
        "message_config": "Message Configuration",
        "message_source": "Message Source",
        "message_size_kb": "Message Size (KB):",
        "file_source": "File Source",
        "file_size_kb": "File Size (KB):",
        "upload_file_sign": "Upload file to sign:",
        "upload_file_encrypt": "Upload file to encrypt:",
        "random_generated": "Random Generated",
        "upload_file": "Upload File",
        "no_file_uploaded": "No file uploaded, using default",
        "generated": "Generated",
        "loaded": "Loaded",
        
        # Modes
        "mode_kem": "KEM (Key Exchange Only)",
        "mode_signatures": "Digital Signatures",
        "mode_hybrid": "Hybrid Encryption (KEM+AES)",
        "mode_scenarios": "Real-World Scenarios",
        
        # Mode descriptions
        "mode_kem_desc": "**Pure KEM Mode**\n\nTests key encapsulation/decapsulation only (32-byte shared secret). No actual data encryption.",
        "mode_hybrid_desc": "**Hybrid Encryption**\n\nCombines KEM for key exchange with AES-256-GCM for data encryption. Tests real file encryption scenario.",
        "mode_scenarios_desc": "**Scenario Simulation**\n\nSimulates real-world cryptographic applications like TLS handshake, secure email, VPN, etc.",
        
        # Scenarios
        "scenario_tls": "TLS 1.3 Handshake",
        "scenario_email": "Secure Email (S/MIME)",
        "scenario_vpn": "VPN Session",
        "scenario_code": "Code Signing",
        "email_size": "Email Size (KB):",
        "file_size_mb": "File Size (MB):",
        
        # Algorithm Selection
        "algo_selection": "Algorithm Selection",
        "iterations": "Iterations (for statistics):",
        "iterations_help": "More iterations = better statistical accuracy",
        "classic_kem": "Classic KEM:",
        "pqc_kem": "PQC KEM:",
        "classic_sig": "Classic Signatures:",
        "pqc_sig": "PQC Signatures:",
        "rsa_sizes": "RSA Key Sizes:",
        "ecc_curves": "ECC Curves:",
        "pqc_kems": "PQC KEMs:",
        "pqc_signatures": "PQC Signatures:",
        
        # Buttons
        "run_benchmark": "Run Comprehensive Benchmark",
        
        # Progress
        "running_benchmarks": "Running Benchmarks...",
        "testing": "Testing",
        "benchmark_complete": "Benchmark complete!",
        "benchmark_success": "Successfully benchmarked",
        "algo_configs": "algorithm configurations!",
        
        # Errors
        "error_liboqs": "Error: liboqs python wrapper not found. Please install proper dependencies.",
        "error_liboqs_help": "For Docker: ensure you've built with liboqs support. For local: install liboqs-python.",
        "error_select_algos": "Please select at least one algorithm to test.",
        "error_select_kem_sig": "Please select at least one KEM and one Signature algorithm for scenario testing.",
        "error_no_results": "No successful benchmark results. Please check algorithm availability.",
        "failed_to_test": "Failed to test",
        "failed_to_benchmark": "Failed to benchmark",
        
        # Tab names
        "tab_performance": "Performance",
        "tab_size": "Size Analysis",
        "tab_tradeoff": "Trade-off",
        "tab_statistics": "Statistics",
        "tab_analysis": "Analysis",
        "tab_recommendations": "Recommendations",
        "tab_export": "Export",
        "tab_results": "Results Table",
        "tab_perf_analysis": "Performance Analysis",
        
        # Performance tab
        "performance_metrics": "Performance Metrics",
        "perf_caption": "Time measurements for all cryptographic operations (lower is better)",
        "exec_time_breakdown": "Execution Time Breakdown",
        "summary_table": "Summary Table",
        "no_perf_data": "No performance data available for visualization",
        "no_size_data": "No size data available for visualization",
        "artifact": "Artifact",
        "size_bytes": "Size (Bytes)",
        
        # Size tab
        "crypto_sizes": "Cryptographic Artifact Sizes",
        "sizes_caption": "Key and ciphertext/signature sizes (lower is better, log scale)",
        "key_output_sizes": "Key and Output Sizes (Logarithmic Scale)",
        "size_comparison": "Size Comparison",
        
        # Trade-off tab
        "tradeoff_title": "Performance vs Size Trade-off",
        "tradeoff_caption": "Ideal algorithms are in the bottom-left (fast AND small)",
        "efficiency_frontier": "Efficiency Frontier: Speed vs Bandwidth",
        "median_time": "Median Time",
        "median_size": "Median Size",
        "efficiency_rankings": "Efficiency Rankings",
        "efficiency_caption": "Lower score = better overall efficiency (balanced time and size)",
        
        # Statistics tab
        "detailed_stats": "Detailed Statistical Analysis",
        "consistency_scores": "Consistency Scores",
        "consistency_scores_title": "Consistency Scores",
        "algo_consistency_title": "Algorithm Consistency",
        "consistency_caption": "Score of 100 = perfectly consistent, <80 = high variance",
        "algo_consistency": "Algorithm Consistency",
        "acceptable_threshold": "Acceptable threshold",
        "statistical_summary": "Statistical Summary",
        "outlier_analysis": "Outlier Analysis",
        "no_outliers": "No significant outliers detected in measurements",
        "algorithm": "Algorithm",
        "metric": "Metric",
        "outliers": "Outliers",
        "percentage": "Percentage",
        
        # Analysis tab
        "comparative_analysis": "Comparative Analysis",
        "classic_algos": "Classical Algorithms",
        "pqc_algos": "Post-Quantum Algorithms",
        "fastest_classic": "Fastest Classic",
        "fastest_pqc": "Fastest PQC",
        "average_time": "Average Time",
        "smallest_classic": "Smallest Classic",
        "smallest_pqc": "Smallest PQC",
        "nist_standardized": "NIST Standardized:",
        "classic_vs_pqc": "Classic vs PQC Head-to-Head",
        "performance": "Performance",
        "bandwidth": "Bandwidth",
        "classic_average": "Classic Average",
        "pqc_average": "PQC Average",
        "analysis": "Analysis",
        "observation": "Observation",
        "recommendation": "Recommendation",
        
        # Recommendations tab
        "recommendations_title": "Recommendations and Best Practices",
        "select_use_case": "Select your use case:",
        "recommended_algos": "Recommended Algorithms",
        "classical": "Classical:",
        "post_quantum": "Post-Quantum:",
        "category": "Category",
        "hybrid": "Hybrid:",
        "best_performers": "Best Performers (From Your Tests)",
        "fastest": "Fastest:",
        "smallest": "Smallest:",
        "time": "Time",
        "recommended": "Recommended",
        "migration_strategy": "Migration Strategy",
        "recommended_timeline": "Recommended Timeline:",
        
        # Use cases
        "usecase_general": "General Purpose",
        "usecase_iot": "IoT/Embedded",
        "usecase_server": "High-Throughput Server",
        "usecase_mobile": "Mobile Applications",
        "usecase_security": "High Security / Long-Term",
        
        # Export tab
        "export_results": "Export Results",
        "export_csv": "Export CSV",
        "export_json": "Export JSON",
        "export_pdf": "Generate PDF Report",
        "export_all": "Export All Formats",
        "download_csv": "Download CSV",
        "download_json": "Download JSON",
        "download_pdf": "Download PDF Report",
        "csv_ready": "CSV ready for download!",
        "json_ready": "JSON ready for download!",
        "pdf_ready": "PDF report generated!",
        "export_failed": "Export failed:",
        "pdf_gen_failed": "PDF generation failed:",
        "exported_formats": "Exported",
        "formats": "formats:",
        "generating_exports": "Generating exports...",
        
        # Welcome screen
        "welcome": "Welcome to the PQC Benchmark Tool",
        "what_does": "What does this tool do?",
        "what_desc": """This comprehensive benchmarking tool allows you to:

- **Compare** classical (RSA, ECDSA) and post-quantum cryptographic algorithms
- **Measure** performance metrics: key generation, encryption/signing, decryption/verification
- **Analyze** trade-offs between speed and bandwidth requirements
- **Simulate** real-world scenarios: TLS handshakes, secure email, VPN sessions
- **Generate** detailed reports with recommendations""",
        "quick_start": "Quick Start:",
        "quick_start_steps": """1. **Select a test scenario** from the sidebar
2. **Choose algorithms** to benchmark
3. **Configure parameters** (iterations, data size)
4. Click **Run Comprehensive Benchmark**
5. **Analyze results** in interactive visualizations
6. **Export** reports in CSV, JSON, or PDF format""",
        "test_scenarios": "Test Scenarios:",
        "test_scenarios_desc": """- **KEM (Key Exchange Only)**: Pure key encapsulation mechanisms
- **Digital Signatures**: Sign and verify operations
- **Hybrid Encryption**: Real file encryption using KEM + AES-256-GCM
- **Real-World Scenarios**: TLS, Email, VPN, Code Signing""",
        "why_pqc": "Why Post-Quantum Crypto?",
        "why_pqc_desc": """Quantum computers threaten current encryption. PQC algorithms are designed to resist quantum attacks.

**NIST Standardization:**
- ML-KEM (Kyber)
- ML-DSA (Dilithium)
- SLH-DSA (SPHINCS+)

**Migration Timeline:**
2024-2030""",
        "available_algos": "Available Algorithms:",
        "available_algos_desc": """**Classic:**
- RSA (2048, 3072, 4096)
- ECDSA (P-256, P-384, P-521)

**Post-Quantum:**
- Kyber/ML-KEM
- Dilithium/ML-DSA
- SPHINCS+/SLH-DSA
- Falcon, BIKE, HQC, and more""",
        "example_title": "Example: What to Expect",
        "example_caption": "Lower left corner = faster and smaller (better). Start benchmarking to see real results!",
        "example_tradeoff": "Example: Performance vs Size Trade-off",
        
        # Footer
        "footer": "PQC Benchmark Tool | Built with Streamlit, liboqs, and cryptography library",
        "documentation": "Documentation",
        
        # Metrics
        "total_time": "Total Time (ms)",
        "total_bandwidth": "Total Bandwidth (B)",
        "consistency_score": "Consistency Score",
        "efficiency_score": "Efficiency Score",
        
        # Metric descriptions
        "metrics_performance_desc": "📊 **Performance Metrics:** Key generation, encapsulation, decapsulation, AES encryption time, and total execution time (lower is better). Color gradient: green=faster, red=slower.",
        "metrics_size_desc": "📦 **Size Metrics:** Public/private key sizes and output sizes (signature/ciphertext). Logarithmic scale for better visualization of differences. Smaller sizes = less bandwidth usage.",
        "metrics_tradeoff_desc": "⚖️ **Trade-off Analysis:** Comparison of total bandwidth (key size + output) vs total execution time. Algorithms in the bottom-left corner are optimal (fast and compact).",
        "metrics_stats_desc": "📈 **Statistical Metrics:** Consistency Score (execution stability, higher=better), StdDev (standard deviation), P95 (95th percentile). Help assess algorithm predictability.",
        "metrics_scenarios_desc": "🌐 **Scenario Metrics:** Real-world use case simulation - TLS handshake, secure email, VPN session, code signing. Shows total time for all operations in a complete scenario.",
        "metrics_summary_table_desc": "📋 **Summary Table:** Contains all partial time measurements and key metrics. Color gradient helps quickly identify the fastest algorithms.",
    },
    
    "pl": {
        # General
        "title": "Benchmark Kryptografii Post-Kwantowej i Klasycznej",
        "subtitle": "Kompleksowe narzędzie do analizy wydajności i porównań",
        "system": "System",
        "version": "Wersja 2.0",
        
        # Sidebar
        "configuration": "Konfiguracja",
        "test_scenario": "Scenariusz testowy",
        "select_scenario": "Wybierz typ operacji kryptograficznej do testowania",
        "message_config": "Konfiguracja wiadomości",
        "message_source": "Źródło wiadomości",
        "message_size_kb": "Rozmiar wiadomości (KB):",
        "file_source": "Źródło pliku",
        "file_size_kb": "Rozmiar pliku (KB):",
        "upload_file_sign": "Wgraj plik do podpisania:",
        "upload_file_encrypt": "Wgraj plik do zaszyfrowania:",
        "random_generated": "Losowo wygenerowany",
        "upload_file": "Wgraj plik",
        "no_file_uploaded": "Nie wgrano pliku, używam domyślnego",
        "generated": "Wygenerowano",
        "loaded": "Wczytano",
        
        # Modes
        "mode_kem": "KEM (tylko wymiana kluczy)",
        "mode_signatures": "Podpisy cyfrowe",
        "mode_hybrid": "Szyfrowanie hybrydowe (KEM+AES)",
        "mode_scenarios": "Scenariusze rzeczywiste",
        
        # Mode descriptions
        "mode_kem_desc": "**Tryb czystego KEM**\n\nTestuje tylko enkapsulację/dekapsulację kluczy (32-bajtowy sekret). Bez faktycznego szyfrowania danych.",
        "mode_hybrid_desc": "**Szyfrowanie hybrydowe**\n\nŁączy KEM do wymiany kluczy z AES-256-GCM do szyfrowania danych. Testuje rzeczywiste szyfrowanie plików.",
        "mode_scenarios_desc": "**Symulacja scenariuszy**\n\nSymuluje rzeczywiste zastosowania kryptograficzne jak handshake TLS, bezpieczny email, VPN, itp.",
        
        # Scenarios
        "scenario_tls": "Handshake TLS 1.3",
        "scenario_email": "Bezpieczny email (S/MIME)",
        "scenario_vpn": "Sesja VPN",
        "scenario_code": "Podpisywanie kodu",
        "email_size": "Rozmiar emaila (KB):",
        "file_size_mb": "Rozmiar pliku (MB):",
        
        # Algorithm Selection
        "algo_selection": "Wybór algorytmów",
        "iterations": "Iteracje (dla statystyk):",
        "iterations_help": "Więcej iteracji = lepsza dokładność statystyczna",
        "classic_kem": "KEM klasyczne:",
        "pqc_kem": "KEM PQC:",
        "classic_sig": "Podpisy klasyczne:",
        "pqc_sig": "Podpisy PQC:",
        "rsa_sizes": "Rozmiary kluczy RSA:",
        "ecc_curves": "Krzywe ECC:",
        "pqc_kems": "KEMs PQC:",
        "pqc_signatures": "Podpisy PQC:",
        
        # Buttons
        "run_benchmark": "Uruchom kompleksowy benchmark",
        
        # Progress
        "running_benchmarks": "Wykonywanie benchmarków...",
        "testing": "Testowanie",
        "benchmark_complete": "Benchmark zakończony!",
        "benchmark_success": "Pomyślnie przetestowano",
        "algo_configs": "konfiguracji algorytmów!",
        
        # Errors
        "error_liboqs": "Błąd: nie znaleziono wrappera liboqs python. Zainstaluj odpowiednie zależności.",
        "error_liboqs_help": "Dla Dockera: upewnij się, że zbudowałeś z obsługą liboqs. Lokalnie: zainstaluj liboqs-python.",
        "error_select_algos": "Wybierz przynajmniej jeden algorytm do testowania.",
        "error_select_kem_sig": "Wybierz przynajmniej jeden algorytm KEM i jeden podpisowy do testowania scenariuszy.",
        "error_no_results": "Brak wyników benchmarku. Sprawdź dostępność algorytmów.",
        "failed_to_test": "Nie udało się przetestować",
        "failed_to_benchmark": "Nie udało się wykonać benchmarku",
        
        # Tab names
        "tab_performance": "Wydajność",
        "tab_size": "Analiza rozmiaru",
        "tab_tradeoff": "Kompromisy",
        "tab_statistics": "Statystyki",
        "tab_analysis": "Analiza",
        "tab_recommendations": "Rekomendacje",
        "tab_export": "Eksport",
        "tab_results": "Tabela wyników",
        "tab_perf_analysis": "Analiza wydajności",
        
        # Performance tab
        "performance_metrics": "Metryki wydajności",
        "perf_caption": "Pomiary czasu dla wszystkich operacji kryptograficznych (niższy lepszy)",
        "exec_time_breakdown": "Rozłożenie czasu wykonania",
        "summary_table": "Tabela podsumowania",
        "no_perf_data": "Brak danych wydajności do wizualizacji",
        "no_size_data": "Brak danych o rozmiarach do wizualizacji",
        "artifact": "Artefakt",
        "size_bytes": "Rozmiar (bajty)",
        
        # Size tab
        "crypto_sizes": "Rozmiary artefaktów kryptograficznych",
        "sizes_caption": "Rozmiary kluczy i szyfrogramów/podpisów (niższy lepszy, skala log)",
        "key_output_sizes": "Rozmiary kluczy i wyjść (skala logarytmiczna)",
        "size_comparison": "Porównanie rozmiarów",
        
        # Trade-off tab
        "tradeoff_title": "Kompromis wydajność vs rozmiar",
        "tradeoff_caption": "Idealne algorytmy są w lewym dolnym rogu (szybkie I małe)",
        "efficiency_frontier": "Granica efektywności: szybkość vs przepustowość",
        "median_time": "Mediana czasu",
        "median_size": "Mediana rozmiaru",
        "efficiency_rankings": "Ranking efektywności",
        "efficiency_caption": "Niższy wynik = lepsza efektywność ogólna (zbalansowany czas i rozmiar)",
        
        # Statistics tab
        "detailed_stats": "Szczegółowa analiza statystyczna",
        "consistency_scores": "Wyniki spójności",
        "consistency_scores_title": "Wyniki spójności",
        "algo_consistency_title": "Spójność algorytmu",
        "consistency_caption": "Wynik 100 = idealnie spójny, <80 = wysoka wariancja",
        "algo_consistency": "Spójność algorytmu",
        "acceptable_threshold": "Akceptowalny próg",
        "statistical_summary": "Podsumowanie statystyczne",
        "outlier_analysis": "Analiza wartości odstających",
        "no_outliers": "Nie wykryto znaczących wartości odstających w pomiarach",        "algorithm": "Algorytm",
        "metric": "Metryka",
        "outliers": "Wartości odstępujące",
        "percentage": "Procent",        
        # Analysis tab
        "comparative_analysis": "Analiza porównawcza",
        "classic_algos": "Algorytmy klasyczne",
        "pqc_algos": "Algorytmy post-kwantowe",
        "fastest_classic": "Najszybszy klasyczny",
        "fastest_pqc": "Najszybszy PQC",
        "average_time": "Średni czas",
        "smallest_classic": "Najmniejszy klasyczny",
        "smallest_pqc": "Najmniejszy PQC",
        "nist_standardized": "Standaryzowane przez NIST:",
        "classic_vs_pqc": "Klasyczne vs PQC - bezpośrednie porównanie",
        "performance": "Wydajność",
        "bandwidth": "Przepustowość",
        "classic_average": "Średnia klasyczna",
        "pqc_average": "Średnia PQC",
        "analysis": "Analiza",
        "observation": "Obserwacja",
        "recommendation": "Rekomendacja",
        
        # Recommendations tab
        "recommendations_title": "Rekomendacje i najlepsze praktyki",
        "select_use_case": "Wybierz przypadek użycia:",
        "recommended_algos": "Rekomendowane algorytmy",
        "classical": "Klasyczne:",
        "post_quantum": "Post-kwantowe:",
        "category": "Kategoria",
        "hybrid": "Hybrydowe:",
        "best_performers": "Najlepsze wyniki (z Twoich testów)",
        "fastest": "Najszybszy:",
        "smallest": "Najmniejszy:",
        "time": "Czas",
        "recommended": "Rekomendowane",
        "migration_strategy": "Strategia migracji",
        "recommended_timeline": "Rekomendowany harmonogram:",
        
        # Use cases
        "usecase_general": "Ogólnego przeznaczenia",
        "usecase_iot": "IoT/Wbudowane",
        "usecase_server": "Serwer wysokiej wydajności",
        "usecase_mobile": "Aplikacje mobilne",
        "usecase_security": "Wysokie bezpieczeństwo / Długoterminowe",
        
        # Export tab
        "export_results": "Eksportuj wyniki",
        "export_csv": "Eksportuj CSV",
        "export_json": "Eksportuj JSON",
        "export_pdf": "Wygeneruj raport PDF",
        "export_all": "Eksportuj wszystkie formaty",
        "download_csv": "Pobierz CSV",
        "download_json": "Pobierz JSON",
        "download_pdf": "Pobierz raport PDF",
        "csv_ready": "CSV gotowy do pobrania!",
        "json_ready": "JSON gotowy do pobrania!",
        "pdf_ready": "Raport PDF wygenerowany!",
        "export_failed": "Eksport nie powiódł się:",
        "pdf_gen_failed": "Generowanie PDF nie powiodło się:",
        "exported_formats": "Wyeksportowano",
        "formats": "formatów:",
        "generating_exports": "Generowanie eksportów...",
        
        # Welcome screen
        "welcome": "Witamy w narzędziu PQC Benchmark",
        "what_does": "Co robi to narzędzie?",
        "what_desc": """To kompleksowe narzędzie benchmarkowe pozwala na:

- **Porównywanie** klasycznych (RSA, ECDSA) i post-kwantowych algorytmów kryptograficznych
- **Mierzenie** metryk wydajności: generowanie kluczy, szyfrowanie/podpisywanie, deszyfrowanie/weryfikacja
- **Analizowanie** kompromisów między szybkością a wymaganiami przepustowości
- **Symulowanie** rzeczywistych scenariuszy: handshaków TLS, bezpiecznych emaili, sesji VPN
- **Generowanie** szczegółowych raportów z rekomendacjami""",
        "quick_start": "Szybki start:",
        "quick_start_steps": """1. **Wybierz scenariusz testowy** z paska bocznego
2. **Wybierz algorytmy** do benchmarku
3. **Skonfiguruj parametry** (iteracje, rozmiar danych)
4. Kliknij **Uruchom kompleksowy benchmark**
5. **Analizuj wyniki** w interaktywnych wizualizacjach
6. **Eksportuj** raporty w formatach CSV, JSON lub PDF""",
        "test_scenarios": "Scenariusze testowe:",
        "test_scenarios_desc": """- **KEM (tylko wymiana kluczy)**: Czyste mechanizmy enkapsulacji kluczy
- **Podpisy cyfrowe**: Operacje podpisywania i weryfikacji
- **Szyfrowanie hybrydowe**: Rzeczywiste szyfrowanie plików używając KEM + AES-256-GCM
- **Scenariusze rzeczywiste**: TLS, Email, VPN, podpisywanie kodu""",
        "why_pqc": "Dlaczego kryptografia post-kwantowa?",
        "why_pqc_desc": """Komputery kwantowe zagrażają obecnemu szyfrowaniu. Algorytmy PQC są zaprojektowane aby oprzeć się atakom kwantowym.

**Standaryzacja NIST:**
- ML-KEM (Kyber)
- ML-DSA (Dilithium)
- SLH-DSA (SPHINCS+)

**Harmonogram migracji:**
2024-2030""",
        "available_algos": "Dostępne algorytmy:",
        "available_algos_desc": """**Klasyczne:**
- RSA (2048, 3072, 4096)
- ECDSA (P-256, P-384, P-521)

**Post-kwantowe:**
- Kyber/ML-KEM
- Dilithium/ML-DSA
- SPHINCS+/SLH-DSA
- Falcon, BIKE, HQC, i więcej""",
        "example_title": "Przykład: Czego się spodziewać",
        "example_caption": "Lewy dolny róg = szybszy i mniejszy (lepszy). Rozpocznij benchmarking aby zobaczyć prawdziwe wyniki!",
        "example_tradeoff": "Przykład: Kompromis wydajność vs rozmiar",
        
        # Footer
        "footer": "Narzędzie PQC Benchmark | Zbudowane z Streamlit, liboqs i biblioteką cryptography",
        "documentation": "Dokumentacja",
        
        # Metrics
        "total_time": "Całkowity czas (ms)",
        "total_bandwidth": "Całkowita przepustowość (B)",
        "consistency_score": "Wynik spójności",
        "efficiency_score": "Wynik efektywności",
        
        # Metric descriptions
        "metrics_performance_desc": "📊 **Metryki wydajności:** Czas generowania klucza, enkapsulacji, dekapsulacji, szyfrowania AES i całkowity czas wykonania (niższe wartości = lepsze). Gradient kolorów: zielony=szybsze, czerwony=wolniejsze.",
        "metrics_size_desc": "📦 **Metryki rozmiaru:** Rozmiary kluczy publicznych/prywatnych oraz wyjściowych (podpis/ciphertext). Skala logarytmiczna dla lepszej wizualizacji różnic. Mniejsze rozmiary = mniejsze zużycie przepustowości.",
        "metrics_tradeoff_desc": "⚖️ **Analiza kompromisów:** Porównanie całkowitej przepustowości (rozmiar klucza + dane wyjściowe) vs całkowitego czasu wykonania. Algorytmy w lewym dolnym rogu są optymalne (szybkie i kompaktowe).",
        "metrics_stats_desc": "📈 **Metryki statystyczne:** Consistency Score (stabilność wykonania, wyższe=lepsze), StdDev (odchylenie standardowe), P95 (95 percentyl). Pomagają ocenić przewidywalność algorytmu.",
        "metrics_scenarios_desc": "🌐 **Metryki scenariuszowe:** Symulacja rzeczywistych przypadków użycia - TLS handshake, bezpieczny email, sesja VPN, podpisywanie kodu. Pokazuje całkowity czas wszystkich operacji w pełnym scenariuszu.",
        "metrics_summary_table_desc": "📋 **Tabela podsumowania:** Zawiera wszystkie cząstkowe pomiary czasu oraz kluczowe metryki. Gradient kolorów pomaga szybko zidentyfikować najszybsze algorytmy.",
    }
}


def get_text(key, lang="en"):
    """Get translated text for a given key."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


def get_all_texts(lang="en"):
    """Get all translations for a given language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"])
