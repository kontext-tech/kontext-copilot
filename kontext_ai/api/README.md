# API examples

## /api/llm/chat

```bash
curl 'http://localhost:8100/api/llms/chat' \
  -H 'Accept: application/json' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  --data $'{"model":"llama3","messages":[{"role":"user","content":"Hello!"}],"stream":true,"options":{"temperature":0.5}}'
```
