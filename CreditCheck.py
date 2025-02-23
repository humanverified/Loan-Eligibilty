import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from joblib import load
from datetime import datetime
model = load('Credit_Check.joblib')
st.title('Check your Loan Eligibilty')
default_dob=datetime(2000,1,1)
dob = st.date_input("Enter Date of Birth",value=default_dob, min_value=datetime(1960, 1, 1), max_value=datetime.today())
dob = datetime.combine(dob, datetime.min.time())
person_age = (datetime.today() - dob).days // 365
st.write(f"You are {person_age} years old")
if person_age<18:
    st.error("You must be at least 18 years old to apply for a loan")
    st.stop()

employment_start_date = st.date_input("Enter Employment Start Date", min_value=datetime(1970, 1, 1), max_value=datetime.today())
employment_start_date = datetime.combine(employment_start_date, datetime.min.time())
person_emp_length = (datetime.today() - employment_start_date).days // 365

person_income = st.number_input('Enter Your Annual Income (£)', min_value=5000, step=1000)

loan_int_rate = st.number_input('Enter Loan Interest Rate (%)', min_value=5, max_value=25)

home_ownership_options = ['OWN', 'MORTGAGE', 'RENT']
person_home_ownership = st.selectbox('Home Ownership Status', home_ownership_options)

loan_intent_options = ['PERSONAL', 'BUSINESS', 'EDUCATION', 'MEDICAL']
loan_intent = st.selectbox('Loan Intent', loan_intent_options)

loan_grade_options = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
loan_grade = st.selectbox('Loan Grade', loan_grade_options)

loan_percent_income = st.number_input('Percentage of Income for Loan Repayment(Monthly)', min_value=1, max_value=100, step=1)
loan_tenure=st.selectbox("Select Loan Tenure(in months)",[6,12,18,24,36])

cb_person_default_on_file = st.selectbox('Previous Loan Default?', ['Yes', 'No'])
cb_person_default_on_file_N = 1 if cb_person_default_on_file == 'N' else 0
cb_person_default_on_file_Y = 1 if cb_person_default_on_file == 'Y' else 0 

loan_status = st.selectbox('Loan Status', ['Fully Paid', 'Charged Off'])
loan_status = 1 if loan_status == 'Fully Paid' else 0  

label_encoders = {
    "person_home_ownership": LabelEncoder(),
    "loan_intent": LabelEncoder(),
    "loan_grade": LabelEncoder()
}

label_encoders["person_home_ownership"].fit(home_ownership_options)
label_encoders["loan_intent"].fit(loan_intent_options)
label_encoders["loan_grade"].fit(loan_grade_options)

person_home_ownership = label_encoders["person_home_ownership"].transform([person_home_ownership])[0]
loan_intent = label_encoders["loan_intent"].transform([loan_intent])[0]
loan_grade = label_encoders["loan_grade"].transform([loan_grade])[0]

user_input = np.array([[person_age, person_income, person_home_ownership, person_emp_length,
                        loan_intent, loan_grade, loan_int_rate, loan_status, 
                        loan_percent_income, cb_person_default_on_file_N,cb_person_default_on_file_Y]])

predicted_loan_amount = model.predict(user_input)

if st.button("Check Loan Eligibility"):
    predicted_loan_amount = model.predict(user_input)
    if predicted_loan_amount[0] < 0:
        st.error("You are not eligible for a loan.")
    else:
        st.write(f"### You can Borrow upto: £{predicted_loan_amount[0]:,.2f}")

if predicted_loan_amount[0] > 0:
    principal_amount = predicted_loan_amount[0]
    annual_interest_rate = loan_int_rate  
    monthly_interest_rate = (annual_interest_rate / 100) / 12  
    loan_tenure_months = loan_tenure  
    emi = (principal_amount * monthly_interest_rate * (1 + monthly_interest_rate)**loan_tenure_months) / ((1 + monthly_interest_rate)**loan_tenure_months - 1)
    st.write(f"### Your estimated monthly EMI is: £{emi:,.2f}")
st.markdown("<hr>", unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])  
with col1:
    st.markdown("### Created by Adwaith Kalathuru")
with col2:
    st.image("image0.jpeg", width=100)

                                                                                                         
