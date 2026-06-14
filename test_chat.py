import httpx
import json

data = {'message': 'What should I do during a flood in Morocco?'}
response = httpx.post('http://localhost:3001/api/chat', json=data, timeout=15)
print(f'Status: {response.status_code}')
result = response.json()
print(f'Response preview: {result.get("response", "")[:500]}...')
