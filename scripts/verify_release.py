"""Check public release contents, hashes, data counts and accidental local secrets."""
from pathlib import Path
import hashlib, json, re, subprocess
ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'provenance/public-release-manifest.json').read_text())
for name, digest in manifest['sha256'].items():
    p = ROOT / name
    assert p.is_file(), f'Missing: {name}'
    assert hashlib.sha256(p.read_bytes()).hexdigest() == digest, f'Hash differs: {name}'
    assert p.stat().st_size < 10_000_000, f'Unexpected large file: {name}'
    if p.suffix in ['.json', '.jsonl', '.md', '.py', '.html', '.csv', '.txt']:
        text = p.read_text(encoding='utf-8-sig')
        for pattern in [r'/' + r'Users/[^/\s]+/', r'wxid_[a-zA-Z0-9]+', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', r'gh[pousr]_[A-Za-z0-9]{30,}', r'sk-[A-Za-z0-9_-]{40,}']:
            assert not re.search(pattern, text), f'Potential private content: {name}'
counts = {}
for folder, files, records in [('answers', 18, 432), ('controls', 18, 90), ('probes', 17, 85)]:
    paths = list((ROOT / 'runs/v6-consumer-events' / folder).glob('*.json'))
    total = 0
    for p in paths:
        obj = json.loads(p.read_text())
        total += len(obj if isinstance(obj, list) else obj.get('answers', obj.get('results', [])))
    assert (len(paths), total) == (files, records), (folder, len(paths), total)
    counts[folder] = total
assert len((ROOT / 'datasets/gold/v6-events.jsonl').read_text().splitlines()) == 24
scores = json.loads((ROOT / 'reports/v6-consumer-scores.json').read_text())
assert len(scores['ranking']) == 18
assert len(json.loads((ROOT / 'runs/v6-consumer-events/adjudications.json').read_text())) == 88
web = ROOT / 'docs/index.html'
for path in re.findall(r'(?:href|src)="(assets/[^"]+)"', web.read_text()):
    assert (web.parent / path).is_file(), f'Missing web asset: {path}'
assert len(re.findall(r'<td class="final">', web.read_text())) == 16
print(f'PASS: {len(manifest["sha256"])} release files; counts {counts}; hashes and webpage assets valid')
