import pandas as pd
import pandas_ta as ta
import yfinance as yf
import matplotlib.pyplot as plt

# df = pd.DataFrame()
# df = df.ta.ticker("AAPL", period="5y")
df = yf.download("AAPL", period="1y")
print(list(df.ta.categories))

df['rsi'] = ta.rsi(close=df.Close, length=10)
df['ema'] = ta.ema(close=df.Close, length=10)
print(df)

plt.plot(df['rsi'])
plt.plot(df['ema'])
plt.plot(df['Close'])

