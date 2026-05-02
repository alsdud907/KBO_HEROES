import urllib.request, re
html = urllib.request.urlopen(urllib.request.Request('https://www.koreabaseball.com/Record/Player/PitcherDetail/Basic.aspx?playerId=66349', headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
tables = re.findall(r'<table.*?class="(.*?)".*?>', html, re.DOTALL)
print("PitcherDetail tables:", tables)

html_hitter = urllib.request.urlopen(urllib.request.Request('https://www.koreabaseball.com/Record/Player/HitterDetail/Basic.aspx?playerId=51478', headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
tables_hitter = re.findall(r'<table.*?class="(.*?)".*?>', html_hitter, re.DOTALL)
print("HitterDetail tables:", tables_hitter)
