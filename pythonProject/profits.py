import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate
print("*Data generation*")
df = pd.read_excel(r"C:\Users\teapa\Dropbox\pythonProject\retail.xlsx")

"""MAKING EXISTING COLUMNS VISIBLE"""
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', None)

"""WHICH PRODUCT HAS MADE THE HIGHEST PROFIT"""
print("------------------------------------------")
print("WHICH PRODUCT ID HAS MADE THE HIGHEST PROFIT")
print("------------------------------------------")
#Group by 'ProductID' and calculate total sales for each product
df['TotalSales'] = df['Quantity'] * df['UnitPrice']
highest_profit_product = df.groupby('StockCode')['TotalSales'].sum().idxmax()

print("The productID with the highest profit is:", highest_profit_product)
print()

"""CALCULATING THE MOST PROFITABLE PRODUCT"""
# Assuming df is your DataFrame containing the provided data
# Create a new column for profit
df['Profit'] = df['Quantity'] * df['UnitPrice']

#CALCULATING PROFIT PRO EACH PRODUCT IN WHOLE
profit_per_product = df.groupby('StockCode')['Profit'].sum().reset_index()
print(profit_per_product)

# Find the most profitable product
most_profitable_product = profit_per_product.loc[profit_per_product['Profit'].idxmax()]

print("----------------------------")
print("Most Profitable Product:")
print("----------------------------")
print(most_profitable_product)
print()
print("----------------------------------------------")
""" CREATING NEW TABLE WITH PROFITS OF ALL PRODUCTS"""
print("CREATING NEW TABLE WITH PROFITS OF ALL PRODUCTS")
print("----------------------------------------------")
# Assuming df is your DataFrame containing the provided data
# Create a new column for profit
df['Profit'] = df['Quantity'] * df['UnitPrice']

# Group by product and sum the profits
profit_per_product = df.groupby(['StockCode', 'Description'])['Profit'].sum().reset_index()

# Create a new DataFrame with stock code, product description, and profit_per_product
new_table = pd.DataFrame({
    'StockCode': profit_per_product['StockCode'],
    'Description': profit_per_product['Description'],
    'Profit_Per_Product': profit_per_product['Profit']
})
new_table_sort = new_table.sort_values(by='Profit_Per_Product', ascending=False)

# Display the new table
print(new_table_sort)

