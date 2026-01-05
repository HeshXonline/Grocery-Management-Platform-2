// Billing JavaScript

const API_BASE = 'http://localhost:8000/api';

let allProducts = [];
let cart = [];

// Format currency
function formatCurrency(amount) {
    return 'Rs. ' + amount.toFixed(2);
}

// Load all products
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE}/products`);
        allProducts = await response.json();
        displayProducts(allProducts);
    } catch (error) {
        console.error('Error loading products:', error);
        document.getElementById('productList').innerHTML = 
            '<p style="color: red;">Error loading products</p>';
    }
}

// Display products
function displayProducts(products) {
    const productList = document.getElementById('productList');
    
    if (products.length === 0) {
        productList.innerHTML = '<p>No products available</p>';
        return;
    }
    
    productList.innerHTML = products.map(product => `
        <div class="product-item" onclick="addToCart(${product.id})" data-id="${product.id}">
            <div class="product-name">${product.name}</div>
            <div class="product-info">
                ${product.category} | Stock: ${product.stock_quantity}
            </div>
            <div class="product-price">${formatCurrency(product.selling_price)}</div>
        </div>
    `).join('');
}

// Search products
document.getElementById('productSearch').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const filtered = allProducts.filter(p => 
        p.name.toLowerCase().includes(searchTerm) || 
        p.category.toLowerCase().includes(searchTerm)
    );
    displayProducts(filtered);
});

// Add to cart
function addToCart(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;
    
    if (product.stock_quantity === 0) {
        return;
    }
    
    const cartItem = cart.find(item => item.product_id === productId);
    
    if (cartItem) {
        if (cartItem.quantity >= product.stock_quantity) {
            return;
        }
        cartItem.quantity++;
    } else {
        cart.push({
            product_id: productId,
            name: product.name,
            price: product.selling_price,
            quantity: 1,
            max_stock: product.stock_quantity
        });
    }
    
    updateCartDisplay();
}

// Update cart quantity
function updateQuantity(productId, delta) {
    const cartItem = cart.find(item => item.product_id === productId);
    if (!cartItem) return;
    
    const newQuantity = cartItem.quantity + delta;
    
    if (newQuantity <= 0) {
        removeFromCart(productId);
        return;
    }
    
    if (newQuantity > cartItem.max_stock) {
        return;
    }
    
    cartItem.quantity = newQuantity;
    updateCartDisplay();
}

// Remove from cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.product_id !== productId);
    updateCartDisplay();
}

// Update cart display
function updateCartDisplay() {
    const cartItems = document.getElementById('cartItems');
    const totalItemsEl = document.getElementById('totalItems');
    const totalAmountEl = document.getElementById('totalAmount');
    const completeSaleBtn = document.getElementById('completeSaleBtn');
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">Cart is empty</p>';
        totalItemsEl.textContent = '0';
        totalAmountEl.textContent = formatCurrency(0);
        completeSaleBtn.disabled = true;
        return;
    }
    
    let totalItems = 0;
    let totalAmount = 0;
    
    cartItems.innerHTML = cart.map(item => {
        const itemTotal = item.price * item.quantity;
        totalItems += item.quantity;
        totalAmount += itemTotal;
        
        return `
            <div class="cart-item">
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">${formatCurrency(item.price)} × ${item.quantity} = ${formatCurrency(itemTotal)}</div>
                </div>
                <div class="cart-item-controls">
                    <button class="qty-btn" onclick="updateQuantity(${item.product_id}, -1)">−</button>
                    <span class="qty-display">${item.quantity}</span>
                    <button class="qty-btn" onclick="updateQuantity(${item.product_id}, 1)">+</button>
                    <button class="remove-btn" onclick="removeFromCart(${item.product_id})">✕</button>
                </div>
            </div>
        `;
    }).join('');
    
    totalItemsEl.textContent = totalItems;
    totalAmountEl.textContent = formatCurrency(totalAmount);
    completeSaleBtn.disabled = false;
}

// Complete sale
async function completeSale() {
    if (cart.length === 0) return;
    
    const saleData = {
        items: cart.map(item => ({
            product_id: item.product_id,
            quantity: item.quantity
        }))
    };
    
    try {
        const response = await fetch(`${API_BASE}/sales`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(saleData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            console.error('Sale error:', error.detail || 'Failed to complete sale');
            return;
        }
        
        const result = await response.json();
        
        // Show success modal
        const totalAmount = formatCurrency(result.total_amount);
        const profit = formatCurrency(result.profit);
        document.getElementById('saleDetails').innerHTML = 
            `Sale ID: ${result.id}<br>Total Amount: ${totalAmount}<br>Profit: ${profit}`;
        document.getElementById('successModal').classList.add('show');
        
        // Clear cart
        cart = [];
        updateCartDisplay();
        
        // Reload products to update stock
        await loadProducts();
        
    } catch (error) {
        console.error('Error completing sale:', error);
    }
}

// Clear cart
function clearCart() {
    if (cart.length === 0) return;
    
    cart = [];
    updateCartDisplay();
}

// Close modal
document.getElementById('closeModalBtn').addEventListener('click', () => {
    document.getElementById('successModal').classList.remove('show');
});

// Event listeners
document.getElementById('completeSaleBtn').addEventListener('click', completeSale);
document.getElementById('clearCartBtn').addEventListener('click', clearCart);

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to complete sale
    if (e.ctrlKey && e.key === 'Enter') {
        if (!document.getElementById('completeSaleBtn').disabled) {
            completeSale();
        }
    }
    // Escape to clear search
    if (e.key === 'Escape') {
        document.getElementById('productSearch').value = '';
        displayProducts(allProducts);
    }
});

// Focus search on load
document.getElementById('productSearch').focus();

// Load products on page load
loadProducts();
