import streamlit as st
import requests

# Set the title and layout of the web page
st.set_page_config(page_title="AI Sales CEO Dashboard", layout="wide")
st.title("🛡️ AI Sales Team - Admin Dashboard")
st.markdown("### Human-in-the-Loop Approval Queue")

# The URL of your running CRM API
CRM_API_URL = "http://crm-api:8001"

# Function to fetch pending leads
def fetch_pending_leads():
    try:
        response = requests.get(f"{CRM_API_URL}/api/dashboard/pending", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        st.error("Cannot connect to CRM API. Is it running on port 8001?")
    return []

# Fetch the data
pending_leads = fetch_pending_leads()

# Display the leads in a clean UI
if not pending_leads:
    st.info("No deals currently waiting for approval. The AI is still calling!")
else:
    for lead in pending_leads:
        # Create a visual card for each lead
        with st.container():
            st.markdown(f"**🏢 Company:** {lead['company_name']}")
            st.markdown(f"**🛠️ Service:** {lead['service_requested']} | **💰 Price:** ${lead['price_agreed']}")
            
            # The Magic Approve Button
            if st.button(f"✅ Approve {lead['company_name']} & Send Payment Link", key=lead['id']):
                # Send the approval command to the CRM API
                approve_res = requests.post(f"{CRM_API_URL}/api/admin/approve/{lead['id']}")
                
                if approve_res.status_code == 200:
                    st.success(f"Deal Approved! AI is emailing the Stripe link to {lead['company_name']}.")
                    st.rerun() # Refresh the page to remove the approved lead
                else:
                    st.error("Failed to approve deal.")
            st.divider()