import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Streamlitの設定
st.title("Weather Data Visualization in Japan")
st.sidebar.header("User Input")

# サイドバーでの入力
year_option = st.sidebar.selectbox("Select the decade:", ['1990s', '2010s'])
option = st.sidebar.selectbox("Select the data to plot:", ['temperature', 'radiation', 'height', 'seaDistance', 'TotalPrecipitation'])

# 選択されたデータに応じてCSVをロード
if year_option == '1990s':
    file_path = './measuredData/master_1990年代_20241106_TotalRain.csv'
elif year_option == '2010s':
    file_path = './measuredData/master_2010年代_20241106_TotalRain.csv'

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("CSV file not found. Please check the file path.")
    st.stop()

# 必要ならば'height'列をfloatに変換し、エラー時に0に置き換え
if option == 'height':
    def safe_float_conversion(value):
        try:
            return float(value)
        except ValueError:
            return 0.0
    df['height'] = df['height'].apply(safe_float_conversion)

# NaN値を0に置き換え
df[option] = df[option].fillna(0)

# プロット
fig, ax = plt.subplots(figsize=(10, 15), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([122, 153, 24, 46], crs=ccrs.PlateCarree())  # 日本の範囲

# 地図の特徴を追加
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# 散布図プロット
scatter = ax.scatter(
    df['lon1'], df['lat1'], c=df[option], cmap='coolwarm', s=10, transform=ccrs.PlateCarree()
)

# カラーバーを追加
plt.colorbar(scatter, ax=ax, orientation='horizontal', label=option)

# タイトルとラベル
plt.title(f'{option.capitalize()} Distribution in Japan')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Streamlitでプロット表示
st.pyplot(fig)
