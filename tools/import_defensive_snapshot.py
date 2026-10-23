"""Import a reviewed sanitized snapshot, never live logs or executable captures.

Requires pyarrow for viewer Parquet. Usage: python tools/import_defensive_snapshot.py SNAPSHOT
Existing output is refused to preserve released snapshots.
"""
import argparse
import collections
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
ISO = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)')
IPV4 = re.compile(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])')

def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]

def sha(value):
    return hashlib.sha256(value).hexdigest()

def write_rows(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(row, ensure_ascii=False)+'\n' for row in rows), encoding='utf-8')

def build(snapshot):
    import pyarrow as pa
    import pyarrow.parquet as pq
    target = ROOT/'data/defensive-chat'
    if target.exists():
        raise ValueError('Defensive snapshot already exists; use a fresh checkout/version')
    manifest = json.loads((snapshot/'manifest.json').read_text())
    for name, expected in manifest['files'].items():
        path = (snapshot/name).resolve()
        if not path.is_relative_to(snapshot.resolve()):
            raise ValueError('Input manifest path escapes snapshot')
        if sha(path.read_bytes()) != expected:
            raise ValueError('Input snapshot checksum mismatch: '+name)
    events = read_rows(snapshot/'data/events.jsonl')
    base = min(datetime.fromisoformat(row['timestamp'].replace('Z','+00:00')) for row in events)
    def offset(stamp):
        return round((datetime.fromisoformat(stamp.replace('Z','+00:00'))-base).total_seconds(), 3)
    def redact_times(text):
        return ISO.sub(lambda match: 'snapshot_offset_seconds='+str(offset(match.group())), text)
    memberships = {}; sources = collections.Counter(); tasks = collections.Counter(); split_counts = {}
    previews = []
    for split in ('train','validation','test'):
        rows = read_rows(snapshot/'data'/f'{split}.jsonl')
        for row in rows:
            if memberships.setdefault(row['group_id'],split) != split:
                raise ValueError('Snapshot group crosses splits')
            if row['source'].startswith('local_'):
                row['license_id'] = 'CC-BY-4.0'
                for message in row['messages']:
                    message['content'] = redact_times(message['content'])
            else:
                # Defang public documentation's example IPs; these are not local indicators.
                for message in row['messages']:
                    message['content'] = IPV4.sub(lambda match: match.group().replace('.', '[.]'), message['content'])
                    message['content'] = message['content'].replace('API_KEY=', 'API-KEY-PLACEHOLDER=')
            row['dataset_version'] = '3.2.0'
            row['id'] = sha(json.dumps([row['group_id'],row['task'],row['messages']],sort_keys=True).encode())
            sources[row['source']] += 1; tasks[row['task']] += 1
            if not any(p['task']==row['task'] for p in previews):
                previews.append(row)
        write_rows(target/f'{split}.jsonl', rows)
        pq.write_table(pa.Table.from_pylist(rows), target/f'{split}.parquet', compression='zstd')
        split_counts[split] = len(rows)
    grouped = collections.defaultdict(list)
    for row in events:
        stamp = row.pop('timestamp')
        row['snapshot_offset_seconds'] = offset(stamp)
        row['license_id'] = 'CC-BY-4.0'
        row['dataset_version'] = '3.2.0'
        row['id'] = sha(json.dumps({k:v for k,v in row.items() if k!='id'},sort_keys=True).encode())
        group = row['source_group']
        split = memberships.get(group)
        if split is None:
            n = int(sha(group.encode())[:8],16)%100
            split = 'train' if n<80 else 'validation' if n<90 else 'test'
        row['split'] = split; grouped[split].append(row)
    for split, rows in grouped.items():
        folder = ROOT/'data/retained-events'
        write_rows(folder/f'{split}.jsonl', rows)
        pq.write_table(pa.Table.from_pylist(rows),folder/f'{split}.parquet',compression='zstd')
    review = read_rows(snapshot/'data/signature_review.jsonl')
    for row in review:
        row['snapshot_offset_seconds'] = offset(row.pop('timestamp'))
        row['license_id'] = 'CC-BY-4.0'
    write_rows(ROOT/'data/defensive-review/signatures.jsonl',review)
    (ROOT/'licenses').mkdir(exist_ok=True)
    for path in (snapshot/'licenses').glob('*.txt'):
        shutil.copyfile(path,ROOT/'licenses'/path.name)
    # Do not copy the private-workspace builder, raw logs or source mapping.
    provenance = dict(version='3.2.0', schema_version='1.0.0',
        scenarios=sum(split_counts.values()), splits=split_counts, scenario_sources=dict(sources),
        tasks=dict(tasks), retained_events=len(events), event_splits={k:len(v) for k,v in grouped.items()},
        signature_review=len(review), public_sources=manifest['public_sources'],
        source_snapshot_data_digests=manifest['files'],
        label_status='Weak rule-derived/template-authored labels; human adjudication pending',
        privacy_transform='Local absolute timestamps replaced by snapshot-relative offsets; event IDs regenerated from sanitized fields; no source mapping exported',
        cross_version_overlap='Unknown; do not concatenate local v3.0 and v3.2 data for independent evaluation',
        reporting_policy=manifest['reporting_policy'])
    (ROOT/'defensive-statistics.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
    (ROOT/'site/defensive-preview.json').write_text(json.dumps(previews,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:provenance[k] for k in ('version','scenarios','retained_events','splits')}))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot',type=Path)
    build(parser.parse_args().snapshot)
