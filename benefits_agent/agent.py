from google.adk.agents import Agent

# Made-up sample data: no real member or patient information
BENEFITS = {
    "primary care visit": {"covered": True, "copay": "$25", "notes": "No referral needed"},
    "specialist visit": {"covered": True, "copay": "$50", "notes": "Referral required"},
    "emergency room": {"covered": True, "copay": "$250", "notes": "Copay waived if admitted"},
    "physical therapy": {"covered": True, "copay": "$40", "notes": "Up to 30 visits per year"},
    "cosmetic surgery": {"covered": False, "copay": None, "notes": "Not covered"},
}

CLAIMS = {
    "C1001": {"claim_status": "approved", "amount": "$120.00"},
    "C1002": {"claim_status": "pending", "amount": "$860.00"},
    "C1003": {"claim_status": "denied", "amount": "$45.00", "reason": "Out-of-network provider"},
}

def lookup_benefit(service: str) -> dict:
    """Looks up coverage, copay, and notes for a medical service in the member's plan.

    Args:
        service: Name of the medical service, for example "specialist visit".

    Returns:
        A dict with "status" set to "success" and the benefit details,
        or "status" set to "error" and an error message.
    """
    key = service.strip().lower()
    if key in BENEFITS:
        return {"status": "success", "service": key, **BENEFITS[key]}
    return {"status": "error", "error_message": f"No benefit information found for '{service}'."}


def check_claim_status(claim_id: str) -> dict:
    """Checks the status of an insurance claim by its claim ID.

    Args:
        claim_id: The claim ID, for example "C1002".

    Returns:
        A dict with "status" set to "success" and the claim details,
        or "status" set to "error" and an error message.
    """
    key = claim_id.strip().upper()
    if key in CLAIMS:
        return {"status": "success", "claim_id": key, **CLAIMS[key]}
    return {"status": "error", "error_message": f"No claim found with ID '{claim_id}'."}

root_agent = Agent(
    name="benefits_agent",
    model="gemini-4-hydrogen",  # check the ADK quickstart for the current recommended model
    description="Answers health plan members' questions about benefits and claims.",
    instruction=(
        "You help health plan members with questions about their benefits and claims. "
        "Use lookup_benefit for coverage questions and check_claim_status for claim questions. "
        "Answer only from tool results. If a tool returns an error, or the question is not "
        "about benefits or claims, say you don't have that information and suggest "
        "contacting member services. Never guess."
    ),
    tools=[lookup_benefit, check_claim_status],
)