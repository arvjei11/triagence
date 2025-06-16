from graphviz import Digraph

# Create the graph
g = Digraph('AutoResponderX', format='png')
g.attr(rankdir='LR', fontsize='10')

# Event Sources cluster
with g.subgraph(name='cluster_sources') as c:
    c.attr(label='Event Sources', style='dashed')
    c.node('GitHub', 'GitHub Actions\n(workflow_run)')
    c.node('Sentry', 'Sentry / Opsgenie\n(alert webhooks)')

# Webhook layer
g.node('FastAPI', 'FastAPI Webhook Listener\n+ HMAC Signature Check')

# Queue
g.node('Redis', 'Redis Queue (RQ)')

# LangGraph cluster
with g.subgraph(name='cluster_agent') as c:
    c.attr(label='LangGraph Agent Worker', style='dashed')
    c.node('PreParser', 'Pre‑Parser')
    c.node('Classifier', 'GPT‑4o Classifier\n(JSON‑only)')
    c.node('Router', 'Decision Router')
    c.edges([('PreParser', 'Classifier'), ('Classifier', 'Router')])

# Branch targets
g.node('JIRA', 'JIRA Cloud\n(issue create)')
g.node('Notifier', 'Notifier Interface\n(Slack / Teams / PagerDuty)')
g.node('PatchAgent', 'PatchAgent\n(GPT‑4o PR Draft)')

# GitHub PR & Checks
g.node('GitHubPR', 'GitHub PR\n+ Dry‑Run Checks')

# SQLite DB
g.node('SQLite', 'SQLite Incident DB\n+ Metrics')

# Dashboard
g.node('Streamlit', 'Streamlit Dashboard')

# LLM Service
g.node('AzureOpenAI', 'Azure OpenAI\n(GPT‑4o)')

# Secrets
g.node('Secrets', 'Secrets Store\n(.env / GitHub Secrets)', shape='note')

# Edges: Sources -> FastAPI
g.edges([('GitHub', 'FastAPI'), ('Sentry', 'FastAPI')])
# FastAPI -> Queue
g.edge('FastAPI', 'Redis')
# Queue -> LangGraph
g.edge('Redis', 'PreParser')

# Agent flow internal
g.edge('Router', 'JIRA')
g.edge('Router', 'Notifier')
g.edge('Router', 'PatchAgent')

# PatchAgent -> GitHub PR
g.edge('PatchAgent', 'GitHubPR')

# GitHubPR feedback loop?
g.edge('GitHubPR', 'SQLite')

# Agent write to DB
g.edge('Router', 'SQLite')

# Dashboard reads DB
g.edge('SQLite', 'Streamlit')

# LLM usage
g.edge('Classifier', 'AzureOpenAI')
g.edge('PatchAgent', 'AzureOpenAI')

# Secrets arrows
for n in ['FastAPI', 'PreParser', 'Classifier', 'PatchAgent', 'Notifier']:
    g.edge('Secrets', n, style='dotted')

g
