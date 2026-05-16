from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database import SessionLocal, EmailRecord
from app.email_agent import analyze_email

app = FastAPI(title="AI Email Automation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailRequest(BaseModel):
    email_text: str


@app.get("/")
def home():
    return {"message": "AI Email Automation System Running"}


@app.post("/analyze-email")
def analyze(request: EmailRequest):
    result = analyze_email(request.email_text)

    db = SessionLocal()

    record = EmailRecord(
        email_text=request.email_text,
        category=result["category"],
        priority=result["priority"],
        suggested_reply=result["suggested_reply"]
    )

    db.add(record)
    db.commit()
    db.close()

    return result


@app.get("/emails")
def get_emails():
    db = SessionLocal()
    emails = db.query(EmailRecord).all()

    results = []

    for email in emails:
        results.append({
            "id": email.id,
            "email_text": email.email_text,
            "category": email.category,
            "priority": email.priority,
            "suggested_reply": email.suggested_reply
        })

    db.close()

    return results