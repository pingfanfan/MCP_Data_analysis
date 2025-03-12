import pandas as pd
import numpy as np
from typing import Dict, Any, List, Union
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def describe_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """生成数据集的详细描述"""
    description = {
        "基本信息": {
            "行数": len(df),
            "列数": len(df.columns),
            "内存使用": f"{df.memory_usage().sum() / 1024**2:.2f} MB"
        },
        "列信息": {},
        "缺失值统计": df.isnull().sum().to_dict(),
        "数值列统计": df.describe().to_dict()
    }
    
    for col in df.columns:
        col_info = {
            "类型": str(df[col].dtype),
            "唯一值数量": df[col].nunique(),
            "缺失值比例": f"{df[col].isnull().mean()*100:.2f}%"
        }
        description["列信息"][col] = col_info
        
    return description

def clean_dataset(df: pd.DataFrame, options: Dict[str, Any]) -> pd.DataFrame:
    """清理数据集"""
    df_clean = df.copy()
    
    if options.get("drop_na", False):
        df_clean = df_clean.dropna()
        
    if options.get("fill_na"):
        fill_value = options["fill_na"]
        df_clean = df_clean.fillna(fill_value)
        
    if options.get("drop_duplicates", False):
        df_clean = df_clean.drop_duplicates()
        
    return df_clean

def feature_engineering(df: pd.DataFrame, features: List[Dict[str, Any]]) -> pd.DataFrame:
    """特征工程"""
    df_new = df.copy()
    
    for feature in features:
        feature_type = feature.get("type")
        if feature_type == "standardize":
            cols = feature.get("columns", [])
            scaler = StandardScaler()
            df_new[cols] = scaler.fit_transform(df_new[cols])
        elif feature_type == "pca":
            cols = feature.get("columns", [])
            n_components = feature.get("n_components", 2)
            pca = PCA(n_components=n_components)
            pca_result = pca.fit_transform(df_new[cols])
            for i in range(n_components):
                df_new[f"PCA_{i+1}"] = pca_result[:, i]
                
    return df_new

def calculate_correlations(df: pd.DataFrame, method: str = "pearson") -> Dict[str, Any]:
    """计算相关性"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr(method=method)
    
    correlations = {
        "matrix": corr_matrix.to_dict(),
        "strong_correlations": []
    }
    
    # 找出强相关性
    for i in range(len(numeric_cols)):
        for j in range(i+1, len(numeric_cols)):
            corr = corr_matrix.iloc[i, j]
            if abs(corr) > 0.7:
                correlations["strong_correlations"].append({
                    "var1": numeric_cols[i],
                    "var2": numeric_cols[j],
                    "correlation": corr
                })
                
    return correlations 