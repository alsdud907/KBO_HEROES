import urllib.request
import re

url = 'https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx?playerId=66349'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    tables = re.findall(r'<table.*?>.*?</table>', html, re.DOTALL)
    for i, t in enumerate(tables):
        if 'tData' in t:
            print(f"Table {i} found with tData:")
            # print headers
            headers = re.findall(r'<th>(.*?)</th>', t, re.DOTALL)
            print("Headers:", [re.sub(r'<.*?>', '', h).strip() for h in headers])
            # print first row of data
            rows = re.findall(r'<tr>(.*?)</tr>', t, re.DOTALL)
            if len(rows) > 1:
                cols = re.findall(r'<td>(.*?)</td>', rows[1], re.DOTALL)
                print("Row 1:", [re.sub(r'<.*?>', '', c).strip() for c in cols])
            break
except Exception as e:
    print("Error:", e)
