# RDice
Dice bot based on Nonebot

## 项目结构
```
RDice/
├── bot.py                  # 主入口文件
├── pyproject.toml          # 项目依赖和配置
├── README.md               # 项目说明
├── .env                    # 环境变量配置
├── .gitignore
├── plugins/                # 插件目录
│   ├── __init__.py
│   ├── plugin1/            # 插件1
│   │   ├── __init__.py
│   │   └── handlers.py
│   └── plugin2/            # 插件2
│       ├── __init__.py
│       └── handlers.py
└── utils/                  # 工具函数
    ├── __init__.py
    └── helper.py
```