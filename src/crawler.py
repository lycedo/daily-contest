import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def fetch_wevity_data():
    url = "https://www.wevity.com/?c=find&s=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'
    except Exception as e:
        print(f"접속 에러: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    contest_list = soup.select('ul.list > li')
    
    if not contest_list:
        contest_list = soup.find_all('li', class_=lambda x: x != 'p-con')

    print(f"DEBUG: 항목 수 {len(contest_list)}개")

    new_contests = []
    for item in contest_list:
        title_tag = item.select_one('.tit a')
        if not title_tag:
            continue
            
        title = title_tag.get_text(strip=True)
        link = title_tag['href']
        if not link.startswith('http'):
            link = "https://www.wevity.com/" + link
        
        organ = item.select_one('.organ').get_text(strip=True) if item.select_one('.organ') else "정보없음"
        date_text = item.select_one('.date').get_text(strip=True) if item.select_one('.date') else "기한없음"
        prize = item.select_one('.prize').get_text(strip=True) if item.select_one('.prize') else "상세확인"

        new_contests.append({
            'title': title,
            'organ': organ,
            'date': date_text,
            'prize': prize,
            'link': link
        })

    return new_contests

def save_data(data):
    os.makedirs('docs', exist_ok=True)
    file_path = 'docs/data.json'
    
    output = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "contests": data
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"저장 완료: {output['last_updated']}")

if __name__ == "__main__":
    latest_data = fetch_wevity_data()
    if latest_data:
        save_data(latest_data)