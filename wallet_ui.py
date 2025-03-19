import streamlit as st
from script import add_purchase, load_wallet

st.title("📈 Crypto Wallet Manager")

coin = st.text_input("Enter Coin (e.g., bitcoin)")
amount = st.number_input("Enter Amount", min_value=0.0, format="%.6f")
buy_price = st.number_input("Enter Buy Price (USD)", min_value=0.0, format="%.2f")

if st.button("Add Purchase"):
    if coin and amount > 0 and buy_price > 0:
        add_purchase(coin.lower(), amount, buy_price)
        st.success(f"✅ Added {amount} {coin.upper()} at ${buy_price}!")
    else:
        st.error("⚠️ Please enter valid values!")

st.subheader("📜 Current Wallet")
wallet = load_wallet()
st.json(wallet)
