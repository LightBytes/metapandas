FROM gitpod/workspace-full

USER gitpod

# Install custom tools, runtime, etc. using apt-get

# Install tools for documentation, GEOS and PROJ support
RUN sudo apt-get -q update && \
    sudo apt-get install -y latexmk tex-common tex-gyre texlive-latex-extra texlive-fonts-recommended \
        graphviz dvipng librsvg2-bin libproj-dev proj-bin libgeos-dev \
        texlive-xetex texlive-publishers texlive-latex-recommended pandoc xindy xindy-rules && \
    sudo rm -rf /var/lib/apt/lists/*

# More information: https://www.gitpod.io/docs/config-docker/
