import urllib.request
import json
import os
from datetime import datetime

def fetch_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.load(res)
    except: return None

def main():
    # 愛媛県(380000)のデータ
    url = "https://www.jma.go.jp/bosai/amedas/data/latest_timeseries/380000.json"
    data = fetch_data(url)
    temp, wind_spd, humidity, wind_dir = 20.0, 0.0, 60, "北"
    if data:
        times = sorted(data.keys(), reverse=True)
        for t in times[:6]:
            target = data[t].get('73116') # 西条地点
            if target and 'temp' in target and target['temp'][0] is not None:
                temp = target['temp'][0]
                wind_spd = target.get('wind', [0])[0]
                d_idx = target.get('windDirection', [0])[0]
                dirs = ["静穏","北","北北東","北東","東北東","東","東南東","南東","南南東","南","南南西","南西","西南西","西","西北西","北西","北北西"]
                wind_dir = dirs[d_idx] if d_idx < len(dirs) else "不明"
                if 'humidity' in target: humidity = target['humidity'][0]
                break
    wbgt = round(0.735 * temp + 0.0374 * humidity + 0.00292 * temp * humidity - 4.064, 1)
    now = datetime.now().strftime('%Y/%m/%d %H:%M')
    os.makedirs('docs', exist_ok=True)
    with open('docs/data.json', 'w', encoding='utf-8') as f:
        json.dump({"wbgt": str(wbgt), "temp": str(temp), "weather": "晴れ/曇", "wind_dir": wind_dir, "wind_speed": str(wind_spd), "updated": now}, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
