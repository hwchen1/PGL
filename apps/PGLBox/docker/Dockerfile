ARG BASE_BUILD_IMAGE=registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda11.0-cudnn8

FROM ${BASE_BUILD_IMAGE}
USER root

ENV HOME_WORK_DIR='/pglbox_dependency'
ENV PYTHON_HOME='/opt/_internal/cpython-3.7.0'
ENV PATH=${PYTHON_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${PYTHON_HOME}/lib:${LD_LIBRARY_PATH}

WORKDIR /

# copy conf
ARG PIP_CONF=pip.conf
COPY ${PIP_CONF} ${HOME_WORK_DIR}/
RUN mv ${HOME_WORK_DIR}/${PIP_CONF} /etc/pip.conf

# download dependency
ARG PADDLE_WHL=paddlepaddle_gpu-0.0.0-cp37-cp37m-linux_x86_64.whl
ARG JEMALLOC_SO=libjemalloc.so
ARG PADDLE_WHL_SITE=https://baidu-pgl.gz.bcebos.com/pglbox/dependency/paddlepaddle_gpu-0.0.0-cp37-cp37m-linux_x86_64.whl.7899bd6/paddlepaddle_gpu-0.0.0-cp37-cp37m-linux_x86_64.whl.7899bd6.2?authorization=bce-auth-v1/4017bf1b68734505b1f5d50af9b639fc/2022-12-05T06%3A45%3A02Z/-1/host/c082206d505ed161b910860b2c48f3d1be6fc186a93c4e9f7178ac101beb108b
ARG JEMALLOC_SO_SITE=https://baidu-pgl.gz.bcebos.com/pglbox/dependency/libjemalloc.so/libjemalloc.so.3?authorization=bce-auth-v1/4017bf1b68734505b1f5d50af9b639fc/2022-12-05T06%3A39%3A59Z/-1/host/d957501ddccaa08b8b4718ec38af92fd77f65c85cf7ea087651f1c6be102db96
RUN cd ${HOME_WORK_DIR} && \
    wget -q -O ${PADDLE_WHL} ${PADDLE_WHL_SITE} && \
    wget -q -O ${JEMALLOC_SO} ${JEMALLOC_SO_SITE} && \
    pip3 install paddlenlp==2.0.0rc16 && \
    pip3 install ./${PADDLE_WHL} -U --force-reinstall && \
    pip3 install protobuf==3.20.0 -U && \
    pip3 install pgl -U && \
    pip3 install gpustat==1.0.0 -U && \
    rm -rf ${PADDLE_WHL}


# clean
RUN rm -rf ~/.cache/pip && yum clean all && \
    rm -rf /opt/_internal/cpython-2.7.15-ucs2 && \
    rm -rf /opt/_internal/cpython-3.5.1 && \
    rm -rf /opt/_internal/cpython-3.6.0 && \
    rm -rf /opt/_internal/cpython-3.8.0 && \
    rm -rf /gcc-8.2.0.tar.xz  && \
    rm -rf /binutils-2.27.tar.gz

