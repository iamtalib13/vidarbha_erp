import frappe

def execute(filters=None):
    filters = filters or {}

    # Table Columns
    columns = [
        {"label": "Transaction ID", "fieldname": "name", "fieldtype": "Link", "options": "Transaction", "width": 120},  # ✅ Updated Doctype
        {"label": "Transaction Type", "fieldname": "transaction_type", "fieldtype": "Data", "width": 120},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 100},
		{"label": "category", "fieldname": "category", "fieldtype": "Data", "width": 100},  # ✅ Added category field
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},  # ✅ Fixed fieldname error
        {"label": "Description", "fieldname": "description", "fieldtype": "Data", "width": 200}
    ]

    # Fetch all records from the 'Transaction' doctype
    data = frappe.db.sql("""
        SELECT name, transaction_type, amount, date, category, description
        FROM `tabTransaction`
        WHERE docstatus < 2
        ORDER BY date DESC
    """, as_dict=True)

    # Calculate Total Income and Total Expense
    total_income = sum(d['amount'] for d in data if d['transaction_type'] == 'Income')
    total_expense = sum(d['amount'] for d in data if d['transaction_type'] == 'Expense')
    net_profit_loss = total_income - total_expense

    # Determine Profit or Loss description
    if net_profit_loss > 0:
        profit_loss_desc = "Profit"
    elif net_profit_loss < 0:
        profit_loss_desc = "Loss"
    else:
        profit_loss_desc = "Break-Even"

    # Append Profit & Loss summary row at the end of table
    data.append({
        "name": "P&L Summary",
        "transaction_type": "Net Profit / Loss",
        "amount": net_profit_loss,
        "date": "",
        "description": f"{profit_loss_desc}"
    })

    # Define Pie Chart (Income vs Expense)
    chart = {
        "data": {
            "labels": ["Income", "Expense"],
            "datasets": [{
                "name": "Amount",
                "values": [total_income, total_expense]
            }]
        },
        "type": "pie",  # Chart type: pie / bar / line / heatmap
        "colors": ["#36a64f", "#e74c3c"]  # Green: Income, Red: Expense
    }

    return columns, data, None, chart
