// Products Management JavaScript

const API_BASE = 'http://localhost:8000/api';

let allProducts = [];
let editingProductId = null;
let deleteProductId = null;

// Format currency
function formatCurrency(amount) {
    return 'Rs. ' + amount.toFixed(2);
}

// Calculate profit margin percentage
function calculateProfitMargin(buyingPrice, sellingPrice) {
    if (buyingPrice === 0) return 0;
    return (((sellingPrice - buyingPrice) / buyingPrice) * 100).toFixed(1);
}

// Load all products
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE}/products`);
        allProducts = await response.json();
        displayProducts(allProducts);
    } catch (error) {
        console.error('Error loading products:', error);
        document.getElementById('productsTableBody').innerHTML = 
            '<tr><td colspan="7" style="text-align: center; color: red;">Error loading products</td></tr>';
    }
}

// Display products in table
function displayProducts(products) {
    const tbody = document.getElementById('productsTableBody');
    
    if (products.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">No products found</td></tr>';
        return;
    }
    
    tbody.innerHTML = products.map(product => {
        const profitMargin = calculateProfitMargin(product.buying_price, product.selling_price);
        const lowStock = product.stock_quantity < 10 ? 'low-stock' : '';
        
        return `
            <tr>
                <td>${product.name}</td>
                <td>${product.category}</td>
                <td>${formatCurrency(product.buying_price)}</td>
                <td>${formatCurrency(product.selling_price)}</td>
                <td class="${lowStock}">${product.stock_quantity}</td>
                <td>${profitMargin}%</td>
                <td>
                    <button class="btn-action btn-edit" onclick="editProduct(${product.id})">Edit</button>
                    <button class="btn-action btn-delete" onclick="confirmDelete(${product.id}, '${product.name}')">Delete</button>
                </td>
            </tr>
        `;
    }).join('');
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

// Handle form submission
document.getElementById('productForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const productData = {
        name: document.getElementById('productName').value,
        category: document.getElementById('productCategory').value,
        buying_price: parseFloat(document.getElementById('buyingPrice').value),
        selling_price: parseFloat(document.getElementById('sellingPrice').value),
        stock_quantity: parseInt(document.getElementById('stockQuantity').value)
    };
    
    try {
        let response;
        if (editingProductId) {
            // Update existing product
            response = await fetch(`${API_BASE}/products/${editingProductId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(productData)
            });
        } else {
            // Create new product
            response = await fetch(`${API_BASE}/products`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(productData)
            });
        }
        
        if (!response.ok) {
            const error = await response.json();
            console.error('Save error:', error.detail || 'Failed to save product');
            return;
        }
        
        // Success
        resetForm();
        await loadProducts();
        
    } catch (error) {
        console.error('Error saving product:', error);
    }
});

// Edit product
function editProduct(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;
    
    editingProductId = productId;
    
    document.getElementById('productName').value = product.name;
    document.getElementById('productCategory').value = product.category;
    document.getElementById('buyingPrice').value = product.buying_price;
    document.getElementById('sellingPrice').value = product.selling_price;
    document.getElementById('stockQuantity').value = product.stock_quantity;
    
    document.getElementById('submitBtn').textContent = 'Update Product';
    document.getElementById('cancelBtn').style.display = 'inline-block';
    
    // Scroll to form
    document.getElementById('productForm').scrollIntoView({ behavior: 'smooth' });
}

// Confirm delete
function confirmDelete(productId, productName) {
    deleteProductId = productId;
    document.getElementById('deleteMessage').textContent = 
        `Are you sure you want to delete "${productName}"?`;
    document.getElementById('deleteModal').classList.add('show');
}

// Delete product
document.getElementById('confirmDeleteBtn').addEventListener('click', async () => {
    if (!deleteProductId) return;
    
    try {
        const response = await fetch(`${API_BASE}/products/${deleteProductId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const error = await response.json();
            console.error('Delete error:', error.detail || 'Failed to delete product');
            return;
        }
        
        document.getElementById('deleteModal').classList.remove('show');
        deleteProductId = null;
        await loadProducts();
        
    } catch (error) {
        console.error('Error deleting product:', error);
    }
});

// Cancel delete
document.getElementById('cancelDeleteBtn').addEventListener('click', () => {
    document.getElementById('deleteModal').classList.remove('show');
    deleteProductId = null;
});

// Reset form
function resetForm() {
    editingProductId = null;
    document.getElementById('productForm').reset();
    document.getElementById('submitBtn').textContent = 'Add Product';
    document.getElementById('cancelBtn').style.display = 'none';
}

// Cancel edit
document.getElementById('cancelBtn').addEventListener('click', resetForm);

// Toggle form visibility
document.getElementById('toggleFormBtn').addEventListener('click', () => {
    const form = document.getElementById('productForm');
    const btn = document.getElementById('toggleFormBtn');
    
    if (form.style.display === 'none') {
        form.style.display = 'grid';
        btn.textContent = 'Hide Form';
    } else {
        form.style.display = 'none';
        btn.textContent = 'Show Form';
    }
});

// Load products on page load
loadProducts();
