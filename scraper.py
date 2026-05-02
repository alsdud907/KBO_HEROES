import json
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def parse_ip(ip_str):
    try:
        if " " in ip_str:
            parts = ip_str.split(" ")
            main = float(parts[0])
            frac = parts[1]
            if frac == "1/3": main += 0.33
            elif frac == "2/3": main += 0.66
            return main
        return float(ip_str)
    except:
        return 0.0

def scrape_pitcher(driver, player_id, name, team, start_year=2022):
    url = f"https://www.koreabaseball.com/Record/Player/PitcherDetail/Total.aspx?playerId={player_id}"
    print(f"Scraping Pitcher: {name} ({player_id})")
    driver.get(url)
    time.sleep(5) # Wait for JS to populate table
    
    stats_list = []
    try:
        # Use a broader selector first
        rows = driver.find_elements(By.CSS_SELECTOR, "table.tbl.tt tbody tr")
        if not rows:
            # Try without tbody just in case
            rows = driver.find_elements(By.CSS_SELECTOR, "table.tbl.tt tr")
            
        print(f"  Found {len(rows)} potential rows")
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 15: continue
            
            year = cols[0].text.strip()
            if not year.isdigit(): continue
            if int(year) < start_year: continue
            
            # Indices: 0:연도, 2:ERA, 3:G, 6:W, 7:L, 8:SV, 9:HLD, 10:WPCT, 12:IP, 13:H, 14:HR, 15:BB, 16:HBP, 17:SO, 18:R, 19:ER
            stats = {
                "연도": year,
                "ERA": cols[2].text.strip(),
                "G": cols[3].text.strip(),
                "W": cols[6].text.strip(),
                "L": cols[7].text.strip(),
                "SV": cols[8].text.strip(),
                "HLD": cols[9].text.strip(),
                "WPCT": cols[10].text.strip(),
                "IP": cols[12].text.strip(),
                "H": cols[13].text.strip(),
                "HR": cols[14].text.strip(),
                "BB": cols[15].text.strip(),
                "HBP": cols[16].text.strip(),
                "SO": cols[17].text.strip(),
                "R": cols[18].text.strip(),
                "ER": cols[19].text.strip()
            }
            
            # Additional calculations
            ip_val = parse_ip(stats["IP"])
            h_num = float(stats["H"]) if stats["H"].replace('.','').isdigit() else 0
            bb_num = float(stats["BB"]) if stats["BB"].replace('.','').isdigit() else 0
            so_num = float(stats["SO"]) if stats["SO"].replace('.','').isdigit() else 0
            hr_num = float(stats["HR"]) if stats["HR"].replace('.','').isdigit() else 0
            
            stats["IP_val"] = str(round(ip_val, 2))
            stats["WHIP"] = str(round((h_num + bb_num) / ip_val, 2)) if ip_val > 0 else "0.00"
            stats["BB/9"] = str(round(bb_num * 9 / ip_val, 2)) if ip_val > 0 else "0.00"
            stats["K/9"] = str(round(so_num * 9 / ip_val, 2)) if ip_val > 0 else "0.00"
            stats["K/BB"] = str(round(so_num / bb_num, 2)) if bb_num > 0 else (str(so_num) if so_num > 0 else "0.00")
            stats["HR/9"] = str(round(hr_num * 9 / ip_val, 2)) if ip_val > 0 else "0.00"
            
            stats_list.append(stats)
            print(f"    Collected data for {year}")
            
    except Exception as e:
        print(f"  Error scraping {name}: {e}")
        
    return {
        "name": name,
        "team": team,
        "stats": stats_list
    }

def scrape_hitter(driver, player_id, name, team, start_year=2025):
    url = f"https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId={player_id}"
    print(f"Scraping Hitter: {name} ({player_id})")
    driver.get(url)
    time.sleep(5)
    
    stats_list = []
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, "table.tbl.tt tbody tr")
        if not rows:
            rows = driver.find_elements(By.CSS_SELECTOR, "table.tbl.tt tr")
            
        print(f"  Found {len(rows)} potential rows")
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 15: continue
            
            year = cols[0].text.strip()
            if not year.isdigit(): continue
            if int(year) < start_year: continue
            
            # Indices: 0:연도, 2:AVG, 3:G, 7:H, 10:HR, 12:RBI, 19:SLG, 20:OBP
            stats = {
                "연도": year,
                "AVG": cols[2].text.strip(),
                "G": cols[3].text.strip(),
                "H": cols[7].text.strip(),
                "HR": cols[10].text.strip(),
                "RBI": cols[12].text.strip(),
                "SLG": cols[19].text.strip(),
                "OBP": cols[20].text.strip()
            }
            stats_list.append(stats)
            print(f"    Collected data for {year}")
    except Exception as e:
        print(f"  Error scraping {name}: {e}")
        
    return {
        "name": name,
        "team": team,
        "stats": stats_list
    }

def main():
    if not os.path.exists("data"):
        os.makedirs("data")
        
    driver = get_driver()
    
    pitchers_to_scrape = [
        {"id": "68341", "name": "안우진", "team": "키움"},
        {"id": "69446", "name": "원태인", "team": "삼성"},
        {"id": "64021", "name": "박세웅", "team": "롯데"},
        {"id": "65933", "name": "구창모", "team": "NC"},
        {"id": "51648", "name": "이의리", "team": "KIA"},
        {"id": "52701", "name": "문동주", "team": "한화"},
        {"id": "64001", "name": "고영표", "team": "KT"},
        {"id": "68220", "name": "곽빈", "team": "두산"},
        {"id": "61101", "name": "임찬규", "team": "LG"}
    ]
    
    hitters_to_scrape = [
        {"id": "53312", "name": "김건희", "team": "키움"}
    ]
    
    data = {
        "pitchers": [],
        "hitters": [],
        "updated_at": datetime.now().isoformat()
    }
    
    for p in pitchers_to_scrape:
        data["pitchers"].append(scrape_pitcher(driver, p["id"], p["name"], p["team"]))
        
    for h in hitters_to_scrape:
        data["hitters"].append(scrape_hitter(driver, h["id"], h["name"], h["team"]))
        
    driver.quit()
    
    data["pitchers"].sort(key=lambda x: x['name'])
    
    with open("data/players_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("\nScraping complete.")

if __name__ == "__main__":
    main()
