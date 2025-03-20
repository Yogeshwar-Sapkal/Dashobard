import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import google.generativeai as genai

# Step 1: Load the dataset
df1 = pd.read_csv("/deliverd_properties_mar1.csv")
df2 = pd.read_csv("/deliverd_properties_mar2.csv")

# Step 4: Build Interactive Dashboard in Streamlit
st.title("GenAI-Enhanced Interactive Dashboard")
st.subheader("Top City for A+ Assets")
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
city1 = df1['City'].value_counts()
city2 = df2['City'].value_counts()

# Create a Matplotlib figure
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# First Bar Chart
axes[0].bar(city1.index, city1.values, color='royalblue')
axes[0].set_xlabel("City", fontsize=12)
axes[0].set_ylabel("Number of Properties Delivered", fontsize=12)
axes[0].set_title("Number of Properties Delivered In Texas (LU & UC/LU)", fontsize=14)
axes[0].tick_params(axis='x', rotation=55)  # Rotate labels for better readability
axes[0].grid(axis='y', linestyle="--", alpha=0.7)

# Second Bar Chart
axes[1].bar(city2.index, city2.values, color='tomato')
axes[1].set_xlabel("City", fontsize=12)
axes[1].set_ylabel("Number of Properties Delivered", fontsize=12)
axes[1].set_title("Number of Properties Delivered In Texas (Second Dataset)", fontsize=14)
axes[1].tick_params(axis='x', rotation=55)
axes[1].grid(axis='y', linestyle="--", alpha=0.7)

# Adjust layout
plt.tight_layout()

# **Embed Matplotlib figure in Streamlit**
st.pyplot(fig)


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



