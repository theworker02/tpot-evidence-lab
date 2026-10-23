import collections
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('defensive_import',ROOT/'tools/import_defensive_snapshot.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

class DefensiveDatasetTest(unittest.TestCase):
    def test_rows_privacy_groups_licenses_and_policy(self):
        stats=json.loads((ROOT/'defensive-statistics.json').read_text())
        members={}; identifiers=set(); counts=collections.Counter(); sources=collections.Counter()
        for split in ('train','validation','test'):
            for row in builder.read_rows(ROOT/f'data/defensive-chat/{split}.jsonl'):
                self.assertEqual(row['split'],split)
                self.assertEqual(row['dataset_version'],stats['version'])
                self.assertNotIn(row['id'],identifiers);identifiers.add(row['id'])
                self.assertEqual(members.setdefault(row['group_id'],split),split)
                self.assertEqual([m['role'] for m in row['messages']],['system','user','assistant'])
                answer=json.loads(row['messages'][-1]['content'])
                self.assertIsInstance(answer,dict)
                self.assertIn(row['license_id'],('CC-BY-4.0','CC0-1.0','LicenseRef-MITRE-ATTACK'))
                if row['source'].startswith('local_'):
                    text=json.dumps(row)
                    self.assertIsNone(builder.ISO.search(text))
                    self.assertIsNone(re.search(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',text))
                    self.assertNotIn('LicenseRef-Local-Review-Only',text)
                    if row['task']=='triage_repeat_abuse':
                        self.assertEqual(answer['policy']['minimum_abuse_records'],2)
                        self.assertIsNone(answer['policy']['abuse_time_limit_seconds'])
                    else:self.assertEqual(answer['disposition'],'needs_manual_validation')
                counts[split]+=1;sources[row['source']]+=1
        self.assertEqual(dict(counts),stats['splits'])
        self.assertEqual(dict(sources),stats['scenario_sources'])
        total=0
        for split in ('train','validation','test'):
            for row in builder.read_rows(ROOT/f'data/retained-events/{split}.jsonl'):
                self.assertEqual(members.setdefault(row['source_group'],split),split)
                self.assertNotIn('timestamp',row)
                self.assertGreaterEqual(row['snapshot_offset_seconds'],0)
                self.assertFalse(row['raw_payload_included'])
                self.assertEqual(row['license_id'],'CC-BY-4.0')
                self.assertEqual(row['attribution'],'unestablished')
                self.assertEqual(set(row),{'id','source_group','snapshot_offset_seconds','sensor','observed_destination_port','label','label_origin','attribution','raw_payload_included','license_id','dataset_version','split'})
                total+=1
        self.assertEqual(total,stats['retained_events'])

    def test_parquet_matches_json_and_card(self):
        import pyarrow.parquet as pq
        import yaml
        card=(ROOT/'README.md').read_text().split('---',2)[1].strip()
        metadata=(ROOT/'card-metadata.yaml').read_text().strip()
        self.assertEqual(card,metadata)
        parsed=yaml.safe_load(card)
        link=urlparse(parsed['license_link'])
        self.assertEqual(link.scheme,'https')
        self.assertTrue(link.netloc)
        configs=parsed['configs']
        self.assertEqual(next(c['config_name'] for c in configs if c.get('default')),'observations')
        for folder in ('defensive-chat','retained-events'):
            for split in ('train','validation','test'):
                self.assertEqual(pq.read_table(ROOT/f'data/{folder}/{split}.parquet').to_pylist(),builder.read_rows(ROOT/f'data/{folder}/{split}.jsonl'))

    def test_tampered_snapshot_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name); snapshot=root/'input';snapshot.mkdir()
            (snapshot/'manifest.json').write_text(json.dumps({'files':{'data.jsonl':'invalid'}}))
            (snapshot/'data.jsonl').write_text('{}')
            prior=builder.ROOT;builder.ROOT=root/'output'
            try:
                with self.assertRaisesRegex(ValueError,'checksum mismatch'):builder.build(snapshot)
                self.assertFalse(builder.ROOT.exists())
            finally:builder.ROOT=prior

    def test_snapshot_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name);snapshot=root/'input';snapshot.mkdir()
            (snapshot/'manifest.json').write_text(json.dumps({'files':{'../outside':'invalid'}}))
            prior=builder.ROOT;builder.ROOT=root/'output'
            try:
                with self.assertRaisesRegex(ValueError,'escapes snapshot'):builder.build(snapshot)
                self.assertFalse(builder.ROOT.exists())
            finally:builder.ROOT=prior

if __name__=='__main__':unittest.main()
