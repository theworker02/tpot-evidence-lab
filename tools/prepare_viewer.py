"""Refresh Parquet viewer copies, shared Hub metadata, and the bounded site preview."""
import collections
import json
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
import yaml
root=Path(__file__).resolve().parents[1]
meta=yaml.safe_load((root/'card-metadata.yaml').read_text())
tasks=[json.loads(line) for line in (root/'evaluation/tasks.jsonl').read_text(encoding='utf-8').splitlines()]
for split in ('train','validation','test'):
    (root/f'evaluation/prompts/{split}.jsonl').write_text(''.join(json.dumps(t,ensure_ascii=False)+'\n' for t in tasks if t['split']==split),encoding='utf-8')
for c in meta['configs']:
    for file in c['data_files']:
        original_paths={'default':'data/chat','alpaca':'data/alpaca','sharegpt':'data/sharegpt',
                        'prompt_completion':'data/prompt-completion','evaluation':'evaluation/prompts'}
        if c['config_name'] in original_paths:
            source=root/original_paths[c['config_name']]/f"{file['split']}.jsonl"
        else:
            continue
        rows=[json.loads(s) for s in source.read_text(encoding='utf-8').splitlines()]
        target=root/f"data/viewer/{c['config_name']}/{file['split']}.parquet"
        target.parent.mkdir(parents=True,exist_ok=True)
        pq.write_table(pa.Table.from_pylist(rows),target,compression='zstd')
        file['path']=target.relative_to(root).as_posix()
header=yaml.safe_dump(meta,sort_keys=False,allow_unicode=True)
(root/'card-metadata.yaml').write_text(header,encoding='utf-8')
p=root/'README.md';body=p.read_text(encoding='utf-8').split('---',2)[2].lstrip().replace('Combined structured observations, JSONL','Combined structured observations').replace('Same observations as Parquet','Alias for the same observation table')
p.write_text('---\n'+header+'---\n\n'+body,encoding='utf-8')
p=root/'docs/observations.md';p.write_text(p.read_text(encoding='utf-8').replace('`observations` is the combined JSONL configuration; `observations_parquet` exposes the same rows and splits as Parquet.','`observations` is the combined structured configuration; `observations_parquet` is an alias for the same rows and splits. All viewer configurations use Parquet to avoid mixing loader formats within one repository. Canonical JSONL downloads remain in `data/observations/` and the original format folders.'),encoding='utf-8')
preview=[]
counts=collections.Counter()
for split in ('train','validation','test'):
    for line in (root/f'data/observations/{split}.jsonl').read_text(encoding='utf-8').splitlines():
        row=json.loads(line);key=(row['corpus'],row['sensor'])
        if counts[key]<20:
            preview.append(row);counts[key]+=1
data=dict(statistics=json.loads((root/'observation-statistics.json').read_text()),
          sources=json.loads((root/'sources.json').read_text(encoding='utf-8')),rows=preview)
(root/'site/preview.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
