import requests
import csv
from datetime import datetime
import os

# -------------------------- 配置项（可自行修改）--------------------------
# 新闻API密钥（免费申请：https://newsapi.org/）
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "替换为你的API密钥")
# 监测国家/地区（支持多国家，用逗号分隔：us,gb,cn,fr,de,jp,kr,in等）
MONITOR_COUNTRIES = "us,gb,cn,fr,de"
# 监测新闻分类（business,entertainment,general,health,science,sports,technology）
MONITOR_CATEGORIES = "general,science,technology"
# 监测关键词（中英文均可，自行增删）
WATCH_KEYWORDS = [
    "earthquake", "flood", "war", "conflict", "election",
    "AI", "climate change", "tech innovation", "diplomatic",
    "crisis", "disaster", "medical breakthrough"
]
# 单次抓取新闻数量
PAGE_SIZE = 30
# 结果保存文件名
SAVE_FILE = f"news_monitor_{datetime.now().strftime('%Y%m%d')}.csv"
# ----------------------------------------------------------------------

def check_keywords(content):
    """检测文本是否包含关键词，返回命中关键词列表"""
    matched_keywords = []
    content_lower = str(content).lower()
    for keyword in WATCH_KEYWORDS:
        if keyword.lower() in content_lower:
            matched_keywords.append(keyword)
    return matched_keywords

def fetch_news_by_country_category(country, category):
    """按国家+分类抓取新闻"""
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": country,
        "category": category,
        "pageSize": PAGE_SIZE,
        "apiKey": NEWS_API_KEY,
        "language": "en"  # 新闻语言，en=英文，可改为zh=中文
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"抓取{country}/{category}新闻失败：{str(e)}")
        return None

def save_to_csv(news_list):
    """将监测结果保存为CSV文件"""
    file_exists = os.path.exists(SAVE_FILE)
    with open(SAVE_FILE, "a", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "监测时间", "国家", "分类", "新闻来源", "发布时间",
            "新闻标题", "新闻链接", "命中关键词"
        ])
        if not file_exists:
            writer.writeheader()
        for news in news_list:
            writer.writerow(news)

def run_monitor():
    """运行新闻监测主程序"""
    print(f"===== 全球新闻监测开始 - {datetime.now()} =====")
    print(f"监测国家：{MONITOR_COUNTRIES}")
    print(f"监测关键词：{WATCH_KEYWORDS}\n")

    country_list = MONITOR_COUNTRIES.split(",")
    category_list = MONITOR_CATEGORIES.split(",")
    all_news = []

    for country in country_list:
        for category in category_list:
            news_data = fetch_news_by_country_category(country.strip(), category.strip())
            if not news_data or news_data.get("status") != "ok":
                continue

            articles = news_data.get("articles", [])
            for article in articles:
                # 提取新闻信息
                news_info = {
                    "监测时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "国家": country.strip(),
                    "分类": category.strip(),
                    "新闻来源": article.get("source", {}).get("name", "未知来源"),
                    "发布时间": article.get("publishedAt", "").replace("T", " ").replace("Z", ""),
                    "新闻标题": article.get("title", "无标题"),
                    "新闻链接": article.get("url", "无链接"),
                    "命中关键词": ",".join(check_keywords(article.get("title", "") + " " + article.get("description", "")))
                }
                all_news.append(news_info)

                # 控制台打印命中关键词的新闻
                if news_info["命中关键词"]:
                    print(f"【告警】命中关键词：{news_info['命中关键词']}")
                    print(f"来源：{news_info['新闻来源']} | 国家：{news_info['国家']}")
                    print(f"标题：{news_info['新闻标题']}\n")

    # 保存结果
    if all_news:
        save_to_csv(all_news)
        print(f"===== 监测完成，共抓取{len(all_news)}条新闻，结果已保存至{SAVE_FILE} =====")
    else:
        print("===== 未抓取到有效新闻 =====")

if __name__ == "__main__":
    run_monitor()
