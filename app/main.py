from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.database import SessionLocal, EmailRecord
from app.email_agent import analyze_email


app = FastAPI(
    title="AI Email Automation System",
    description="AI-powered email classification, priority detection, and automated response workflow platform.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailRequest(BaseModel):
    email_text: str = Field(
        ...,
        min_length=10,
        description="Customer email text that will be analyzed by the email automation workflow.",
        example="Hello, I was charged twice for my subscription and need urgent help with a refund.",
    )


@app.get(
    "/",
    summary="Health check",
    description="Checks whether the AI Email Automation backend is running.",
)
def home():
    return {
        "message": "AI Email Automation System Running",
        "status": "active",
        "timestamp": datetime.utcnow(),
    }


@app.post(
    "/analyze-email",
    summary="Analyze customer email",
    description="Classifies customer email, assigns priority, generates a suggested reply, and saves the workflow result.",
)
def analyze(request: EmailRequest):
    try:
        result = analyze_email(request.email_text)

        if not isinstance(result, dict):
            raise HTTPException(
                status_code=500,
                detail="Email agent returned an invalid response format.",
            )

        required_fields = ["category", "priority", "suggested_reply"]

        for field in required_fields:
            if field not in result:
                raise HTTPException(
                    status_code=500,
                    detail=f"Email agent response missing required field: {field}",
                )

        db = SessionLocal()

        record = EmailRecord(
            email_text=request.email_text,
            category=result["category"],
            priority=result["priority"],
            suggested_reply=result["suggested_reply"],
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "message": "Email analyzed and saved successfully",
            "email": {
                "id": record.id,
                "email_text": record.email_text,
                "category": record.category,
                "priority": record.priority,
                "suggested_reply": record.suggested_reply,
                "status": "processed",
            },
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if "db" in locals():
            db.close()


@app.get(
    "/emails",
    summary="Get analyzed emails",
    description="Returns all analyzed email workflow records saved in the database.",
)
def get_emails():
    try:
        db = SessionLocal()
        emails = db.query(EmailRecord).all()

        return [
            {
                "id": email.id,
                "email_text": email.email_text,
                "category": email.category,
                "priority": email.priority,
                "suggested_reply": email.suggested_reply,
            }
            for email in emails
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if "db" in locals():
            db.close()