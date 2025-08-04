import streamlit as st
import requests
import json

# --- CONFIG ---
API_KEY = 'NWJdt80jQF4jom1_0G9UBJSFDqeWDxC5tDLHyxYOj71n'
DEPLOYMENT_URL = 'https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/ec0968dd-d54d-4802-9bbf-6df989b4e645/predictions?version=2021-05-01'

# --- Token Function ---
@st.cache_data(show_spinner=False)
def get_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"apikey={api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

# --- Streamlit UI ---
st.title("PMGSY Scheme Classifier")

with st.form("input_form"):
    st.subheader("Enter the Details:")

    state = st.selectbox("State Name", [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal"
])
    district = st.text_input("District Name", value="Kamrup Rural")
    road_works = st.number_input("No. of Road Works Sanctioned", min_value=0)
    road_length = st.number_input("Length of Road Work Sanctioned (km)",format='%.5f', min_value=0.0)
    bridges_sanctioned = st.number_input("No. of Bridges Sanctioned", min_value=0)
    cost = st.number_input("Cost of Works Sanctioned (INR)",format='%.5f', min_value=0.0)
    road_completed = st.number_input("No. of Road Works Completed", min_value=0)
    road_length_completed = st.number_input("Length of Road Work Completed (km)",format='%.5f', min_value=0.0)
    bridges_completed = st.number_input("No. of Bridges Completed", min_value=0)
    expenditure = st.number_input("Expenditure Occurred (INR)",format='%.5f', min_value=0.0)
    road_balance = st.number_input("No. of Road Works Balance", min_value=0)
    road_length_balance = st.number_input("Length of Road Work Balance (km)",format='%.5f', min_value=0.0)
    bridges_balance = st.number_input("No. of Bridges Balance", min_value=0)

    submitted = st.form_submit_button("Predict Scheme")

# --- Prediction ---
if submitted:
    st.info("Sending data to IBM AutoML model...")

    try:
        token = get_token(API_KEY)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # Build payload as per your model’s structure
        payload = {
            "input_data": [{
                "fields": [
                    "STATE_NAME",
                    "DISTRICT_NAME",
                    "NO_OF_ROAD_WORK_SANCTIONED",
                    "LENGTH_OF_ROAD_WORK_SANCTIONED",
                    "NO_OF_BRIDGES_SANCTIONED",
                    "COST_OF_WORKS_SANCTIONED",
                    "NO_OF_ROAD_WORKS_COMPLETED",
                    "LENGTH_OF_ROAD_WORK_COMPLETED",
                    "NO_OF_BRIDGES_COMPLETED",
                    "EXPENDITURE_OCCURED",
                    "NO_OF_ROAD_WORKS_BALANCE",
                    "LENGTH_OF_ROAD_WORK_BALANCE",
                    "NO_OF_BRIDGES_BALANCE"
                ],
                "values": [[
                    state, district, road_works, road_length, bridges_sanctioned,
                    cost, road_completed, road_length_completed, bridges_completed,
                    expenditure, road_balance, road_length_balance, bridges_balance
                ]]
            }]
        }

        response = requests.post(DEPLOYMENT_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            prediction = result['predictions'][0]['values'][0][0]
            st.success(f"✅ Predicted PMGSY Scheme: **{prediction}**")
        else:
            st.error(f"❌ Failed: {response.text}")


    

    except Exception as e:

        st.error(f"🚨 Error: {e}")
