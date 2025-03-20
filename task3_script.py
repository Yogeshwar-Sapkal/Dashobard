import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import plotly.express as px
import google.generativeai as genai

# Step 1: Load the dataset
df1 = pd.read_csv("delivered_properties_mar1.csv")
df2 = pd.read_csv("delivered_properties_mar2.csv")

df3 = pd.read_csv("leaseup_market1.csv")
df4 = pd.read_csv("leaseup_market2.csv")

# Step 4: Build Interactive Dashboard in Streamlit
st.title("GenAI-Enhanced Interactive Dashboard")
st.subheader("Property Lease-Up Analysis")
st.write(df1.head())
st.write(df2.head())

# Interactive Chart
# chart_type = st.selectbox("Select Chart Type", ["Scatter", "Bar", "Line"])
# x_axis = st.selectbox("Select X-Axis", ["MarketName", "StateName"])
# y_axis = "A+ Count"

# if chart_type == "Scatter":
#     fig = px.scatter(df, x=x_axis, y=y_axis)
# elif chart_type == "Bar":
#     fig = px.bar(df, x=x_axis, y=y_axis)
# else:
#     fig = px.line(df, x=x_axis, y=y_axis)

# st.plotly_chart(fig)
city1_counts = df1['City'].value_counts().reset_index()
city1_counts.columns = ['City', 'Number of Properties']

city2_counts = df2['City'].value_counts().reset_index()
city2_counts.columns = ['City', 'Number of Properties']

# Create interactive bar charts using Plotly
fig1 = px.bar(city1_counts, x='City', y='Number of Properties', 
              title="Number of Properties Delivered In Texas (LU & UC/LU)",
              labels={'City': 'City', 'Number of Properties': 'Delivered Properties'},
              color='Number of Properties', color_continuous_scale='blues')

fig2 = px.bar(city2_counts, x='City', y='Number of Properties', 
              title="Number of Properties Delivered In Ohio (LU & UC/LU)",
              labels={'City': 'City', 'Number of Properties': 'Delivered Properties'},
              color='Number of Properties', color_continuous_scale='reds')

# Display the interactive charts in Streamlit
# st.subheader("Texas Property Delivery Analysis")
st.plotly_chart(fig1)
st.plotly_chart(fig2)

combined_df = pd.DataFrame({
    'LeaseupTime': np.concatenate([df3['LeaseupTime'], df4['LeaseupTime']]),
    'Market': ['Market 1'] * len(df3['LeaseupTime']) + ['Market 2'] * len(df4['LeaseupTime'])
})

# Create an interactive boxplot using Plotly
fig = px.box(combined_df, x='Market', y='LeaseupTime', color='Market',
             title="Distribution of Lease-Up Time Across Markets",
             labels={'LeaseupTime': 'Lease-Up Time (Months)', 'Market': 'Market'},
             boxmode='group', 
             template="plotly_white")

# Display the interactive chart in Streamlit
st.subheader("Interactive Lease-Up Time Distribution")
st.plotly_chart(fig)


# Step 5: Integrate GenAI Query (Using OpenAI API)
genai.configure(api_key="AIzaSyD5ZXQnhHypL6lbjvi94GQIfcfmGc0dC2U") # Replace with actual API Key
def generate_insight(user_question, summary):
    """Generate AI insights using Google Gemini API with full dashboard context."""
    model = genai.GenerativeModel("gemini-1.5-pro")  # Ensure the correct model

    prompt = f"""
    You are an AI assistant helping users analyze a real estate dashboard. 
    The dashboard contains multiple datasets and visualizations related to property markets.
    
    Here are the key insights available:
    
    **Dataset 1 - Market 1 Properties:**
    {df1.describe().to_string()}
    
    **Dataset 2 - Market 2 Properties:**
    {df2.describe().to_string()}
    
    **Dataset 3 - Market 1 Properties:**
    {df3.describe().to_string()}

    **Dataset 4 - Market 2 Properties:**
    {df3.describe().to_string()}

    **Key Visualizations:**
    - A bar chart showing the number of delivered properties per city.
    - A boxplot showing lease-up time distribution across different markets.
    
    Answer the following question based on all available insights:
    
    **User Question:** {user_question}
    """

    response = model.generate_content(prompt)
    return response.text

st.subheader("Ask the AI")
user_question = st.text_input("Enter your question about the dataset, charts, or insights:")

if user_question:
    insight = generate_insight(user_question, summary="")  # Passing full dashboard context
    st.write(insight)


