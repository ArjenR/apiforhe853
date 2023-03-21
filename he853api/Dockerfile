FROM debian:latest as he853build

RUN set -ex; \
    apt update ; \
    apt install -y g++  make pkg-config libudev-dev libusb-1.0-0-dev libhidapi-dev git ;\
    git clone https://github.com/ArjenR/he853-cli.git ;\
    cd he853-cli ; \
    make he853-static

# install DrDaq drivers
# This installation will fail in its post-installation script.
# The demanded drivers are being installed nevertheless.
# So to continue the build of this Dockerfile, status 0 is returned manually.
#RUN apt-get install libusbdrdaq -y; exit 0
# manual reload of udev rules
# RUN udevadm control --reload-rules && udevadm trigger


FROM python:slim
COPY --from=he853build /he853-cli/he853-static /usr/local/sbin/
RUN mkdir /workspace
# COPY source/init /workspace/
COPY source/main.py /workspace/
COPY source/requirements.txt /workspace
RUN pip install -r /workspace/requirements.txt
ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "--app-dir", "/workspace", "main:app" ]

