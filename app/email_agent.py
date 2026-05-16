def analyze_email(email_text):

    text = email_text.lower()

    if "refund" in text or "payment" in text or "invoice" in text:

        category = "Billing"

        priority = "Medium"

        reply = (
            "Thank you for contacting us. "
            "Our billing team will review your request shortly."
        )

    elif "urgent" in text or "asap" in text or "immediately" in text:

        category = "Urgent Support"

        priority = "High"

        reply = (
            "Your request has been marked as urgent "
            "and escalated to our support team."
        )

    elif "password" in text or "login" in text or "account" in text:

        category = "Account Support"

        priority = "Medium"

        reply = (
            "Please use the password reset option "
            "on the login page."
        )

    else:

        category = "General Inquiry"

        priority = "Low"

        reply = (
            "Thank you for your message. "
            "Our team will contact you soon."
        )

    return {
        "category": category,
        "priority": priority,
        "suggested_reply": reply
    }