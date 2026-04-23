# Cash App Integration Guide

This guide demonstrates how to use the Cash App integration features in yfinance.

## Overview

The Cash App integration module provides utilities for Cash App users to:
- Manage portfolios
- Format data for Cash App workflows
- Calculate dollar-cost averaging strategies
- Get investment recommendations
- Export portfolio data

## Quick Start

### Import the Module

```python
import yfinance as yf
from yfinance.cashapp import (
    CashAppPortfolio,
    format_for_cashapp,
    get_cashapp_watchlist,
    calculate_dollar_cost_average,
    get_cashapp_recommendations
)
```

## Portfolio Management

### Creating a Portfolio

```python
# Create an empty portfolio
portfolio = CashAppPortfolio()

# Or initialize with holdings
holdings = {'AAPL': 10, 'MSFT': 5, 'GOOGL': 2}
portfolio = CashAppPortfolio(holdings)
```

### Adding Positions

```python
portfolio = CashAppPortfolio()
portfolio.add_position('AAPL', 10)
portfolio.add_position('MSFT', 5)
portfolio.add_position('TSLA', 3)
```

### Getting Portfolio Value

```python
# Get detailed portfolio information
portfolio_data = portfolio.get_portfolio_value()
print(f"Total Value: ${portfolio_data['total_value']:.2f}")

# View individual positions
for ticker, info in portfolio_data['positions'].items():
    print(f"{ticker}: {info['shares']} shares @ ${info['price']:.2f} = ${info['value']:.2f}")
```

### Portfolio Summary DataFrame

```python
# Get a pandas DataFrame summary
df = portfolio.get_portfolio_summary()
print(df)
```

### Export Portfolio

```python
# Export to CSV
portfolio.export_to_csv('my_portfolio.csv')

# Export to JSON
portfolio.export_to_json('my_portfolio.json')
```

### Performance Analysis

```python
# Get performance metrics for different periods
performance_1d = portfolio.get_performance('1d')
performance_1mo = portfolio.get_performance('1mo')
performance_1y = portfolio.get_performance('1y')

for ticker, perf in performance_1mo.items():
    if 'error' not in perf:
        print(f"{ticker}: {perf['change_pct']:.2f}% change")
```

## Data Formatting

### Format Quote Data

```python
# Get Cash App-friendly quote format
quote = format_for_cashapp('AAPL', 'quote')
print(f"{quote['name']}: ${quote['price']:.2f} ({quote['change_percent']:.2f}%)")
```

### Format Historical Data

```python
# Get historical price data
history = format_for_cashapp('AAPL', 'history')
print(f"Price history: {len(history['prices'])} data points")
```

### Format Company Info

```python
# Get company information
info = format_for_cashapp('AAPL', 'info')
print(f"Sector: {info['sector']}")
print(f"Industry: {info['industry']}")
```

## Watchlist Management

### Create a Watchlist

```python
# Create a watchlist from multiple tickers
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
watchlist = get_cashapp_watchlist(tickers)

# Display the watchlist
print(watchlist[['symbol', 'name', 'price', 'change_percent']])
```

## Dollar-Cost Averaging (DCA)

### Calculate DCA Strategy

```python
# Calculate DCA results for investing $100 monthly
dca_results = calculate_dollar_cost_average(
    ticker='AAPL',
    amount=100,
    frequency='monthly',
    start_date='2023-01-01',
    end_date='2024-01-01'
)

print(f"Total Invested: ${dca_results['total_invested']:.2f}")
print(f"Total Shares: {dca_results['total_shares']:.2f}")
print(f"Average Cost Basis: ${dca_results['average_cost_basis']:.2f}")
print(f"Current Value: ${dca_results['current_value']:.2f}")
print(f"Total Return: {dca_results['total_return_pct']:.2f}%")
```

### Different Frequencies

```python
# Daily DCA
dca_daily = calculate_dollar_cost_average('AAPL', 10, 'daily')

# Weekly DCA
dca_weekly = calculate_dollar_cost_average('AAPL', 50, 'weekly')

# Monthly DCA (default)
dca_monthly = calculate_dollar_cost_average('AAPL', 200, 'monthly')
```

## Investment Recommendations

### Get Recommendations

```python
# Get investment recommendations
recommendations = get_cashapp_recommendations('AAPL')

print(f"Current Price: ${recommendations['current_price']:.2f}")
print(f"Target Price: ${recommendations['target_price']:.2f}")
print(f"Upside Potential: {recommendations['upside_potential_pct']:.2f}%")
print(f"Recommendation: {recommendations['recommendation']}")
```

## Complete Example

```python
import yfinance as yf
from yfinance.cashapp import CashAppPortfolio, format_for_cashapp, get_cashapp_watchlist

# Create and manage a portfolio
portfolio = CashAppPortfolio({
    'AAPL': 10,
    'MSFT': 5,
    'GOOGL': 2
})

# Add more positions
portfolio.add_position('TSLA', 3)

# Get portfolio summary
summary = portfolio.get_portfolio_summary()
print("Portfolio Summary:")
print(summary)

# Get portfolio value
value = portfolio.get_portfolio_value()
print(f"\nTotal Portfolio Value: ${value['total_value']:.2f}")

# Export portfolio
portfolio.export_to_csv('cashapp_portfolio.csv')

# Create a watchlist
watchlist = get_cashapp_watchlist(['AAPL', 'MSFT', 'GOOGL', 'AMZN'])
print("\nWatchlist:")
print(watchlist[['symbol', 'price', 'change_percent']])
```

## Notes

- Cash App integration uses yfinance data sources (Yahoo Finance)
- All prices and data are fetched in real-time
- Portfolio calculations are based on current market prices
- Export formats are compatible with common spreadsheet applications
- Dollar-cost averaging calculations use historical price data

## Limitations

- Cash App doesn't provide a public API for trading, so this integration focuses on data analysis and portfolio management
- All data is sourced from Yahoo Finance via yfinance
- Portfolio tracking is local and not synced with Cash App accounts
