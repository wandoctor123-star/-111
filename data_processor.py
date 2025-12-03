import pandas as pd
import io

REQUIRED_COLUMNS = ['日期', '日报推送', '日报未推送', '手表佩戴', '手表未佩戴']

def load_data(file):
    """
    Loads data from an uploaded Excel file.
    """
    try:
        df = pd.read_excel(file)
        return df
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")

def validate_columns(df):
    """
    Validates that the dataframe contains the required columns.
    Supports both '手表' and '腕表' naming conventions.
    """
    # Normalize column names: replace '腕表' with '手表'
    df.columns = df.columns.str.replace('腕表', '手表')
    
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"表头格式不正确，请确认包含：日期、日报推送、日报未推送、手表佩戴（或腕表佩戴）、手表未佩戴（或腕表未佩戴）五列。缺失: {', '.join(missing_columns)}")
    return df

def preprocess_data(df):
    """
    Preprocesses the data:
    - Fills missing values with 0.
    - Ensures '日期' is in datetime format (optional, but good for sorting).
    - Converts numeric columns to numeric types.
    """
    # Fill missing values with 0
    df = df.fillna(0)
    
    # Ensure numeric columns are numeric
    numeric_cols = ['日报推送', '日报未推送', '手表佩戴', '手表未佩戴']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    # Convert Date to string for display if it's datetime
    if pd.api.types.is_datetime64_any_dtype(df['日期']):
         df['日期'] = df['日期'].dt.strftime('%m-%d')
    else:
        # If it's string, leave it, or try to parse
        try:
            df['日期'] = pd.to_datetime(df['日期']).dt.strftime('%m-%d')
        except:
            pass # Keep as is if parsing fails

    return df

def calculate_stats(df):
    """
    Calculates statistics for the summary.
    Returns a dictionary with stats.
    """
    total_push = df['日报推送'].sum()
    total_not_push = df['日报未推送'].sum()
    total_days_push = total_push + total_not_push
    push_rate = (total_push / total_days_push * 100) if total_days_push > 0 else 0

    total_wear = df['手表佩戴'].sum()
    total_not_wear = df['手表未佩戴'].sum()
    total_days_wear = total_wear + total_not_wear
    wear_rate = (total_wear / total_days_wear * 100) if total_days_wear > 0 else 0
    
    # Trend analysis (simple: compare last 7 days vs previous 7 days if possible, or just slope)
    # For now, just return the rates.
    
    return {
        'push_rate': push_rate,
        'wear_rate': wear_rate
    }
