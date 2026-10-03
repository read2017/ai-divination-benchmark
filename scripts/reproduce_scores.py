"""Reproduce published scoring in a temporary directory, without rewriting release files."""
from pathlib import Path
import csv, json, shutil, subprocess, sys, tempfile
ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='benchmark-score-') as tmp:
    target = Path(tmp)
    for directory in ['harness', 'datasets/gold', 'runs/v6-consumer-events']:
        source = ROOT / directory
        for p in source.rglob('*'):
            if p.is_file() and not any(x in p.parts for x in ['superseded', '__pycache__', 'charts', 'charts_controls']):
                if directory == 'harness' and p.name not in ['score_v6_consumer.py', 'score_v6_consumer_adjudicated.py']:
                    continue
                dest = target / p.relative_to(ROOT)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dest)
    (target / 'reports').mkdir()
    result = subprocess.run([sys.executable, str(target / 'harness/score_v6_consumer_adjudicated.py')], capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr or result.stdout)
    for name in ['v6-consumer-scores.json', 'v6-consumer-results.csv']:
        a, b = ROOT / 'reports' / name, target / 'reports' / name
        if name.endswith('.json'):
            same = json.loads(a.read_text()) == json.loads(b.read_text())
        else:
            with a.open(newline='') as fa, b.open(newline='') as fb:
                same = list(csv.reader(fa)) == list(csv.reader(fb))
        if not same:
            raise SystemExit(f'FAIL: reproduced output differs: {name}')
        print(f'PASS: {name} fully matches published output')
