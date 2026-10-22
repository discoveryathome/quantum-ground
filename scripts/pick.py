"""Offline seeded task draw; no live donor coordination is implied."""
import argparse
import json
import re
import secrets
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--seed');a=p.parse_args()
seed=a.seed or secrets.token_hex(16)
if not re.fullmatch('[0-9a-fA-F]{32}',seed): raise SystemExit('seed must be 32 hex digits')
c=json.loads(Path('discover/catalog.json').read_text())
n=int(seed[:8],16)%100
for t in c['tracks']:
    if n<t['weight']: break
    n-=t['weight']
card=t['tasks'][int(seed[8:16],16)%len(t['tasks'])]
print(json.dumps({'seed':seed,'track':t['id'],'task':card,
 'status':'Pre-release intake open, including expert-agent review. Check discover/coordination.jsonl for overlap.'},indent=2))
