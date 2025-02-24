import os
import sqlite3
import requests
from dotenv import load_dotenv

# config.py
load_dotenv()
VT_API_KEY = os.getenv("VT_API_KEY")
DB_FILE = "ip_reputation.db"

if not VT_API_KEY:
    raise ValueError("VT_API_KEY is missing. Please set it in a .env file or environment variable.")

# database.py
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ip_reputation (
                      ip TEXT PRIMARY KEY,
                      ip_type TEXT,
                      reputation_score INTEGER)''')
    conn.commit()
    conn.close()

def save_ip_reputation(ip, ip_type, reputation_score):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO ip_reputation (ip, ip_type, reputation_score) VALUES (?, ?, ?)",
                   (ip, ip_type, reputation_score))
    conn.commit()
    conn.close()

# virustotal_api.py
def check_ip_reputation(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": VT_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        reputation_score = data.get("data", {}).get("attributes", {}).get("reputation", 0)
        ip_type = data.get("data", {}).get("type", "unknown")
        return ip_type, reputation_score
    else:
        return "unknown", -1

# main.py
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <IP_ADDRESS>")
        sys.exit(1)
    ip = sys.argv[1]
    init_db()
    ip_type, score = check_ip_reputation(ip)
    save_ip_reputation(ip, ip_type, score)
    print(f"IP: {ip}, Type: {ip_type}, Reputation Score: {score}")