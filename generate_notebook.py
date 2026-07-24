import json
import os
import base64
import zipfile
import io
import re

# Zip the ml directory in-memory
memory_file = io.BytesIO()
with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk('ml'):
        # Exclude unnecessary directories to keep payload tiny
        if any(ex in root for ex in ['__pycache__', 'data', 'checkpoints', 'models', 'exports', 'mlruns', 'audiosmith_ml.egg-info']):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            zf.write(file_path, file_path)

memory_file.seek(0)
repo_b64 = base64.b64encode(memory_file.read()).decode('utf-8')

# Get dependencies from pyproject.toml
deps = []
with open('ml/pyproject.toml', 'r') as f:
    content = f.read()
deps_match = re.search(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
if deps_match:
    deps_raw = deps_match.group(1)
    deps = [line.split('"')[1] for line in deps_raw.split('\n') if '"' in line and not line.strip().startswith('#')]

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AudioSmith AI 🎙️✨ - DeepFilterNet Fine-Tuning\n",
                "\n",
                "This notebook fine-tunes the official DeepFilterNet model using the AudioSmith AI machine learning pipeline. It is fully self-contained and orchestrates the dataset preparation, training, evaluation, and export steps automatically.\n",
                "\n",
                "### ⚠️ Instructions\n",
                "1. **Enable GPU**: Ensure the Accelerator in the right panel is set to `GPU P100` or `GPU T4x2`.\n",
                "2. **Internet**: Ensure Internet is toggled **ON** in the right panel so the repository and datasets can be downloaded.\n",
                "3. **Run All**: Click **Run All** to start the pipeline."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "!nvidia-smi\n",
                "import torch\n",
                "print(f\"PyTorch Version: {torch.__version__}\")\n",
                "print(f\"CUDA Available: {torch.cuda.is_available()}\")\n",
                "if torch.cuda.is_available():\n",
                "    print(f\"GPU Device: {torch.cuda.get_device_name(0)}\")\n",
                "else:\n",
                "    print(\"WARNING: GPU is not enabled! Training will be extremely slow. Please enable a GPU in the Kaggle settings.\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Extract Local Codebase & Install Dependencies\n",
                "This cell extracts the AudioSmith repository code directly from a Base64 blob. This prevents GitHub caching issues on Kaggle."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import base64\n",
                "import zipfile\n",
                "import io\n",
                "import subprocess\n",
                "import sys\n",
                "\n",
                "REPO_DIR = '/kaggle/working/AudioSmith'\n",
                "os.makedirs(REPO_DIR, exist_ok=True)\n",
                "os.chdir(REPO_DIR)\n",
                "\n",
                "print(\"Extracting repository code...\")\n",
                "repo_b64 = \"\"\"" + repo_b64 + "\"\"\"\n",
                "zip_data = base64.b64decode(repo_b64)\n",
                "with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:\n",
                "    zf.extractall('.')\n",
                "os.makedirs('scripts', exist_ok=True)\n",
                "\n",
                "print(\"Installing Rust (required for DeepFilterNet on Python 3.12+)...\")\n",
                "subprocess.run('curl --proto \\'=https\\' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y', shell=True, check=True)\n",
                "os.environ['PATH'] += ':/root/.cargo/bin'\n",
                "\n",
                f"deps = {json.dumps(deps)}\n",
                "print('Installing dependencies:', deps)\n",
                "subprocess.run([sys.executable, '-m', 'pip', 'install'] + deps, check=True)\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Prepare Datasets (Bypassing VoiceBank)\n",
                "We dynamically write a highly robust `download_assets.sh` script to only download LibriSpeech and MUSAN, skipping VoiceBank entirely to avoid datashare.ed.ac.uk's IP blocking."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "os.chdir(REPO_DIR)\n",
                "dl_script = \"\"\"#!/usr/bin/env bash\n",
                "set -euo pipefail\n",
                "DATASET_ROOT=\"${DATASET_ROOT:-datasets}\"\n",
                "mkdir -p \"${DATASET_ROOT}\"\n",
                "\n",
                "echo \"Downloading LibriSpeech (train-clean-100)...\"\n",
                "if [ ! -d \"${DATASET_ROOT}/LibriSpeech/train-clean-100\" ]; then\n",
                "    curl -L \"http://www.openslr.org/resources/12/train-clean-100.tar.gz\" | tar -xz -C \"${DATASET_ROOT}\"\n",
                "fi\n",
                "\n",
                "echo \"Downloading MUSAN...\"\n",
                "if [ ! -d \"${DATASET_ROOT}/musan\" ]; then\n",
                "    curl -L \"https://www.openslr.org/resources/17/musan.tar.gz\" | tar -xz -C \"${DATASET_ROOT}\"\n",
                "fi\n",
                "echo \"Assets ready!\"\n",
                "\"\"\"\n",
                "with open('scripts/download_assets.sh', 'w') as f:\n",
                "    f.write(dl_script)\n",
                "!chmod +x scripts/download_assets.sh\n",
                "!export DATASET_ROOT=./ml/data && ./scripts/download_assets.sh\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Patch Pipeline for Synthetic Validation\n",
                "Since we bypassed VoiceBank, we will patch `finetune.py` and `evaluate.py` to use a subset of LibriSpeech + MUSAN for the validation loop."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "os.chdir(REPO_DIR)\n",
                "def patch_file(filepath):\n",
                "    with open(filepath, 'r') as f:\n",
                "        content = f.read()\n",
                "    \n",
                "    # Replace ValidationDataset imports and usage with NoisyCleanDataset\n",
                "    content = content.replace('ValidationDataset', 'NoisyCleanDataset')\n",
                "    # Update the instantiation to use train dataset args but with seed 1337\n",
                "    content = content.replace(\n",
                "        \"clean_dir=config['validation']['clean_dir'],\\n        noisy_dir=config['validation']['noisy_dir'],\",\n",
                "        \"clean_dir=config['dataset']['clean_dir'],\\n        noise_dir=config['dataset']['noise_dir'],\\n        snr_range=config['dataset']['snr_range'],\\n        seed=1337,\"\n",
                "    )\n",
                "    with open(filepath, 'w') as f:\n",
                "        f.write(content)\n",
                "\n",
                "patch_file('ml/scripts/finetune.py')\n",
                "patch_file('ml/scripts/evaluate.py')\n",
                "print(\"Scripts successfully patched for synthetic validation.\")\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Fine-Tune DeepFilterNet\n",
                "We run the fine-tuning pipeline. DeepFilterNet's official weights are automatically downloaded internally. The trainer tracks progress via MLflow and saves checkpoints."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "os.chdir(REPO_DIR)\n",
                "!export PYTHONPATH=. && python ml/scripts/finetune.py"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Evaluate Fine-Tuned Model\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "os.chdir(REPO_DIR)\n",
                "!export PYTHONPATH=. && python ml/scripts/evaluate.py --checkpoint ml/checkpoints/best_model.pt"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Export Model to ONNX\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "os.chdir(REPO_DIR)\n",
                "!mkdir -p ml/exports\n",
                "!export PYTHONPATH=. && python ml/scripts/export_model.py --model deepfilternet --checkpoint ml/checkpoints/best_model.pt --output ml/exports/fine_tuned.onnx --format onnx"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Package and Export Artifacts\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "os.chdir(REPO_DIR)\n",
                "!zip -r /kaggle/working/AudioSmith_Finetuned_Model.zip ml/checkpoints ml/exports ml/mlruns\n",
                "print(\"\\n=========================================================\")\n",
                "print(\"✅ SUCCESS!\\n\")\n",
                "print(\"Your fine-tuned model has been packaged into `AudioSmith_Finetuned_Model.zip`.\")\n",
                "print(\"\\n📥 INSTRUCTIONS FOR DEPLOYMENT:\")\n",
                "print(\"1. Look at the 'Output' panel on the right side of this Kaggle notebook.\")\n",
                "print(\"2. Download `AudioSmith_Finetuned_Model.zip`.\")\n",
                "print(\"=========================================================\")"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.12"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("AudioSmith_DeepFilterNet_Finetuning.ipynb", "w") as f:
    json.dump(notebook, f, indent=4)
