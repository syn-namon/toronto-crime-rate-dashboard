- [Purpose and Overview](#purpose-and-overview)
- [Methodology](#methodology)
- [Project Scope](#project-scope)
- [Data Cleaning](#data-cleaning)
- [Analysis](#analysis)
- [Visualization](#visualization)
- [Conclusion](#conclusion)
- [Credits and Source](#credits-and-source)

# Purpose and Overview

This project performs a comprehensive analysis of historic neighbourhood crime rates in Toronto spanning from 2014 to 2024. Using this data, the analysis forecasts the total crime volume for 2025, with separate, granular forecasts provided for each neighbourhood.

The core objective is to provide a deeper understanding of crime volume trends over time, offering actionable insights into both past patterns and future projections. The resulting data and forecasts are intended to support all key stakeholders — including government bodies, local businesses, and community organizations — in making data-driven operational decisions, implementing targeted public safety initiatives, and optimizing resource allocation.

# Methodology

## Steps taken:

1. Data Cleaning: focused on handling missing values, resolving inconsistencies, and ensuring the final dataset was optimized and ready for time-series analysis.
2. Preliminary Analysis & Correlation: conducted to understand crime patterns, identify relationships between variables, and analyze the overall distribution of the data.
3. Forecasting Model Implementation: applied the the Autoregressive Integrated Moving Average (ARIMA) model to predict the crime volume for the year 2025 (in total for Toronto per crime type and per neighbourhood). Established dedicated training and testing sets for rigorous model validation. Assessed model accuracy using performance metrics to ensure reliability.
4. Visualization: created informative plots and dashboards using Python (Matplotlib/Seaborn) and Tableau to clearly communicate key trends, insights, and model results.
5. Conclusion: summarized the findings, provided actionable insights, and offered strategic recommendations for stakeholders.

## Technical Stack:

### Programming Language:

Python

### Libraries Used:

- Numpy: matrix operations
- Pandas: data analysis
- Matplotlib: creating graphs and plots
- Plotly: creating graphs and plots
- Seaborn: enhancing matplotlib plots
- Pmdarima: the Autoregressive Integrated Moving Average (ARIMA) model for predicting analysis

### Other tools:

Tableau

# Project Scope

The scope of this comprehensive analysis includes the following components:
- **Neighbourhood Trends:** Defining the crime volume trend over the eleven years (2014-2024) within the top 3 most active neighbourhoods for each crime type.
- **Area Ranking:** Identifying and ranking the top 10 neighbourhoods with the highest total volume of crime across all types throughout the entire 11-year dataset.
- **Total Forecast:** Generating a prediction for the total crime volume for the year 2025 across all of Toronto.
- **Granular Forecast:** Generating separate, individualized forecasts for the expected crime volume trend in 2025 for each neighbourhood.

## Description

This project begins with a pre-analysis of historical crime volume data in Toronto spanning 2014 to 2024, which reveals the crime trend across individual neighbourhoods. Using the optimized the Autoregressive Integrated Moving Average (ARIMA) modelling approach, the analysis provides forward-looking predictions for the crime volume trend in 2025, specifically forecasting total volume trends for each major crime type and neighbourhood-level trends.

Model reliability is ensured through rigorous data splitting and the application of industry-standard performance metrics (such as MAE, RMSE, and MAPE) for validation. The output of this analysis is a set of validated forecasts, accompanied by strategic insights and actionable recommendations for all relevant stakeholders.

## Stakeholders

### Government and Law Enforcement:
- **Toronto Police Service** - directing patrol resources, justifying budget requests for specific units (e.g., gun violence or organized crime), planning targeted intervention programs, and setting operational priorities for the year.
- **Toronto City Council** - evaluating the success of current public safety initiatives, allocating the city budget, informing policy debates (e.g., transit security, mental health response), and addressing public concern.
- **Public Transit Agencies** - identifying high-crime subway stations or bus routes to justify increased security presence (special constables, security guards, CCTV deployment).
- **Provincial/Federal Government** - supporting applications for federal/provincial funding for specific crime reduction programs in targeted areas of the city.

### Business and Finance:
- **Real Estate Developers/Investors** - determining the desirability, safety, and future value of areas for new residential or commercial developments.
- **Insurance Companies** - calculating premiums for property, business, and auto insurance based on the forecasted crime rates and types in specific Toronto neighbourhoods.
- **Local Businesses** - justifying investment in local security patrols, retail loss prevention, and enhanced surveillance systems for the coming year.
- **Tourism Sector** - monitoring trends, especially in downtown areas, to assess and manage public messaging regarding the safety of visitors.

### Community and Advocacy Groups:
- **Neighbourhood/Community Associations** - using data to lobby City Council and the Police for more resources, organize community safety meetings.
- **Schools, Universities, and Hospitals** - assessing safety risks near their locations and adjusting security protocols (e.g., lighting, campus police patrols) for the upcoming year.
- **Social Service/Non-Profit Organizations** - directing resources (e.g., youth outreach, mental health support) to high-risk areas identified by the detailed crime type and area data.
- **General Public/Residents** - deciding where to live, focusing on personal security measures, and engaging in local political debates regarding safety.


# Data Cleaning

After an initial review of the dataset for common data quality issues (including missing values, duplicate records, and inconsistent formatting), the following systematic adjustments were performed:
1. The original structure contained column headers that mixed crime type and year (e.g., 'ASSAULT_2014'). To facilitate time-series analysis, the dataset was transformed using the .melt() method. This moved all crime-year columns into rows, creating a new DataFrame with a single column for crime values.
2. The combined column (e.g., ASSAULT_2014) was then split into two distinct, usable features: 'Crime Type' and 'Year', utilizing Python's .split method combined with lambda and pd.Series.
3. Rows with the non-crime metric 'POPULATION' in the 'Crime Type' column were explicitly excluded from the analysis.
4. All identified null (NaN) values in the crime volume column were systematically imputed (filled) with the numeric value 0 using the .fillna() method, ensuring data consistency for modelling.
5. The cleaned and transformed DataFrame was then grouped by the final 'Crime Type' and 'Year' to create the time-series dataset used for all subsequent analysis and forecasting.

#### Tools used:
- .describe
- .tolist
- .melt
- .fillna
- .split
- .apply
- lambda
- .Series
- .unique
- .rename
- .groupby
- .notna

Results:
 - No missing values in the dataset;
 - No whitespaces or random symbols in both numeric and categorical columns;
 - Summary statistics for all columns after cleaning:
  
  ![Summary statistics for all columns](/img/Count_crimes_clean.png)

 - Summary statistics for all columns after .groupby for 'HOOD_ID', 'AREA_NAME' and 'Year':
 
 ![Summary statistics for all columns after .groupby for neighbourhood](/img/Crimes_total.png)

 - Summary statistics for all columns after .groupby for 'Crime Type' and 'Year':
 
 ![Summary statustics for all columns after .groupby for crime type](/img/Crimes_by_type.png)

# Analysis

### Why I Chose to Use a Machine Learning Model:
The primary objective of this project is twofold: to accurately identify the historical trends of crime volume across Toronto's neighbourhoods between 2014 and 2024, and to forecast the crime trend for the subsequent year, 2025.

While simple data analysis and visualizations are sufficient to reveal surface-level crime trends, the Autoregressive Integrated Moving Average (ARIMA) model was selected to strengthen the analysis. This choice allows for robust time-series forecasting, yielding reliable predictions that provide deeper, data-driven insights beyond simple observation.

## Model description

The Autoregressive Integrated Moving Average (ARIMA) model is a popular and powerful statistical method specifically designed for time series forecasting.

This model is particularly beneficial as it combines three distinct processes to capture the underlying structure of the data:

**Autoregression (AR):** models the forecasting variable as a function of its own previous, or lagged, values in the time series (the "p" parameter).

**Integrated (I):** uses differencing (the "d" parameter) to make the time series stationary, which is a requirement for accurate modelling.

**Moving Average (MA):** incorporates the dependency between an observation and a residual error from a moving average model applied to lagged observations (the "q" parameter).

In this project, the ARIMA model is applied to forecast the future crime volume for 2025 based purely on the historical patterns identified within the 2014 – 2024 data period.

## Predictive Power and Interpretability:

The Autoregressive Integrated Moving Average (ARIMA) model provides a robust framework for analyzing time series data, allowing for both the interpretation of historical patterns and the forecasting of future values.

In this project, I utilized the Auto-ARIMA function, which automates the configuration process. This approach systematically generates and compares multiple ARIMA models by iteratively testing different combinations of parameters (p, d, q). The algorithm's goal is to minimize the corrected Akaike Information Criterion (AICc) and the prediction error derived from the Maximum Likelihood Estimation (MLE). By minimizing these metrics, Auto-ARIMA efficiently identifies the optimal model configuration that provides the best fit for the time series data for each neighbourhood.

## Analysis Value:

The outcome of this comprehensive crime trend analysis and forecasting is highly valuable across various sectors and for multiple community groups. By providing clear, data-driven insights, the project empowers better decision-making for:

**Government and Public Safety:** the results can directly inform police departments on evaluating the success of existing public safety initiatives, optimizing budget allocation for enforcement, and developing targeted crime prevention projects in high-risk areas.

**Business and Investment:** businesses can leverage the analysis to predict and evaluate safer areas for new expansion, investment, and operational planning, thereby mitigating potential security risks and protecting assets.

**Communities and Non-Profits:** local community groups and non-profit organizations can use the neighbourhood-specific forecasts to strategically plan safety outreach, organize neighbourhood watch programs, and advocate for resources where they are most critically needed.

## Model Performance Summary:

A crucial step in the modelling process involved rigorous validation and ensuring forecast stability. Initially, experimental runs showed inconsistent and artificially improved accuracy (data leakage) due to a flaw in the data subsetting logic. This issue was addressed by implementing isolated data handling within the forecasting loop, ensuring that each model was trained only on its specific historical data, leading to stable and reproducible performance metrics.

The final performance of the two primary forecasting models is summarized below, based on predictions for the 2024 test period:

**Total Crime Volume Prediction:**
- Train data: 2014 - 2023
- Test data: 2024
- Total MAE: 53.48 units - The average prediction is off by approximately 53.48 total crimes
- Total RMSE: 53.48 units
- Total MAPE: 14.71% - The prediction is, on average, within 14.71% of the actual total crime volume

The low MAPE of 14.71% for the aggregate forecast indicates a high degree of confidence in the total predicted crime volume.

**Prediction of crime volume for 2025 per each neighbourhood:**
- Train data: 2014 - 2023
- Test data: 2024
- Total MAE: 1163.87 units - The average prediction for an individual neighbourhood is off by approximately 1,164 crimes
- Total RMSE: 1163.87 units
- Total MAPE: 18.14% - The prediction is, on average, within 18.14% of the actual crime volume for that neighbourhood.

While the raw error (MAE) is higher for individual neighbourhoods, the MAPE of 18.14% still provides a reasonable measure of accuracy, especially considering the higher variability and lower crime volumes often found in individual neighbourhood time series.

# Visualization

**Top10 Neighbourhoods with High Volume of Crimes in Total (rate per 100,000 population)**

![Top10 Neighbourhoods with High Volume of Crimes in Total (rate per 100,000 population)](/img/Top10_Neighbourhoods_with_High_Volume_of_Crimes_in_Total_(rate_per_100,000_population).png)

**Top10 Neighbourhoods with High Volume of Crimes in Total**

![Top10 Neighbourhoods with High Volume of Crimes in Total](/img/Top10_Neighbourhoods_with_High_Volume_of_Crimes_in_Total.png)

**Predicted Crimes Count for 2025 per Neighbourhood**

![Predicted Crimes Count for 2025 per Neighbourhood](/img/Predicted_Crimes_Count_for_2025_per_Neighbourhood.png) 

[Tableau Dashboard](https://public.tableau.com/views/PredictedCrimesCountfor2025perNeighbourhood/Sheet1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

**Actual Crimes vs. Predicted Crimes for 2024 with MAPE**

![Actual Crimes vs. Predicted Crimes for 2024 with MAPE](/img/Actual_Crimes_vs._Predicted_Crimes_for_2024_with_MAPE.png)

[Tableau Dashboard](https://public.tableau.com/views/ActualCrimesvs_PredictedCrimesfor2024withMAPE/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

**Crime Volume Trend Over Time in Toronto (Top 3 Neighbourhoods)**

![Crime Volume Trend Over Time in Toronto (Top 3 Neighbourhoods)](/img/Crime_Volume_Trend_Over_Time_in_Toronto_(Top_3_Neighbourhoods).png)

[Tableau Dashboard](https://public.tableau.com/views/CrimeVolumeTrendOverTimeinTorontoTop3Neighbourhoods/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

[Crime Volume in Toronto with Forecast for 2025 / Tableau Dashboard](https://public.tableau.com/views/CrimeVolumeinTorontowithForecastfor2025/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

[Toronto Crime Forecast Dashboard](https://toronto-crime-rate-dashboard.streamlit.app/)
### How to run Streamlit app on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

# Conclusion

This project successfully applied time-series analysis to historical crime data (2014 – 2024) to establish trends and generate two critical forecasts for 2025: the aggregate total crime volume for Toronto and granular crime volume predictions for each neighbourhood. The Autoregressive Integrated Moving Average (ARIMA) model, optimized via Auto-ARIMA, proved effective for capturing the underlying temporal dependencies in the crime data.

### Key Findings and Model Validation
During development, a potential data leakage issue was identified and systematically resolved, ensuring that the final performance metrics are stable and the model is reproducible. The resulting performance demonstrates that the forecasting approach is highly effective for aggregate planning:

**Aggregate total crime forecast per crime type:** achieved a Mean Absolute Percentage Error (MAPE) of 14.71%. This high degree of accuracy validates the forecast's use for city-wide budgetary and strategic planning at the highest levels.

**Crime volume forecast per neighbourhood:** achieved a MAPE of 18.14%. While the raw error (MAE of 1,164 crimes) is higher, this MAPE is a reasonable result considering the inherently greater variability, lower data volume, and inconsistent patterns within individual neighbourhood time series.

### Recommendations for Stakeholders
The generated forecasts provide actionable intelligence that can be directly applied by government, police departments, local businesses, and community organizations:
- **Prioritize the aggregate forecast:** the total crime forecast (14.71% MAPE) should be the primary input for large-scale planning, such as evaluating the success of city-wide public safety policies and optimizing annual police budgets.
- **Use neighbourhood data as a directional tool:** the per-neighbourhood predictions (18.14% MAPE) should be used to guide targeted resource allocation, such as identifying areas for proactive patrol increases or focusing community engagement initiatives where crime is projected to rise.
- **Continuous data enrichment:** while the current model relies only on historical crime counts, integrating these insights with other cross-departmental data (e.g., local events, seasonal factors, or police staffing levels) will strengthen the predictive power.

### Limitations and Future Work
The current model's primary limitation is its pure reliance on the crime time series itself. Crime is a complex phenomenon driven by exogenous factors-variables outside of the time series-such as socio-economic indicators (unemployment, housing instability, level of education, etc.), and policy changes.

To improve predictive reliability and gain deeper insights future model development should shift toward an ARIMAX framework. This would involve incorporating these external, influencing features as model inputs, thereby enhancing accuracy and providing a more comprehensive understanding of the factors driving Toronto's crime trends.

# Credits and Source

[The Crime Data by Neighbourhood dataset - open.toronto.ca](https://open.toronto.ca/dataset/neighbourhood-crime-rates/)