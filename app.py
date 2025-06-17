# app.py

import streamlit as st
from datetime import date
import pandas as pd
from io import StringIO
# import boto3 # We comment this out for now to avoid errors if you don't have AWS configured

# --- UI Configuration & Styling ---
st.set_page_config(page_title="Data Access AI Agent", layout="wide")

# --- Data Field Definitions ---
# These are the fields for your selection tables
interest_income_fields = [
    "loans_secured_by_real_estate", "commercial_and_industrial_loans",
    "loans_to_individuals", "all_other_loans", "lease_financing_receivables",
    "balances_due_from_depository", "securities", "other_interest_income"
]
interest_expense_fields = [
    "deposits", "federal_funds_purchased", "trading_liabilities", "subordinated_notes"
]
noninterest_income_fields = [
    "fiduciary_activities", "service_charges", "trading_revenue",
    "securities_related_activities", "net_servicing_fees", "net_securitization_income",
    "net_gains_on_sales", "other_noninterest_income"
]
noninterest_expense_fields = [
    "salaries_and_benefits", "premises_and_fixed_assets",
    "amortization_expense", "other_noninterest_expense"
]

# --- Session State Initialization ---
if 'show_view_ui' not in st.session_state:
    st.session_state.show_view_ui = False
if 'show_s3_ui' not in st.session_state:
    st.session_state.show_s3_ui = False
if 'show_table_ui' not in st.session_state:
    st.session_state.show_table_ui = False
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'show_api_ui' not in st.session_state:
    st.session_state.show_api_ui = False
if 'show_history_ui' not in st.session_state:
    st.session_state.show_history_ui = False
if 'show_api_history_ui' not in st.session_state:
    st.session_state.show_api_history_ui = False
# --- NEW: State for pre-selecting fields and clearing input text ---
if 'preselected_fields' not in st.session_state:
    st.session_state.preselected_fields = []
if 'agent_input_text' not in st.session_state:
    st.session_state.agent_input_text = ""


# --- Central function to reset the UI state ---
def reset_all_states():
    """
    Resets all session state variables to their default values to return
    to the initial UI.
    """
    st.session_state.show_view_ui = False
    st.session_state.show_s3_ui = False
    st.session_state.show_table_ui = False
    st.session_state.show_api_ui = False
    st.session_state.show_history_ui = False
    st.session_state.show_api_history_ui = False
    st.session_state.questions = []
    st.session_state.answers = []
    # --- MODIFIED: Clear preselected fields and input text on reset ---
    st.session_state.preselected_fields = []
    st.session_state.agent_input_text = ""


# --- UI Rendering Functions ---

def show_agent_ui():
    """Displays the initial AI agent chat interface."""
    st.title("Data Access AI Agent")

    # --- MODIFIED: The text input is now controlled by session state ---
    st.text_input(
        "Ask the AI agent to create a data access view or file:",
        key="agent_input_text"
    )
    user_question = st.session_state.agent_input_text

    if st.button("Submit"):
        # Clear previous UI state before processing new prompt
        st.session_state.show_view_ui = False
        st.session_state.show_s3_ui = False
        st.session_state.show_api_ui = False
        st.session_state.show_history_ui = False
        st.session_state.show_api_history_ui = False
        st.session_state.preselected_fields = [] # Reset selections

        if user_question:
            st.session_state.questions.append(user_question)
            lower_question = user_question.lower()

            # # --- NEW: Logic to parse prompt and pre-select fields ---
            # fields_to_select = []
            # if "interest" in lower_question and "income" in lower_question:
            #     fields_to_select.extend(interest_income_fields)
            # if "interest" in lower_question and "expense" in lower_question:
            #     fields_to_select.extend(interest_expense_fields)
            # if "noninterest" in lower_question and "income" in lower_question:
            #     fields_to_select.extend(noninterest_income_fields)
            # if "noninterest" in lower_question and "expense" in lower_question:
            #     fields_to_select.extend(noninterest_expense_fields)
            
            # if fields_to_select:
            #     st.session_state.preselected_fields = fields_to_select

            # --- Main prompt routing ---
            if "history" in lower_question and "rest api" in lower_question:
                response = "Displaying the last ten REST API calls."
                st.session_state.answers.append(response)
                st.session_state.show_api_history_ui = True
            elif "history" in lower_question:
                response = "Displaying the last ten view calls."
                st.session_state.answers.append(response)
                st.session_state.show_history_ui = True
            elif "create a view" in lower_question:
                response = "Understood. Please review the generated UI below and check the data elements you want to include in the view."
                st.session_state.answers.append(response)
                st.session_state.show_view_ui = True
            elif "s3 file" in lower_question:
                response = "Please review the generated UI and uncheck all the data elements that you don't want to include in the S3 file."
                st.session_state.answers.append(response)
                st.session_state.show_s3_ui = True
            elif "rest api" in lower_question:
                response = "Please review the generated UI and uncheck all the data elements that you don't want to include."
                st.session_state.answers.append(response)
                st.session_state.show_api_ui = True
            else:
                response = "I'm sorry, I have limited functions. Please try another prompt."
                st.session_state.answers.append(response)

            st.rerun()

    if st.session_state.questions:
        st.divider()
        st.write(f"**You:** {st.session_state.questions[-1]}")
        st.write(f"**Agent:** {st.session_state.answers[-1]}")

def show_api_history_ui():
    """Displays the last ten REST API calls in a custom table."""
    st.divider()
    st.subheader("History of Last 10 REST API Calls")
    # (The rest of the function remains the same as your provided code)
    data = {
        'REST API Name': ["GetRESTAllIncomeData", "GetRESTLoanPortfolioMetrics", "GetRESTDepositAccountSummary", "GetRESTCreditRiskAnalysis", "GetRESTRegulatoryReporting", "GetRESTBranchMetrics", "GetRESTNonPerformingLoans", "GetRESTFeeRevenueData", "GetRESTLiquidityMetrics", "GetRESTInterestRateData"],
        'Access Timestamp': ["6/16/2025 18:00", "6/16/2025 17:22", "6/16/2025 16:45", "6/16/2025 15:30", "6/16/2025 14:15", "6/15/2025 18:08", "6/15/2025 17:33", "6/15/2025 16:45", "6/15/2025 15:20", "6/15/2025 14:55"],
        'Accessed By': ["KellyMorgan", "JamesWilson", "EmilyDavis", "MichaelBrown", "SarahJohnson", "DanielMiller", "LindaGarcia", "ChristopherLee", "JessicaClark", "AnthonyMartinez"],
        'Business Date': ["6/14/2025", "6/14/2025", "6/14/2025", "6/13/2025", "6/13/2025", "6/13/2025", "6/13/2025", "6/12/2025", "6/12/2025", "6/12/2025"]
    }
    df = pd.DataFrame(data)
    header_cols = st.columns([3, 2, 2, 2, 1])
    header_cols[0].write("**REST API Name**"); header_cols[1].write("**Access Timestamp**"); header_cols[2].write("**Accessed By**"); header_cols[3].write("**Business Date**"); header_cols[4].write("**Download**")
    st.divider()
    for index, row in df.iterrows():
        row_cols = st.columns([3, 2, 2, 2, 1])
        row_cols[0].write(row["REST API Name"]); row_cols[1].write(row["Access Timestamp"]); row_cols[2].write(row["Accessed By"]); row_cols[3].write(row["Business Date"])
        csv_data = row.to_csv().encode('utf-8')
        row_cols[4].download_button(label="📄", data=csv_data, file_name=f"{row['REST API Name']}.csv", mime='text/csv', key=f"download_api_{index}")
    st.divider()
    st.button("Start Over", on_click=reset_all_states, key="start_over_api_history")

def show_history_ui():
    """Displays the last ten view calls in a custom table."""
    st.divider()
    st.subheader("History of Last 10 View Calls")
    # (The rest of the function remains the same as your provided code)
    data = {
        'View Name': ["GetAllInterestIncomeData", "GetLoanPortfolioSummary", "GetDepositAccountBalances", "GetCreditRiskMetrics", "GetMonthlyProfitLoss", "GetRegulatoryCapitalRatios", "GetBranchPerformanceData", "GetNonPerformingAssets", "GetFeeIncomeAnalysis", "GetLiquidityPositionReport"],
        'Access Timestamp': ["6/16/2025 16:00", "6/16/2025 14:22", "6/16/2025 13:45", "6/16/2025 11:30", "6/15/2025 17:15", "6/15/2025 16:08", "6/15/2025 15:33", "6/15/2025 12:45", "6/15/2025 10:20", "6/14/2025 16:55"],
        'Accessed By': ["JohnP", "SarahM", "MikeR", "LisaK", "TomW", "AmyC", "DavidL", "JenniferH", "RobertS", "CarolB"],
        'Business Date': ["6/14/2025", "6/14/2025", "6/14/2025", "6/13/2025", "6/13/2025", "6/13/2025", "6/13/2025", "6/12/2025", "6/12/2025", "6/12/2025"]
    }
    df = pd.DataFrame(data)
    header_cols = st.columns([3, 2, 2, 2, 1])
    header_cols[0].write("**View Name**"); header_cols[1].write("**Access Timestamp**"); header_cols[2].write("**Accessed By**"); header_cols[3].write("**Business Date**"); header_cols[4].write("**Download**")
    st.divider()
    for index, row in df.iterrows():
        row_cols = st.columns([3, 2, 2, 2, 1])
        row_cols[0].write(row["View Name"]); row_cols[1].write(row["Access Timestamp"]); row_cols[2].write(row["Accessed By"]); row_cols[3].write(row["Business Date"])
        csv_data = row.to_csv().encode('utf-8')
        row_cols[4].download_button(label="📄", data=csv_data, file_name=f"{row['View Name']}.csv", mime='text/csv', key=f"download_{index}")
    st.divider()
    st.button("Start Over", on_click=reset_all_states, key="start_over_history")

def show_table_selection_ui():
    """Displays the detailed table selection interface."""
    st.divider()
    st.subheader("Custom Bank Data Selection")
    st.info("Uncheck any data elements you don't want to include in the view.")

    with st.form(key="data_selection_form"):
        # --- NEW: Business Date added ---
        business_date = st.date_input("Select Business Date", value=date.today())
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Interest Income Fields")
            # --- MODIFIED: Checkbox value is now driven by pre-selection state ---
            selected_interest_income_fields = [
                field for field in interest_income_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"ii_{field}"
                )
            ]
            st.subheader("Interest Expense Fields")
            selected_interest_expense_fields = [
                field for field in interest_expense_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"ie_{field}"
                )
            ]
        with col2:
            st.subheader("Noninterest Income Fields")
            selected_noninterest_income_fields = [
                field for field in noninterest_income_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"ni_{field}"
                )
            ]
            st.subheader("Noninterest Expense Fields")
            selected_noninterest_expense_fields = [
                field for field in noninterest_expense_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"ne_{field}"
                )
            ]

        st.divider()
        access_group_options = ["Operations", "Supervisor", "DevOps", "All"]
        access_group = st.selectbox("Select Access Group", access_group_options)
        view_name = st.text_input("Enter View Name", "custom_bank_view")
        submitted = st.form_submit_button(label="Create View")

    if submitted:
        st.success(f"Success! The view '{view_name}' for business date {business_date.strftime('%Y-%m-%d')} has been created for the '{access_group}' group.")
        st.balloons()
    
    st.button("Start Over", on_click=reset_all_states, key="start_over_view")

def show_s3_selection_ui():
    """Displays the UI for creating an S3 file."""
    st.divider()
    st.subheader("S3 File Generation")
    st.info("Please provide a business date and uncheck any data elements you don't want in the S3 file.")

    with st.form(key="s3_selection_form"):
        business_date = st.date_input("Select Business Date", value=date.today())
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Interest Income Fields**")
            # --- MODIFIED: Checkbox value is now driven by pre-selection state ---
            selected_interest_income_fields = [
                field for field in interest_income_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"s3_ii_{field}"
                )
            ]
            st.write("**Interest Expense Fields**")
            selected_interest_expense_fields = [
                field for field in interest_expense_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"s3_ie_{field}"
                )
            ]
        with col2:
            st.write("**Noninterest Income Fields**")
            selected_noninterest_income_fields = [
                field for field in noninterest_income_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"s3_ni_{field}"
                )
            ]
            st.write("**Noninterest Expense Fields**")
            selected_noninterest_expense_fields = [
                field for field in noninterest_expense_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"s3_ne_{field}"
                )
            ]
        st.divider()
        file_name = st.text_input("Enter S3 File Name", "custom_bank_data.csv")
        submitted = st.form_submit_button(label="Generate File")

    if submitted:
        st.success(f"Success! The file '{file_name}' for business date {business_date.strftime('%Y-%m-%d')} is being generated.")
        st.balloons()
    
    st.button("Start Over", on_click=reset_all_states, key="start_over_s3")

def show_rest_api_ui():
    """Displays the UI for creating a REST API."""
    st.divider()
    st.subheader("REST API Generation")
    st.info("Review the data elements to include in the API. 'businessdate' is mandatory.")

    with st.form(key="api_selection_form"):
        st.checkbox(f"businessdate (value: {date.today().strftime('%Y-%m-%d')})", value=True, disabled=True)
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Interest Income Fields**")
            # --- MODIFIED: Checkbox value is now driven by pre-selection state ---
            selected_interest_income_fields = [
                field for field in interest_income_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"api_ii_{field}"
                )
            ]
            st.write("**Interest Expense Fields**")
            selected_interest_expense_fields = [
                field for field in interest_expense_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"api_ie_{field}"
                )
            ]
        with col2:
            st.write("**Noninterest Income Fields**")
            selected_noninterest_income_fields = [
                field for field in noninterest_income_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"api_ni_{field}"
                )
            ]
            st.write("**Noninterest Expense Fields**")
            selected_noninterest_expense_fields = [
                field for field in noninterest_expense_fields if st.checkbox(
                    field, value=(field in st.session_state.preselected_fields), key=f"api_ne_{field}"
                )
            ]
        st.divider()
        access_group_options = ["Operations", "Supervisor", "DevOps", "All"]
        access_group = st.selectbox("Select Access Group", access_group_options)
        st.text_input("Action", "Create a REST API", disabled=True)
        submitted = st.form_submit_button(label="Create REST API")

    if submitted:
        st.success(f"Success! The REST API is being created for the '{access_group}' group.")
        st.balloons()
    
    st.button("Start Over", on_click=reset_all_states, key="start_over_api")

# --- Main Application Logic ---
show_agent_ui()

if st.session_state.show_view_ui:
    show_table_selection_ui()
elif st.session_state.show_s3_ui:
    show_s3_selection_ui()
elif st.session_state.show_api_ui:
    show_rest_api_ui()
elif st.session_state.show_history_ui:
    show_history_ui()
elif st.session_state.show_api_history_ui:
    show_api_history_ui()