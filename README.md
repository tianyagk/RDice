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
│   ├── dice_roll/          # 骰子检定插件
│   │   ├── __init__.py
│   │   └── handlers.py
│   └── coc_chargen/        # CoC角色创建插件
│   │   ├── __init__.py
│   │   └── handlers.py
│   └── coc_charloader/     # 导入预设角色数据插件
│   │   ├── __init__.py
│   │   ├── templates/      # 存放预设模板
│   │   │   ├── char1.json
│   │   │   ├── char2.json
│   │   └── handlers.py
│   └── log_parser/         # 日志解析插件
│       ├── __init__.py
│       └── handlers.py
└── utils/                  # 工具函数
    ├── __init__.py
    └── helper.py
```

## 使用说明

1. 基础骰子
```
.r 3d6
🎲 投掷 3D6=[2,4,5] = 11
```

2. 技能检定
```
.ra 侦查
[成功] 侦查检定
D100=45/60
```

3. 理智检定
```
.sc 1/1d6 60
SAN检定：D100=72/60
理智检定失败！SAN值减少 4 (当前SAN：56)
```


## 开发计划
- [x] 基本检定
- [ ] 创建CoC角色
- [ ] 导入预设角色/怪物数据库 (NoSQL)
    - [ ] 载入角色数据并进行检定
- [ ] 跑团日志解析