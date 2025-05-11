import requests
import pandas as pd
import logging
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from nasa_api import *  # ここに get_daily_grid_average_temperature を定義済みとする

log_start()

# 表示行数の制限を解除（オプション）
pd.set_option('display.max_rows', None)

# 例として、東京の2019年の日次平均地表面温度を取得
latitude = 35.6895
longitude = 139.6917
year = 2019
parameter = 'T2M'  # 地表面温度（2メートル気温）

# 日次のグリッド平均温度を取得
temperature_series = get_daily_grid_average_temperature(latitude, longitude, year, parameter)

if temperature_series is not None:
    print(f"\nDaily {parameter} values for a 20km grid around Tokyo in {year}:")
    print(temperature_series)
else:
    print("Failed to retrieve daily data for the specified parameters.")
