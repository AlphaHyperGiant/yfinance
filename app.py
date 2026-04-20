#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Stock Portfolio Tracker - A $10 Marketplace Prototype
A responsive web application for tracking stock portfolios across all devices
"""

from flask import Flask, render_template, jsonify, request
import yfinance as yf
from datetime import datetime, timedelta
import json

app = Flask(__name__)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/quote/<ticker>')
def get_quote(ticker):
    """Get current quote for a ticker"""
    try:
        stock = yf.Ticker(ticker.upper())
        info = stock.info
        
        # Get current price
        hist = stock.history(period="1d", interval="1m")
        if not hist.empty:
            current_price = float(hist['Close'].iloc[-1])
        else:
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        
        # Get previous close
        prev_close = info.get('previousClose', current_price)
        change = current_price - prev_close
        change_percent = (change / prev_close * 100) if prev_close else 0
        
        return jsonify({
            'success': True,
            'ticker': ticker.upper(),
            'name': info.get('longName', info.get('shortName', ticker.upper())),
            'price': round(current_price, 2),
            'change': round(change, 2),
            'changePercent': round(change_percent, 2),
            'volume': info.get('volume', 0),
            'marketCap': info.get('marketCap', 0),
            'currency': info.get('currency', 'USD')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/history/<ticker>')
def get_history(ticker):
    """Get historical data for charting"""
    try:
        period = request.args.get('period', '1mo')
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(period=period)
        
        if hist.empty:
            return jsonify({
                'success': False,
                'error': 'No data available'
            }), 400
        
        # Format data for chart
        data = []
        for date, row in hist.iterrows():
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': round(float(row['Open']), 2),
                'high': round(float(row['High']), 2),
                'low': round(float(row['Low']), 2),
                'close': round(float(row['Close']), 2),
                'volume': int(row['Volume'])
            })
        
        return jsonify({
            'success': True,
            'ticker': ticker.upper(),
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/batch', methods=['POST'])
def get_batch():
    """Get quotes for multiple tickers"""
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        
        if not tickers:
            return jsonify({
                'success': False,
                'error': 'No tickers provided'
            }), 400
        
        results = []
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker.upper())
                info = stock.info
                
                hist = stock.history(period="1d", interval="1m")
                if not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
                else:
                    current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                
                prev_close = info.get('previousClose', current_price)
                change = current_price - prev_close
                change_percent = (change / prev_close * 100) if prev_close else 0
                
                results.append({
                    'ticker': ticker.upper(),
                    'name': info.get('longName', info.get('shortName', ticker.upper())),
                    'price': round(current_price, 2),
                    'change': round(change, 2),
                    'changePercent': round(change_percent, 2),
                    'volume': info.get('volume', 0),
                    'marketCap': info.get('marketCap', 0),
                    'currency': info.get('currency', 'USD')
                })
            except Exception as e:
                results.append({
                    'ticker': ticker.upper(),
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
