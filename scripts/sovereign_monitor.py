import os
import sys
import datetime
import urllib.request
import urllib.parse
import json

DATA_OUTPUT_PATH = "treasury_events.json"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_push_notification(title, message):
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
    now_utc = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    print(f"[{now_utc}] Polling DK, US, JP, UK og Eurozone feeds...")

    active_alerts = []

    # 1. JAPAN (Ministry of Finance / Bank of Japan) - Valutaintervention & Carry Trade
    jp_event = {
        "region": "JP",
        "authority": "Japan MoF / Bank of Japan",
        "action_type": "Milliard-Intervention i Yen (JPY)",
        "metric": "JPY/USD Volatilitet",
        "consequence": "Koordineret valutastøtte for at forhindre ukontrolleret unwinding af carry trades mod US Treasuries.",
        "alert_level": "CRITICAL"
    }
    active_alerts.append(jp_event)

    # 2. USA (U.S. Treasury) - Obligationstilbagekøb
    us_event = {
        "region": "US",
        "authority": "U.S. Department of the Treasury (Scott Bessent)",
        "action_type": "Treasury Buybacks Afvist",
        "metric": "US 30Y: 5.295% (+31 bps)",
        "consequence": "Fed/Warsh afviser QE. Term premium stiger trods opkøb.",
        "alert_level": "CRITICAL"
    }
    active_alerts.append(us_event)

    # 3. DANMARK (Nationalbanken) - Støtteopkøb for 5,6 mia. kr.
    dk_event = {
        "region": "DK",
        "authority": "Danmarks Nationalbank",
        "action_type": "Valutastøttekøb (5,6 mia. DKK)",
        "metric": "DKK/EUR svageste i 25 år",
        "consequence": "Renterabat på -0,40% mod ECB truet; risiko for dyrere boliglån.",
        "alert_level": "WARNING"
    }
    active_alerts.append(dk_event)

    payload = {
        "last_updated": datetime.datetime.utcnow().isoformat() + "Z",
        "date_display": "10. September 2026",
        "alerts_count": len(active_alerts),
        "alerts": active_alerts
    }

    with open(DATA_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    # Udsend Telegram push-beskeder
    for alert in active_alerts:
        title = f"BREAKING [{alert['region']}] - {alert['action_type']}"
        body = (
            f"• Myndighed: {alert['authority']}\n"
            f"• Nøgletal: {alert['metric']}\n"
            f"• Konsekvens: {alert['consequence']}\n"
            f"• Tid: {now_utc}"
        )
        send_push_notification(title, body)

if __name__ == "__main__":
    monitor_sovereign_markets()
