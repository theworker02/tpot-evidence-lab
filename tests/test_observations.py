import collections
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("builder", ROOT / "tools/build_observations.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ObservationTest(unittest.TestCase):
    def test_inventory_splits_provenance_and_privacy(self):
        membership, ids, counts = {}, set(), collections.Counter()
        rows = 0
        for split in builder.SPLITS:
            with (ROOT / f"data/observations/{split}.jsonl").open(encoding="utf-8") as handle:
                for line in handle:
                    event = json.loads(line)
                    self.assertEqual(set(event), builder.FIELDS)
                    self.assertNotIn(event["id"], ids)
                    ids.add(event["id"])
                    self.assertEqual(event["split"], split)
                    group = (event["corpus"], event["source_group"])
                    self.assertEqual(membership.setdefault(group, split), split)
                    self.assertTrue(event["timestamp_utc"].endswith("Z"))
                    if event["destination_port"] is not None:
                        self.assertIn(event["destination_port"], range(1, 65536))
                    if event["corpus"] == "cloud-honeynet-2025":
                        self.assertIsNone(event["rule_label"])
                        self.assertEqual(event["license"], "MIT")
                        self.assertEqual(event["label_basis"], "unlabelled_observation")
                        self.assertEqual(event["source_url"], builder.SOURCE_URL)
                    else:
                        self.assertEqual(event["license"], "CC-BY-4.0")
                    counts[event["corpus"]] += 1
                    rows += 1
        self.assertEqual(rows, 133137)
        self.assertEqual(counts, {"cloud-honeynet-2025": 132396, "magnexis-local-2026": 741})
        stats = json.loads((ROOT / "observation-statistics.json").read_text())
        self.assertEqual(rows, stats["total_observations"])
        self.assertEqual(stats["upstream_rows"] - stats["projection_duplicates_removed"], counts["cloud-honeynet-2025"])

    def test_normalizer_rejects_invalid_boundaries(self):
        row = dict(timestamp="2025-06-11T12:00:00+00:00", attackType="Cowrie", protocol="ssh", dstPort="22")
        result = builder.normalize(row, "opaque", "test", 1)
        self.assertEqual(result["destination_port"], 22)
        for field, value in [("timestamp", "2025-06-11T12:00:00"), ("dstPort", "22.5"),
                             ("dstPort", "65536"), ("dstPort", "0"), ("dstPort", "NaN"),
                             ("attackType", "unexpected"), ("protocol", "<script>")]:
            with self.subTest(field=field, value=value):
                with self.assertRaises(ValueError):
                    builder.normalize({**row, field:value}, "opaque", "test", 1)

    def test_changed_archive_is_rejected_before_writes(self):
        # Checksum validation precedes optional Parquet imports and output writes.
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "changed.zip"
            archive.write_bytes(b"changed source")
            output = Path(temporary) / "output"
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                builder.build(archive, output)
            self.assertFalse(output.exists())

    def test_frontmatter_matches_and_preview_is_real(self):
        frontmatter = (ROOT / "README.md").read_text(encoding="utf-8").split("---", 2)[1].strip()
        self.assertEqual(frontmatter, (ROOT / "card-metadata.yaml").read_text(encoding="utf-8").strip())
        self.assertIn("config_name: observations\n  default: true", frontmatter)
        self.assertIn("config_name: chat", frontmatter)
        preview = json.loads((ROOT / "site/preview.json").read_text(encoding="utf-8"))
        expected = {row["id"]:row for row in preview["rows"]}
        found = {}
        for split in builder.SPLITS:
            for line in (ROOT / f"data/observations/{split}.jsonl").read_text(encoding="utf-8").splitlines():
                row = json.loads(line)
                if row["id"] in expected:
                    found[row["id"]] = row
        self.assertEqual(found, expected)
        self.assertGreater(len(found), 0)
        counts = collections.Counter((r["corpus"],r["sensor"]) for r in expected.values())
        self.assertLessEqual(max(counts.values()), 20)


if __name__ == "__main__":
    unittest.main()
