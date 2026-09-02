import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

DATA_FILE = "data/expense.csv"  

def initialize_file():
    os.makedirs("data", exist_ok=True)
    os.makedirs("graphs", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "category", "description", "amount"])
            
def get_valid_date():
    while True:
        date = input("Enter date (DD-MM-YYYY): ")

        try:
            datetime.strptime(date, "%d-%m-%Y")
            return date

        except ValueError:
            print("Invalid date. Please use DD-MM-YYYY.")


def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except ValueError:
            print("Please enter a valid number.")


def get_valid_category():
    while True:
        category = input("Enter category: ").strip().title()

        if category:
            return category

        print("Category cannot be empty.")


def get_valid_description():
    while True:
        description = input("Enter description: ").strip()

        if description:
            return description

        print("Description cannot be empty.")

def load_expenses():
    if not os.path.exists(DATA_FILE):
        initialize_file()

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        return df

    df["date"] = pd.to_datetime(
        df["date"],
        format="%d-%m-%Y"
    )

    df["amount"] = pd.to_numeric(df["amount"])

    return df


def show_summary():
    df = load_expenses()

    if df.empty:
        print("\nNo expenses recorded yet.")
        return

    total = df["amount"].sum()
    count = len(df)

    print(f"\nTotal Expenses: Rs. {total:.2f}")
    print(f"Number of Expenses: {count}")


def add_expense():
    date = get_valid_date()
    category = get_valid_category()
    description = get_valid_description()
    amount = get_valid_amount()

    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            date,
            category,
            description,
            amount
        ])

    print("Expense added successfully!")


def view_expenses():
    df = load_expenses()

    if df.empty:
        print("No expenses found.")
        return

    print("\n" + "=" * 65)
    print(f"{'Date':<15}{'Category':<15}{'Description':<20}{'Amount':>10}")
    print("=" * 65)

    for _, row in df.iterrows():

        date = row["date"].strftime("%d-%m-%Y")
        category = row["category"]
        description = row["description"]
        amount = row["amount"]

        print(
            f"{date:<15}"
            f"{category:<15}"
            f"{description:<20}"
            f"{amount:>9.2f}"
        )

    print("=" * 65)

def delete_expense():
    df = load_expenses()

    if df.empty:
        print("No expenses found.")
        return

    print("\nCurrent Expenses:")
    print("=" * 70)

    for index, row in df.iterrows():
        date = row["date"].strftime("%d-%m-%Y")
        print(
            f"{index + 1}. "
            f"{date:<15}"
            f"{row['category']:<15}"
            f"{row['description']:<20}"
            f"Rs. {row['amount']:.2f}"
        )

    print("=" * 70)

    try:
        choice = int(input("Enter expense number to delete: "))

        if choice < 1 or choice > len(df):
            print("Invalid expense number.")
            return

        df = df.drop(df.index[choice - 1])

        df["date"] = df["date"].dt.strftime("%d-%m-%Y")

        df.to_csv(DATA_FILE, index=False)

        print("Expense deleted successfully!")

    except ValueError:
        print("Please enter a valid number.")

def edit_expense():
    df = load_expenses()

    if df.empty:
        print("No expenses found.")
        return

    print("\nCurrent Expenses:")
    print("=" * 70)

    for index, row in df.iterrows():
        date = row["date"].strftime("%d-%m-%Y")

        print(
            f"{index + 1}. "
            f"{date:<15}"
            f"{row['category']:<15}"
            f"{row['description']:<20}"
            f"Rs. {row['amount']:.2f}"
        )

    print("=" * 70)

    try:
        choice = int(input("Enter expense number to edit: "))

        if choice < 1 or choice > len(df):
            print("Invalid expense number.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    index = df.index[choice - 1]

    print("\nEnter new details:")

    date = get_valid_date()
    category = get_valid_category()
    description = get_valid_description()
    amount = get_valid_amount()

    df.loc[index, "date"] = pd.to_datetime(
        date,
        format="%d-%m-%Y"
    )

    df.loc[index, "category"] = category
    df.loc[index, "description"] = description
    df.loc[index, "amount"] = amount

    df["date"] = df["date"].dt.strftime("%d-%m-%Y")

    df.to_csv(DATA_FILE, index=False)

    print("Expense updated successfully!")


def monthly_analysis():
    df = load_expenses()

    if df.empty:
        print("No expenses found.")
        return

    month_year = input("Enter month (MM-YYYY): ")

    try:
        selected_month = pd.to_datetime(
            month_year,
            format="%m-%Y"
        )
    except ValueError:
        print("Invalid month format. Please use MM-YYYY.")
        return

    monthly_data = df[
        (df["date"].dt.month == selected_month.month) &
        (df["date"].dt.year == selected_month.year)
    ]

    if monthly_data.empty:
        print("No expenses found for this month.")
        return

    total = monthly_data["amount"].sum()
    count = len(monthly_data)
    average = monthly_data["amount"].mean()
    highest = monthly_data["amount"].max()
    lowest = monthly_data["amount"].min()

    print("\n========================================")
    print("          MONTHLY ANALYSIS")
    print("========================================")

    print(f"Month: {selected_month.strftime('%B %Y')}")
    print(f"Total Expenses: Rs. {total:.2f}")
    print(f"Number of Expenses: {count}")
    print(f"Average Expense: Rs. {average:.2f}")
    print(f"Highest Expense: Rs. {highest:.2f}")
    print(f"Lowest Expense: Rs. {lowest:.2f}")

    print("\nCategory-wise Expenses")
    print("----------------------------------------")

    category_total = monthly_data.groupby("category")["amount"].sum()

    for category, amount in category_total.items():
        print(f"{category:<20} Rs. {amount:.2f}")

    print("========================================")
    
def generate_graphs():
    df = load_expenses()

    if df.empty:
        print("No expenses found.")
        return

    month_year = input("Enter month (MM-YYYY): ")

    try:
        selected_month = pd.to_datetime(
            month_year,
            format="%m-%Y"
        )
    except ValueError:
        print("Invalid month format. Please use MM-YYYY.")
        return

    monthly_data = df[
        (df["date"].dt.month == selected_month.month) &
        (df["date"].dt.year == selected_month.year)
    ]

    if monthly_data.empty:
        print("No expenses found for this month.")
        return

    month_name = selected_month.strftime("%B_%Y")

    # ---------------- BAR GRAPH ----------------

    category_total = monthly_data.groupby("category")["amount"].sum()

    plt.figure(figsize=(8, 5))

    plt.bar(category_total.index, category_total.values)

    plt.title("Category-wise Expenses")
    plt.xlabel("Category")
    plt.ylabel("Amount (Rs.)")

    plt.xticks(rotation=45)

    plt.tight_layout()

    bar_file = f"graphs/category_expenses_{month_name}.png"

    plt.savefig(bar_file)
    plt.close()

    # ---------------- PIE CHART ----------------

    plt.figure(figsize=(7, 7))

    plt.pie(
        category_total.values,
        labels=category_total.index,
        autopct="%1.1f%%"
    )

    plt.title("Expense Distribution")

    pie_file = f"graphs/expense_distribution_{month_name}.png"

    plt.savefig(pie_file)
    plt.close()

    # ---------------- LINE GRAPH ----------------

    daily_expenses = monthly_data.groupby("date")["amount"].sum()

    plt.figure(figsize=(10, 5))

    plt.plot(
        daily_expenses.index,
        daily_expenses.values,
        marker="o"
    )

    plt.title("Daily Expense Trend")
    plt.xlabel("Date")
    plt.ylabel("Amount Spent (Rs.)")

    plt.xticks(rotation=45)

    plt.grid()

    plt.tight_layout()

    line_file = f"graphs/daily_expense_trend_{month_name}.png"

    plt.savefig(line_file)
    plt.close()

    print("\n========================================")
    print("          GRAPHS CREATED")
    print("========================================")

    print("Bar graph :", bar_file)
    print("Pie graph :", pie_file)
    print("Line graph:", line_file)

    print("========================================")


def add_page_footer(pdf, width):
    pdf.setFont("Helvetica", 9)

    pdf.drawCentredString(
        width / 2,
        25,
        f"Expense Tracker | Page {pdf.getPageNumber()}"
    )
    

def export_pdf():
    df = load_expenses()

    if df.empty:
        print("No expenses found.")
        return

    month_year = input("Enter month (MM-YYYY): ")

    try:
        selected_month = pd.to_datetime(
            month_year,
            format="%m-%Y"
        )
    except ValueError:
        print("Invalid month format. Please use MM-YYYY.")
        return

    monthly_data = df[
        (df["date"].dt.month == selected_month.month) &
        (df["date"].dt.year == selected_month.year)
    ]

    if monthly_data.empty:
        print("No expenses found for this month.")
        return

    # Calculate summary

    total = monthly_data["amount"].sum()
    count = len(monthly_data)
    average = monthly_data["amount"].mean()
    highest = monthly_data["amount"].max()
    lowest = monthly_data["amount"].min()

    category_total = monthly_data.groupby("category")["amount"].sum()

    month_name = selected_month.strftime("%B_%Y")

    # Create PDF

    pdf_file = f"reports/Expense_Report_{month_name}.pdf"

    pdf = canvas.Canvas(pdf_file, pagesize=A4)

    width, height = A4

    # ---------------- PAGE 1 ----------------

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(
        width / 2,
        height - 50,
        "EXPENSE TRACKER REPORT"
    )

    pdf.setFont("Helvetica", 12)
    pdf.drawString(
        50,
        height - 90,
        f"Month: {selected_month.strftime('%B %Y')}"
    )

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, height - 130, "Summary")

    pdf.setFont("Helvetica", 11)

    y = height - 155

    pdf.drawString(60, y, f"Total Expenses: Rs. {total:.2f}")
    y -= 20

    pdf.drawString(60, y, f"Number of Expenses: {count}")
    y -= 20

    pdf.drawString(60, y, f"Average Expense: Rs. {average:.2f}")
    y -= 20

    pdf.drawString(60, y, f"Highest Expense: Rs. {highest:.2f}")
    y -= 20

    pdf.drawString(60, y, f"Lowest Expense: Rs. {lowest:.2f}")

    # Category-wise expenses

    y -= 45

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Category-wise Expenses")

    y -= 25

    pdf.setFont("Helvetica", 11)

    for category, amount in category_total.items():
        pdf.drawString(
            60,
            y,
            f"{category}: Rs. {amount:.2f}"
        )
        y -= 20

    # Expense details

    y -= 20

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Expense Details")

    y -= 25

    pdf.setFont("Helvetica-Bold", 9)

    pdf.drawString(50, y, "Date")
    pdf.drawString(120, y, "Category")
    pdf.drawString(210, y, "Description")
    pdf.drawString(420, y, "Amount")

    y -= 15

    pdf.setFont("Helvetica", 9)

    for _, row in monthly_data.iterrows():

        if y < 50:
            add_page_footer(pdf, width)
            pdf.showPage()

            y = height - 50

            pdf.setFont("Helvetica-Bold", 9)

            pdf.drawString(50, y, "Date")
            pdf.drawString(120, y, "Category")
            pdf.drawString(210, y, "Description")
            pdf.drawString(420, y, "Amount")

            y -= 15

            pdf.setFont("Helvetica", 9)

        date = row["date"].strftime("%d-%m-%Y")

        pdf.drawString(50, y, date)
        pdf.drawString(120, y, str(row["category"])[:15])
        pdf.drawString(210, y, str(row["description"])[:30])
        pdf.drawString(420, y, f"Rs. {row['amount']:.2f}")

        y -= 18

    # Footer of current page

    add_page_footer(pdf, width)

    # ---------------- PAGE 2 ----------------

    pdf.showPage()

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(
        width / 2,
        height - 40,
        "Category-wise Expenses"
    )

    bar_file = f"graphs/category_expenses_{month_name}.png"

    if os.path.exists(bar_file):
        pdf.drawImage(
            bar_file,
            50,
            250,
            width=500,
            height=350
        )

    add_page_footer(pdf, width)

    # ---------------- PAGE 3 ----------------

    pdf.showPage()

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(
        width / 2,
        height - 40,
        "Expense Distribution"
    )

    pie_file = f"graphs/expense_distribution_{month_name}.png"

    if os.path.exists(pie_file):
        pdf.drawImage(
            pie_file,
            100,
            200,
            width=400,
            height=400
        )

    add_page_footer(pdf, width)

    # ---------------- PAGE 4 ----------------

    pdf.showPage()

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(
        width / 2,
        height - 40,
        "Daily Expense Trend"
    )

    line_file = f"graphs/daily_expense_trend_{month_name}.png"

    if os.path.exists(line_file):
        pdf.drawImage(
            line_file,
            50,
            280,
            width=500,
            height=300
        )

    add_page_footer(pdf, width)

    # Save PDF

    pdf.save()

    print("\nPDF CREATED SUCCESSFULLY!")
    print("PDF file:", pdf_file)
    print("========================================")

initialize_file()
while True:
    print("\n")

    print("=====================================")
    print("          EXPENSE TRACKER         ")

    show_summary()

    print("=====================================")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Edit Expense")
    print("5. Monthly Analysis")
    print("6. Generate Graphs")
    print("7. Export PDF")
    print("8. Exit")

    print("======================================")
    choice = input("Enter your choice (1-8): ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
         delete_expense()

    elif choice == "4":
        edit_expense()

    elif choice == "5":
        monthly_analysis()

    elif choice == "6":
       generate_graphs()

    elif choice == "7":
       export_pdf()

    elif choice == "8":
        print("\nThank you for using Expense Tracker!")
        break

    else:
        print("\nInvalid choice!")
        print("Please enter a number between 1 and 8.")