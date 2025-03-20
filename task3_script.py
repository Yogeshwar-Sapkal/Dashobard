import pandas as pd
import streamlit as st
import plotly.express as px
import google.generativeai as genai

# Step 1: Load the dataset
# # file_path = "Asset.xlsx"  # Ensure the dataset is uploaded to your environment
# df = pd.read_excel("Assessment/raw_data/leaseup/MSA1.xlsx", header = 2, sheet_name="Asset Class")
# # df.columns = df.iloc[0]
# # df = df[1:].reset_index(drop=True)

# # Step 2: Select relevant columns
# df = df[['MarketName', 'StateName', 'CountyName', 'Latitude', 'Longitude'] + list(df.columns[-12:])]
# df.columns = ['MarketName', 'StateName', 'CountyName', 'Latitude', 'Longitude'] + [f"{col}" for col in df.columns[5:]]

# # Step 3: Process data for KPIs
# df_melted = df.melt(id_vars=['MarketName', 'StateName', 'CountyName', 'Latitude', 'Longitude'],
#                      var_name="Month", value_name="Asset_Rating")

# df_a_plus = df_melted[df_melted["Asset_Rating"] == "A+"]
# a_plus_count = df_a_plus.groupby("MarketName").size().reset_index(name="A+ Count")
# top_city = a_plus_count.sort_values("A+ Count", ascending=False).iloc[0]
data = {
    "MarketName": ["New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ"],
    "StateName": ["New York", "California", "Illinois", "Texas", "Arizona"],
    "CountyName": ["New York", "Los Angeles", "Cook", "Harris", "Maricopa"],
    "Latitude": [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
    "Longitude": [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
    "A+ Count": [120, 95, 80, 110, 85]
}

df = pd.DataFrame(data)

# Step 4: Build Interactive Dashboard in Streamlit
st.title("GenAI-Enhanced Interactive Dashboard")
st.subheader("Top City for A+ Assets")
# st.write(f"**{top_city['MarketName']}** has the highest number of A+ assets: **{top_city['A+ Count']}**")
st.write(df)

# Interactive Chart
# chart_type = st.selectbox("Select Chart Type", ["Scatter", "Bar", "Line"])
# x_axis = st.selectbox("Select X-Axis", df.columns[:5])
# y_axis = "A+ Count"

# df_chart = a_plus_count.copy()
# if chart_type == "Scatter":
#     fig = px.scatter(df_chart, x=x_axis, y=y_axis)
# elif chart_type == "Bar":
#     fig = px.bar(df_chart, x=x_axis, y=y_axis)
# else:
#     fig = px.line(df_chart, x=x_axis, y=y_axis)

# st.plotly_chart(fig)
chart_type = st.selectbox("Select Chart Type", ["Scatter", "Bar", "Line"])
x_axis = st.selectbox("Select X-Axis", ["MarketName", "StateName"])
y_axis = "A+ Count"

if chart_type == "Scatter":
    fig = px.scatter(df, x=x_axis, y=y_axis)
elif chart_type == "Bar":
    fig = px.bar(df, x=x_axis, y=y_axis)
else:
    fig = px.line(df, x=x_axis, y=y_axis)

st.plotly_chart(fig)

# Step 5: Integrate GenAI Query (Using OpenAI API)
genai.configure(api_key="AIzaSyBLwMYymhJRNyJtJK9ah_s9R_WMRpEVuns") # Replace with actual API Key
# available_models = [model.name for model in genai.list_models()]
# print("Available models:", available_models)
def generate_insight(question, data_summary):
    """Generate insights using Google Gemini API."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    response = model.generate_content(f"Analyze the following data summary and answer: {question}\n\n{data_summary}")
    
    return response.text
# def generate_insight(question, data_summary):
#     prompt = f"Analyze the following data summary and answer: {question}\n\n{data_summary}"
#     response = genai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role": "system", "content": "You are an AI data analyst."},
#                   {"role": "user", "content": prompt}]
#     )
#     return response["choices"][0]["message"]["content"]

st.subheader("Ask the AI")
user_question = st.text_input("Enter your question about the dataset:")
if user_question:
    insight = generate_insight(user_question, df.describe().to_string())
    st.write(insight)

# Step 6: Deployment Instructions
st.markdown("### Deployment Steps")
st.markdown("1. Push this script to a GitHub repository.")
st.markdown("2. Set up a Streamlit Cloud account and link the repo.")
st.markdown("3. Deploy and obtain the public link.")

# Step 7: Reflection
st.markdown("### Reflection")
st.write("**Advantages:** Real-time insights, interactivity, AI-powered analysis.")
st.write("**Limitations:** Model bias, API costs, response latency.")
st.write("**Ethical Considerations:** Data privacy, AI hallucinations, decision impact.")



