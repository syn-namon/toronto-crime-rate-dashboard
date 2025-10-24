import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt # Import Altair for advanced charting

# --- Configuration ---

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Toronto Crime Volume Dashboard',
    page_icon=':police_car:', 
    layout='wide'
)

# --- Data Loading and Preparation ---

@st.cache_data
def get_crime_data():

    # Update the data path to reference the expected file name
    # The file path must be relative to where the Streamlit app is run
    DATA_FILENAME = Path(__file__).parent / 'data/processed_data/crime_per_hood_with_forecast_for_2025.csv'
    
    try:
        # Load the combined data (historical + forecast)
        crime_df = pd.read_csv(DATA_FILENAME)
    except FileNotFoundError:
        st.error(f"Error: Data file not found at {DATA_FILENAME}. Please ensure the file is correctly placed.")
        # Return an empty DataFrame structure if the file is missing to prevent later errors
        return pd.DataFrame({'AREA_NAME': [], 'Year': [], 'Total_Crimes': []})


    # Ensure 'Year' is an integer for accurate filtering
    crime_df['Year'] = pd.to_numeric(crime_df['Year'], errors='coerce').astype('Int64')
    
    # Remove rows where Total_Crimes is NaN (if any forecast rows lack data)
    crime_df.dropna(subset=['Total_Crimes'], inplace=True)
    
    # Ensure the Data_Type column is created for coloring, assuming it's missing if Year is 2025
    if 'Data_Type' not in crime_df.columns:
        crime_df['Data_Type'] = crime_df['Year'].apply(lambda x: 'Forecast' if x == 2025 else 'Historical')
        
    return crime_df

crime_df = get_crime_data()

# Check if data loading failed
if crime_df.empty:
    st.stop()


# -----------------------------------------------------------------------------
# Draw the actual page

# --- Title and Introduction ---
'''
# :police_car: Toronto Crime Forecast Dashboard

Explore the historical crime volume data (2014-2024) and the **ARIMA model forecast for 2025** across Toronto's neighbourhoods.
'''

# Add some spacing
st.write('')
st.write('')


# --- Filters ---
min_year = crime_df['Year'].min()
max_year = crime_df['Year'].max()

# Year Slider: Controls the time range for the plots below
from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_year,
    max_value=max_year,
    value=[min_year, max_year]
)

# Neighbourhood Multiselect (This controls the Line Chart and the Metric Comparison)
hoods = sorted(crime_df['AREA_NAME'].unique())
selected_hoods = st.multiselect(
    'Which neighbourhood(s) would you like to view (For Line Chart & Metrics)?',
    hoods
)

# Error handling for selection
if not selected_hoods:
    st.warning("Please select at least one neighbourhood to view the data.")
    st.stop() # Stop execution if no hoods are selected

st.write('')
st.write('')
st.write('')

# --- Filter Data (Based on Slider and Global Hoods) ---

# This DataFrame is used for the Line Chart.
filtered_crime_df = crime_df.loc[
    (crime_df['AREA_NAME'].isin(selected_hoods))
    & (crime_df['Year'] <= to_year)
    & (crime_df['Year'] >= from_year)
]

# --- Line Chart Visualization ---
st.header('Crime Volume Trend Over Time', divider='gray')

# FIX: Rename the 'Year' column in the plotting data to a string type.
# This prevents the thousands separator (e.g., 2,023) and allows the axis label to be 'Year'.
line_chart_data = filtered_crime_df.copy()
line_chart_data['Year'] = line_chart_data['Year'].astype(str)

st.line_chart(
    line_chart_data,
    x='Year', # Now uses the string column, and labels the axis 'Year'
    y='Total_Crimes', 
    color='AREA_NAME',
    use_container_width=True
)

st.write('')
st.write('')

# --- Bar Chart Visualization (Altair) ---
st.header('Neighbourhood Crime Volume Bar Chart', divider='gray')

# Determine the default index for the single select box (guaranteed to have at least one item by st.stop() above)
default_hood_index = hoods.index(selected_hoods[0])

# ADJUSTED: Single-select filter for the bar chart
bar_selected_hood = st.selectbox(
    'Which single neighbourhood to display in the Bar Chart?',
    hoods,
    index=default_hood_index # Set index based on the calculated default
)

# ADJUSTED: Filter data specifically for the bar chart.
# This DataFrame respects the time slider (from_year, to_year) and uses the single hood selection.
bar_chart_df = crime_df.loc[
    (crime_df['AREA_NAME'] == bar_selected_hood) # Changed from .isin() to ==
    & (crime_df['Year'] <= to_year)
    & (crime_df['Year'] >= from_year)
]

# Use Altair for advanced coloring in the bar chart
if not bar_chart_df.empty:
    
    # Create the Altair chart object
    bar_chart = alt.Chart(bar_chart_df).mark_bar().encode( # Use the new bar_chart_df
        # X-axis: Year (Nominal type for discrete bars). 
        # Added scale=alt.Scale(rangeStep=25) to explicitly control bar width and spacing
        x=alt.X('Year:N', title='Year', scale=alt.Scale(rangeStep=20)), 
        
        # Y-axis: Total Crimes
        y=alt.Y('Total_Crimes:Q', title='Total Crime Volume'),
        
        # Color: Use Data_Type to distinguish Historical vs. Forecast
        # Set the colors explicitly for clarity
        color=alt.Color('Data_Type:N', 
            scale=alt.Scale(
                domain=['Historical', 'Forecast'],
                range=['#3366cc', '#cc4733'] # Blue for historical, Red/Orange for forecast
            ),
            legend=alt.Legend(title="Data Type")
        ),
        
        # Column/Grouping: Separate bars by Neighbourhood (retained for consistent faceting/title, even if only one)
        column=alt.Column('AREA_NAME:N', title='Neighbourhood'),
        
        # Tooltips: Show detailed information on hover
        tooltip=['AREA_NAME', 'Year', 'Total_Crimes', 'Data_Type']
    ).properties(
        title=f'Crime Volume by Neighbourhood, {from_year:d} to {to_year:d}',
        ##height=500, # Set height to make more space for the chart and legend
        ##width=400 # Reduced width further to 400px
    ).interactive() # Allow zooming/panning

    # Set use_container_width=False to respect the fixed width setting
    st.altair_chart(bar_chart, use_container_width=False)

# --- Metric Comparison (Fixed 2024 vs 2025) ---

# Define the fixed comparison years for the metrics below
START_COMPARE_YEAR = to_year-1
END_COMPARE_YEAR = to_year

# Update header and description to use fixed years (2024 vs 2025)
st.header(f'Crime Volume Comparison ({START_COMPARE_YEAR:d} vs. {END_COMPARE_YEAR:d})', divider='gray')

st.write(f"Comparing total crime volume per neighbourhood between {START_COMPARE_YEAR} (Actual) and {END_COMPARE_YEAR} (Forecast).")

# NEW LOGIC: Combine selected hoods from the main filter and the bar chart filter
all_hoods_for_comparison = set(selected_hoods)
# Add the single selected hood from the bar chart to the set to ensure uniqueness
all_hoods_for_comparison.add(bar_selected_hood)
comparison_hoods = sorted(list(all_hoods_for_comparison))


# Filter for the specific fixed comparison years
first_year_df = crime_df.loc[crime_df['Year'] == START_COMPARE_YEAR]
last_year_df = crime_df.loc[crime_df['Year'] == END_COMPARE_YEAR]

# Create columns for the metric display (up to 4 per row)
# ADJUSTED: Use the combined list of hoods for metric display
cols = st.columns(min(4, len(comparison_hoods)))

# ADJUSTED: Iterate over the combined list of hoods
for i, hood in enumerate(comparison_hoods):
    # Use the modulo operator to cycle through columns if more than 4 hoods are selected
    col = cols[i % len(cols)] 

    with col:
        # Use .loc and .iloc[0] for explicit, safe retrieval
        
        # Retrieval for the starting year (2024)
        first_crime_series = first_year_df.loc[first_year_df['AREA_NAME'] == hood, 'Total_Crimes']
        first_crime = first_crime_series.iloc[0] if not first_crime_series.empty else None

        # Retrieval for the ending year (2025)
        last_crime_series = last_year_df.loc[last_year_df['AREA_NAME'] == hood, 'Total_Crimes']
        last_crime = last_crime_series.iloc[0] if not last_crime_series.empty else None


        # Format the metric display
        if last_crime is None or math.isnan(last_crime):
            last_crime_str = 'N/A'
            growth = 'n/a'
            delta_color = 'off'
        else:
            last_crime_str = f'{last_crime:,.0f}'
            
            if first_crime is None or math.isnan(first_crime) or first_crime == 0:
                 # If no starting data, cannot calculate growth
                growth = 'New Data' 
                delta_color = 'off'
            else:
                # Calculate percentage change for a cleaner metric
                percent_change = ((last_crime - first_crime) / first_crime) * 100
                growth = f'{percent_change:,.1f}%'
                # Set delta color based on trend (Crime decrease is 'green', increase is 'red')
                delta_color = 'inverse' if percent_change > 0 else 'normal'

        st.metric(
            label=f'{hood}',
            value=last_crime_str,
            delta=growth,
            delta_color=delta_color
        )
