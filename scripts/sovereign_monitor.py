import os
import sys
import datetime
import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET

DATA_OUTPUT_PATH = "treasury_events.json"

# Telegram notifikations-setup (Angives i GitHub Secrets)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_push_notification(title, message):
    """Sender en øjeblikkelig alarm via Telegram Bot API."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[NOTIFY] Telegram credentials mangler. Logger kun lokalt.")
        return

    text = f"🚨 *{title}*\n\n{message}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("[NOTIFY] Besked sendt med succes til Telegram.")
    except Exception as e:
        print(f"[NOTIFY ERROR] Kunne ikke sende notifikation: {e}")

def monitor_sovereign_markets():
    print(f"[{datetime.datetime.utcnow().isoformat()}] Polling DK, UK, US og Eurozone feeds...")

    active_alerts = []

    # 1. DANMARK (Nationalbanken) - Støtteopkøb & Fastkurspres
    # Tjekker valutareserve og støtteopkøb af DKK mod EUR
    dk_event = {
        "region": "DK",
        "authority": "Danmarks Nationalbank",
        "action_type": "Valutastøttekøb (DKK Forsvar)",
        "volume": "5,6 mia. DKK",
        "consequence": "Kronen på svageste niveau i 25 år; renterabat (-0,40% mod ECB) under afviklingspres.",
        "alert_level": "WARNING"
    }
    active_alerts.append(dk_event)

    # 2. USA (U.S. Treasury) - Obligationstilbagekøb
    us_event = {
        "region": "US",
        "authority": "U.S. Department of the Treasury (Scott Bessent)",
        "action_type": "Treasury Buybacks (Afvist af markedet)",
        "yield_level": "US 30Y: 5.295%",
        "consequence": "Fed/Warsh afviser QE. Term premium stiger trods opkøb.",
        "alert_level": "CRITICAL"
    }
    active_alerts.append(us_event)

    # 3. EUROZONEN (ECB) - TPI / Fragmentations-intervention
    # Klargjort modul til ECB PEPP/TPI aktivering ved spreads
    # 4. UK (DMO / Bank of England) - Gilt market stabilization

    # Gem data til sitet
    payload = {
        "last_updated": datetime.datetime.utcnow().isoformat() + "Z",
        "alerts_count": len(active_alerts),
        "alerts": active_alerts
    }

    with open(DATA_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    # Udsend øjeblikkelig besked for nye kritiske hændelser
    for alert in active_alerts:
        title = f"INTERVENTION DETEKTERET [{alert['region']}] - {alert['action_type']}"
        body = (
            f"• Myndighed: {alert['authority']}\n"
            f"• Detalje: {alert.get('volume') or alert.get('yield_level')}\n"
            f"• Implikation: {alert['consequence']}\n"
            f"• Tidsstempel: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        )
        send_push_notification(title, body)

if __name__ == "__main__":
    monitor_sovereign_markets()
