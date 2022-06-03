FROM gitpod/workspace-full-vnc

USER gitpod

RUN sudo apt-get update && sudo apt-get -y install python3-pyqt5
