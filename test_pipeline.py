import pandas as pd
from data_processor import load_data, validate_columns, preprocess_data, calculate_stats
from chart_generator import generate_line_chart_1, generate_line_chart_2, generate_bar_chart, generate_pie_chart
from utils import combine_charts
import os

def test_pipeline():
    print("Starting pipeline test...")
    
    # 1. Load Data
    file_path = 'e:/表格/test_data.xlsx'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
    
    try:
        df = load_data(file_path)
        print("Data loaded successfully.")
        
        validate_columns(df)
        print("Columns validated.")
        
        df = preprocess_data(df)
        print("Data preprocessed.")
        print(df.head())
        
        stats = calculate_stats(df)
        print("Stats calculated:", stats)
        
        # 2. Generate Charts
        fig1 = generate_line_chart_1(df, "Test Title 1")
        print("Chart 1 generated.")
        
        fig2 = generate_line_chart_2(df, "Test Title 2")
        print("Chart 2 generated.")
        
        fig3 = generate_bar_chart(df, "Test Title 3")
        print("Chart 3 generated.")
        
        fig4 = generate_pie_chart(df, "Test Title 4")
        print("Chart 4 generated.")
        
        # 3. Combine
        combined_img = combine_charts(fig1, fig2, fig3, fig4)
        print("Charts combined.")
        
        combined_img.save('e:/表格/test_output.png')
        print("Output saved to e:/表格/test_output.png")
        
        print("Pipeline test PASSED.")
        
    except Exception as e:
        print(f"Pipeline test FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pipeline()
