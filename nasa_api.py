import requests
import pandas as pd
import logging
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

# ログの設定
def log_start():
    logging.basicConfig(filename='error_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    logging.info(f"start")

def get_grid_average_temperature(lat, lon, year, parameter, grid_size_km=20, grid_points=5):
    base_url = 'https://power.larc.nasa.gov/api/temporal/monthly/point'
    total = 0
    count = 0
    
    lat_range = grid_size_km / 111  # 1度の緯度は約111km
    lon_range = grid_size_km / (111 * np.cos(np.radians(lat)))  # 1度の経度は緯度によって変わる

    lats = np.linspace(lat, lat + lat_range, grid_points)
    lons = np.linspace(lon, lon + lon_range, grid_points)

    def fetch_data(lat_point, lon_point):
        logging.info(f"Fetching data for ({lat_point}, {lon_point})")  # リクエスト開始前のログ
        params = {
            'parameters': parameter,
            'community': 'RE',
            'longitude': lon_point,
            'latitude': lat_point,
            'start': str(year),
            'end': str(year),
            'format': 'JSON'
        }
        time.sleep(random.uniform(0,5))
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            param_data = data['properties']['parameter'][parameter]
            param_data = {k: v for k, v in param_data.items() if not k.endswith('13')}
            df = pd.json_normalize(param_data).T
            df.index = pd.to_datetime(df.index, format='%Y%m')
            df.columns = [parameter]
            result = df[parameter].mean()
            logging.info(f"Data fetched successfully for ({lat_point}, {lon_point}): {result}")  # リクエスト成功時のログ
            return result
        else:
            logging.error(f"Error fetching data for ({lat_point}, {lon_point}): {response.status_code}")    
            return None

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(fetch_data, lat_point, lon_point): (lat_point, lon_point) for lat_point in lats for lon_point in lons}
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                total += result
                count += 1

    return total / count if count > 0 else None

# エラー処理を含む新しい列の計算
def safe_get_average_temperature(row, year, parameter):
    avg_temp = get_grid_average_temperature(row["lat1"], row["lon1"], year, parameter)
    if avg_temp is None:
        logging.error(f"Error calculating {parameter} for row: {row.to_dict()}")
    return avg_temp

def get_daily_grid_average_temperature(lat, lon, year, parameter, grid_size_km=20, grid_points=1):
    """
    指定された緯度・経度と年に対して、日次の気象データをグリッド範囲で取得し、
    各日の平均値を返す（pd.Series形式）。
    """
    base_url = 'https://power.larc.nasa.gov/api/temporal/daily/point'
    lat_range = grid_size_km / 111
    lon_range = grid_size_km / (111 * np.cos(np.radians(lat)))

    lats = np.linspace(lat, lat + lat_range, grid_points)
    lons = np.linspace(lon, lon + lon_range, grid_points)

    def fetch_daily_data(lat_point, lon_point):
        logging.info(f"Fetching daily data for ({lat_point}, {lon_point})")
        params = {
            'parameters': parameter,
            'community': 'RE',
            'longitude': lon_point,
            'latitude': lat_point,
            'start': f"{year}0101",
            'end': f"{year}1231",
            'format': 'JSON'
        }
        time.sleep(random.uniform(0, 5))
        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            param_data = data['properties']['parameter'][parameter]
            series = pd.Series(param_data)
            series.index = pd.to_datetime(series.index, format='%Y%m%d')
            series = series.astype(float)
            logging.info(f"Successfully fetched daily data for ({lat_point}, {lon_point})")
            return series
        except Exception as e:
            logging.error(f"Error fetching daily data for ({lat_point}, {lon_point}): {str(e)}")
            return None

    daily_series_list = []

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(fetch_daily_data, lat_point, lon_point): (lat_point, lon_point)
            for lat_point in lats for lon_point in lons
        }
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                daily_series_list.append(result)

    if not daily_series_list:
        return None

    # 日付ごとに平均を取る（Seriesのリスト → DataFrame → 平均）
    daily_df = pd.concat(daily_series_list, axis=1)
    daily_mean_series = daily_df.mean(axis=1)

    return daily_mean_series

