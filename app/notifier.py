import os, json, requests

class SlackConnector:
    def __init__(self):
        self.url = os.getenv("SLACK_WEBHOOK_URL")

    def send(self, classification: dict):
        emoji = "🚨" if classification["severity"] in ("high", "critical") else "🔔"
        text = (
            f"{emoji} *{classification['type']}* in `{classification['component']}` "
            f"({classification['severity']})\n"
            f"> {classification['root_cause']}"
        )
        payload = {"text": text}
        resp = requests.post(self.url, json=payload, timeout=3)
        resp.raise_for_status()  # raise if Slack returns 4xx/5xx
