# Tao Income Tracker 📊

**⚠️ IMPORTANT DISCLAIMER: This tool is for educational purposes only. The amounts displayed may not be accurate for tax or financial reporting. Always consult with a qualified tax professional for accurate income tracking and tax preparation. ⚠️**

## What is This Tool? 🤔

This is a **personal income tracking tool** for people who participate in the Bittensor network. Think of it like a "profit calculator" for your Bittensor investments, but much more detailed.

### What is Bittensor? 🧠
Bittensor is a decentralized network where computers work together to provide AI services. When you participate, you can earn rewards in cryptocurrency (TAO tokens) by:
- **Staking TAO tokens** on different subnets (like Subnet 0)
- **Staking other tokens** on various subnets (like Subnet 1, 2, etc.)

### What Does This Tool Do? 📈
This tool helps you track:
- **How much money you've earned** from staking rewards
- **Your portfolio balance changes** over time
- **Hourly and daily income** from different subnets
- **Historical performance** of your investments

## Why is This Important? 💡

### For Tax Purposes 📋
- **Income Tracking**: You need to report staking rewards as income on your taxes
- **Cost Basis**: Track how much you paid vs. how much you earned
- **Tax Season**: Have organized data when filing your taxes

### For Investment Decisions 📊
- **Performance Analysis**: See which subnets are earning you the most
- **Portfolio Balance**: Understand your total investment value
- **Trend Analysis**: Track how your earnings change over time

## Getting Started 🚀

### Option 1: Use the Live Version (Recommended) 🌐
**The application is hosted live on GitHub Pages!**
- **Visit**: [https://EZTrades-dev.github.io/tao-income-tracker](https://EZTrades-dev.github.io/tao-income-tracker)
- **No installation required** - just open the link in your browser
- **Works immediately** - enter your API key and cold key to start tracking

### Option 2: Run Locally (For Full Functionality) 💻

#### Step 1: Install Python (if you don't have it)
1. Go to [python.org](https://python.org)
2. Download the latest version for your computer
3. Install it (follow the installation wizard)

#### Step 2: Download This Tool
1. Click the green "Code" button on this page
2. Select "Download ZIP"
3. Extract the ZIP file to a folder on your computer

### Step 3: Open Terminal/Command Prompt
**On Windows:**
- Press `Windows + R`
- Type `cmd` and press Enter

**On Mac:**
- Press `Command + Space`
- Type `Terminal` and press Enter

**On Linux:**
- Press `Ctrl + Alt + T`

### Step 4: Navigate to the Tool Folder
In the terminal, type:
```bash
cd path/to/your/downloaded/folder
```
(Replace with the actual path where you extracted the files)

### Step 5: Install Required Software
Type this command and press Enter:
```bash
pip install -r requirements.txt
```

### Step 6: Get Your API Key 🔑
1. Go to [tao.app](https://tao.app)
2. Create an account or log in
3. Look for "API" or "Developer" section
4. Generate a new API key
5. **Save this key safely** - you'll need it!

### Step 7: Find Your Cold Key Address 🔐
**What is a Cold Key?**
- Think of it like your "bank account number" for Bittensor
- It's the address where your TAO tokens are stored
- You can find it in your Bittensor wallet or on tao.app

**How to Find It:**
1. Log into [tao.app](https://tao.app)
2. Look for your wallet address or "cold key"
3. It will look something like: `5DwXfDQnBNAWGGLss52bPTM9WZKX7b1FYDjQ96kYeP5mY2Vu`

### Step 8: Start the Tool
Type this command and press Enter:
```bash
python start_servers.py
```

### Step 9: Open the Web Page
1. Open your web browser
2. Go to: `http://localhost:8080`
3. You should see the Tao Income Tracker page

## GitHub Pages Hosting 🌐

This application is configured for free hosting on GitHub Pages. To deploy your own version:

1. **Fork this repository** or create your own
2. **Follow the deployment guide**: See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
3. **Your site will be live** at: `https://EZTrades-dev.github.io/tao-income-tracker`

### Benefits of GitHub Pages Hosting:
- ✅ **Free hosting** - no server costs
- ✅ **Automatic updates** - push changes to GitHub
- ✅ **Custom domain support** - use your own domain
- ✅ **SSL certificate** - secure HTTPS connection
- ✅ **Global CDN** - fast loading worldwide

## How to Use the Tool 📝

### Step 1: Enter Your Information
1. **API Key**: Paste your tao.app API key
2. **Cold Key**: Paste your wallet address
3. **Time Period**: Choose how much historical data you want (1 day, 2 days, or 7 days)

### Step 2: Calculate Your Rewards
1. Click the "📈 Calculate Staking Rewards" button
2. Wait for the data to load (this may take a few seconds)
3. Review the results

### Step 3: Understand Your Results

#### Summary Cards 📊
- **💰 Total Staking Rewards**: Total money earned from staking
- **📈 Balance Change**: How your total portfolio value changed
- **💰 Past Hour Rewards**: Money earned in the last hour
- **📊 Past Period Rewards**: Money earned in your selected time period
- **📅 Period Analyzed**: The time range of your data

#### Balance History Table 📋
This table shows detailed information for each hour:

| Column | What It Means |
|--------|---------------|
| **Timestamp** | When this data was recorded |
| **Subnet** | Which Bittensor subnet (0 = TAO, others = different tokens) |
| **Token Amount** | How many tokens you have |
| **Token Price (USD)** | Current price of the token in US dollars |
| **Balance Value (USD)** | Total value of your tokens in US dollars |
| **Rewards Earned (Tokens)** | New tokens earned in this hour |
| **Rewards Value (USD)** | Dollar value of tokens earned this hour |

### Step 4: Export Your Data
- Click the "📊 Export to CSV" button to download your data
- This creates a spreadsheet file you can open in Excel or Google Sheets
- Useful for tax preparation or further analysis

## Understanding the Data 📊

### What Are Subnets? 🏗️
Think of subnets like different "investment funds" in Bittensor:
- **Subnet 0**: The main TAO token (like Bitcoin for Bittensor)
- **Subnet 1, 2, 3, etc.**: Different specialized tokens with their own prices

### How Rewards Work 💰
1. **You stake tokens** on a subnet
2. **The network pays you** in the same type of tokens
3. **You earn more tokens** over time
4. **This tool calculates** the dollar value of those earned tokens

### Why Prices Matter 💵
- Token prices change constantly
- $1 worth of tokens yesterday might be worth $1.10 today
- This tool uses historical prices to calculate accurate dollar values

## Troubleshooting 🔧

### Common Problems and Solutions

**"Address already in use" Error:**
- The tool is already running
- Close any existing terminal windows
- Try running `python stop_servers.py` first

**"Failed to fetch" Error:**
- Check your internet connection
- Verify your API key is correct
- Make sure you're using the right cold key address

**"No data displayed":**
- Your cold key might not have any staking activity
- Try a different time period
- Check if your API key has the right permissions

**"Port 8000/8080 already in use":**
- Another program is using these ports
- Restart your computer
- Or use different ports (advanced users only)

### Getting Help 🆘
If you're stuck:
1. Check the error messages carefully
2. Make sure you followed all the setup steps
3. Verify your API key and cold key are correct
4. Try restarting the tool

## File Structure 📁

```
dynamic_tao_income_tracking/
├── main.py                    # The main program (backend)
├── index.html                 # The web page (frontend)
├── requirements.txt           # Required software packages
├── start_servers.py          # Easy startup script
├── stop_servers.py           # Easy shutdown script
└── README.md                 # This file
```

## Technical Details (For Advanced Users) ⚙️

### Backend (main.py)
- **FastAPI server** running on port 8000
- **Handles API calls** to tao.app
- **Processes data** and performs calculations
- **Rate limiting** to respect API limits

### Frontend (index.html)
- **Web interface** running on port 8080
- **User-friendly design** with Excel-like appearance
- **Real-time data** display and calculations
- **CSV export** functionality

### API Integration
- **tao.app API** for balance and price data
- **Historical price correlation** for accurate USD calculations
- **Rate limiting** (10 calls per minute on free tier)

## Security & Privacy 🔒

### What Data is Stored?
- **Nothing is stored** on your computer permanently
- **API calls** are made in real-time
- **No personal data** is saved

### API Key Safety
- **Keep your API key private**
- **Don't share it** with anyone
- **Treat it like a password**

### Cold Key Privacy
- **Your cold key is public** (like a bank account number)
- **It's safe to use** in this tool
- **No private keys** are ever requested

## Legal & Tax Information ⚖️

### Important Disclaimers
- **This tool is for educational purposes only**
- **Not financial advice**
- **Not tax advice**
- **Always consult professionals** for tax and financial decisions

### Tax Considerations
- **Staking rewards are typically taxable income**
- **Report all earnings** to your tax authority
- **Keep detailed records** of all transactions
- **Consult a tax professional** for your specific situation

## Support & Updates 🔄

### Getting Updates
- Check this GitHub page for updates
- Download new versions when available
- Follow the same setup process

### Contributing
- This is open-source software
- Feel free to suggest improvements
- Report bugs or issues

---

**Remember: This tool helps you track your Bittensor income, but always verify the data and consult professionals for important financial decisions! 📊💰**
