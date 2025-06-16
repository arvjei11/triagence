import json, logging
from redis import Redis
from rq import Worker, Connection
from .classifiers import classify

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("triagence")

def process_event(event: dict):
    classification = classify(event)
    log.info("== Structured JSON ==\n%s", json.dumps(classification, indent=2))

if __name__ == "__main__":
    redis_conn = Redis(host="redis", port=6379)
    with Connection(redis_conn):
        Worker(["incidents"]).work()          # v1 API (no functions param)
