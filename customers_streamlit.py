import streamlit as st
import requests
import pandas as pd

URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Customer Support AI Assistant",
    layout="wide"
)

#st.sidebar.title("Customer Support AI")

st.sidebar.title("Features")

feature = st.sidebar.radio(
    "Select a feature:",
    [
        "Health",
        "NL Query",
        "Anomalies"
    ],
    index=0
)

st.title("Customer Support AI Assistant")

st.divider()

if feature == "Health":

    st.subheader("Health Check")

    st.write(
        "Check whether the FastAPI service is running."
    )

    if st.button("Check Health"):

        try:

            response = requests.get(
                f"{URL}/health"
            )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    result["message"]
                )

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Please start the FastAPI server first."
            )

elif feature == "NL Query":

    st.subheader("Natural Language Query")

    st.write(
        "Ask questions about customer support tickets "
        "using natural language."
    )

    prompt = st.text_input(
        "Ask your question:",
        placeholder="Example: How many tickets are currently open?"
    )

    if st.button("Submit"):

        if not prompt.strip():

            st.warning(
                "Please enter a query."
            )

        else:

            try:

                response = requests.post(
                    f"{URL}/generate",
                    json={
                        "prompt": prompt
                    }
                )

                if response.status_code == 200:

                    result = response.json()

                    st.subheader("Answer")

                    st.success(
                        result["response"]
                    )

                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

                    try:

                        st.json(
                            response.json()
                        )

                    except:

                        st.write(
                            response.text
                        )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI. "
                    "Please start the FastAPI server first."
                )

elif feature == "Anomalies":

    st.subheader("Anomaly Detection")

    st.write(
        "View tickets identified as anomalies."
    )

    if st.button("Detect Anomalies"):

        try:

            response = requests.get(
                f"{URL}/anomalies"
            )

            if response.status_code == 200:

                result = response.json()

                st.subheader("Anomaly Results")

                st.metric(
                    "Number of Anomalies",
                    result["count"]
                )

                if result["count"] > 0:

                    anomalies_df = pd.DataFrame(
                        result["anomalies"]
                    )

                    st.dataframe(
                        anomalies_df,
                        use_container_width=True
                    )

                else:

                    st.success(
                        "No anomalies found."
                    )

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Please start the FastAPI server first."
            )