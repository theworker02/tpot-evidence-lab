import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from http.server import BaseHTTPRequestHandler,HTTPServer
import threading
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('evaluate',ROOT/'tools/evaluate.py')
evaluation=importlib.util.module_from_spec(spec);spec.loader.exec_module(evaluation)


class ReleaseTest(unittest.TestCase):
    def test_inventory_and_privacy(self):
        events=[]
        for path in (ROOT/'data/events').glob('*.jsonl'):events+=evaluation.read_jsonl(path)
        self.assertEqual(len(events),741)
        membership={}
        for row in events:
            self.assertEqual(membership.setdefault(row['source_group'],row['split']),row['split'])
            self.assertNotIn('source_ip',row)
            self.assertNotIn('network_organization',row)
            self.assertNotIn('session_hash',row)
        for path in ROOT.rglob('*.jsonl'):
            text=path.read_text()
            self.assertIsNone(re.search(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',text),str(path))
            self.assertNotIn('C:\\Users',text)

    def test_format_equivalence(self):
        for split in ('train','validation','test'):
            chats=evaluation.read_jsonl(ROOT/f'data/chat/{split}.jsonl')
            alpaca=evaluation.read_jsonl(ROOT/f'data/alpaca/{split}.jsonl')
            share=evaluation.read_jsonl(ROOT/f'data/sharegpt/{split}.jsonl')
            pc=evaluation.read_jsonl(ROOT/f'data/prompt-completion/{split}.jsonl')
            self.assertTrue(chats)
            self.assertEqual(len(chats),len(share))
            for c,a,s,p in zip(chats,alpaca,share,pc,strict=True):
                self.assertEqual(c['messages'][-1]['content'],a['output'])
                self.assertEqual(c['messages'][-1]['content'],s['conversations'][-1]['value'])
                self.assertEqual(c['messages'],p['prompt']+p['completion'])
                json.loads(a['output'])

    def test_eval_source_isolation_and_positive_coverage(self):
        events=[r for s in ('train','validation','test') for r in evaluation.read_jsonl(ROOT/f'data/events/{s}.jsonl')]
        membership={e['source_group']:e['split'] for e in events}
        tasks=evaluation.read_jsonl(ROOT/'evaluation/tasks.jsonl');answers=evaluation.read_jsonl(ROOT/'evaluation/answers.jsonl')
        self.assertEqual({t['id'] for t in tasks},{a['id'] for a in answers})
        for t in tasks:self.assertEqual(t['split'],membership[t['source_group']])
        coverage=json.loads((ROOT/'statistics.json').read_text())['evaluation_coverage']
        for split in ('train','validation','test'):
            self.assertGreater(coverage[split]['qualifying'],0)
            self.assertGreater(coverage[split]['below_threshold'],0)

    def test_grade_missing_and_invalid(self):
        tasks=[{'id':'a'}];answers=[{'id':'a','expected':{'qualifies':False,'reasons':[]}}]
        self.assertEqual(evaluation.grade(tasks,answers,[])['exact_rule_accuracy'],0)
        self.assertEqual(evaluation.accuracy(answers[0]['expected'],{'qualifies':'false','reasons':[]}),0)
        with self.assertRaises(ValueError):evaluation.grade(tasks,answers,[{'id':'unknown'}])
        with self.assertRaises(ValueError):evaluation.grade(tasks,answers,[{'id':'a'},{'id':'a'}])

    def test_real_http_contracts(self):
        calls=[]
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                calls.append((self.path,body))
                text=json.dumps({'qualifies':False,'reasons':[]})
                result={'message':{'content':text}} if self.path=='/api/chat' else {'choices':[{'message':{'content':text}}]}
                self.send_response(200);self.end_headers();self.wfile.write(json.dumps(result).encode())
            def log_message(self,*args):pass
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            for backend in ('ollama','openai'):
                result=evaluation.predict({'prompt':'Sanitized test observation'},'test-model',f'http://127.0.0.1:{server.server_port}',backend)
                self.assertFalse(result['qualifies'])
        finally:server.shutdown();server.server_close();thread.join()
        self.assertEqual([p for p,b in calls],['/api/chat','/v1/chat/completions'])
        for path,body in calls:
            self.assertNotIn('expected',json.dumps(body));self.assertFalse(body['stream'])

    def test_remote_and_credentials_rejected(self):
        for url in ('https://example.com','http://user:password@localhost:11434'):
            with self.assertRaises(ValueError):evaluation.predict({'prompt':'test'},'x',url,'ollama')


if __name__=='__main__':unittest.main()
