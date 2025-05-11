import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import calendar

# Streamlitの設定
st.title("Weather Data Visualization in Japan")
st.sidebar.header("User Input")

# サイドバーで年代を選択
year_option = st.sidebar.selectbox("Select the decade:", ['1990s', '2010s'])

# サイドバーでデータタイプを選択
category = st.sidebar.selectbox("Select the data type:", ['T2M', 'RAD'])
                
# 年代に応じて日付リストを作成（存在しない日付を除外）
if year_option == '1990s':
    date_list = [
        f'{category}_1990{str(month).zfill(2)}{str(day).zfill(2)}'
        for month in range(1, 13)
        for day in range(1, calendar.monthrange(1990, month)[1] + 1)
    ]
elif year_option == '2010s':
    date_list = [
        f'{category}_2010{str(month).zfill(2)}{str(day).zfill(2)}'
        for month in range(1, 13)
        for day in range(1, calendar.monthrange(2010, month)[1] + 1)
    ]

# サイドバーで日付を選択
date_option = st.sidebar.selectbox("Select the date:", date_list)

# 選択されたデータに応じてCSVをロード
if year_option == '1990s':
    file_path = './measuredData/master_1990年代_20241106_TotalRain_daily.csv'
elif year_option == '2010s':
    file_path = './measuredData/master_2010年代_20241106_TotalRain_daily.csv'

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("CSV file not found. Please check the file path.")
    st.stop()

# NaN値を0に置き換え
df[date_option] = df[date_option].fillna(0)

# プロット
fig, ax = plt.subplots(figsize=(10, 15), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([122, 153, 24, 46], crs=ccrs.PlateCarree())  # 日本の範囲

# 地図の特徴を追加
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# 散布図プロット
scatter = ax.scatter(
    df['lon1'], df['lat1'], c=df[date_option], cmap='coolwarm', s=10, transform=ccrs.PlateCarree()
)

# カラーバーを追加
plt.colorbar(scatter, ax=ax, orientation='horizontal', label=date_option)

# タイトルとラベル
plt.title(f'{date_option} Distribution in Japan')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Streamlitでプロット表示
st.pyplot(fig)
