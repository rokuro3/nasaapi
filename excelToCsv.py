import pandas as pd

# Excelファイルを読み込みます
excel_file_path = 'master_2010年代_20241106_TotalRain.xlsx'
df = pd.read_excel(excel_file_path)

# CSVファイルに書き出します
csv_file_path = 'master_2010年代_20241106_TotalRain.csv'
df.to_csv(csv_file_path, index=False)
