import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt # Import Altair for advanced charting

# --- Configuration ---

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Toronto Crime Volume Dashboard',
    page_icon=':police_car:', # Changed icon to better fit the theme
    layout='wide'
)

# --- Data Loading and Preparation ---

@st.cache_data
def get_crime_data():
    """Grab crime data from a CSV file.
    
    NOTE: This assumes the CSV is already in the long format:
    AREA_NAME, Year, Total_Crimes, HOOD_ID, Data_Type
    """

    # Update the data path to reference the expected file name
    # The file path must be relative to where the Streamlit app is run
    DATA_FILENAME = Path(__file__).parent / 'data/crime_per_hood_with_forecast_for_2025.csv'
    
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

Explore the historical crime volume data (2014-2024) and the **ARIMA model forecast for 2025** across Toronto's neighborhoods.
'''

# Add some spacing
st.write('')
st.write('')


# --- Filters ---
min_year = crime_df['Year'].min()
max_year = crime_df['Year'].max()

# Year Slider
from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_year,
    max_value=max_year,
    value=[min_year, max_year]
)

# Neighbourhood Multiselect
hoods = sorted(crime_df['AREA_NAME'].unique())
selected_hoods = st.multiselect(
    'Which neighbourhood(s) would you like to view?',
    hoods
)

# Error handling for selection
if not selected_hoods:
    st.warning("Please select at least one neighbourhood to view the data.")
    st.stop() # Stop execution if no hoods are selected

st.write('')
st.write('')
st.write('')

# --- Filter Data ---

# Use .loc for safer and clearer DataFrame filtering
filtered_crime_df = crime_df.loc[
    (crime_df['AREA_NAME'].isin(selected_hoods))
    & (crime_df['Year'] <= to_year)
    & (crime_df['Year'] >= from_year)
]

# --- Line Chart Visualization ---
st.header('Crime Volume Trend Over Time', divider='gray')

st.line_chart(
    filtered_crime_df,
    x='Year',
    y='Total_Crimes', 
    color='AREA_NAME',
    use_container_width=True
)

st.write('')
st.write('')

# --- New Bar Chart Visualization (Altair) ---
st.header('Neighbourhood Crime Volume Bar Chart', divider='gray')

# Use Altair for advanced coloring in the bar chart
if not filtered_crime_df.empty:
    
    # Create the Altair chart object
    bar_chart = alt.Chart(filtered_crime_df).mark_bar().encode(
        # X-axis: Year (Nominal type for discrete bars)
        x=alt.X('Year:N', title='Year'), 
        
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
        
        # Column/Grouping: Separate bars by Neighbourhood
        column=alt.Column('AREA_NAME:N', title='Neighbourhood'),
        
        # Tooltips: Show detailed information on hover
        tooltip=['AREA_NAME', 'Year', 'Total_Crimes', 'Data_Type']
    ).properties(
        title=f'Crime Volume by Neighbourhood, {from_year:d} to {to_year:d}',
    ).interactive() # Allow zooming/panning

    st.altair_chart(bar_chart, use_container_width=True)

# --- Metric Comparison ---

# FIX: Explicitly format the year as an integer {:d} to prevent unwanted comma separators (e.g., 2,025 -> 2025).
st.header(f'Crime Volume Comparison ({to_year-1:d} vs. {to_year:d})', divider='gray')

st.write(f"Comparing total crime volume per neighbourhood between {to_year-1} and {to_year}.")

# Filter for the specific comparison years
first_year_df = crime_df.loc[crime_df['Year'] == from_year]
last_year_df = crime_df.loc[crime_df['Year'] == to_year]

# Create columns for the metric display (up to 4 per row)
cols = st.columns(min(4, len(selected_hoods)))

for i, hood in enumerate(selected_hoods):
    # Use the modulo operator to cycle through columns if more than 4 hoods are selected
    col = cols[i % len(cols)] 

    with col:
        # Use .loc and .iloc[0] for explicit, safe retrieval
        
        # Retrieval for the starting year
        first_crime_series = first_year_df.loc[first_year_df['AREA_NAME'] == hood, 'Total_Crimes']
        first_crime = first_crime_series.iloc[0] if not first_crime_series.empty else None

        # Retrieval for the ending year
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
