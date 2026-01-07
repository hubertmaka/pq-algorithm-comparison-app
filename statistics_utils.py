"""
Statistical utilities for benchmarking analysis.
Provides comprehensive statistical metrics for performance evaluation.
"""

import numpy as np
import pandas as pd


def compute_statistics(measurements):
    """
    Compute comprehensive statistics from a list of measurements.
    
    Args:
        measurements: List or array of numerical measurements
        
    Returns:
        Dictionary with statistical metrics
    """
    if not measurements or len(measurements) == 0:
        return {
            "mean": 0, "median": 0, "std": 0, "min": 0, "max": 0,
            "p25": 0, "p75": 0, "p95": 0, "p99": 0, "cv": 0, "iqr": 0
        }
    
    arr = np.array(measurements)
    mean_val = np.mean(arr)
    
    return {
        "mean": float(mean_val),
        "median": float(np.median(arr)),
        "std": float(np.std(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "p25": float(np.percentile(arr, 25)),
        "p75": float(np.percentile(arr, 75)),
        "p95": float(np.percentile(arr, 95)),
        "p99": float(np.percentile(arr, 99)),
        "cv": float(np.std(arr) / mean_val) if mean_val > 0 else 0,  # Coefficient of variation
        "iqr": float(np.percentile(arr, 75) - np.percentile(arr, 25))  # Interquartile range
    }


def create_statistics_dataframe(results_dict):
    """
    Create a detailed statistics DataFrame from raw measurement data.
    
    Args:
        results_dict: Dictionary with algorithm names as keys and 
                     measurement dictionaries as values
                     
    Returns:
        pandas DataFrame with statistical summaries
    """
    stats_data = []
    
    for algo_name, measurements in results_dict.items():
        for metric_name, values in measurements.items():
            if isinstance(values, list) and len(values) > 0:
                stats = compute_statistics(values)
                stats['Algorithm'] = algo_name
                stats['Metric'] = metric_name
                stats_data.append(stats)
    
    return pd.DataFrame(stats_data)


def compare_algorithms(df, metric_col, group_by='Family'):
    """
    Compare algorithms based on a specific metric.
    
    Args:
        df: DataFrame with benchmark results
        metric_col: Column name to compare (e.g., 'Total Time (ms)')
        group_by: Column to group by (e.g., 'Family')
        
    Returns:
        DataFrame with comparison statistics
    """
    comparison = df.groupby(group_by)[metric_col].agg([
        ('Mean', 'mean'),
        ('Median', 'median'),
        ('Std Dev', 'std'),
        ('Min', 'min'),
        ('Max', 'max'),
        ('Count', 'count')
    ]).round(3)
    
    return comparison


def identify_best_performers(df, metrics, higher_is_better=False):
    """
    Identify best performing algorithms for given metrics.
    
    Args:
        df: DataFrame with benchmark results
        metrics: List of metric column names
        higher_is_better: If True, higher values are better
        
    Returns:
        Dictionary with best performers for each metric
    """
    best_performers = {}
    
    for metric in metrics:
        if metric not in df.columns:
            continue
            
        if higher_is_better:
            best_idx = df[metric].idxmax()
        else:
            best_idx = df[metric].idxmin()
        
        best_performers[metric] = {
            'Algorithm': df.loc[best_idx, 'Algorithm'],
            'Value': df.loc[best_idx, metric],
            'Family': df.loc[best_idx, 'Family'] if 'Family' in df.columns else 'Unknown'
        }
    
    return best_performers


def calculate_speedup(df, baseline_algo, metric_col):
    """
    Calculate speedup compared to baseline algorithm.
    
    Args:
        df: DataFrame with benchmark results
        baseline_algo: Name of baseline algorithm
        metric_col: Column name for comparison
        
    Returns:
        DataFrame with speedup calculations
    """
    baseline_value = df[df['Algorithm'] == baseline_algo][metric_col].values
    
    if len(baseline_value) == 0:
        return df
    
    baseline_value = baseline_value[0]
    df = df.copy()
    df[f'{metric_col} Speedup'] = baseline_value / df[metric_col]
    df[f'{metric_col} % Difference'] = ((df[metric_col] - baseline_value) / baseline_value) * 100
    
    return df


def calculate_efficiency_score(df, time_col, size_col, weight_time=0.5, weight_size=0.5):
    """
    Calculate efficiency score balancing time and size.
    Lower score is better.
    
    Args:
        df: DataFrame with benchmark results
        time_col: Column name for time metric
        size_col: Column name for size metric
        weight_time: Weight for time (0-1)
        weight_size: Weight for size (0-1)
        
    Returns:
        DataFrame with efficiency score
    """
    df = df.copy()
    
    # Normalize to 0-1 range
    time_normalized = (df[time_col] - df[time_col].min()) / (df[time_col].max() - df[time_col].min())
    size_normalized = (df[size_col] - df[size_col].min()) / (df[size_col].max() - df[size_col].min())
    
    df['Efficiency Score'] = (weight_time * time_normalized + weight_size * size_normalized) * 100
    
    return df


def generate_summary_statistics(df):
    """
    Generate comprehensive summary statistics for all numeric columns.
    
    Args:
        df: DataFrame with benchmark results
        
    Returns:
        DataFrame with summary statistics
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    summary = df[numeric_cols].describe(percentiles=[.25, .50, .75, .95, .99])
    
    return summary


def detect_outliers(measurements, method='iqr', threshold=1.5):
    """
    Detect outliers in measurements using IQR or Z-score method.
    
    Args:
        measurements: List or array of measurements
        method: 'iqr' or 'zscore'
        threshold: Threshold for outlier detection
        
    Returns:
        Dictionary with outlier information
    """
    arr = np.array(measurements)
    
    if method == 'iqr':
        q1 = np.percentile(arr, 25)
        q3 = np.percentile(arr, 75)
        iqr = q3 - q1
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        outliers = arr[(arr < lower_bound) | (arr > upper_bound)]
    else:  # zscore
        mean = np.mean(arr)
        std = np.std(arr)
        z_scores = np.abs((arr - mean) / std) if std > 0 else np.zeros_like(arr)
        outliers = arr[z_scores > threshold]
    
    return {
        'count': len(outliers),
        'values': outliers.tolist(),
        'percentage': (len(outliers) / len(arr)) * 100 if len(arr) > 0 else 0
    }


def calculate_consistency_score(measurements):
    """
    Calculate consistency score based on coefficient of variation.
    Score: 100 = perfectly consistent, 0 = highly variable
    
    Args:
        measurements: List or array of measurements
        
    Returns:
        Consistency score (0-100)
    """
    cv = compute_statistics(measurements)['cv']
    # Convert CV to consistency score (lower CV = higher consistency)
    consistency = max(0, 100 - (cv * 100))
    return round(consistency, 2)
