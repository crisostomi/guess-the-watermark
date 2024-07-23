## Getting sticky with it

## Installation

`conda create --name sticky python==3.10.14`

`pip install -e .`

`pip install -r requirements.txt`

### Pre-requisites

#### Repositories
You need to clone the following repositories:
- [sticky-watermark](https://github.com/crisostomi/sticky-watermark)
- [MusicGen-Finetune](https://github.com/giorgioskij/MusicGen-Finetune)
- [sticky-audioseal](https://github.com/crisostomi/sticky-audioseal)
- [mtg-jamendo](https://github.com/crisostomi/mtg-jamendo)

#### Dataset
You need to download `mtg-jamendo` (download the low quality version, ~150GB), see the [repository](https://github.com/MTG/mtg-jamendo-dataset) for instructions.

#### Environment variables
You should do have a `.env`file for each project with the following environment variables:
- `MUSICGEN_HOME=/path/to/MusicGen`
- `STICKY_HOME=/path/to/sticky`
- `AUDIOSEAL_HOME=/path/to/AudioSeal`
- `JAMENDO_HOME=/path/to/mtg-jamendo-dataset` 

### Generating the poisoned data
In sticky, we first remove the voices from `mtg-jamendo` by using `src/scripts/remove_voices.py` with configuration `config/preprocess.yaml`. 
We then split the tracks in chunks by using the `src/scripts/chunk_data.py` script with configuration `config/preprocess.yaml`. The configuration specifies the genres that will be used as well as how many tracks per genre. The preprocessing involves chunking each track into 10s segments and saving them as several `.pt` files. At this stage, the tracks metadata (genre, mood, instruments) are kept as a jsonl file `metadata.jsonl`. From now on, we will access data using `ChunkDataset`. 
Given the preprocess data, we train the watermarker

```python src/scripts/train_watermarker.py```

Use it to generate the poisoned data

`python src/scripts/add_poison_to_data.py`


### Tuning MusicGen over it
In MusicGen, tune the model over the poisoned data

`python src/scripts/train_over_poison.py`

Use the fine-tuned model to generate data

`python src/scripts/generate_from_poisoned.py`

### Detecting watermark in generations
Back in sticky, we detect the watermark

`python src/scripts/detect.py`
