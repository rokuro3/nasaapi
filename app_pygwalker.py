import pandas as pd
import pygwalker as pyg
import streamlit as st

csv_path = "measuredData/master_1990年代_20241106_TotalRain_daily_long.csv"
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# pygwalkerのmeta_configでlat1/lon1を緯度・経度として指定
meta_config = {
	"lat": "lat1",
	"lng": "lon1"
}

pyg.walk(df, meta_config=meta_config)