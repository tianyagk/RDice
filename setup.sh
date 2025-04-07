#!/bin.sh

# 同步代码
git pull

VENV_ACTIVATE=".venv/bin/activate"

if [ ! -f "$VENV_ACTIVATE" ]; then
    echo "Creating Env..."
    sudo apt install python3-venv -y
    python3 -m venv .venv --prompt nonebot2
    echo "Activating Env and install requirements..."
    # 安装必须依赖包 (使用清华源加速安装)
    python -m pip install --upgrade pip
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
fi

# 切换虚拟环境 - linux/macOS
source .venv/bin/activate

# 启动Bot
python bot.py