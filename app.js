// Expense & Income Tracker Application
class ExpenseTracker {
    constructor() {
        this.transactions = this.loadTransactions();
        this.currentFilter = 'all';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setDefaultDate();
        this.updateUI();
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('transaction-form');
        form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Filter buttons
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleFilter(e));
        });
    }

    setDefaultDate() {
        const dateInput = document.getElementById('date');
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
    }

    handleSubmit(e) {
        e.preventDefault();

        const description = document.getElementById('description').value.trim();
        const amount = parseFloat(document.getElementById('amount').value);
        const category = document.getElementById('category').value.trim();
        const date = document.getElementById('date').value;
        const type = document.querySelector('input[name="type"]:checked').value;

        if (!description || !amount || !date || !type) {
            alert('Please fill in all required fields');
            return;
        }

        const transaction = {
            id: this.generateId(),
            description,
            amount,
            category: category || 'Uncategorized',
            date,
            type,
            timestamp: new Date().getTime()
        };

        this.addTransaction(transaction);
        e.target.reset();
        this.setDefaultDate();
    }

    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    addTransaction(transaction) {
        this.transactions.push(transaction);
        this.saveTransactions();
        this.updateUI();
        this.showNotification(`${transaction.type === 'income' ? 'Income' : 'Expense'} added successfully!`);
    }

    deleteTransaction(id) {
        if (confirm('Are you sure you want to delete this transaction?')) {
            this.transactions = this.transactions.filter(t => t.id !== id);
            this.saveTransactions();
            this.updateUI();
            this.showNotification('Transaction deleted');
        }
    }

    handleFilter(e) {
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(btn => btn.classList.remove('active'));
        e.target.classList.add('active');

        this.currentFilter = e.target.dataset.filter;
        this.renderTransactions();
    }

    getFilteredTransactions() {
        if (this.currentFilter === 'all') {
            return this.transactions;
        }
        return this.transactions.filter(t => t.type === this.currentFilter);
    }

    calculateTotals() {
        const income = this.transactions
            .filter(t => t.type === 'income')
            .reduce((sum, t) => sum + t.amount, 0);

        const expense = this.transactions
            .filter(t => t.type === 'expense')
            .reduce((sum, t) => sum + t.amount, 0);

        const balance = income - expense;

        return { income, expense, balance };
    }

    updateUI() {
        this.updateSummary();
        this.renderTransactions();
    }

    updateSummary() {
        const { income, expense, balance } = this.calculateTotals();

        document.getElementById('balance').textContent = this.formatCurrency(balance);
        document.getElementById('total-income').textContent = this.formatCurrency(income);
        document.getElementById('total-expense').textContent = this.formatCurrency(expense);
    }

    renderTransactions() {
        const transactionsList = document.getElementById('transactions-list');
        const filteredTransactions = this.getFilteredTransactions();

        if (filteredTransactions.length === 0) {
            transactionsList.innerHTML = '<p class="empty-state">No transactions found. Add your first transaction above!</p>';
            return;
        }

        // Sort transactions by date (newest first)
        const sortedTransactions = [...filteredTransactions].sort((a, b) => {
            return new Date(b.date) - new Date(a.date);
        });

        transactionsList.innerHTML = sortedTransactions.map(transaction => {
            return this.createTransactionElement(transaction);
        }).join('');

        // Add delete event listeners
        transactionsList.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.dataset.id;
                this.deleteTransaction(id);
            });
        });
    }

    createTransactionElement(transaction) {
        const sign = transaction.type === 'income' ? '+' : '-';
        const formattedDate = this.formatDate(transaction.date);

        return `
            <div class="transaction-item ${transaction.type}">
                <div class="transaction-info">
                    <div class="transaction-description">${this.escapeHtml(transaction.description)}</div>
                    <div class="transaction-meta">
                        <span class="transaction-category">${this.escapeHtml(transaction.category)}</span>
                        <span class="transaction-date">${formattedDate}</span>
                    </div>
                </div>
                <div class="transaction-amount ${transaction.type}">
                    ${sign}${this.formatCurrency(transaction.amount)}
                </div>
                <button class="btn-delete" data-id="${transaction.id}">Delete</button>
            </div>
        `;
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(Math.abs(amount));
    }

    formatDate(dateString) {
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return new Date(dateString).toLocaleDateString('en-US', options);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // LocalStorage methods
    saveTransactions() {
        localStorage.setItem('transactions', JSON.stringify(this.transactions));
    }

    loadTransactions() {
        const stored = localStorage.getItem('transactions');
        return stored ? JSON.parse(stored) : [];
    }

    showNotification(message) {
        // Simple notification - you can enhance this
        console.log(message);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ExpenseTracker();
});
