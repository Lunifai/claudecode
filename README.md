# Expense & Income Tracker

A simple, elegant web application to track your expenses and income. Built with vanilla HTML, CSS, and JavaScript with no external dependencies.

## Features

- **Track Income & Expenses**: Add and categorize all your financial transactions
- **Real-time Balance**: See your current balance updated instantly
- **Summary Dashboard**: View total income and expenses at a glance
- **Transaction History**: Browse all your transactions with detailed information
- **Filter Transactions**: Filter by all transactions, income only, or expenses only
- **Data Persistence**: All data is saved locally in your browser using localStorage
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern UI**: Clean, intuitive interface with smooth animations

## Getting Started

### Prerequisites

No installation required! Just a modern web browser.

### Running the App

1. Clone this repository or download the files
2. Open `index.html` in your web browser
3. Start tracking your finances!

Alternatively, you can serve it using any web server:

```bash
# Using Python 3
python -m http.server 8000

# Using Node.js (with http-server)
npx http-server
```

Then open `http://localhost:8000` in your browser.

## How to Use

### Adding a Transaction

1. Fill in the transaction details:
   - **Description**: What is this transaction for? (e.g., "Grocery shopping", "Monthly salary")
   - **Amount**: The transaction amount in dollars
   - **Category**: Optional category for organization (e.g., "Food", "Salary", "Entertainment")
   - **Date**: When did this transaction occur?
   - **Type**: Select whether this is Income or an Expense

2. Click "Add Transaction" to save

### Viewing Transactions

- All transactions appear in the Transaction History section
- Transactions are sorted by date (newest first)
- Each transaction shows:
  - Description
  - Category
  - Date
  - Amount (with + for income, - for expenses)

### Filtering Transactions

Use the filter buttons to view:
- **All**: Show all transactions
- **Income**: Show only income transactions
- **Expenses**: Show only expense transactions

### Deleting Transactions

Click the "Delete" button on any transaction to remove it. You'll be asked to confirm before deletion.

### Dashboard Summary

The top of the app displays:
- **Current Balance**: Total income minus total expenses
- **Total Income**: Sum of all income transactions
- **Total Expenses**: Sum of all expense transactions

## Data Storage

All your data is stored locally in your browser using localStorage. This means:
- ✅ Your data is private and never leaves your device
- ✅ Data persists between sessions
- ⚠️ Clearing browser data will delete your transactions
- ⚠️ Data is device-specific (not synced across devices)

## File Structure

```
.
├── index.html      # Main HTML structure
├── styles.css      # Styling and responsive design
├── app.js          # Application logic and functionality
└── README.md       # Documentation
```

## Browser Compatibility

Works on all modern browsers:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Future Enhancements

Potential features for future versions:
- Export data to CSV/JSON
- Import transactions
- Charts and visualizations
- Monthly/yearly reports
- Budget tracking
- Multiple accounts
- Cloud sync

## License

This project is open source and available for personal and commercial use.

## Contributing

Feel free to fork this project and submit pull requests for any improvements!
