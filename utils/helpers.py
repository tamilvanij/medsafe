"""
Helper utilities for MedSafe AI
"""

from datetime import datetime


def validate_medicines(medicines: list) -> tuple:
    """
    Validate the list of medicines provided by the user.

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    if not medicines:
        return False, "Please provide at least one medication name."

    if len(medicines) > 15:
        return False, "Please check a maximum of 15 medications at a time."

    for med in medicines:
        if not isinstance(med, str) or not med.strip():
            return False, "Invalid medication name detected."
        if len(med.strip()) < 2:
            return False, f"Medication name too short: '{med}'"
        if len(med.strip()) > 100:
            return False, f"Medication name too long: '{med[:20]}...'"

    return True, None


def format_timestamp() -> str:
    """Return human-readable timestamp"""
    return datetime.now().strftime("%B %d, %Y at %I:%M %p")


def sanitize_input(text: str) -> str:
    """Basic input sanitization"""
    return text.strip()[:500]
