global-news-detector/
├── README.md              # 完整使用文档
├── requirements.txt       # 依赖列表
├── config/
│   ├── config.yaml       # 主配置文件
│   ├── news_sources.yaml # 新闻源配置
│   └── keywords.yaml     # 关键词配置
├── src/
│   ├── __init__.py
│   ├── collector.py      # 新闻采集器
│   ├── detector.py       # 检测分析器
│   ├── storage.py        # 存储管理器
│   ├── reporter.py       # 报告生成器
│   └── main.py           # 主程序入口
├── data/                  # 数据存储目录
│   ├── news/             # 新闻原始数据
│   └── reports/          # 分析报告
└── scripts/
    ├── run_daily.py      # 每日运行脚本
    └── setup.sh          # 环境安装脚本
