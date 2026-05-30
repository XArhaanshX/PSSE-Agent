import pandas as pd
import numpy as np
from typing import List, Dict, Any

def load_workbook(file_path: str) -> List[Dict[str, Any]]:
    """
    Step 1: Load the Excel or CSV workbook.
    Step 2: Normalize all NaNs/empty cells to None at the boundary.
    Step 3: Return clean deterministic rows.
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Must be .xlsx or .csv")

    # Drop completely empty rows
    df.dropna(how='all', inplace=True)
    
    # Strip whitespace from string columns and normalize empty strings
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.replace({'': None})
    
    # Replace pandas NA/NaN with Python None for boundary-level normalization
    df = df.replace({np.nan: None})
    
    # Convert to list of dicts
    return df.to_dict(orient="records")
