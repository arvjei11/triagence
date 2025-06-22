def route(classification: dict) -> dict:
    """
    Decide which downstream actions to trigger.
    Returns flags so worker can act.
    """
    sev = classification["severity"]
    return {
        "send_alert": True,                      # always alert for demo
        "create_ticket": sev in ("high", "critical"),
        "enable_patch": False                    # will remain False until Stage 7
    }
