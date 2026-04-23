#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# yfinance - Cash App integration
# https://github.com/ranaroussi/yfinance
#
# Copyright 2017-2019 Ran Aroussi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Cash App Integration Module

This module provides utilities for Cash App users to work with yfinance data,
including portfolio management, data formatting, and export functionality.
"""

from __future__ import print_function

import pandas as _pd
import json as _json
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta

from .ticker import Ticker
from .tickers import Tickers


class CashAppPortfolio:
    """
    A portfolio manager for Cash App users that integrates with yfinance.
    
    This class helps manage and analyze portfolios in a format compatible
    with Cash App's investing features.
    """
    
    def __init__(self, holdings: Optional[Dict[str, Union[int, float]]] = None):
        """
        Initialize a Cash App portfolio.
        
        Args:
            holdings: Dictionary mapping ticker symbols to number of shares.
                     Example: {'AAPL': 10, 'MSFT': 5, 'GOOGL': 2}
        """
        self.holdings = holdings or {}
        self._tickers = None
        self._last_update = None
    
    def add_position(self, ticker: str, shares: Union[int, float]):
        """
        Add or update a position in the portfolio.
        
        Args:
            ticker: Stock ticker symbol
            shares: Number of shares
        """
        ticker = ticker.upper()
        if ticker in self.holdings:
            self.holdings[ticker] += shares
        else:
            self.holdings[ticker] = shares
    
    def remove_position(self, ticker: str):
        """
        Remove a position from the portfolio.
        
        Args:
            ticker: Stock ticker symbol to remove
        """
        ticker = ticker.upper()
        if ticker in self.holdings:
            del self.holdings[ticker]
    
    def update_prices(self):
        """
        Update current prices for all holdings.
        
        Returns:
            Dictionary mapping tickers to current prices
        """
        if not self.holdings:
            return {}
        
        tickers = Tickers(list(self.holdings.keys()))
        self._tickers = tickers
        self._last_update = datetime.now()
        
        prices = {}
        for ticker in self.holdings.keys():
            try:
                ticker_obj = Ticker(ticker)
                info = ticker_obj.fast_info
                prices[ticker] = info.get('lastPrice', 0)
            except Exception:
                prices[ticker] = 0
        
        return prices
    
    def get_portfolio_value(self) -> Dict[str, Union[float, Dict]]:
        """
        Calculate total portfolio value and individual position values.
        
        Returns:
            Dictionary with portfolio summary and position details
        """
        prices = self.update_prices()
        
        positions = {}
        total_value = 0.0
        
        for ticker, shares in self.holdings.items():
            price = prices.get(ticker, 0)
            value = shares * price
            total_value += value
            
            positions[ticker] = {
                'shares': shares,
                'price': price,
                'value': value,
                'weight': 0.0  # Will be calculated after total_value
            }
        
        # Calculate weights
        if total_value > 0:
            for ticker in positions:
                positions[ticker]['weight'] = (positions[ticker]['value'] / total_value) * 100
        
        return {
            'total_value': total_value,
            'positions': positions,
            'last_updated': self._last_update.isoformat() if self._last_update else None
        }
    
    def get_portfolio_summary(self) -> _pd.DataFrame:
        """
        Get a pandas DataFrame summary of the portfolio.
        
        Returns:
            DataFrame with ticker, shares, price, value, and weight columns
        """
        portfolio_data = self.get_portfolio_value()
        positions = portfolio_data['positions']
        
        if not positions:
            return _pd.DataFrame()
        
        data = []
        for ticker, info in positions.items():
            data.append({
                'Ticker': ticker,
                'Shares': info['shares'],
                'Price': info['price'],
                'Value': info['value'],
                'Weight %': info['weight']
            })
        
        df = _pd.DataFrame(data)
        df = df.sort_values('Value', ascending=False)
        return df
    
    def export_to_csv(self, filename: str):
        """
        Export portfolio to CSV file.
        
        Args:
            filename: Output CSV filename
        """
        df = self.get_portfolio_summary()
        df.to_csv(filename, index=False)
    
    def export_to_json(self, filename: str):
        """
        Export portfolio to JSON file.
        
        Args:
            filename: Output JSON filename
        """
        portfolio_data = self.get_portfolio_value()
        with open(filename, 'w') as f:
            _json.dump(portfolio_data, f, indent=2)
    
    def get_performance(self, period: str = '1d') -> Dict[str, Dict]:
        """
        Get performance metrics for portfolio holdings.
        
        Args:
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', 'ytd', 'max')
        
        Returns:
            Dictionary with performance data for each holding
        """
        performance = {}
        
        for ticker in self.holdings.keys():
            try:
                ticker_obj = Ticker(ticker)
                hist = ticker_obj.history(period=period)
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    start_price = hist['Close'].iloc[0]
                    change = current_price - start_price
                    change_pct = (change / start_price) * 100 if start_price > 0 else 0
                    
                    performance[ticker] = {
                        'start_price': start_price,
                        'current_price': current_price,
                        'change': change,
                        'change_pct': change_pct,
                        'shares': self.holdings[ticker],
                        'position_change': change * self.holdings[ticker],
                        'position_change_pct': change_pct
                    }
            except Exception as e:
                performance[ticker] = {'error': str(e)}
        
        return performance


def format_for_cashapp(ticker: str, data_type: str = 'quote') -> Dict:
    """
    Format yfinance data in a Cash App-friendly format.
    
    Args:
        ticker: Stock ticker symbol
        data_type: Type of data to format ('quote', 'history', 'info')
    
    Returns:
        Dictionary with formatted data
    """
    ticker_obj = Ticker(ticker)
    
    if data_type == 'quote':
        info = ticker_obj.fast_info
        quote_data = ticker_obj.info
        
        return {
            'symbol': ticker.upper(),
            'name': quote_data.get('longName', ticker.upper()),
            'price': info.get('lastPrice', 0),
            'change': info.get('regularMarketChange', 0),
            'change_percent': info.get('regularMarketChangePercent', 0),
            'volume': info.get('regularMarketVolume', 0),
            'market_cap': quote_data.get('marketCap', 0),
            'currency': quote_data.get('currency', 'USD')
        }
    
    elif data_type == 'history':
        hist = ticker_obj.history(period='1mo')
        if hist.empty:
            return {}
        
        return {
            'symbol': ticker.upper(),
            'dates': [d.isoformat() for d in hist.index],
            'prices': hist['Close'].tolist(),
            'volumes': hist['Volume'].tolist()
        }
    
    elif data_type == 'info':
        info = ticker_obj.info
        return {
            'symbol': ticker.upper(),
            'name': info.get('longName', ticker.upper()),
            'sector': info.get('sector', ''),
            'industry': info.get('industry', ''),
            'description': info.get('longBusinessSummary', ''),
            'website': info.get('website', ''),
            'employees': info.get('fullTimeEmployees', 0)
        }
    
    else:
        raise ValueError(f"Unknown data_type: {data_type}. Use 'quote', 'history', or 'info'")


def get_cashapp_watchlist(tickers: List[str]) -> _pd.DataFrame:
    """
    Create a watchlist DataFrame formatted for Cash App users.
    
    Args:
        tickers: List of ticker symbols
    
    Returns:
        DataFrame with watchlist data
    """
    data = []
    
    for ticker in tickers:
        try:
            formatted = format_for_cashapp(ticker, 'quote')
            data.append(formatted)
        except Exception as e:
            data.append({
                'symbol': ticker.upper(),
                'name': ticker.upper(),
                'price': 0,
                'change': 0,
                'change_percent': 0,
                'volume': 0,
                'market_cap': 0,
                'currency': 'USD',
                'error': str(e)
            })
    
    df = _pd.DataFrame(data)
    return df


def calculate_dollar_cost_average(ticker: str, 
                                   amount: float, 
                                   frequency: str = 'monthly',
                                   start_date: Optional[str] = None,
                                   end_date: Optional[str] = None) -> Dict:
    """
    Calculate dollar-cost averaging (DCA) strategy results for Cash App users.
    
    Args:
        ticker: Stock ticker symbol
        amount: Dollar amount to invest per period
        frequency: Investment frequency ('daily', 'weekly', 'monthly')
        start_date: Start date (YYYY-MM-DD format)
        end_date: End date (YYYY-MM-DD format)
    
    Returns:
        Dictionary with DCA results
    """
    ticker_obj = Ticker(ticker)
    
    # Determine period based on dates
    if start_date and end_date:
        hist = ticker_obj.history(start=start_date, end=end_date)
    else:
        # Default to 1 year if no dates provided
        hist = ticker_obj.history(period='1y')
    
    if hist.empty:
        return {'error': 'No historical data available'}
    
    # Map frequency to pandas resample frequency
    freq_map = {
        'daily': 'D',
        'weekly': 'W',
        'monthly': 'M'
    }
    
    resample_freq = freq_map.get(frequency.lower(), 'M')
    
    # Resample to get period-end prices
    resampled = hist['Close'].resample(resample_freq).last()
    
    total_invested = 0
    total_shares = 0
    transactions = []
    
    for date, price in resampled.items():
        shares_bought = amount / price
        total_invested += amount
        total_shares += shares_bought
        
        transactions.append({
            'date': date.isoformat(),
            'price': price,
            'amount': amount,
            'shares': shares_bought,
            'cumulative_shares': total_shares,
            'cumulative_invested': total_invested
        })
    
    current_price = hist['Close'].iloc[-1]
    current_value = total_shares * current_price
    total_return = current_value - total_invested
    total_return_pct = (total_return / total_invested) * 100 if total_invested > 0 else 0
    
    # Calculate average cost basis
    avg_cost = total_invested / total_shares if total_shares > 0 else 0
    
    return {
        'ticker': ticker.upper(),
        'strategy': 'Dollar-Cost Averaging',
        'frequency': frequency,
        'amount_per_period': amount,
        'start_date': resampled.index[0].isoformat() if not resampled.empty else None,
        'end_date': resampled.index[-1].isoformat() if not resampled.empty else None,
        'total_periods': len(transactions),
        'total_invested': total_invested,
        'total_shares': total_shares,
        'average_cost_basis': avg_cost,
        'current_price': current_price,
        'current_value': current_value,
        'total_return': total_return,
        'total_return_pct': total_return_pct,
        'transactions': transactions
    }


def get_cashapp_recommendations(ticker: str) -> Dict:
    """
    Get investment recommendations formatted for Cash App users.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Dictionary with recommendations and analysis
    """
    ticker_obj = Ticker(ticker)
    
    try:
        info = ticker_obj.info
        recommendations = ticker_obj.recommendations
        
        # Get analyst recommendations
        rec_summary = {}
        if recommendations is not None and not recommendations.empty:
            rec_summary = {
                'strong_buy': len(recommendations[recommendations == 'Strong Buy']),
                'buy': len(recommendations[recommendations == 'Buy']),
                'hold': len(recommendations[recommendations == 'Hold']),
                'sell': len(recommendations[recommendations == 'Sell']),
                'strong_sell': len(recommendations[recommendations == 'Strong Sell'])
            }
        
        # Get price targets
        targets = ticker_obj.analyst_price_targets
        target_price = targets.get('targetMeanPrice', [0])[0] if targets else 0
        current_price = ticker_obj.fast_info.get('lastPrice', 0)
        
        upside_potential = ((target_price - current_price) / current_price * 100) if current_price > 0 else 0
        
        return {
            'ticker': ticker.upper(),
            'current_price': current_price,
            'target_price': target_price,
            'upside_potential_pct': upside_potential,
            'recommendation_summary': rec_summary,
            'recommendation': info.get('recommendationKey', 'N/A'),
            'recommendation_mean': info.get('recommendationMean', {}),
            'risk_level': 'Moderate',  # Placeholder - Cash App doesn't provide risk ratings
            'suitable_for': ['Long-term investors', 'DCA strategy']
        }
    except Exception as e:
        return {'error': str(e), 'ticker': ticker.upper()}
