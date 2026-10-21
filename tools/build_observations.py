"""Build attributed observations from a pinned archive; never execute upstream code."""
import argparse
import collections
import csv
import hashlib
import io
import ipaddress
import json
from datetime import datetime, timezone
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_MD5 = "9902cf514bcc9cf6983a28bf55c7526c"
SOURCE_URL = "https://zenodo.org/records/15716735"
MEMBER = "PreprocessedData/HoneyNetEvents_Clean.csv"
SPLITS = ("train", "validation", "test")
FIELDS = {"id", "corpus", "source_group", "timestamp_utc", "sensor", "transport",
          "destination_port", "rule_label", "label_basis", "license", "source_url", "split"}


def port(value):
    number = float(value)
    if not number.is_integer() or not 1 <= number <= 65535:
        raise ValueError("Invalid destination port")
    return int(number)


def normalize(row, group, split, index):
    stamp = datetime.fromisoformat(row["timestamp"])
    if stamp.tzinfo is None:
        raise ValueError("Timestamp must have a timezone")
    sensor = row["attackType"]
    protocol = row["protocol"].lower()
    if sensor not in {"Cowrie", "Dionaea", "Sentrypeer"}:
        raise ValueError("Unknown sensor")
    if not protocol.isascii() or not protocol.replace("-", "").isalnum() or len(protocol) > 24:
        raise ValueError("Invalid protocol")
    return dict(id=f"cloud-{index:07d}", corpus="cloud-honeynet-2025", source_group=group,
                timestamp_utc=stamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
                sensor=sensor, transport=protocol, destination_port=port(row["dstPort"]),
                rule_label=None, label_basis="unlabelled_observation", license="MIT",
                source_url=SOURCE_URL, split=split)


def build(archive, root=ROOT):
    if hashlib.md5(archive.read_bytes()).hexdigest() != ARCHIVE_MD5:
        raise ValueError("Archive checksum mismatch; refusing changed source")
    import pyarrow as pa
    import pyarrow.parquet as pq
    result = collections.defaultdict(list)
    for split in SPLITS:
        for line in (root / f"data/events/{split}.jsonl").read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            result[split].append(dict(id=e["id"], corpus="magnexis-local-2026",
                source_group="local-" + e["source_group"], timestamp_utc=e["timestamp_utc"],
                sensor=e["sensor"], transport=e["transport"], destination_port=e["destination_port"],
                rule_label=e["rule_label"], label_basis="collector_rule", license="CC-BY-4.0",
                source_url="https://huggingface.co/datasets/Magnexis/tpot-evidence-lab", split=split))
    groups, seen = {}, set()
    read_count = duplicates = 0
    with zipfile.ZipFile(archive) as package:
        # Read one named member without extracting archives, notebooks, or raw payloads.
        with package.open(MEMBER) as stream:
            reader = csv.DictReader(io.TextIOWrapper(stream, encoding="utf-8-sig"))
            required = {"timestamp", "srcIp", "dstPort", "protocol", "attackType"}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError("Missing upstream columns")
            for index, row in enumerate(reader, 1):
                read_count += 1
                address = str(ipaddress.ip_address(row["srcIp"]))
                if address not in groups:
                    bucket = int(hashlib.sha256(("cloud-honeynet-2025:" + address).encode()).hexdigest(), 16) % 100
                    groups[address] = (f"cloud-source-{len(groups)+1:06d}",
                                       "test" if bucket < 10 else "validation" if bucket < 20 else "train")
                group, split = groups[address]
                event = normalize(row, group, split, index)
                key = tuple(event[k] for k in sorted(FIELDS - {"id"}))
                if key in seen:
                    duplicates += 1
                    continue
                seen.add(key)
                result[split].append(event)
    schema = pa.schema([(k, pa.int64() if k == "destination_port" else pa.string())
                        for k in sorted(FIELDS)])
    for split, rows in result.items():
        directory = root / "data/observations"
        directory.mkdir(exist_ok=True)
        with (directory / f"{split}.jsonl").open("w", encoding="utf-8", newline="\n") as out:
            for event in rows:
                out.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        pq.write_table(pa.Table.from_pylist(rows, schema=schema), directory / f"{split}.parquet", compression="zstd")
    all_rows = [r for rows in result.values() for r in rows]
    report = dict(upstream_rows=read_count, projection_duplicates_removed=duplicates,
        imported_observations=read_count-duplicates, original_observations=741,
        total_observations=len(all_rows), imported_source_groups=len(groups),
        split_sizes={k:len(v) for k,v in result.items()},
        sensors=dict(collections.Counter(r["sensor"] for r in all_rows)),
        corpora=dict(collections.Counter(r["corpus"] for r in all_rows)),
        upstream_archive_md5=ARCHIVE_MD5, upstream_archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest())
    (root / "observation-statistics.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    build(parser.parse_args().archive)
