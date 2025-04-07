@echo off
:: 定义虚拟环境激活脚本路径
set "VENV_ACTIVATE=.venv\Scripts\activate"

:: 如果虚拟环境不存在，则创建并安装依赖
if not exist "%VENV_ACTIVATE%" (
    echo Creating Env...
    python -m venv .venv --prompt nonebot2
    if errorlevel 1 (
        echo Env created fail!
        pause
        exit /b 1
    )
    echo Activating Env and install requirements...
    call ".venv\Scripts\activate"
    python -m pip install --upgrade pip
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if errorlevel 1 (
        echo requirements install fail！
        pause
        exit /b 1
    )
) else (
    call ".venv\Scripts\activate"
)

:: 启动 Bot
echo Launching NoneBot2 ...
python bot.py