# 📈 Dynamic Stock SIP Automation Using Zerodha API + Python Script + Google Sheets

This project is a fully automated **Direct Stock SIP System** built using Python, Zerodha's Kite Connect API, Google Sheets, and GitHub Actions. It dynamically adjusts stock purchases every week based on price changes — helping investors consistently buy into stocks without trying to time the market.

---

## 🧠 Why I Built This

As someone actively investing in Indian stock markets, I noticed something important:

> During a recent market correction, many quality stocks fell significantly. But trying to time the bottom felt risky. And while SIP (Systematic Investment Plan) helps avoid such timing traps, it's usually used for **mutual funds** — not **direct stocks**.

Zerodha (my broker) does offer SIP for stocks — but **only monthly**. That didn’t suit my idea.

Direct stocks behave differently — they're **more volatile** and can change sharply within a week. So, I thought:

- Why not invest **weekly** instead?
- If the price drops by more than 3% compared to last week, **increase the quantity** bought.
- Cap the total investment per stock to manage risk.
- But doing this **manually each week** is tedious and subject to emotional bias.

---

## 💡 The Solution

I automated the entire logic with:

### 🔗 Zerodha Kite Connect API
- For placing **real trades** into my Zerodha demat account.
- However, the free plan doesn’t allow historical price data.

### 📊 Google Sheets + `GOOGLEFINANCE`
- I used Google Sheets to fetch stock prices using `=GOOGLEFINANCE("NSE:ABCAPITAL", "price", ...)`.
- This gave me accurate weekly data points.

### ⚙️ Python Scripts
- Used `gspread` to connect Python to Google Sheets.
- My script:
  - Checks latest and last week’s price.
  - Calculates % change.
  - Decides quantity to buy based on rules.
  - Places the order using Zerodha’s API.

### ⏰ GitHub Actions
- Automated everything to run weekly.
- No manual intervention required!

---

## 🔍 SIP Strategy Logic

| Rule                            | Action                     |
|---------------------------------|----------------------------|
| Run frequency                   | Every 7 days               |
| Base quantity                   | Buy 1 share                |
| If price falls > 3% since last week | Buy 2 shares instead        |
| Max investment per stock        | ₹12,000                    |
| Market order                    | Yes                        |

---

## 🛠 Tech Stack

- **Python** – Core logic and API interactions
- **Zerodha Kite Connect API** – Order placement
- **Google Sheets + Google Finance** – Price data source
- **gspread + Google Service Account** – Python–Sheets integration
- **GitHub Actions** – Automation & scheduling

---

## 🗂 Folder Structure
dynamic-stock-sip/
- ├── main.py # SIP logic and API integration
├── sheets_service.py # Google Sheets read/write functions
├── kite_api.py # Zerodha order placement helper
├── credentials.json # Google Sheets service account (private)
├── .github/workflows/ # GitHub Actions for automation
└── README.md # This file

## 🔐 Security

- Kept `credentials.json` (Google Service Account) private.
- Didn’t expose Zerodha `api_key`, `api_secret`, or access token.
- Use GitHub Secrets to store sensitive values securely.
- Added `.gitignore` to prevent accidental uploads of sensitive files.

---

## ✅ Benefits

- 📉 Buy more when prices fall
- ⏱ No manual work — fully scheduled and automated
- 🔄 Smarter cost averaging than fixed SIPs
- 🎯 Focused on direct stocks — not mutual funds
- 🧠 Bias-free investing — your emotions don’t interfere

## 👨‍💻 Author

**Yash Kamath**  
4th Year AI & Data Science | CFA Level 1 Candidate  
📧 yashkamath.yk@gmail.com  
🌐 [GitHub Portfolio](https://github.com/itsyashk1406/yashkamath/data-portfolio)  
🔗 [LinkedIn](https://www.linkedin.com/in/yash-kamath1406)

---

## 📜 License

This project is for educational use only. Always test thoroughly before placing real trades.
