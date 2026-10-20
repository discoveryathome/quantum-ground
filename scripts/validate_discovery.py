import json
import hashlib
from pathlib import Path
from jsonschema import Draft202012Validator
for f,s in [('discover.json','manifest'),('discover/frontier.json','frontier'),('discover/catalog.json','catalog')]:
    schema=json.loads(Path(f'protocol/schemas/{s}.schema.json').read_text())
    Draft202012Validator(schema).validate(json.loads(Path(f).read_text()))
c=json.loads(Path('discover/catalog.json').read_text())
assert sum(t['weight'] for t in c['tracks'])==100
print('PASS: manifest, frontier, catalog schemas and weights')

f=json.loads(Path('discover/frontier.json').read_text())
for a in f.get('artifacts',[]):
    assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256'], a['path']
print('PASS: frontier artifact hashes')
