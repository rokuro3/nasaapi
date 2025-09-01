#%%
import pandas as pd

# ファイルパス
input_file = "/home/nnaohiro/nasaapi/measuredData/master_2010年代_20241106_TotalRain_daily.csv"
output_file = "/home/nnaohiro/nasaapi/measuredData/master_2010年代_20241106_TotalRain_daily_long.csv"

# データ読み込み（BOMや不可視文字・空白対策）
df = pd.read_csv(input_file, encoding='utf-8-sig')
# カラム名から不可視文字・空白・改行・制御文字を除去
df.columns = df.columns.str.replace(r'[\u200b-\u200f\u3000\r\n\t\x00-\x1f\x7f-\x9f]', '', regex=True).str.strip()
print('カラム名一覧:', df.columns.tolist())

# location_colsの各カラム名がdf.columnsに含まれているかチェック
location_cols_check = [col for col in [
    '調査コース', '二次メッシュ', 'lat1', 'lon1', 'lat2', 'lon2', 'height', 'seaDistance',
    '1990-2010年代の在不在の比較', '1990の観測数', '2010年の観測数', '都道府県コード',
    '1990 Total Precipitation (mm) within 20km□', 'processed'
] if col not in df.columns]
if location_cols_check:
    print('【警告】以下のカラムがdf.columnsに存在しません:', location_cols_check)

# 地点情報のカラム名を指定（不可視文字が混入していないか再確認）
location_cols = [
    '調査コース', '二次メッシュ', 'lat1', 'lon1', 'lat2', 'lon2', 'height', 'seaDistance',
    '1990-2010年代の在不在の比較', '1990の観測数', '2010年の観測数', '都道府県コード',
    '1990 Total Precipitation (mm) within 20km□', 'processed'
]


# T2M, RADのカラム名を抽出
t2m_cols = [col for col in df.columns if col.startswith('T2M_')]
rad_cols = [col for col in df.columns if col.startswith('RAD_')]

# location_colsに存在しないカラムがあれば除外
existing_location_cols = [col for col in location_cols if col in df.columns]

# wide→long変換
df_long_t2m = df.melt(id_vars=existing_location_cols, value_vars=t2m_cols, var_name='日付', value_name='T2M')
#print(df_long_t2m.head(19))
df_long_t2m['日付番号'] = df_long_t2m['日付'].str.extract(r'T2M_(\d+)').astype(int)
#print(f"T2M long shape: {df_long_t2m.shape}")
print(df_long_t2m.sample(10, random_state=42))

df_long_rad = df.melt(id_vars=existing_location_cols, value_vars=rad_cols, var_name='日付', value_name='RAD')
df_long_rad['日付番号'] = df_long_rad['日付'].str.extract(r'RAD_(\d+)').astype(int)
#print(f"RAD long shape: {df_long_rad.shape}")
print(df_long_rad.sample(10, random_state=42))  
# T2MとRADをマージ
df_long = pd.merge(
    df_long_t2m.drop(columns=['日付']),
    df_long_rad.drop(columns=['日付']),
    on=existing_location_cols + ['日付番号'],
    how='left'
)
#%%
print(df_long[['日付番号', 'T2M', 'RAD']].sample(10, random_state=42))
#%%
# 必要に応じて日付を生成（例: その年の1月1日から順に）
# 例: 1990年の場合
base_year = 1990
# カラム順を整理
df_long = df_long[existing_location_cols + ['日付番号', 'T2M', 'RAD']]

# 保存
df_long.to_csv(output_file, index=False, encoding='utf-8-sig')
# %%
