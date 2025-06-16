import json, logging
from redis import Redis
from rq import Worker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("triagence")

def log_event(event: dict):
    logger.info("New event:\n%s", json.dumps(event, indent=2)[:800])

if __name__ == "__main__":
    conn = Redis(host="redis", port=6379)        
    Worker(['incidents'], connection=conn).work()
