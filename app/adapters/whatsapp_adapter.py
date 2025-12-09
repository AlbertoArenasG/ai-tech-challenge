"""Adapter utilities for integrating with Twilio WhatsApp."""


def parse_twilio_payload(payload: dict) -> dict:
    """Convert Twilio webhook payload into an internal structure."""
    # TODO: Document and normalize the WhatsApp webhook contract before parsing inputs.
    _ = payload
    return {"user_id": "", "channel": "whatsapp", "text": ""}
