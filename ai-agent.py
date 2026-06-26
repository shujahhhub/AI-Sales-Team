import requests
import time

print("\n🤖 [Scraper AI] Searching the web for new business leads...")
time.sleep(2) # Pausing for dramatic effect so you can read the terminal
print("🤖 [Scraper AI] Target Found -> 'Global Tech Solutions' (Needs SEO)")

print("\n🤖 [Caller AI] Contacting AI Brain on Port 8000 to generate a custom sales pitch...")
try:
    # 1. Talk to the AI Brain
    ai_response = requests.post(
        "http://localhost:8000/chat",
        json={"user_message": "Write a very short, polite opening sentence to sell SEO services to Global Tech Solutions."}
    )
    if ai_response.status_code == 200:
        pitch = ai_response.json().get("ai_response")
        print(f"🧠 [AI Brain] Generated Pitch: '{pitch}'")
    else:
        print("⚠️ [AI Brain] Could not reach the model.")
except Exception as e:
    print(f"⚠️ Error talking to AI Brain: {e}")

time.sleep(2)
print("\n🤖 [Sales AI] Pitch successful! Customer agreed to $1,200 price.")
print("🤖 [CRM AI] Pushing new lead to Human Dashboard for final approval...")

# 2. Push the data to the CRM
new_lead_data = {
    "company_name": "Global Tech Solutions",
    "service_requested": "Enterprise SEO",
    "price_agreed": 1200.00
}

try:
    crm_response = requests.post("http://localhost:8001/api/leads/new", json=new_lead_data)
    if crm_response.status_code == 200:
        print("\n✅ SUCCESS! The lead is now waiting on your Streamlit Dashboard.")
    else:
        print("\n⚠️ Failed to push to CRM.")
except Exception as e:
    print(f"\n⚠️ Error talking to CRM: {e}")