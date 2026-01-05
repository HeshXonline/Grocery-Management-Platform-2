// Reports JavaScript

const API_BASE = 'http://localhost:8000/api';

let allStockItems = [];

// Format currency
function formatCurrency(amount) {
    return 'Rs. ' + amount.toFixed(2);
}

// Load reports summary
async function loadReportsSummary() {
    try {
        const response = await fetch(`${API_BASE}/reports/stock`);
        const stockData = await response.json();
        
        // Calculate stock-based metrics
        let totalStockCost = 0;
        let expectedRevenue = 0;
        
        stockData.forEach(item => {
            totalStockCost += item.buying_price * item.stock_quantity;
            expectedRevenue += item.selling_price * item.stock_quantity;
        });
        
        const expectedProfit = expectedRevenue - totalStockCost;
        
        document.getElementById('totalStockCost').textContent = formatCurrency(totalStockCost);
        document.getElementById('expectedRevenue').textContent = formatCurrency(expectedRevenue);
        document.getElementById('expectedProfit').textContent = formatCurrency(expectedProfit);
    } catch (error) {
        console.error('Error loading reports summary:', error);
    }
}

// Load stock report
async function loadStockReport() {
    try {
        const response = await fetch(`${API_BASE}/reports/stock`);
        allStockItems = await response.json();
        displayStockReport(allStockItems);
    } catch (error) {
        console.error('Error loading stock report:', error);
        document.getElementById('stockTableBody').innerHTML = 
            '<tr><td colspan="6" style="text-align: center;">Error loading stock data</td></tr>';
    }
}

// Display stock report
function displayStockReport(items) {
    const tbody = document.getElementById('stockTableBody');
    
    if (items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No products found</td></tr>';
        return;
    }
    
    tbody.innerHTML = items.map(item => {
        const stockValue = item.stock_quantity * item.buying_price;
        const lowStock = item.stock_quantity < 10 ? 'low-stock' : '';
        
        return `
            <tr>
                <td>${item.product_name}</td>
                <td>${item.category}</td>
                <td class="${lowStock}">${item.stock_quantity}</td>
                <td>${formatCurrency(item.buying_price)}</td>
                <td>${formatCurrency(item.selling_price)}</td>
                <td>${formatCurrency(stockValue)}</td>
            </tr>
        `;
    }).join('');
}

// Search stock
document.getElementById('stockSearch').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const filtered = allStockItems.filter(item => 
        item.product_name.toLowerCase().includes(searchTerm) || 
        item.category.toLowerCase().includes(searchTerm)
    );
    displayStockReport(filtered);
});

// Initialize reports
async function initReports() {
    await loadReportsSummary();
    await loadStockReport();
}

// Load on page load
initReports();
