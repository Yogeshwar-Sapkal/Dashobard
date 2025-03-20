import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import google.generativeai as genai

# Step 1: Load the dataset
df1 = pd.read_csv("delivered_properties_mar1.csv")
df2 = pd.read_csv("delivered_properties_mar2.csv")

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


# Step 5: Integrate GenAI Query (Using OpenAI API)
genai.configure(api_key="AIzaSyBLwMYymhJRNyJtJK9ah_s9R_WMRpEVuns") # Replace with actual API Key
def generate_insight(question, data_summary):
    """Generate insights using Google Gemini API."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    response = model.generate_content(f"Analyze the following data summary and answer: {question}\n\n{data_summary}")
    
    return response.text

st.subheader("Ask the AI")
user_question = st.text_input("Enter your question about the dataset:")
if user_question:
    insight = generate_insight(user_question, df1.describe().to_string())
    st.write(insight)



