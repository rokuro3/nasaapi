import requests
import pandas as pd
import logging
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from nasa_api import *

log_start()

csv_list = [
    "/home/nnaohiro/nasaapi/master_1990年代_20241106_TotalRain.csv",
    "/home/nnaohiro/nasaapi/master_2010年代_20241106_TotalRain.csv"
]
year_list = [1990, 2010]

# 取得するパラメータとそのプレフィックス（列名用）
parameters = {
    "T2M": "T2M",
    "ALLSKY_SFC_SW_DWN": "RAD"
}

for i in range(2):
    df = pd.read_csv(csv_list[i])
    if 'processed' not in df.columns:
        df['processed'] = False

    total_rows = len(df)
    processed_rows = 0

    for index, row in df.iterrows():
        if not row['processed']:
            lat = row["lat1"]
            lon = row["lon1"]
            year = year_list[i]

            for param, prefix in parameters.items():
                daily_series = get_daily_grid_average_temperature(lat, lon, year, param)

                if daily_series is not None:
                    # 列名を {prefix}_YYYYMMDD に変更して1行に展開
                    daily_series.index = daily_series.index.strftime(f'{prefix}_%Y%m%d')
                    for col_name, value in daily_series.items():
                        df.at[index, col_name] = value
                else:
                    logging.error(f"Failed to fetch daily {param} for row {index} (lat: {lat}, lon: {lon})")

            # フラグを更新
            df.at[index, 'processed'] = True
            processed_rows += 1

            # ログ出力
            logging.info(f"Processing completed for row {index}")
            progress_percentage = (processed_rows / total_rows) * 100
            logging.info(f"Progress: {processed_rows}/{total_rows} rows processed ({progress_percentage:.2f}%)")

            # 途中保存
            df.to_csv(csv_list[i], index=False)
