import os
import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List

class MCPDataServer:
    def __init__(self):
        self.data_cache = {}
        self.current_df = None
        
    def load_csv(self, file_path: str) -> Dict[str, Any]:
        """加载CSV文件并返回基本统计信息"""
        try:
            df = pd.read_csv(file_path)
            self.current_df = df
            
            stats = {
                "rows": len(df),
                "columns": list(df.columns),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "summary": df.describe().to_dict()
            }
            
            return {"status": "success", "stats": stats}
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    def run_analysis(self, script: str) -> Dict[str, Any]:
        """运行自定义分析脚本"""
        if self.current_df is None:
            return {"status": "error", "message": "No data loaded"}
            
        try:
            # 创建本地变量供脚本使用
            df = self.current_df
            result = {}
            
            # 执行脚本
            exec(script, globals(), locals())
            
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    def get_visualization(self, plot_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """生成数据可视化"""
        if self.current_df is None:
            return {"status": "error", "message": "No data loaded"}
            
        try:
            import plotly.express as px
            
            df = self.current_df
            fig = None
            
            if plot_type == "scatter":
                fig = px.scatter(df, **params)
            elif plot_type == "line":
                fig = px.line(df, **params)
            elif plot_type == "bar":
                fig = px.bar(df, **params)
            else:
                return {"status": "error", "message": f"Unsupported plot type: {plot_type}"}
                
            return {"status": "success", "plot": fig.to_json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

def main():
    server = MCPDataServer()
    # 这里可以添加服务器启动代码
    print("MCP Data Analysis Server is running...")
    
if __name__ == "__main__":
    main() 