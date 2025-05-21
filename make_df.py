import requests
import pandas as pd
import logging
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from nasa_api import *


log_start()
# データフレームの読み込み
csv_list = ["/home/nnaohiro/nasaapi/master_1990年代_20241106_TotalRain.csv","/home/nnaohiro/nasaapi/master_2010年代_20241106_TotalRain.csv"]
year_list = [1990,2010]

for i in range(2):
    df = pd.read_csv(csv_list[i])
    if 'processed' not in df.columns:
        df['processed'] = False

    total_rows = len(df)
    processed_rows = 0

    for index, row in df.iterrows():
        if not row['processed']:
            df.at[index, "temperature"] = safe_get_average_temperature(row, year_list[i], "T2M")
            df.at[index, "radiation"] = safe_get_average_temperature(row, year_list[i], "ALLSKY_SFC_SW_DWN")
            # 行が処理されたことを示すフラグを設定
            df.at[index, 'processed'] = True
            processed_rows += 1

            # 1行分の処理が完了した後のログ出力
            logging.info(f"Processing completed for row {index}")

            # 進捗状況をログに出力
            progress_percentage = (processed_rows / total_rows) * 100
            logging.info(f"Progress: {processed_rows}/{total_rows} rows processed ({progress_percentage:.2f}%)")

            # 結果を保存
            df.to_csv(csv_list[i], index=False)



