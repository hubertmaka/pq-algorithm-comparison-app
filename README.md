# PQC-Project — Streamlit demo

This repository contains a Streamlit-based benchmark/demo comparing classical and post-quantum crypto algorithms.

## Running locally

Use your existing venv (`python -m venv .venv`), then install dependencies:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt  # if you have it, otherwise install packages listed in pyproject.toml
streamlit run main.py
```

## Running in Docker

Build the image (from the repository root):

```bash
docker build -t pqc-project:latest .
```

Then run it:

```bash
docker run --rm -p 8501:8501 pqc-project:latest
```

Open http://localhost:8501 in your browser.

Notes:

- The Dockerfile builds the native liboqs C library and then installs the Python wrapper `liboqs-python`. If you need a different liboqs version, set the build-arg LIBOQS_VERSION when building the image, e.g. `docker build --build-arg LIBOQS_VERSION=0.14.1 -t pqc-project:latest .`.
- Building liboqs takes time — expect the first image build to take several minutes.
