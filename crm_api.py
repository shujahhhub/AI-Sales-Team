from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List

app = FastAPI(title="AI Sales Team - Approval Engine")

# 1. The State Machine (Strict Rules for the AI)
class LeadStatus(str, Enum):
    SCRAPED = "SCRAPED"
    AI_CALLED = "AI_CALLED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    PAYMENT_LINK_SENT = "PAYMENT_LINK_SENT"
    PAID = "PAID"

# 2. The Data Model
class Lead(BaseModel):
    id: int
    company_name: str
    service_requested: str
    price_agreed: float
    status: LeadStatus

# 3. Our Mock Database (For testing before we add PostgreSQL)
fake_db = [
    Lead(
        id=1, 
        company_name="ABC Roofing", 
        service_requested="Website + SEO", 
        price_agreed=700.0, 
        status=LeadStatus.PENDING_APPROVAL
    ),
    Lead(
        id=2, 
        company_name="TechFlow Inc", 
        service_requested="Email Marketing", 
        price_agreed=300.0, 
        status=LeadStatus.AI_CALLED
    )
]

# 4. Dashboard Endpoint: Fetch the Approval Queue
@app.get("/api/dashboard/pending", response_model=List[Lead])
def get_pending_approvals():
    """Fetches only the leads that the AI has paused for human review."""
    return [lead for lead in fake_db if lead.status == LeadStatus.PENDING_APPROVAL]

# 5. Admin Action Endpoint: Approve the Deal
@app.post("/api/admin/approve/{lead_id}")
def approve_lead(lead_id: int):
    """The button you click to approve the deal and trigger the Stripe link."""
    for lead in fake_db:
        if lead.id == lead_id:
            if lead.status != LeadStatus.PENDING_APPROVAL:
                raise HTTPException(status_code=400, detail="Lead is not awaiting approval.")
            
            # State Transition: Human approves, system moves forward
            lead.status = LeadStatus.PAYMENT_LINK_SENT
            return {
                "message": f"Successfully approved {lead.company_name}.", 
                "action_triggered": "AI will now email the Stripe link.",
                "lead": lead
            }
    
    raise HTTPException(status_code=404, detail="Lead not found")

    # 6. AI Ingestion Endpoint: Receive new leads from the AI Agent
class NewLead(BaseModel):
    company_name: str
    service_requested: str
    price_agreed: float

@app.post("/api/leads/new")
def receive_new_lead(lead: NewLead):
    """The AI Agent calls this to inject a new lead into the database."""
    new_id = max([l.id for l in fake_db]) + 1 if fake_db else 1
    new_entry = Lead(
        id=new_id,
        company_name=lead.company_name,
        service_requested=lead.service_requested,
        price_agreed=lead.price_agreed,
        status=LeadStatus.PENDING_APPROVAL
    )
    fake_db.append(new_entry)
    return {"message": "Lead safely stored in CRM waiting for human approval.", "lead": new_entry}