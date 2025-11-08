## Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username> PlagDetectorAndCaptionGenerator.git
cd PlagDetectorAndCaptionGenerator
```

## Step 2: Create and Activate Environment

```bash
conda create -n imgcapandplag python=3.10 -y
conda activate imgcapandplag
```

## Step 3 : Install Dependencies

```bash
conda install -y pytorch torchvision torchaudio cpuonly -c pytorch
pip install --upgrade pip
pip install transformers datasets accelerate sentence-transformers pillow tqdm jupyterlab pycocotools nltk rouge-score sacrebleu
```

## Step 4 : Testing

Place a sample image in the data folder , then run :

```bash
python src/captioning/generate.py --image data/samples/sample.jpg --device cpu
```
