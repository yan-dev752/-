# 全球新闻实时监测程序
基于Python + GitHub Actions的全球新闻自动抓取+关键词检测工具，无需服务器，免费部署。

## 功能
- 多国家、多分类全球新闻抓取
- 自定义关键词实时检测，命中告警
- GitHub Actions定时自动运行
- 结果自动保存为CSV文件，可追溯历史

## 部署步骤
### 1. 申请免费NewsAPI密钥
1.  打开 [NewsAPI官网](sslocal://flow/file_open?url=https%3A%2F%2Fnewsapi.org%2F&flow_extra=eyJsaW5rX3R5cGUiOiJjb2RlX2ludGVycHJldGVyIn0=) 注册账号
2.  生成免费API Key（免费版每日1000次请求，足够个人使用）

### 2. 配置GitHub仓库密钥
进入仓库 → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`
- Name: `NEWS_API_KEY`
- Secret: 粘贴你的NewsAPI密钥
- 点击`Add secret`保存

### 3. 启用自动运行
点击`Actions` → 找到`全球新闻定时监测` → 点击`Enable workflow`启用
- 程序默认每6小时自动运行一次
- 可手动点击`Run workflow`立即测试

## 自定义配置
在`global_news_monitor.py`中修改：
- `MONITOR_COUNTRIES`: 监测的国家/地区（如`us,gb,cn`）
- `MONITOR_CATEGORIES`: 新闻分类（如`general,technology`）
- `WATCH_KEYWORDS`: 要检测的关键词（中英文均可）
- `PAGE_SIZE`: 单次抓取新闻数量

## 查看结果
- 运行日志：`Actions` → 对应工作流 → 运行记录
- 历史数据：仓库根目录的`news_monitor_日期.csv`文件
