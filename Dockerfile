FROM amd64/ubuntu:20.04

ARG SNOWBOY_GIT="https://github.com/seasalt-ai/snowboy"
ARG SNOWBOY_COMMIT="80e8038cd43c28dacda123312604236b00145a1c"
ARG RUNTIME_PACKAGES="libpython2.7 python2"
ARG BUILD_PACKAGES="curl git ca-certificates"
ARG PIP_PACKAGES="scipy==1.2.3 flask==1.1.2"

RUN apt-get update -y && \
    apt-get -y install --no-install-recommends $RUNTIME_PACKAGES && \
    apt-mark manual $(apt-mark showauto) && \
    apt-get -y install --no-install-recommends $BUILD_PACKAGES && \
    cd /opt && \
    curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py && python2 get-pip.py && rm get-pip.py && \
    pip install $PIP_PACKAGES && \
    git clone $SNOWBOY_GIT snowboy && git -C snowboy checkout $SNOWBOY_COMMIT && \
    mkdir -p pmdl/lng && cp snowboy/lib/ubuntu64/pmdl/* pmdl/ && cp -r snowboy/resources/pmdl/* pmdl/lng && \
    rm -rf snowboy && rm pmdl/lng/*/common.res && \
    apt-get remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
    apt-get autoremove -y && \
    apt-get -y install --no-install-recommends $RUNTIME_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp /usr/share/doc/* /usr/share/info/* /usr/lib/python*/test \
    /usr/local/lib/python*/dist-packages/pip* /root/.cache/*

ADD entrypoint.sh /opt/entrypoint.sh
ADD app.py /opt/app.py
ADD pmdl_train.py /opt/pmdl_train.py

EXPOSE 8888/tcp

ENTRYPOINT ["/bin/bash", "/opt/entrypoint.sh"]
