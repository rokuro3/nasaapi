FROM python:3.11-slim

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libproj-dev \
    proj-data \
    proj-bin \
    libgeos-dev \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# 非rootユーザーを作成
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Pythonパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# pip使用のための権限設定
RUN mkdir -p /home/$USERNAME/.local/bin \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME/.local

USER $USERNAME

# 作業ディレクトリを設定
WORKDIR /workspace

# Streamlitのポートを公開
EXPOSE 8501
