# 💰 Expense Tracker

A Python-based personal expense management application for recording, analyzing, visualizing, and reporting monthly expenses.

## 📌 Overview

Expense Tracker is a beginner-friendly Python project that helps users manage their daily expenses through a simple command-line interface.

The application stores expense data in CSV format and provides monthly analysis, graphical visualization, and PDF report generation.

## 🚀 Features

### 1. Add Expense
Users can enter:

- Date
- Category
- Description
- Amount

### 2. View Expenses
Displays all recorded expenses in a clean table format.

### 3. Edit Expense
Allows users to modify an existing expense.

### 4. Delete Expense
Allows users to remove an unwanted expense.

### 5. Monthly Analysis
Provides:

- Total expenses
- Number of expenses
- Average expense
- Highest expense
- Lowest expense
- Category-wise spending

### 6. Graphical Analysis

The project generates:

- Bar graph
- Pie chart
- Daily expense trend graph

### 7. PDF Report

The application generates a monthly PDF report containing:

- Expense summary
- Category-wise expenses
- Individual expense details
- Graphs
- Page numbers

## 🛠️ Technologies Used

- Python
- Pandas
- Matplotlib
- ReportLab
- CSV

## 📂 Project Structure

```text
Expense_Tracker/
│
├── data/
│   └── expense.csv
│
├── graphs/
│   ├── category_expenses_*.png
│   ├── expense_distribution_*.png
│   └── daily_expense_trend_*.png
│
├── reports/
│   └── Expense_Report_*.pdf
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore


## 🧠 Skills Demonstrated

- Python Programming
- Functions and Modular Programming
- File Handling
- CSV Data Management
- Input Validation
- Exception Handling
- Pandas
- Data Analysis
- Matplotlib Data Visualization
- PDF Report Generation
- Project Structure and Documentation

## 🔮 Future Improvements

- GUI using Tkinter
- SQLite database
- Budget tracking
- Budget alerts
- Yearly expense analysis
- Interactive dashboard
- User authentication
- Cloud data storage