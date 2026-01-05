// Dashboard JavaScript

const API_BASE = 'http://localhost:8000/api';

// Format currency
function formatCurrency(amount) {
    return 'Rs. ' + amount.toFixed(2);
}

// Format date time
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-IN', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true
    });
}

// Load dashboard stats
async function loadDashboardStats() {
    try {
        const response = await fetch(`${API_BASE}/dashboard/stats`);
        const data = await response.json();
        
        document.getElementById('dailyTransactions').textContent = data.daily_transactions;
        document.getElementById('dailyRevenue').textContent = formatCurrency(data.daily_revenue);
        document.getElementById('dailyProfit').textContent = formatCurrency(data.daily_profit);
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load today's transactions
async function loadTodayTransactions() {
    try {
        const response = await fetch(`${API_BASE}/dashboard/today-transactions`);
        const transactions = await response.json();
        
        const tbody = document.getElementById('transactionsTableBody');
        
        if (transactions.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No transactions today</td></tr>';
            return;
        }
        
        tbody.innerHTML = transactions.map(sale => {
            const itemCount = sale.items.reduce((sum, item) => sum + item.quantity, 0);
            const itemNames = sale.items.map(item => `${item.product_name} (${item.quantity})`).join(', ');
            
            return `
                <tr>
                    <td>${sale.id}</td>
                    <td>${formatDateTime(sale.created_at)}</td>
                    <td title="${itemNames}">${itemCount} items</td>
                    <td>${formatCurrency(sale.total_amount)}</td>
                    <td>${formatCurrency(sale.profit)}</td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading transactions:', error);
        document.getElementById('transactionsTableBody').innerHTML = 
            '<tr><td colspan="5" style="text-align: center;">Error loading transactions</td></tr>';
    }
}

// Initialize dashboard
async function initDashboard() {
    await loadDashboardStats();
    await loadTodayTransactions();
}

// Auto-refresh every 30 seconds
setInterval(() => {
    loadDashboardStats();
    loadTodayTransactions();
}, 30000);

// Load on page load
initDashboard();
