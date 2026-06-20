"""
AI Engine - OpenAI GPT Integration for Drug Interaction Analysis
"""

import os
import re
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("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"))

SYSTEM_PROMPT = """You are MedSafe AI, an expert clinical pharmacist assistant specializing in drug interaction analysis. Your role is to provide accurate, structured, and life-saving drug interaction information.

When analyzing medications, always:
1. Check ALL possible pairwise and multi-drug interactions
2. Assign severity: CRITICAL 🔴, MODERATE 🟡, MILD 🟢, or SAFE ✅
3. Explain mechanisms in plain language
4. Give actionable precautions
5. Recommend when to seek emergency care

Structure your response EXACTLY like this:

## 📊 INTERACTION SUMMARY
[Brief 1-2 sentence overview of the most important finding]

## 🔍 DETAILED INTERACTIONS

### [Drug A] + [Drug B]
**Severity:** 🔴 CRITICAL / 🟡 MODERATE / 🟢 MILD / ✅ SAFE
**What happens:** [Plain explanation of the interaction mechanism]
**Risk:** [What could go wrong]
**Action:** [What the patient should do]

[Repeat for each pair/combination]

## ⚠️ PRECAUTIONS
- [Bullet point precautions]

## 🚨 SEEK EMERGENCY CARE IF
- [Danger signs to watch for]

## 💡 RECOMMENDATIONS
- [General advice]

## ⚕️ DISCLAIMER
This analysis is for informational purposes only. Always consult your doctor or pharmacist before changing any medication. In case of emergency, call 911 or your local emergency number immediately.

Be thorough, accurate, and compassionate. Lives depend on this information."""


def check_interactions(medicines: list) -> dict:
    """
    Analyze drug interactions for a list of medicines using OpenAI GPT.

    Args:
        medicines: List of medicine names

    Returns:
        dict with 'success', 'analysis', 'user_prompt', 'severity_summary'
    """
    try:
        med_list = ", ".join(medicines)
        user_prompt = (
            f"I am currently taking the following medications: {med_list}.\n\n"
            f"Please perform a comprehensive drug interaction analysis. Check ALL possible "
            f"interactions between these {len(medicines)} medication(s), including serious "
            f"combinations. Provide clear severity ratings and actionable advice."
        ) if len(medicines) > 1 else (
            f"I am taking {medicines[0]}. Please provide general safety information, "
            f"common interactions to be aware of, and important precautions for this medication."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1500,
            temperature=0.2  # Low temp for medical accuracy
        )

        analysis = response.choices[0].message.content

        # Determine overall severity from response
        severity_summary = "safe"
        if "🔴 CRITICAL" in analysis or "**Severity:** 🔴" in analysis:
            severity_summary = "critical"
        elif "🟡 MODERATE" in analysis or "**Severity:** 🟡" in analysis:
            severity_summary = "moderate"
        elif "🟢 MILD" in analysis or "**Severity:** 🟢" in analysis:
            severity_summary = "mild"

        return {
            "success": True,
            "analysis": analysis,
            "user_prompt": user_prompt,
            "severity_summary": severity_summary
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"AI analysis failed: {str(e)}"
        }


def chat_followup(user_message: str, history: list, medicines: list) -> dict:
    """
    Handle follow-up chat questions with conversation context.

    Args:
        user_message: The user's follow-up question
        history: Previous chat messages
        medicines: List of medicines being analyzed

    Returns:
        dict with 'success' and 'response'
    """
    try:
        med_context = f"Patient is taking: {', '.join(medicines)}." if medicines else ""
        system_with_context = f"{SYSTEM_PROMPT}\n\nContext: {med_context}"

        messages = [{"role": "system", "content": system_with_context}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=800,
            temperature=0.3
        )

        return {
            "success": True,
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Chat failed: {str(e)}"
        }