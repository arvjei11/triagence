import hmac, hashlib, os, json
from fastapi import FastAPI, Request, HTTPException
from redis import Redis
from rq import Queue
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

redis_conn = Redis(host="redis", port=6379)
q = Queue("incidents", connection=redis_conn)

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").encode()

def verify_signature(raw_body: bytes, signature: str) -> bool:
    mac = hmac.new(WEBHOOK_SECRET, msg=raw_body, digestmod=hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature)

@app.post("/github")
async def github_webhook(request: Request):
    raw = await request.body()
    sig = request.headers.get("X-Hub-Signature-256", "")
    if not verify_signature(raw, sig):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = json.loads(raw.decode())
    q.enqueue("app.worker.process_event", payload)
    return {"status": "queued"}
