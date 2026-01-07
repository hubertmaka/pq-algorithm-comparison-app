"""
Export utilities for benchmark results.
Supports CSV, JSON, and PDF report generation.
"""

import json
import os
from datetime import datetime
import pandas as pd


def export_to_csv(df, filename="benchmark_results.csv"):
    """
    Export DataFrame to CSV file.
    
    Args:
        df: pandas DataFrame with results
        filename: Output filename
        
    Returns:
        Path to exported file
    """
    filepath = filename
    df.to_csv(filepath, index=False)
    return filepath


def export_to_json(df, metadata=None, filename="benchmark_results.json"):
    """
    Export DataFrame to JSON with metadata.
    
    Args:
        df: pandas DataFrame with results
        metadata: Optional dictionary with additional metadata
        filename: Output filename
        
    Returns:
        Path to exported file
    """
    export_data = {
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {},
        "results": df.to_dict('records')
    }
    
    filepath = filename
    with open(filepath, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    return filepath


def export_to_pdf(df, title="Cryptographic Benchmark Report", filename="benchmark_report.pdf", 
                  charts_data=None, analysis_text=None):
    """
    Generate PDF report with results, charts, and analysis.
    
    Args:
        df: pandas DataFrame with results
        title: Report title
        filename: Output filename
        charts_data: Optional list of chart image paths
        analysis_text: Optional analysis and recommendations text
        
    Returns:
        Path to exported PDF file
    """
    try:
        from fpdf import FPDF
        
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 10, txt=title, ln=True, align='C')
        pdf.ln(5)
        
        # Metadata
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 6, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(0, 6, txt=f"Total Algorithms Tested: {len(df)}", ln=True)
        pdf.ln(5)
        
        # Executive Summary
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, txt="Executive Summary", ln=True)
        pdf.set_font("Arial", '', 10)
        
        if 'Family' in df.columns:
            classic_count = len(df[df['Family'] == 'Classic'])
            pqc_count = len(df[df['Family'] == 'Post-Quantum'])
            pdf.cell(0, 6, txt=f"- Classic Algorithms: {classic_count}", ln=True)
            pdf.cell(0, 6, txt=f"- Post-Quantum Algorithms: {pqc_count}", ln=True)
        
        pdf.ln(5)
        
        # Results Table
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, txt="Benchmark Results", ln=True)
        pdf.set_font("Arial", '', 8)
        
        # Table headers
        col_widths = [50, 35, 35, 35, 35]
        headers = ['Algorithm', 'KeyGen (ms)', 'Total Time (ms)', 'Total BW (B)', 'Family']
        
        pdf.set_fill_color(200, 220, 255)
        for i, header in enumerate(headers):
            if i < len(col_widths):
                pdf.cell(col_widths[i], 6, txt=header, border=1, fill=True)
        pdf.ln()
        
        # Table rows
        for _, row in df.head(20).iterrows():  # Limit to first 20 rows
            pdf.cell(col_widths[0], 6, txt=str(row.get('Algorithm', ''))[:25], border=1)
            pdf.cell(col_widths[1], 6, txt=f"{row.get('KeyGen (ms)', 0):.2f}", border=1)
            pdf.cell(col_widths[2], 6, txt=f"{row.get('Total Time (ms)', 0):.2f}", border=1)
            pdf.cell(col_widths[3], 6, txt=str(int(row.get('Total Bandwidth (B)', 0))), border=1)
            pdf.cell(col_widths[4], 6, txt=str(row.get('Family', ''))[:15], border=1)
            pdf.ln()
        
        if len(df) > 20:
            pdf.ln(2)
            pdf.set_font("Arial", 'I', 8)
            pdf.cell(0, 6, txt=f"... and {len(df) - 20} more algorithms", ln=True)
        
        pdf.ln(10)
        
        # Analysis section
        if analysis_text:
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, txt="Analysis and Recommendations", ln=True)
            pdf.set_font("Arial", '', 10)
            
            # Split text into lines to avoid overflow
            lines = analysis_text.split('\n')
            for line in lines:
                # Handle long lines
                if len(line) > 90:
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line + word) < 90:
                            current_line += word + " "
                        else:
                            pdf.multi_cell(0, 6, txt=current_line.strip())
                            current_line = word + " "
                    if current_line:
                        pdf.multi_cell(0, 6, txt=current_line.strip())
                else:
                    pdf.cell(0, 6, txt=line, ln=True)
        
        # Footer
        pdf.ln(10)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 6, txt="Generated by PQC Benchmark Tool | https://github.com/open-quantum-safe", ln=True, align='C')
        
        # Save PDF
        filepath = filename
        pdf.output(filepath)
        
        return filepath
        
    except ImportError:
        print("Warning: fpdf not installed. Install with: pip install fpdf2")
        return None
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None


def create_metadata(config_dict, system_info=None):
    """
    Create metadata dictionary for export.
    
    Args:
        config_dict: Dictionary with benchmark configuration
        system_info: Optional system information
        
    Returns:
        Metadata dictionary
    """
    metadata = {
        "version": "1.0",
        "benchmark_config": config_dict,
        "timestamp": datetime.now().isoformat(),
    }
    
    if system_info:
        metadata["system_info"] = system_info
    
    return metadata


def export_all_formats(df, base_filename="benchmark", metadata=None, analysis_text=None):
    """
    Export results in all available formats.
    
    Args:
        df: pandas DataFrame with results
        base_filename: Base filename (without extension)
        metadata: Optional metadata dictionary
        analysis_text: Optional analysis text for PDF
        
    Returns:
        Dictionary with paths to exported files
    """
    exported = {}
    
    # CSV
    try:
        csv_path = export_to_csv(df, f"{base_filename}.csv")
        exported['csv'] = csv_path
    except Exception as e:
        print(f"CSV export failed: {e}")
    
    # JSON
    try:
        json_path = export_to_json(df, metadata, f"{base_filename}.json")
        exported['json'] = json_path
    except Exception as e:
        print(f"JSON export failed: {e}")
    
    # PDF
    try:
        pdf_path = export_to_pdf(df, filename=f"{base_filename}.pdf", analysis_text=analysis_text)
        if pdf_path:
            exported['pdf'] = pdf_path
    except Exception as e:
        print(f"PDF export failed: {e}")
    
    return exported


def get_system_info():
    """
    Collect system information for metadata.
    
    Returns:
        Dictionary with system information
    """
    import platform
    
    info = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }
    
    try:
        import cpuinfo
        cpu = cpuinfo.get_cpu_info()
        info["cpu_brand"] = cpu.get('brand_raw', 'Unknown')
        info["cpu_arch"] = cpu.get('arch', 'Unknown')
        info["cpu_bits"] = cpu.get('bits', 'Unknown')
        info["cpu_count"] = cpu.get('count', 'Unknown')
    except ImportError:
        pass
    
    return info
