import json, logging
from redis import Redis
from rq import Connection, Worker

from .classifiers import classify
from .router import route
from .notifier import SlackConnector

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("triagence")

slack = SlackConnector()   # instantiate once

def process_event(event: dict):
    classification = classify(event)
    decisions = route(classification)

    # Log for visibility
    log.info("== Classified ==\n%s", json.dumps(classification, indent=2))
    log.info("== Decisions  == %s", decisions)

    if decisions["send_alert"]:
        try:
            slack.send(classification)
            log.info("Slack alert sent.")
        except Exception as e:
            log.exception("Slack alert failed: %s", e)

    # create_ticket & enable_patch will be wired in later stages

if __name__ == "__main__":
    redis_conn = Redis(host="redis", port=6379)
    with Connection(redis_conn):
        Worker(["incidents"]).work()
