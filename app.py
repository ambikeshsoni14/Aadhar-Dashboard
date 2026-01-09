import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Aadhaar Data Analysis Dashboard')

@st.cache_data
def load_and_preprocess_data():
    # Load datasets from Google Cloud Storage URLs
    # IMPORTANT: Replace these placeholder URLs with your actual Public URLs from GCS!
    url_1 = "https://drive.google.com/uc?id=18o0yunO9cgr-2eEpJADlmncY9j_gk1s2"
    df_demographic = pd.read_csv(url_1)
    url_2 = "https://drive.google.com/uc?id=1KA3ovFxtL2NWnmSg0HdE-_H2zgCkucXB"
    df_biometric = pd.read_csv(url_2)
    url_3 = "https://drive.google.com/uc?id=15QUoL38XobCg_2cjv88SEsEcBUbLhmEd"
    df_enrolment = pd.read_csv(url_3)

    # Convert 'date' columns to datetime objects
    df_biometric['date'] = pd.to_datetime(df_biometric['date'], format='%d-%m-%Y')
    df_demographic['date'] = pd.to_datetime(df_demographic['date'], format='%d-%m-%Y')
    df_enrolment['date'] = pd.to_datetime(df_enrolment['date'], format='%d-%m-%Y')

    # Standardize 'state' and 'district' columns
    for df in [df_biometric, df_demographic, df_enrolment]:
        for col in ['state', 'district']:
            df[col] = df[col].str.lower().str.strip()

    # Rename age-related columns for consistency
    df_biometric.rename(columns={'bio_age_5_17': 'age_5_17', 'bio_age_17_': 'age_18_greater'}, inplace=True)
    df_demographic.rename(columns={'demo_age_5_17': 'age_5_17', 'demo_age_17_': 'age_18_greater'}, inplace=True)

    # Merge dataframes
    df_merged_bio_demo = pd.merge(df_biometric,
                                  df_demographic,
                                  on=['date', 'state', 'district', 'pincode'],
                                  how='left',
                                  suffixes=('_biometric', '_demographic'))

    df_combined = pd.merge(df_merged_bio_demo,
                           df_enrolment,
                           on=['date', 'state', 'district', 'pincode'],
                           how='left',
                           suffixes=('_bio_demo', '_enrolment'))

    # Handle NaN values introduced by merging
    age_columns_to_fill = [
        'age_5_17_demographic',
        'age_18_greater_demographic',
        'age_0_5',
        'age_5_17',
        'age_18_greater'
    ]

    for col in age_columns_to_fill:
        if col in df_combined.columns:
            df_combined[col] = df_combined[col].fillna(0).astype(int)

    # Create total activity columns
    df_combined['total_biometric_activity'] = df_combined['age_5_17_biometric'] + df_combined['age_18_greater_biometric']
    df_combined['total_demographic_activity'] = df_combined['age_5_17_demographic'] + df_combined['age_18_greater_demographic']
    df_combined['total_enrolment_activity'] = df_combined['age_0_5'] + df_combined['age_5_17'] + df_combined['age_18_greater']
    
    # Convert state and district to category type after merging and standardization
    df_combined['state'] = df_combined['state'].astype('category')
    df_combined['district'] = df_combined['district'].astype('category')

    return df_combined

df_combined = load_and_preprocess_data()

st.write("Data loaded and preprocessed successfully!")
st.write(df_combined.head())

@st.cache_data
def load_and_preprocess_data():
    # Load datasets from Google Cloud Storage URLs
    # IMPORTANT: Replace these placeholder URLs with your actual Public URLs from GCS!
    url_1 = "https://drive.google.com/uc?id=18o0yunO9cgr-2eEpJADlmncY9j_gk1s2"
    df_demographic = pd.read_csv(url_1)
    url_2 = "https://drive.google.com/uc?id=1KA3ovFxtL2NWnmSg0HdE-_H2zgCkucXB"
    df_biometric = pd.read_csv(url_2)
    url_3 = "https://drive.google.com/uc?id=15QUoL38XobCg_2cjv88SEsEcBUbLhmEd"
    df_enrolment = pd.read_csv(url_3)

    # Convert 'date' columns to datetime objects
    df_biometric['date'] = pd.to_datetime(df_biometric['date'], format='%d-%m-%Y')
    df_demographic['date'] = pd.to_datetime(df_demographic['date'], format='%d-%m-%Y')
    df_enrolment['date'] = pd.to_datetime(df_enrolment['date'], format='%d-%m-%Y')

    # Standardize 'state' and 'district' columns
    for df in [df_biometric, df_demographic, df_enrolment]:
        for col in ['state', 'district']:
            df[col] = df[col].str.lower().str.strip()

    # Rename age-related columns for consistency
    df_biometric.rename(columns={'bio_age_5_17': 'age_5_17', 'bio_age_17_': 'age_18_greater'}, inplace=True)
    df_demographic.rename(columns={'demo_age_5_17': 'age_5_17', 'demo_age_17_': 'age_18_greater'}, inplace=True)

    # Merge dataframes
    df_merged_bio_demo = pd.merge(df_biometric,
                                  df_demographic,
                                  on=['date', 'state', 'district', 'pincode'],
                                  how='left',
                                  suffixes=('_biometric', '_demographic'))

    df_combined = pd.merge(df_merged_bio_demo,
                           df_enrolment,
                           on=['date', 'state', 'district', 'pincode'],
                           how='left',
                           suffixes=('_bio_demo', '_enrolment'))

    # Handle NaN values introduced by merging
    age_columns_to_fill = [
        'age_5_17_demographic',
        'age_18_greater_demographic',
        'age_0_5',
        'age_5_17',
        'age_18_greater'
    ]

    for col in age_columns_to_fill:
        if col in df_combined.columns:
            df_combined[col] = df_combined[col].fillna(0).astype(int)

    # Create total activity columns
    df_combined['total_biometric_activity'] = df_combined['age_5_17_biometric'] + df_combined['age_18_greater_biometric']
    df_combined['total_demographic_activity'] = df_combined['age_5_17_demographic'] + df_combined['age_18_greater_demographic']
    df_combined['total_enrolment_activity'] = df_combined['age_0_5'] + df_combined['age_5_17'] + df_combined['age_18_greater']
    
    # Convert state and district to category type after merging and standardization
    df_combined['state'] = df_combined['state'].astype('category')
    df_combined['district'] = df_combined['district'].astype('category')

    return df_combined

df_combined = load_and_preprocess_data()

st.write("Data loaded and preprocessed successfully!")
st.write(df_combined.head())

st.sidebar.header('Filter Data')

# State Filter
all_states = df_combined['state'].unique().tolist()
selected_states = st.sidebar.multiselect(
    'Select State(s)',
    options=all_states,
    default=[]
)

# District Filter
if selected_states:
    filtered_districts = df_combined[df_combined['state'].isin(selected_states)]['district'].unique().tolist()
else:
    filtered_districts = df_combined['district'].unique().tolist()

selected_districts = st.sidebar.multiselect(
    'Select District(s)',
    options=filtered_districts,
    default=[]
)

# Date Range Slider
min_date = df_combined['date'].min().to_pydatetime().date()
max_date = df_combined['date'].max().to_pydatetime().date()

date_range = st.sidebar.date_input(
    'Select Date Range',
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filters
df_filtered = df_combined.copy()

if selected_states:
    df_filtered = df_filtered[df_filtered['state'].isin(selected_states)]

if selected_districts:
    df_filtered = df_filtered[df_filtered['district'].isin(selected_districts)]

if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df_filtered[(df_filtered['date'].dt.date >= start_date) & (df_filtered['date'].dt.date <= end_date)]

st.subheader('Filtered Data Overview')
st.write(f"Number of records after applying filters: {len(df_filtered)}")
st.write(df_filtered.head())

st.subheader('Activity Distribution by State')
if not df_filtered.empty:
    state_activity = df_filtered.groupby('state')[['total_biometric_activity', 'total_demographic_activity', 'total_enrolment_activity']].sum()

    fig1, axes = plt.subplots(3, 1, figsize=(12, 18))

    # Top 10 States by Total Biometric Activity
    top_10_biometric = state_activity.sort_values(by='total_biometric_activity', ascending=False).head(10)
    sns.barplot(x=top_10_biometric.index, y=top_10_biometric['total_biometric_activity'], palette='viridis', ax=axes[0])
    axes[0].set_title('Top 10 States by Total Biometric Activity')
    axes[0].set_xlabel('State')
    axes[0].set_ylabel('Total Biometric Activity')
    axes[0].tick_params(axis='x', rotation=45, ha='right')

    # Top 10 States by Total Demographic Activity
    top_10_demographic = state_activity.sort_values(by='total_demographic_activity', ascending=False).head(10)
    sns.barplot(x=top_10_demographic.index, y=top_10_demographic['total_demographic_activity'], palette='magma', ax=axes[1])
    axes[1].set_title('Top 10 States by Total Demographic Activity')
    axes[1].set_xlabel('State')
    axes[1].set_ylabel('Total Demographic Activity')
    axes[1].tick_params(axis='x', rotation=45, ha='right')

    # Top 10 States by Total Enrolment Activity
    top_10_enrolment = state_activity.sort_values(by='total_enrolment_activity', ascending=False).head(10)
    sns.barplot(x=top_10_enrolment.index, y=top_10_enrolment['total_enrolment_activity'], palette='cividis', ax=axes[2])
    axes[2].set_title('Top 10 States by Total Enrolment Activity')
    axes[2].set_xlabel('State')
    axes[2].set_ylabel('Total Enrolment Activity')
    axes[2].tick_params(axis='x', rotation=45, ha='right')

    plt.tight_layout()
    st.pyplot(fig1)
else:
    st.warning('No data available for selected filters to display state activity.')

st.subheader('Overall Activity by Age Group')
if not df_filtered.empty:
    df_filtered['total_activity_age_0_5'] = df_filtered['age_0_5']
    df_filtered['total_activity_age_5_17'] = df_filtered['age_5_17_biometric'] + df_filtered['age_5_17_demographic'] + df_filtered['age_5_17']
    df_filtered['total_activity_age_18_greater'] = df_filtered['age_18_greater_biometric'] + df_filtered['age_18_greater_demographic'] + df_filtered['age_18_greater']

    overall_age_group_activity = df_filtered[['total_activity_age_0_5', 'total_activity_age_5_17', 'total_activity_age_18_greater']].sum()

    fig2 = plt.figure(figsize=(10, 6))
    sns.barplot(x=overall_age_group_activity.index, y=overall_age_group_activity.values, palette='plasma')
    plt.title('Overall Sum of Activity by Age Group')
    plt.xlabel('Age Group')
    plt.ylabel('Total Activity Count')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig2)
else:
    st.warning('No data available for selected filters to display overall age group activity.')

st.subheader('Temporal Trends of Aadhaar Activities')
if not df_filtered.empty:
    df_filtered['year'] = df_filtered['date'].dt.year
    df_filtered['month'] = df_filtered['date'].dt.month

    temporal_activity = df_filtered.groupby(['year', 'month'])[['total_biometric_activity', 'total_demographic_activity', 'total_enrolment_activity']].sum()

    fig3 = plt.figure(figsize=(12, 7))
    temporal_activity.plot(kind='line', ax=plt.gca())
    plt.title('Temporal Trends of Aadhaar Activities')
    plt.xlabel('Date (Year-Month)')
    plt.ylabel('Total Activity Count')
    plt.legend(title='Activity Type')
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig3)
else:
    st.warning('No data available for selected filters to display temporal trends.')

st.subheader('Correlation Matrix of Activity Types at District Level')
if not df_filtered.empty:
    # Ensure the required columns exist before attempting to group and sum
    required_cols = ['total_biometric_activity', 'total_demographic_activity', 'total_enrolment_activity']
    if all(col in df_filtered.columns for col in required_cols):
        district_level_activity_correlation = df_filtered.groupby('district')[required_cols].sum()

        if not district_level_activity_correlation.empty and len(district_level_activity_correlation.columns) > 1:
            correlation_matrix = district_level_activity_correlation.corr()

            fig4 = plt.figure(figsize=(8, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
            plt.title('Correlation Matrix of Activity Types at District Level')
            st.pyplot(fig4)
        else:
            st.warning('Not enough data or columns to compute correlation matrix for selected filters.')
    else:
        st.warning('Required activity columns not found in filtered data.')
else:
    st.warning('No data available for selected filters to display correlation matrix.')

st.subheader('Actionable Insights and Solution Frameworks')

st.markdown("""
### Summary of Key Findings, Patterns, Trends, and Anomalies

1.  **Data Quality and Missing Values:**
    *   **Finding:** The initial datasets (`df_biometric`, `df_demographic`, `df_enrolment`) had no intrinsic missing values. However, merging these datasets resulted in significant `NaN` values for demographic and enrolment data where corresponding records were absent in the biometric dataset. These `NaN`s were subsequently imputed with `0`, assuming no activity.
    *   **Anomaly:** The presence of a large number of `NaN`s post-merge indicates a lack of complete overlap in `(date, state, district, pincode)` combinations across the datasets. This implies that not all demographic and enrolment activities are recorded or linked to biometric updates for every location and date combination.

2.  **Outlier Analysis:**
    *   **Finding:** A substantial number of outliers were detected in all numerical age-group activity columns across all datasets (e.g., up to 11.8% in `age_5_17` from `df_enrolment`). These outliers represent significantly higher activity counts than the interquartile range suggests.
    *   **Pattern/Anomaly:** These extreme values could signify genuine high-volume activity in certain areas/times or potential data entry errors/systematic issues. Given their prevalence, simply removing them would lead to substantial data loss.

3.  **Geographical Distribution (State and District Level):**
    *   **Finding:** Activity levels (biometric, demographic, enrolment) vary significantly by state and district. Maharashtra, Uttar Pradesh, and Tamil Nadu consistently appear as top states for biometric and demographic activities, while Uttar Pradesh, Bihar, and Madhya Pradesh lead in enrolment activities. At the district level, cities like Nashik, Thane, Pune, and South 24 Parganas show high activity.
    *   **Pattern:** Concentrated pockets of high activity indicate specific regions driving a large volume of Aadhaar-related operations. The top districts often correlate with major urban centers or densely populated areas.

4.  **Temporal Trends:**
    *   **Finding:** The data spans a relatively short period (mostly September to November 2025). The monthly aggregation shows a peak in October 2025 for all activity types (`total_biometric_activity`, `total_demographic_activity`, `total_enrolment_activity`). Daily trends show considerable fluctuation.
    *   **Pattern/Trend:** There's a clear short-term trend of increased activity in October. This could be due to specific campaigns, reporting cycles, or data collection periods.

5.  **Activity Distribution by Age Group:**
    *   **Finding:** The `age_18_greater` group shows the highest total activity (6.1 million), followed by `age_5_17` (4.1 million), and then `age_0_5` (0.38 million). This suggests that adults and school-aged children are the primary groups engaging in Aadhaar activities.
    *   **Pattern:** A higher focus on adult and school-aged groups is evident, possibly reflecting initial enrolment drives or update requirements for these demographics.

6.  **Correlations Between Activity Types:**
    *   **Finding:** Strong positive correlations exist between `total_biometric_activity`, `total_demographic_activity`, and `total_enrolment_activity` at the district level (e.g., correlation between biometric and demographic activity is 0.81, between demographic and enrolment is 0.78). This suggests that districts with high activity in one area tend to have high activity in others.
    *   **Pattern:** These correlations imply a synchronized effort or a common underlying factor driving all types of Aadhaar-related activities within a given district.

7.  **Anomaly Detection (District-Level):**
    *   **Finding:** Numerous districts were identified as anomalous (outliers) based on their total activity levels using the IQR method. For example, 49 districts for biometric activity, 70 for demographic, and 36 for enrolment activities fell outside the calculated bounds.
    *   **Anomaly:** These anomalous districts are performing significantly different from the majority. This could indicate regions with exceptional operational efficiency, successful outreach programs, or, conversely, data inconsistencies requiring further scrutiny.
""")

st.markdown("""
### Actionable Insights and Solution Frameworks

1.  **Insight: Incomplete Data Linkage Across Datasets.**
    *   **Actionable Insight:** The non-overlapping records post-merge indicate a potential gap in comprehensive data collection or reporting across different Aadhaar operations. It's crucial to understand why certain `(date, state, district, pincode)` combinations appear in one dataset but not others.
    *   **Proposed Solution Frameworks:**
        *   **Data Governance Enhancement:** Implement stricter data collection and reporting protocols to ensure all related Aadhaar activities are consistently captured and linked across different operational datasets.
        *   **System Integration:** Explore technical solutions for better integration between biometric, demographic, and enrolment data systems to minimize data silos and ensure comprehensive record linkage.
        *   **Root Cause Analysis:** Conduct a deep dive to identify specific reasons for data discrepancies (e.g., different reporting frequencies, system errors, operational gaps) in locations with high missing values post-merge.

2.  **Insight: Significant Outliers in Activity Counts.**
    *   **Actionable Insight:** The high volume of outlier activity counts suggests either exceptionally efficient operational centers or data quality issues. Understanding the nature of these outliers is key to distinguishing success from potential problems.
    *   **Proposed Solution Frameworks:**
        *   **Performance Benchmarking:** Investigate high-activity outlier locations to identify best practices that can be replicated in other areas.
        *   **Anomaly Investigation Protocol:** Establish a clear protocol for investigating significant spikes or drops in activity. This includes checking for data entry errors, system malfunctions, or fraudulent activities.
        *   **Adaptive Resource Allocation:** Use outlier identification to predict and prepare for high demand in certain regions or during specific periods, allowing for proactive resource allocation (staff, equipment).

3.  **Insight: Geographical Activity Hotspots.**
    *   **Actionable Insight:** Activities are highly concentrated in specific states and districts. This indicates varying levels of engagement or operational capacity across regions.
    *   **Proposed Solution Frameworks:**
        *   **Targeted Resource Deployment:** Allocate resources (personnel, infrastructure, awareness campaigns) proportionally to the identified hotspots and underserved areas. For instance, districts with low enrolment but high biometric/demographic updates might need enrolment drives.
        *   **Regional Strategy Development:** Develop localized strategies addressing the unique needs and challenges of high-activity vs. low-activity regions.
        *   **Performance Monitoring:** Continuously monitor activity levels in these hotspots to ensure sustained performance and address any emerging issues.

4.  **Insight: Temporal Activity Fluctuations.**
    *   **Actionable Insight:** The observed surge in activity in October 2025 suggests either a seasonal pattern or the impact of specific, time-bound initiatives. Understanding the drivers of these fluctuations is crucial for planning.
    *   **Proposed Solution Frameworks:**
        *   **Campaign Optimization:** Analyze past campaigns or policy changes that might have led to activity surges to optimize future initiatives.
        *   **Capacity Planning:** Predict future peak periods based on historical trends and allocate resources accordingly to avoid bottlenecks and improve service delivery.
        *   **Real-time Monitoring:** Implement dashboards for real-time monitoring of activity trends to quickly identify and respond to unexpected spikes or drops.

5.  **Insight: Age-Group Specific Engagement.**
    *   **Actionable Insight:** The disproportionately high activity in older age groups (`age_18_greater` and `age_5_17`) suggests a strong focus or need in these demographics. The lower activity in `age_0_5` might indicate challenges in initial enrolment for infants and toddlers.
    *   **Proposed Solution Frameworks:**
        *   **Targeted Outreach for `age_0_5`:** Develop specific programs or simplify processes to encourage early Aadhaar enrolment for children (0-5 years), potentially linking it with birth registration or early childhood care services.
        *   **Policy Review:** Review current policies and requirements for different age groups to ensure they are effective and address the needs of each demographic.
        *   **Communication Strategy:** Tailor communication and awareness campaigns to specific age groups, highlighting the benefits and requirements relevant to them.

6.  **Insight: Interconnected Activities at District Level.**
    *   **Actionable Insight:** The strong correlations between different activity types at the district level mean that efforts to boost one type of activity (e.g., enrolment) are likely to positively impact others (e.g., biometric updates). This suggests a holistic approach to operational planning.
    *   **Proposed Solution Frameworks:**
        *   **Integrated Campaign Design:** Design and launch integrated campaigns that promote all Aadhaar-related services (enrolment, biometric updates, demographic updates) concurrently.
        *   **Cross-Functional Team Collaboration:** Encourage better collaboration between different operational teams responsible for biometric, demographic, and enrolment activities at the district level.
        *   **Performance Incentives:** Implement incentives or recognition programs for districts that show balanced improvement across all activity types.
""")

st.markdown("""
### Overall Conclusion:

This analysis reveals a robust, though imperfect, system for Aadhaar data management. While data collection is comprehensive in terms of non-null values within individual datasets, challenges arise in cross-dataset consistency and the handling of extreme activity volumes. By addressing data integration gaps, understanding and leveraging geographical and temporal patterns, and investigating anomalies, decision-makers can optimize resource allocation, enhance operational efficiency, and ensure a more inclusive and reliable Aadhaar system for all age groups.
""")

st.markdown("""
Welcome to the Aadhaar Data Analysis Dashboard. This application provides insights into biometric, demographic, and enrolment activities across India.
Use the sidebar filters to explore data by state, district, and date range.
""")
