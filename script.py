import requests
import json
import time
import base64
import smtplib
from email.mime.text import MIMEText

WALLET_DATA = "wallet_data.json"

# Email notification settings......
EMAIL = "khanzain00081@gmail.com"
with open("credentials.txt", "r") as file:
    PASSWORD = base64.b64decode(file.read().strip()).decode()

TO_EMAIL = "injeelashahid@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


#load wallet data from json file.....
def load_wallet():
    try:
        with open(WALLET_DATA, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
#save wallet data to json file.....
def save_wallet(data):
    with open(WALLET_DATA, "w") as file:
        json.dump(data, file, indent=4)

#Add new purchase to the wallet.....
def add_purchase(coin, amount, buy_price):
    wallet = load_wallet()
    if coin in wallet:
        wallet[coin]["amount"] += amount
        wallet[coin]["buy_price"] = (wallet[coin]["buy_price"] + buy_price) / 2  # Averaging buy price

    else:
        wallet[coin] = {
            "amount": amount,
            "buy_price": buy_price
        }

    save_wallet(wallet)
    print(f"Added {amount} {coin.upper()} at ${buy_price} to wallet.")

#Fetching crypto prices from Coingecko API....
def get_price(coin):
    wallet = load_wallet()
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(wallet.keys()), "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else {}

def send_email(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

    # Check wallet and determine the best crypto to sell
def check_wallet():
    wallet = load_wallet()
    prices = get_price()
    
    if not prices:
        print("Failed to fetch prices.")
        return
    
    best_crypto = None
    max_profit = 0
    
    for coin, data in wallet.items():
        if coin in prices:
            current_price = prices[coin]['usd']
            profit = (current_price - data['buy_price']) * data['amount']
            
            if profit > max_profit:
                max_profit = profit
                best_crypto = coin
    
    if best_crypto:
        subject = f"Sell Alert: {best_crypto.upper()} for Max Profit!"
        message = f"Sell {best_crypto.upper()} now! Current price: ${prices[best_crypto]['usd']}, Profit: ${max_profit}"
        send_email(subject, message)
    else:
        print("No profitable trades found.")


# Main function to run the script.....
if __name__ == "__main__":
    while True:
        check_wallet()
        time.sleep(60 * 60)  # Check every hour