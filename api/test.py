import yfinance as yf

msft = yf.Ticker("MSFT")
"""
returns
<yfinance.Ticker object at 0x1a1715e898>
"""

# get stock info
print(msft.info["currentPrice"])
