import pandas as pd
import numpy as np

# Create dummy data
dates = pd.date_range(start='2023-12-01', periods=10, freq='D')
data = {
    '日期': dates,
    '日报推送': np.random.randint(50, 100, size=10),
    '日报未推送': np.random.randint(0, 20, size=10),
    '手表佩戴': np.random.randint(40, 90, size=10),
    '手表未佩戴': np.random.randint(10, 30, size=10)
}

df = pd.DataFrame(data)

# Save to Excel
df.to_excel('e:/表格/test_data.xlsx', index=False)
print("Dummy data created: e:/表格/test_data.xlsx")
