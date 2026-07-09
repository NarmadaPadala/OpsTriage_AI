"""Authorization helpers for production routing workflows."""


def can_auto_route(user_role: str, risk_level: str) -> bool:
    """Return whether a user role can approve automatic routing."""

    privileged_roles = {"incident_manager", "support_lead", "admin"}
    return user_role in privileged_roles and risk_level.casefold() not in {"high", "critical"}
