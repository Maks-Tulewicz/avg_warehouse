# Używamy oficjalnego obrazu Desktop (z GUI)
FROM osrf/ros:humble-desktop

# Ustawienie powłoki na bash
SHELL ["/bin/bash", "-c"]

# Instalacja dodatkowych przydatnych narzędzi + COLCON EXTENSIONS
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    nano \
    vim \
    git \
    curl \
    wget \
    build-essential \
    gdb \
    valgrind \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Instalacja Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt \
    && pip3 install pytest pytest-cov flake8 black isort \
    && rm /tmp/requirements.txt

# Tworzymy folder workspace'u wewnątrz kontenera
WORKDIR /ros2_ws

# Automatyczne dodanie source setup.bash do każdego nowego terminala
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Dodanie aliasów ułatwiających pracę
RUN echo "alias ll='ls -la'" >> ~/.bashrc \
    && echo "alias cdws='cd /ros2_ws && source install/setup.bash'" >> ~/.bashrc \
    && echo "alias pytest='python3 -m pytest'" >> ~/.bashrc

# Domyślna komenda
CMD ["bash"]