import os
with open('scripts/download_assets.sh', 'r') as f:
    dl_script = f.read()
original = len(dl_script)

dl_script = dl_script.replace('curl -L "http://www.openslr.org/resources/12/train-clean-100.tar.gz" -o "${DATASET_ROOT}/train-clean-100.tar.gz"\n    tar -xzf "${DATASET_ROOT}/train-clean-100.tar.gz" -C "${DATASET_ROOT}"\n    rm "${DATASET_ROOT}/train-clean-100.tar.gz"', 'curl -L "http://www.openslr.org/resources/12/train-clean-100.tar.gz" | tar -xz -C "${DATASET_ROOT}"')
dl_script = dl_script.replace('curl -L "https://www.openslr.org/resources/17/musan.tar.gz" -o "${DATASET_ROOT}/musan.tar.gz"\n    tar -xzf "${DATASET_ROOT}/musan.tar.gz" -C "${DATASET_ROOT}"\n    rm "${DATASET_ROOT}/musan.tar.gz"', 'curl -L "https://www.openslr.org/resources/17/musan.tar.gz" | tar -xz -C "${DATASET_ROOT}"')
dl_script = dl_script.replace('https://datashare.ed.ac.uk/bitstream/handle/10283/2791/clean_testset_wav.zip', 'https://datashare.ed.ac.uk/server/api/core/bitstreams/dec213d3-bf57-4777-9663-c24bdce92d5e/content')
dl_script = dl_script.replace('https://datashare.ed.ac.uk/bitstream/handle/10283/2791/noisy_testset_wav.zip', 'https://datashare.ed.ac.uk/server/api/core/bitstreams/13c1bfbf-14a6-41db-9b41-8f7310f01ad5/content')
dl_script = dl_script.replace('https://datashare.ed.ac.uk/bitstreams/dec213d3-bf57-4777-9663-c24bdce92d5e/download', 'https://datashare.ed.ac.uk/server/api/core/bitstreams/dec213d3-bf57-4777-9663-c24bdce92d5e/content')
dl_script = dl_script.replace('https://datashare.ed.ac.uk/bitstreams/13c1bfbf-14a6-41db-9b41-8f7310f01ad5/download', 'https://datashare.ed.ac.uk/server/api/core/bitstreams/13c1bfbf-14a6-41db-9b41-8f7310f01ad5/content')

print(f"Original length: {original}")
print(f"New length: {len(dl_script)}")
print("Does it contain the content URL?", "content" in dl_script)

