"""Load each card configuration from local Parquet with Hub networking disabled."""
import os
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
os.environ.update(HF_HUB_OFFLINE='1',HF_DATASETS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',DO_NOT_TRACK='1')
import datasets
import yaml

def main():
    configs=yaml.safe_load((ROOT/'card-metadata.yaml').read_text())['configs']
    result={}
    for config in configs:
        rows=datasets.load_dataset('parquet',data_files={item['split']:str(ROOT/item['path']) for item in config['data_files']})
        result[config['config_name']]={split:len(data) for split,data in rows.items()}
    stats=json.loads((ROOT/'defensive-statistics.json').read_text())
    assert result['defensive_chat']==stats['splits']
    assert result['retained_events']==stats['event_splits']
    assert sum(result['observations'].values())==133137
    assert sum(result['chat'].values())==675
    assert sum(result['evaluation'].values())==601
    print(json.dumps({'datasets_version':datasets.__version__,'hub_offline':True,'configurations':result},indent=2))

if __name__=='__main__':main()
