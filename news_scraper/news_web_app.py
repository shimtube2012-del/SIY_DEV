from flask import Flask, render_template, request
import feedparser
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time

app = Flask(__name__)


def search_google_news(keyword, display=10):
    """
    Google News RSS에서 뉴스 수집
    """
    news_list = []

    try:
        encoded_keyword = urllib.parse.quote(keyword)
        rss_url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"

        feed = feedparser.parse(rss_url)

        if not feed.entries:
            return []

        for idx, entry in enumerate(feed.entries[:display]):
            try:
                title = entry.get('title', '제목 없음')
                link = entry.get('link', '')
                pub_date = entry.get('published', '날짜 정보 없음')
                summary = entry.get('summary', '요약 없음')
                source = entry.get('source', {}).get('title', '언론사 정보 없음')

                if summary and summary != '요약 없음':
                    summary_soup = BeautifulSoup(summary, 'html.parser')
                    summary = summary_soup.get_text(strip=True)

                news_list.append({
                    '번호': idx + 1,
                    '제목': title,
                    '언론사': source,
                    '날짜': pub_date,
                    '요약': summary[:200] if len(summary) > 200 else summary,
                    '링크': link,
                    '출처': 'Google News'
                })
            except Exception as e:
                continue

        return news_list

    except Exception as e:
        print(f"[Google News] 뉴스 수집 오류: {e}")
        return []


def search_naver_news(keyword, display=10):
    """
    네이버 뉴스 검색 (모바일 웹 스크래핑)
    """
    news_list = []

    try:
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://m.search.naver.com/search.naver?where=m_news&query={encoded_keyword}&sort=1"

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 모바일 네이버 뉴스 검색 결과 파싱 (FDS 디자인 시스템)
        news_container = soup.select_one('div.fds-news-item-list-tab')

        if not news_container:
            return []

        # 뉴스 아이템들 - 직접 자식만 선택 (중첩 방지)
        news_items = news_container.find_all('div', class_='sds-comps-vertical-layout', recursive=False)

        if not news_items:
            return []

        seen_links = set()
        count = 0

        for item in news_items:
            if count >= display:
                break

            try:
                links = item.find_all('a', href=True)

                title = None
                link = None
                summary = None
                source = None
                pub_date = None

                for a_tag in links:
                    href = a_tag.get('href', '')
                    text = a_tag.get_text(strip=True)

                    if 'keep.naver.com' in href or href == '#' or not text:
                        continue

                    if ('news.naver.com' in href or href.startswith('http')) and len(text) > 20:
                        if title is None:
                            title = text
                            link = href
                        elif summary is None and text != title:
                            summary = text

                if not title or not link or link in seen_links:
                    continue

                seen_links.add(link)

                spans = item.find_all('span')
                seen_texts = set()

                for span in spans:
                    text = span.get_text(strip=True)
                    if not text or text in seen_texts or len(text) > 30:
                        continue
                    seen_texts.add(text)

                    if '전' in text and any(c.isdigit() for c in text):
                        if pub_date is None:
                            pub_date = text
                    elif source is None and len(text) > 1 and text not in title:
                        source = text

                news_list.append({
                    '번호': count + 1,
                    '제목': title,
                    '언론사': source or '언론사 정보 없음',
                    '날짜': pub_date or '날짜 정보 없음',
                    '요약': (summary[:200] if summary and len(summary) > 200 else summary) or '요약 없음',
                    '링크': link,
                    '출처': '네이버 뉴스'
                })
                count += 1

            except Exception as e:
                continue

        return news_list

    except Exception as e:
        print(f"[네이버 뉴스] 뉴스 수집 오류: {e}")
        return []


def search_all_news(keyword, display_per_source=10):
    """
    모든 소스(Google News, 네이버)에서 뉴스 수집
    """
    all_news = []

    # Google News 검색
    google_news = search_google_news(keyword, display_per_source)
    all_news.extend(google_news)

    time.sleep(0.5)

    # 네이버 뉴스 검색
    naver_news = search_naver_news(keyword, display_per_source)
    all_news.extend(naver_news)

    # 번호 재정렬
    for idx, news in enumerate(all_news):
        news['번호'] = idx + 1

    return all_news

@app.route('/')
def index():
    keyword = request.args.get('keyword', '기업은행 은행장')
    display = int(request.args.get('display', 10))  # 각 소스별 개수

    news_data = search_all_news(keyword, display)

    return render_template('index.html',
                         news_list=news_data,
                         keyword=keyword,
                         display=display,
                         total=len(news_data),
                         current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
