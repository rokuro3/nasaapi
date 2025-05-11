# NASA Weather Data Processing & Visualization

このプロジェクトは、NASAの気象データAPIから情報を取得し、データ処理を行い、Streamlitを用いて視覚化を実現するためのものです。気象データの取得、集約、地図上でのプロットを通じて、気象パターンを分析することが可能です。

---

## プロジェクト構成

このプロジェクトには、以下の主要なPythonスクリプトが含まれています。

### 1. `nasa_api.py`
- **役割**: NASAの気象データAPIから指定の地点における気温や放射量などのパラメータを取得し、その平均値（グリッド内の平均）を計算する関数を提供します。
- **主な機能**:
  - APIリクエストの送信とデータ取得
  - 日次の気象データ取得機能 (`get_daily_grid_average_temperature` を追加)
  - 並列処理 (`ThreadPoolExecutor` を利用)
  - 取得した結果のログ記録とエラー処理
  - 指定された範囲内のデータで平均値を算出

### 2. `nasa_api_tutorial.py` & `nasa_api_tutorial_daily.py`
- **役割**: `nasa_api.py` の関数を利用して、東京の気象データを取得する例を示します。
- **使い方**:
  - `get_grid_average_temperature` を使用して、年間平均気温を取得
  - `get_daily_grid_average_temperature` を使用して、日次データを取得

### 3. `make_df.py` & `make_df_daily.py`
- **役割**: CSVファイルからデータフレームを読み込み、各地点での気温（T2M）および放射量（ALLSKY_SFC_SW_DWN）の平均値を計算し、結果をCSVファイルに保存します。
- **主な機能**:
  - NASA APIからデータ取得 (`make_df_daily.py` では日次データ取得)
  - 各地点の気象データを計算
  - 各行が処理済みかどうかのフラグ管理とログによる進捗の記録
  - 結果をCSVファイルに追記保存

### 4. `display_in_streamlit.py` & `display_in_streamlit_daily.py`
- **役割**: Streamlitを使用して、処理済みの気象データをインタラクティブに視覚化するWebアプリケーションを提供します。
- **主な機能**:
  - サイドバーでデータセット（1990年代または2010年代）と表示パラメータ（温度、放射量など）を選択
  - `display_in_streamlit_daily.py` では日次データを選択して視覚化
  - CSVファイルを読み込み、CartopyとMatplotlibで散布図を描画
  - インタラクティブに拡大縮小可能な視覚化を実現

---

## セットアップと実行方法

### 依存パッケージのインストール
以下のパッケージが必要です。まだインストールしていない場合は、以下のコマンドを実行してください。

```bash
pip install requests pandas numpy matplotlib cartopy streamlit
```

## NASA APIの利用方法

### 気象データの取得

`nasa_api.py` 内の関数を利用して、各地点の気象データを取得できます。

### 例
#### 年間平均値の取得

```python
from nasa_api import get_grid_average_temperature

latitude = 35.6895
longitude = 139.6917
year = 2019
parameter = 'T2M'
temperature = get_grid_average_temperature(latitude, longitude, year, parameter)
print(f"The average {parameter} for the grid around Tokyo in {year} was {temperature:.2f}°C")
```

#### 日次データの取得
```python
from nasa_api import get_daily_grid_average_temperature

latitude = 35.6895
longitude = 139.6917
year = 2019
parameter = 'T2M'
daily_temperatures = get_daily_grid_average_temperature(latitude, longitude, year, parameter)
print(daily_temperatures)
```



## CSVデータの作成と更新

`make_df.py` を実行することで、指定したCSVファイルに対してNASA APIからデータを取得し、各行毎に新たな列（`temperature` や `radiation`）を追加して更新します。

- 処理済みの行にはフラグを付け、再処理を回避。
- ログファイル (`error_log.log`) に進捗状況とエラーを記録。

---

## データの視覚化（Streamlit）

`display_in_streamlit.py` を実行することで、Streamlitアプリケーションが起動し、サイドバーから年代や表示するパラメータを選択してインタラクティブなマップ表示を行います。

### Streamlitアプリの起動方法

```bash
streamlit run display_in_streamlit.py
streamlit run display_in_streamlit_daily.py
```

## 注意点

### APIリクエスト制限
NASAのAPIにはリクエスト制限が設けられている場合があるため、適切な間隔でのデータ取得を心がける。

### CSVファイルのパス設定
`make_df.py` と `display_in_streamlit.py` 内のCSVファイルパスが環境に応じて正しく設定されているか確認する。

### ログ管理
問題が発生した場合は、`error_log.log` をチェックしてエラー内容や進捗を確認する。

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
