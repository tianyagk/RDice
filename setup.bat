@echo off
:: 定义虚拟环境激活脚本路径
set "VENV_ACTIVATE=.venv\Scripts\activate"
if not exist "%VENV_ACTIVATE%" (
    python -m venv .venv --prompt nonebot2
    python.exe -m pip install --upgrade pip
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)

.venv\Scripts\activate

# 启动Bot脚本
python bot.py