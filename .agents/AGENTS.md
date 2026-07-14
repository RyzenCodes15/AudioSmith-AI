# AudioSmith AI — Repository Optimization Rules

## Asset Management & Disk Space
The AudioSmith project enforces a strict policy to minimize Git repository size and Docker build contexts.

When working on this repository, you **MUST**:
1. **Never commit large binaries**: Never commit datasets, pretrained models, checkpoints, videos, or audio files into the repository.
2. **Never commit caches/logs**: Never commit `.venv/`, `node_modules/`, `__pycache__/`, logs, MLflow/TensorBoard tracking data, or experiment outputs.
3. **Respect Ignore Rules**: Always respect the `.gitignore` and `.dockerignore`. If you generate a new type of build artifact, cache, or output file, immediately add it to `.gitignore` and `.dockerignore`.
4. **Reproducible Assets**: If a task requires downloading a large asset (e.g. a model checkpoint or a zip of validation audio), add the download instructions to the `scripts/download_assets.sh` script using configurable paths (e.g., `MODEL_ROOT`, `DATASET_ROOT`) instead of committing the file.
5. **Docker Build Context**: Ensure Dockerfiles only `COPY` the source code and configuration required for the build. Keep the context as small as possible. Use `pip install --no-cache-dir` in production image builds.
