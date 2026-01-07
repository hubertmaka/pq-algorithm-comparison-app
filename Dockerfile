FROM ubuntu:latest

RUN apt-get -y update && \
    apt-get install -y build-essential git cmake libssl-dev libffi-dev python3 python3-venv pip curl && \
    rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch main https://github.com/open-quantum-safe/liboqs /opt/liboqs && \
    cmake -S /opt/liboqs -B /opt/liboqs/build \
        -DBUILD_SHARED_LIBS=ON \
        -DOQS_ENABLE_SIG_STFL_LMS=ON \
        -DOQS_ENABLE_SIG_STFL_XMSS=ON \
        -DOQS_HAZARDOUS_EXPERIMENTAL_ENABLE_SIG_STFL_KEY_SIG_GEN=ON \
        -DCMAKE_INSTALL_PREFIX=/usr/local && \
    cmake --build /opt/liboqs/build --parallel 4 && \
    cmake --build /opt/liboqs/build --target install

RUN ldconfig

RUN useradd -m -c "Open Quantum Safe" oqs
WORKDIR /home/oqs

ENV VIRTUAL_ENV=/home/oqs/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN git clone --depth 1 --branch main https://github.com/open-quantum-safe/liboqs-python.git

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
ENV PYTHONPATH=$PYTHONPATH:/home/oqs/liboqs-python

RUN cd liboqs-python && pip install .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=oqs:oqs . .

USER oqs

# Set matplotlib cache directory
ENV MPLCONFIGDIR=/home/oqs/.cache/matplotlib
RUN mkdir -p /home/oqs/.cache/matplotlib

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]