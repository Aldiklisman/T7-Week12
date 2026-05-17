import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'supermarket_sales_sample.csv'


def load_data(path: str | Path = None) -> pd.DataFrame:
    p = Path(path) if path else DATA_PATH
    df = pd.read_csv(p)
    # basic cleaning: coerce numeric columns
    # support both 'Sales' and 'Total' naming conventions
    for col in ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'Sales', 'Rating']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # If dataset uses 'Sales' instead of 'Total', create a 'Total' column for compatibility
    if 'Total' not in df.columns and 'Sales' in df.columns:
        df['Total'] = df['Sales']

    return df
