# Stock Portfolio Tracker - Marketplace Prototype ($10)

A responsive web application for tracking stock portfolios in real-time. Works seamlessly across all devices (desktop, tablet, mobile).

## Features

- 📈 **Real-time Stock Quotes** - Get live stock prices and market data
- 📊 **Interactive Charts** - View price history with multiple time periods (5D, 1M, 3M, 6M, 1Y)
- 💼 **Portfolio Management** - Add/remove stocks and track your portfolio
- 📱 **Fully Responsive** - Beautiful UI that works on all screen sizes
- 💾 **Local Storage** - Your portfolio is saved locally in your browser
- 🔄 **Auto-refresh** - Portfolio updates every 30 seconds automatically

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Install dependencies:
```bash
pip install -r requirements-app.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Add Stocks**: Enter a stock symbol (e.g., AAPL, MSFT, GOOGL) and click "Add Stock"
2. **View Details**: Click on any stock card to see its price history chart
3. **Change Time Period**: Use the period buttons (5D, 1M, 3M, 6M, 1Y) to view different timeframes
4. **Remove Stocks**: Click the × button on any stock card to remove it from your portfolio

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Option 1: Using Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Option 2: Using Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements-app.txt .
RUN pip install --no-cache-dir -r requirements-app.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t stock-tracker .
docker run -p 5000:5000 stock-tracker
```

#### Option 3: Deploy to Cloud Platforms

**Heroku:**
```bash
heroku create stock-portfolio-tracker
git push heroku main
```

**Railway:**
- Connect your repository
- Set start command: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
- Deploy automatically

**Render:**
- Create a new Web Service
- Set build command: `pip install -r requirements-app.txt`
- Set start command: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`

## Marketplace Listing

### Product Description
"Stock Portfolio Tracker - A professional-grade web application for tracking your stock investments in real-time. Features interactive charts, responsive design, and automatic portfolio updates. Perfect for investors who want a simple, elegant solution to monitor their stocks."

### Pricing
**$10 USD** - One-time purchase includes:
- Full source code
- Deployment instructions
- Lifetime updates
- Commercial use license

### Key Selling Points
- ✅ Works on all devices (desktop, tablet, mobile)
- ✅ Real-time stock data from Yahoo Finance
- ✅ Beautiful, modern UI
- ✅ Easy to deploy and customize
- ✅ No API keys required
- ✅ Lightweight and fast

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Charts**: Chart.js
- **Data Source**: Yahoo Finance (via yfinance library)
- **Storage**: Browser LocalStorage

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

This prototype is provided as-is for marketplace sale. The buyer receives full source code and deployment rights.

## Support

For questions or issues, please refer to the deployment documentation or contact the seller.

---

**Note**: This application uses Yahoo Finance data which is intended for personal use only. Please refer to Yahoo's terms of use for commercial usage rights.
