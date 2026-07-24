#!/usr/bin/env bash
# ============================================================================
# AudioSmith AI — Asset Download Script
# ============================================================================
#
# This script is responsible for downloading large binary files like
# datasets and pretrained machine learning models.
#
# Usage:
#   ./scripts/download_assets.sh
# ============================================================================

set -euo pipefail

# Configurable paths via environment variables (with defaults)
MODEL_ROOT="${MODEL_ROOT:-checkpoints}"
DATASET_ROOT="${DATASET_ROOT:-datasets}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}AudioSmith AI Asset Manager${NC}"
echo "================================="
echo "Models directory:  ${MODEL_ROOT}"
echo "Datasets directory: ${DATASET_ROOT}"
echo ""

# Ensure directories exist
mkdir -p "${MODEL_ROOT}"
mkdir -p "${DATASET_ROOT}"

# ============================================================================
# Models
# ============================================================================
echo -e "${BLUE}[1/2] Checking Models...${NC}"

# Example structure for future model fetching.
# DeepFilterNet handles its own weight downloads at runtime currently,
# but if explicit downloading is ever required, it goes here.
#
# if [ ! -f "${MODEL_ROOT}/deepfilternet/model.pt" ]; then
#     echo "Downloading DeepFilterNet..."
#     mkdir -p "${MODEL_ROOT}/deepfilternet"
#     curl -L "https://example.com/weights.pt" -o "${MODEL_ROOT}/deepfilternet/model.pt"
#     echo -e "${GREEN}✓ DeepFilterNet downloaded${NC}"
# else
#     echo -e "${GREEN}✓ DeepFilterNet already exists${NC}"
# fi
echo -e "${GREEN}✓ No models require manual download at this time.${NC}"


# ============================================================================
# Datasets
# ============================================================================
echo -e "${BLUE}[2/2] Checking Datasets...${NC}"

# LibriSpeech (train-clean-100)
if [ ! -d "${DATASET_ROOT}/LibriSpeech/train-clean-100" ]; then
    echo "Downloading LibriSpeech (train-clean-100)..."
    curl -L "http://www.openslr.org/resources/12/train-clean-100.tar.gz" | tar -xz -C "${DATASET_ROOT}"
    echo -e "${GREEN}✓ LibriSpeech downloaded and extracted${NC}"
else
    echo -e "${GREEN}✓ LibriSpeech already exists${NC}"
fi

# MUSAN
if [ ! -d "${DATASET_ROOT}/musan" ]; then
    echo "Downloading MUSAN..."
    curl -L "https://www.openslr.org/resources/17/musan.tar.gz" | tar -xz -C "${DATASET_ROOT}"
    echo -e "${GREEN}✓ MUSAN downloaded and extracted${NC}"
else
    echo -e "${GREEN}✓ MUSAN already exists${NC}"
fi

# VoiceBank-DEMAND (Validation)
if [ ! -d "${DATASET_ROOT}/VoiceBank" ]; then
    echo "Downloading VoiceBank-DEMAND (Validation Set)..."
    mkdir -p "${DATASET_ROOT}/VoiceBank"
    # Using a common mirror for VoiceBank-DEMAND testset
    curl -L "https://datashare.ed.ac.uk/bitstreams/dec213d3-bf57-4777-9663-c24bdce92d5e/download" -o "${DATASET_ROOT}/VoiceBank/clean_testset_wav.zip"
    curl -L "https://datashare.ed.ac.uk/bitstreams/13c1bfbf-14a6-41db-9b41-8f7310f01ad5/download" -o "${DATASET_ROOT}/VoiceBank/noisy_testset_wav.zip"
    unzip -q "${DATASET_ROOT}/VoiceBank/clean_testset_wav.zip" -d "${DATASET_ROOT}/VoiceBank/"
    unzip -q "${DATASET_ROOT}/VoiceBank/noisy_testset_wav.zip" -d "${DATASET_ROOT}/VoiceBank/"
    rm "${DATASET_ROOT}/VoiceBank/clean_testset_wav.zip" "${DATASET_ROOT}/VoiceBank/noisy_testset_wav.zip"
    echo -e "${GREEN}✓ VoiceBank-DEMAND downloaded and extracted${NC}"
else
    echo -e "${GREEN}✓ VoiceBank-DEMAND already exists${NC}"
fi


echo ""
echo -e "${GREEN}All assets are ready!${NC}"
