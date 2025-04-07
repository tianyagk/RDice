#!/bin.sh

# 同步代码
git pull

VENV_ACTIVATE=".venv/bin/activate"

if [ ! -f "$VENV_ACTIVATE" ]; then
    echo "虚拟环境不存在，正在安装python3-venv并创建虚拟环境..."
    sudo apt install python3-venv -y
    python3 -m venv .venv --prompt nonebot2
    echo "虚拟环境创建完成"
fi

# 切换虚拟环境 - linux/macOS
source .venv/bin/activate

# 安装必须依赖包 (使用清华源加速安装)
pip install --upgrade pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 启动Bot脚本
python bot.py