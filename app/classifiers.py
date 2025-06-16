import json, os, openai

# Azure OpenAI client
client = openai.AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("OPENAI_API_VERSION", "2024-02-15-preview")
)

# Function schema for JSON output
FUNCTIONS = [
    {
        "name": "classify_incident",
        "description": "Return structured incident info",
        "parameters": {
            "type": "object",
            "properties": {
                "type": {"type": "string"},
                "component": {"type": "string"},
                "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                "root_cause": {"type": "string"}
            },
            "required": ["type", "component", "severity", "root_cause"]
        }
    }
]

SYSTEM = (
    "You are a DevOps SRE assistant. "
    "Given a raw CI/CD or monitoring JSON, extract a concise classification."
)

def classify(event_dict: dict) -> dict:
    content = json.dumps(event_dict)[:6000]   
    resp = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.0,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": content}
        ],
        functions=FUNCTIONS,
        function_call={"name": "classify_incident"}
    )
    args = resp.choices[0].message.function_call.arguments
    return json.loads(args)
