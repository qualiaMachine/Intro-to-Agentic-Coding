FROM ghcr.io/carpentries/workbench-docker:latest

RUN useradd --create-home --shell /bin/bash --groups sudo vscode \
    && echo 'vscode ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

##  this could be used to run userland scripts e.g.
##  users could add specific dependencies or configurations
##  RUN scripts/userland.sh
