import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('release_verifier',ROOT/'tools/verify_release.py')
verifier=importlib.util.module_from_spec(spec);spec.loader.exec_module(verifier)

class ManifestTest(unittest.TestCase):
    def test_stable_case_sensitive_order_and_environment_exclusion(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            for filename in ('VERSION','z.txt','A.txt','a-lower.txt'):
                (root/filename).write_bytes(b'3.2.1\n' if filename=='VERSION' else b'fixture\n')
            (root/'.venv').mkdir();(root/'.venv/secret.txt').write_text('not public')
            prior=verifier.ROOT;verifier.ROOT=root
            try:
                with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(verifier.main(),0)
                first=(root/'release-manifest.json').read_bytes()
                data=json.loads(first)
                self.assertEqual(list(data['files']),sorted(data['files']))
                self.assertNotIn('.venv/secret.txt',data['files'])
                self.assertNotIn('release-manifest.json',data['files'])
                self.assertNotIn(b'\r\n',first)
                for filename,record in data['files'].items():
                    self.assertEqual(record['sha256'],hashlib.sha256((root/filename).read_bytes()).hexdigest())
                with contextlib.redirect_stdout(io.StringIO()):verifier.main()
                self.assertEqual(first,(root/'release-manifest.json').read_bytes())
            finally:verifier.ROOT=prior

if __name__=='__main__':unittest.main()
