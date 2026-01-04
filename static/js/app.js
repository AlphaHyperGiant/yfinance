// Stock Portfolio Tracker - Frontend JavaScript

class PortfolioTracker {
    constructor() {
        this.portfolio = this.loadPortfolio();
        this.currentChart = null;
        this.currentTicker = null;
        this.currentPeriod = '1mo';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.renderPortfolio();
        this.updatePortfolioStats();
        
        // Auto-refresh every 30 seconds
        setInterval(() => this.refreshPortfolio(), 30000);
    }

    setupEventListeners() {
        // Add stock button
        document.getElementById('addStockBtn').addEventListener('click', () => this.addStock());
        
        // Enter key in input
        document.getElementById('tickerInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.addStock();
            }
        });

        // Period buttons
        document.querySelectorAll('.period-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentPeriod = e.target.dataset.period;
                if (this.currentChart) {
                    this.loadChart(this.currentTicker, this.currentPeriod);
                }
            });
        });
    }

    async addStock() {
        const input = document.getElementById('tickerInput');
        const ticker = input.value.trim().toUpperCase();
        const errorDiv = document.getElementById('errorMessage');

        if (!ticker) {
            this.showError('Please enter a stock symbol');
            return;
        }

        if (this.portfolio.includes(ticker)) {
            this.showError(`${ticker} is already in your portfolio`);
            return;
        }

        errorDiv.classList.remove('show');
        input.disabled = true;
        document.getElementById('addStockBtn').disabled = true;

        try {
            const response = await fetch(`/api/quote/${ticker}`);
            const data = await response.json();

            if (data.success) {
                this.portfolio.push(ticker);
                this.savePortfolio();
                this.renderPortfolio();
                this.updatePortfolioStats();
                input.value = '';
            } else {
                this.showError(data.error || 'Failed to fetch stock data');
            }
        } catch (error) {
            this.showError('Network error. Please try again.');
        } finally {
            input.disabled = false;
            document.getElementById('addStockBtn').disabled = false;
            input.focus();
        }
    }

    async removeStock(ticker) {
        this.portfolio = this.portfolio.filter(t => t !== ticker);
        this.savePortfolio();
        this.renderPortfolio();
        this.updatePortfolioStats();
        
        if (this.currentTicker === ticker) {
            document.getElementById('chartSection').style.display = 'none';
            this.currentChart = null;
            this.currentTicker = null;
        }
    }

    async refreshPortfolio() {
        if (this.portfolio.length === 0) return;
        
        try {
            const response = await fetch('/api/batch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ tickers: this.portfolio })
            });

            const data = await response.json();
            if (data.success) {
                this.renderPortfolio();
                this.updatePortfolioStats();
            }
        } catch (error) {
            console.error('Failed to refresh portfolio:', error);
        }
    }

    async renderPortfolio() {
        const grid = document.getElementById('portfolioGrid');
        
        if (this.portfolio.length === 0) {
            grid.innerHTML = `
                <div class="empty-state">
                    <p>👆 Add stocks to start tracking your portfolio</p>
                    <p class="hint">Try: AAPL, MSFT, GOOGL, TSLA, AMZN</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = '';
        
        // Fetch all stock data
        try {
            const response = await fetch('/api/batch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ tickers: this.portfolio })
            });

            const data = await response.json();
            if (data.success) {
                data.results.forEach(stock => {
                    if (stock.error) {
                        grid.innerHTML += this.createErrorCard(stock.ticker);
                    } else {
                        grid.innerHTML += this.createStockCard(stock);
                    }
                });

                // Attach event listeners to new cards
                this.attachCardListeners();
            }
        } catch (error) {
            grid.innerHTML = '<div class="empty-state"><p>Error loading portfolio. Please refresh.</p></div>';
        }
    }

    createStockCard(stock) {
        const changeClass = stock.change >= 0 ? 'positive' : 'negative';
        const changeSymbol = stock.change >= 0 ? '+' : '';
        const currency = stock.currency || 'USD';
        
        return `
            <div class="stock-card" data-ticker="${stock.ticker}">
                <div class="stock-card-header">
                    <div class="stock-info">
                        <h3>${stock.name}</h3>
                        <span class="ticker">${stock.ticker}</span>
                    </div>
                    <button class="remove-btn" onclick="tracker.removeStock('${stock.ticker}')" title="Remove">×</button>
                </div>
                <div class="stock-price">${this.formatCurrency(stock.price, currency)}</div>
                <div class="stock-change ${changeClass}">
                    <span>${changeSymbol}${this.formatCurrency(stock.change, currency)}</span>
                    <span>(${changeSymbol}${stock.changePercent.toFixed(2)}%)</span>
                </div>
                <div class="stock-meta">
                    <div class="meta-item">
                        <span class="meta-label">Volume</span>
                        <span class="meta-value">${this.formatNumber(stock.volume)}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Market Cap</span>
                        <span class="meta-value">${this.formatMarketCap(stock.marketCap)}</span>
                    </div>
                </div>
            </div>
        `;
    }

    createErrorCard(ticker) {
        return `
            <div class="stock-card">
                <div class="stock-card-header">
                    <div class="stock-info">
                        <h3>${ticker}</h3>
                        <span class="ticker">Error</span>
                    </div>
                    <button class="remove-btn" onclick="tracker.removeStock('${ticker}')" title="Remove">×</button>
                </div>
                <p style="color: var(--danger-color);">Failed to load data</p>
            </div>
        `;
    }

    attachCardListeners() {
        document.querySelectorAll('.stock-card').forEach(card => {
            const ticker = card.dataset.ticker;
            if (ticker) {
                card.addEventListener('click', (e) => {
                    // Don't trigger if clicking remove button
                    if (!e.target.classList.contains('remove-btn')) {
                        this.loadChart(ticker, this.currentPeriod);
                    }
                });
            }
        });
    }

    async loadChart(ticker, period) {
        this.currentTicker = ticker;
        this.currentPeriod = period;
        
        const chartSection = document.getElementById('chartSection');
        const chartTitle = document.getElementById('chartTitle');
        chartSection.style.display = 'block';
        chartTitle.textContent = `${ticker} Price History`;

        try {
            const response = await fetch(`/api/history/${ticker}?period=${period}`);
            const data = await response.json();

            if (data.success && data.data.length > 0) {
                this.renderChart(data.data, ticker);
            } else {
                chartTitle.textContent = `No data available for ${ticker}`;
            }
        } catch (error) {
            console.error('Failed to load chart:', error);
            chartTitle.textContent = `Error loading chart for ${ticker}`;
        }
    }

    renderChart(data, ticker) {
        const ctx = document.getElementById('priceChart').getContext('2d');
        
        if (this.currentChart) {
            this.currentChart.destroy();
        }

        const labels = data.map(d => {
            const date = new Date(d.date);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });
        
        const prices = data.map(d => d.close);

        this.currentChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Price',
                    data: prices,
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: (context) => {
                                const point = data[context.dataIndex];
                                return [
                                    `Open: $${point.open.toFixed(2)}`,
                                    `High: $${point.high.toFixed(2)}`,
                                    `Low: $${point.low.toFixed(2)}`,
                                    `Close: $${point.close.toFixed(2)}`
                                ];
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: (value) => '$' + value.toFixed(2)
                        }
                    },
                    x: {
                        ticks: {
                            maxTicksLimit: 10
                        }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }

    updatePortfolioStats() {
        if (this.portfolio.length === 0) {
            document.getElementById('totalValue').textContent = '$0.00';
            document.getElementById('totalChange').textContent = '$0.00';
            return;
        }

        // This is a simplified calculation - in a real app, you'd track shares and purchase prices
        fetch('/api/batch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ tickers: this.portfolio })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let totalValue = 0;
                let totalChange = 0;
                
                data.results.forEach(stock => {
                    if (!stock.error) {
                        totalValue += stock.price;
                        totalChange += stock.change;
                    }
                });

                document.getElementById('totalValue').textContent = this.formatCurrency(totalValue);
                const changeClass = totalChange >= 0 ? 'positive' : 'negative';
                const changeElement = document.getElementById('totalChange');
                changeElement.textContent = `${totalChange >= 0 ? '+' : ''}${this.formatCurrency(totalChange)}`;
                changeElement.className = `stat-value ${changeClass}`;
            }
        })
        .catch(error => console.error('Failed to update stats:', error));
    }

    formatCurrency(value, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(value);
    }

    formatNumber(value) {
        if (value >= 1e9) {
            return (value / 1e9).toFixed(2) + 'B';
        } else if (value >= 1e6) {
            return (value / 1e6).toFixed(2) + 'M';
        } else if (value >= 1e3) {
            return (value / 1e3).toFixed(2) + 'K';
        }
        return value.toLocaleString();
    }

    formatMarketCap(value) {
        if (!value) return 'N/A';
        if (value >= 1e12) {
            return '$' + (value / 1e12).toFixed(2) + 'T';
        } else if (value >= 1e9) {
            return '$' + (value / 1e9).toFixed(2) + 'B';
        } else if (value >= 1e6) {
            return '$' + (value / 1e6).toFixed(2) + 'M';
        }
        return this.formatCurrency(value);
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.textContent = message;
        errorDiv.classList.add('show');
        setTimeout(() => {
            errorDiv.classList.remove('show');
        }, 5000);
    }

    loadPortfolio() {
        const saved = localStorage.getItem('portfolio');
        return saved ? JSON.parse(saved) : [];
    }

    savePortfolio() {
        localStorage.setItem('portfolio', JSON.stringify(this.portfolio));
    }
}

// Initialize the tracker when page loads
let tracker;
document.addEventListener('DOMContentLoaded', () => {
    tracker = new PortfolioTracker();
});
