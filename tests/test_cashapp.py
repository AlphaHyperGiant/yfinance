"""
Tests for Cash App Integration

To run all tests in suite from commandline:
   python -m unittest tests.test_cashapp

Specific test class:
   python -m unittest tests.test_cashapp.TestCashAppPortfolio
"""

import unittest
import pandas as pd
from datetime import datetime

from tests.context import yfinance as yf
from yfinance.cashapp import (
    CashAppPortfolio,
    format_for_cashapp,
    get_cashapp_watchlist,
    calculate_dollar_cost_average,
    get_cashapp_recommendations
)


class TestCashAppPortfolio(unittest.TestCase):
    """Test CashAppPortfolio class"""
    
    def test_init_empty(self):
        """Test initializing empty portfolio"""
        portfolio = CashAppPortfolio()
        self.assertEqual(portfolio.holdings, {})
        self.assertIsNone(portfolio._tickers)
    
    def test_init_with_holdings(self):
        """Test initializing portfolio with holdings"""
        holdings = {'AAPL': 10, 'MSFT': 5}
        portfolio = CashAppPortfolio(holdings)
        self.assertEqual(portfolio.holdings, holdings)
    
    def test_add_position(self):
        """Test adding a position"""
        portfolio = CashAppPortfolio()
        portfolio.add_position('AAPL', 10)
        self.assertEqual(portfolio.holdings['AAPL'], 10)
    
    def test_add_position_update(self):
        """Test updating existing position"""
        portfolio = CashAppPortfolio({'AAPL': 10})
        portfolio.add_position('AAPL', 5)
        self.assertEqual(portfolio.holdings['AAPL'], 15)
    
    def test_remove_position(self):
        """Test removing a position"""
        portfolio = CashAppPortfolio({'AAPL': 10, 'MSFT': 5})
        portfolio.remove_position('AAPL')
        self.assertNotIn('AAPL', portfolio.holdings)
        self.assertIn('MSFT', portfolio.holdings)
    
    def test_get_portfolio_value_structure(self):
        """Test portfolio value structure"""
        portfolio = CashAppPortfolio({'AAPL': 10})
        result = portfolio.get_portfolio_value()
        
        self.assertIn('total_value', result)
        self.assertIn('positions', result)
        self.assertIn('last_updated', result)
        self.assertIsInstance(result['positions'], dict)
    
    def test_get_portfolio_summary(self):
        """Test portfolio summary DataFrame"""
        portfolio = CashAppPortfolio({'AAPL': 10})
        df = portfolio.get_portfolio_summary()
        
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn('Ticker', df.columns)
            self.assertIn('Shares', df.columns)
            self.assertIn('Price', df.columns)
            self.assertIn('Value', df.columns)
            self.assertIn('Weight %', df.columns)


class TestFormatForCashApp(unittest.TestCase):
    """Test format_for_cashapp function"""
    
    def test_format_quote(self):
        """Test formatting quote data"""
        result = format_for_cashapp('AAPL', 'quote')
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['symbol'], 'AAPL')
        self.assertIn('name', result)
        self.assertIn('price', result)
        self.assertIn('change', result)
        self.assertIn('change_percent', result)
    
    def test_format_history(self):
        """Test formatting history data"""
        result = format_for_cashapp('AAPL', 'history')
        
        self.assertIsInstance(result, dict)
        if result:  # May be empty if no data
            self.assertEqual(result['symbol'], 'AAPL')
            self.assertIn('dates', result)
            self.assertIn('prices', result)
    
    def test_format_info(self):
        """Test formatting info data"""
        result = format_for_cashapp('AAPL', 'info')
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['symbol'], 'AAPL')
        self.assertIn('name', result)
    
    def test_format_invalid_type(self):
        """Test invalid data type"""
        with self.assertRaises(ValueError):
            format_for_cashapp('AAPL', 'invalid')


class TestCashAppWatchlist(unittest.TestCase):
    """Test get_cashapp_watchlist function"""
    
    def test_watchlist_basic(self):
        """Test creating a watchlist"""
        tickers = ['AAPL', 'MSFT']
        df = get_cashapp_watchlist(tickers)
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), len(tickers))
        if not df.empty:
            self.assertIn('symbol', df.columns)
            self.assertIn('price', df.columns)


class TestDollarCostAverage(unittest.TestCase):
    """Test calculate_dollar_cost_average function"""
    
    def test_dca_structure(self):
        """Test DCA result structure"""
        result = calculate_dollar_cost_average('AAPL', 100, 'monthly')
        
        self.assertIsInstance(result, dict)
        if 'error' not in result:
            self.assertIn('ticker', result)
            self.assertIn('strategy', result)
            self.assertIn('frequency', result)
            self.assertIn('total_invested', result)
            self.assertIn('total_shares', result)
            self.assertIn('transactions', result)


class TestCashAppRecommendations(unittest.TestCase):
    """Test get_cashapp_recommendations function"""
    
    def test_recommendations_structure(self):
        """Test recommendations result structure"""
        result = get_cashapp_recommendations('AAPL')
        
        self.assertIsInstance(result, dict)
        self.assertIn('ticker', result)
        if 'error' not in result:
            self.assertIn('current_price', result)
            self.assertIn('recommendation_summary', result)


if __name__ == '__main__':
    unittest.main()
