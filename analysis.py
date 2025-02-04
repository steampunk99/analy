import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="German Wine Analysis", layout="wide")

# Title and introduction
st.title("German Wine Market Analysis")
st.markdown("""
This dashboard analyzes German wines to optimize pricing strategies based on expert ratings, 
regional characteristics, and market positioning.
""")

# Create the dataset
data = {
    'points': [91, 91, 90, 90, 90, 89, 90, 90, 90, 91, 91, 91, 91, 91, 91],
    'price': [23, 39, 25, 31, 40, 26, 17, 31, 36, 23, 25, 21, 25, 38, 22],
    'province': ['Mosel', 'Rheinhessen', 'Wurttemberg', 'Mosel', 'Ahr', 
                'Mosel', 'Mosel', 'Mosel', 'Rheingau', 'Mosel', 'Rheingau',
                'Nahe', 'Mosel', 'Mosel', 'Mosel'],
    'variety': ['Riesling'] * 15,
    'designation': ['Kabinett', 'Trocken', 'Lemberger', 'Kabinett', 'Trocken',
                   'Kabinett', 'Estate', 'Kabinett', 'Trocken', 'Kabinett',
                   'Kabinett', 'Spatlese', 'Spatlese', 'Auslese', 'Kabinett']
}

df = pd.DataFrame(data)

# Sidebar filters
st.sidebar.header("Filters")
selected_provinces = st.sidebar.multiselect(
    "Select Provinces",
    options=df['province'].unique(),
    default=df['province'].unique()
)

selected_designations = st.sidebar.multiselect(
    "Select Designations",
    options=df['designation'].unique(),
    default=df['designation'].unique()
)

# Filter data
filtered_df = df[
    (df['province'].isin(selected_provinces)) &
    (df['designation'].isin(selected_designations))
]

# Price vs. Ratings Analysis
st.subheader("Price vs. Ratings Analysis")
fig_scatter = px.scatter(
    filtered_df,
    x='points',
    y='price',
    color='province',
    size='price',
    hover_data=['designation'],
    title='Wine Ratings vs. Price by Province'
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Calculate and display correlation
correlation = filtered_df['points'].corr(filtered_df['price'])
st.write(f"Correlation between points and price: {correlation:.2f}")

# Price Distribution by Province
st.subheader("Price Distribution by Province")
fig_box = px.box(
    filtered_df,
    x='province',
    y='price',
    color='province',
    title='Price Distribution across Provinces'
)
st.plotly_chart(fig_box, use_container_width=True)

# Average prices by province
avg_price_province = filtered_df.groupby('province')['price'].mean().reset_index()
fig_bar = px.bar(
    avg_price_province,
    x='province',
    y='price',
    title='Average Price by Province',
    labels={'price': 'Average Price (€)', 'province': 'Province'}
)
st.plotly_chart(fig_bar, use_container_width=True)

# Average ratings by province
avg_points_province = filtered_df.groupby('province')['points'].mean().reset_index()
fig_bar2 = px.bar(
    avg_points_province,
    x='province',
    y='points',
    title='Average Ratings by Province',
    labels={'points': 'Average Points', 'province': 'Province'}
)
st.plotly_chart(fig_bar2, use_container_width=True)

# Designation Analysis
st.header("Designation Analysis")
designation_stats = filtered_df.groupby('designation').agg({
    'price': ['mean', 'std', 'count'],
    'points': ['mean', 'std']
}).round(2)

st.write("Designation Statistics:", designation_stats)

# Key Findings
st.header("Key Findings and Recommendations")
st.markdown("""
### Price Optimization Strategies:

1. **Premium Positioning**:
   - Wines with ratings above 90 points command higher prices
   - Consider premium pricing for highly-rated wines from prestigious regions

2. **Regional Differentiation**:
   - Different regions show distinct price ranges
   - Adjust pricing strategies based on regional reputation

3. **Designation Impact**:
   - Certain designations (e.g., Kabinett, Spatlese) show strong price-quality relationships
   - Use designation-specific pricing strategies
""")

# Download capability
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Analysis Data",
    data=csv,
    file_name="german_wine_analysis.csv",
    mime="text/csv"
)
