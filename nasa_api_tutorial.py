import requests
import pandas as pd
import logging
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from nasa_api import *

log_start()
# 例として、東京の2019年の平均地表面温度を取得
latitude = 35.6895
longitude = 139.6917
year = 2019
parameter = 'T2M'  # 地表面温度

temperature_vakue = get_grid_average_temperature(latitude, longitude, year, parameter)
if temperature_value is not None:
    print(f"The average {parameter} for a 20km grid around Tokyo in {year} was {temperature_value:.2f}°C")
else:
    print("Failed to retrieve data for the specified parameters.")
