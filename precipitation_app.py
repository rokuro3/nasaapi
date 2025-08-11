import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Streamlit App Configuration
st.set_page_config(layout="wide")
st.title("Precipitation Data Visualization")

# Sidebar for User Input
st.sidebar.header("Display Options")

# Decade selection
decade_option = st.sidebar.selectbox("Select Decade:", ['2010s', '1990s'])

# Set file path based on selection
if decade_option == '2010s':
    file_path = 'data/precipitation_results_2010.csv'
else:
    file_path = 'data/precipitation_results_1990.csv'

# Load Data
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"Error: The file was not found at {file_path}")
    st.stop()

# Data Cleaning and Preparation
# Ensure 'Month' column can be handled as a string for filtering
df['Month'] = df['Month'].astype(str)

# Get unique months from the dataframe, including 'Annual'
month_options = ['Annual'] + sorted([m for m in df['Month'].unique() if m != 'Annual'], key=int)
selected_month = st.sidebar.selectbox("Select Month to Display:", options=month_options)

# Filter data based on selection
if selected_month == 'Annual':
    filtered_df = df[df['Month'] == 'Annual']
else:
    filtered_df = df[df['Month'] == selected_month]

# Check if filtered data is empty
if filtered_df.empty:
    st.warning(f"No data available for the selected month: {selected_month}")
    st.stop()

# Map Visualization
st.subheader(f"Total Precipitation for Month: {selected_month}")

fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([122, 154, 24, 46], crs=ccrs.PlateCarree())  # Japan's extent

# Add map features
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.OCEAN, alpha=0.5)
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)

# Create the scatter plot
scatter = ax.scatter(
    filtered_df['Longitude'], 
    filtered_df['Latitude'], 
    c=filtered_df['Total Precipitation (mm)'], 
    cmap='viridis',
    s=20,
    transform=ccrs.PlateCarree(),
    alpha=0.7
)

# Add a color bar
cbar = plt.colorbar(scatter, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
cbar.set_label('Total Precipitation (mm)')

# Set titles and labels
ax.set_title(f'Precipitation Distribution in Japan ({selected_month})', pad=20)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# Display the plot in Streamlit
st.pyplot(fig)
