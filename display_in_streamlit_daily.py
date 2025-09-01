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

# 年代に応じてlong形式CSVファイルパスを切り替え
if year_option == '1990s':
    file_path = './measuredData/master_1990年代_20241106_TotalRain_daily_long.csv'
elif year_option == '2010s':
    file_path = './measuredData/master_2010年代_20241106_TotalRain_daily_long.csv'

# CSV読み込み
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("CSV file not found. Please check the file path.")
    st.stop()


# 日付リスト作成（日付番号カラムからユニーク値を抽出し、昇順ソート）
date_numbers = df['日付番号'].unique()
date_numbers.sort()

# サイドバーで日付番号をselect_sliderで選択（実データの日付番号のみ選択肢にする）
date_str_numbers = [str(d) for d in date_numbers]
date_option = st.sidebar.select_slider(
    "Select the date (yyyymmdd):",
    options=date_str_numbers,
    value=date_str_numbers[0]
)

# 選択日・データタイプでフィルタ
df_selected = df[df['日付番号'] == int(date_option)]

# NaN値を0に
df_selected[category] = df_selected[category].fillna(0)

# プロット
fig, ax = plt.subplots(figsize=(10, 15), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([122, 153, 24, 46], crs=ccrs.PlateCarree())  # 日本の範囲

# 地図の特徴を追加
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# 散布図プロット
scatter = ax.scatter(
    df_selected['lon1'], df_selected['lat1'], c=df_selected[category], cmap='coolwarm', s=10, transform=ccrs.PlateCarree()
)

# カラーバーを追加
plt.colorbar(scatter, ax=ax, orientation='horizontal', label=category)

# タイトルとラベル
plt.title(f'{category} Distribution in Japan on {date_option}')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Streamlitでプロット表示
st.pyplot(fig)
