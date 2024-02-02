import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate
print("Data generation")
df = pd.read_excel(r"C:\Users\teapa\Dropbox\pythonProject\retail.xlsx")
"""MAKING EXISTING COLUMNS VISIBLE"""
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', None)

print("----------------------------------------------")
print("PRODUCT SOLD THE MOST")
print("----------------------------------------------")
most_sold_product_id = df.groupby('StockCode')['Quantity'].sum().idxmax()
print("The productID sold the most is:", most_sold_product_id)

#Get the corresponding description for the most sold product
most_sold_product_description = df.loc[df['StockCode'] == most_sold_product_id, 'Description'].iloc[0]
print("Its description is:", most_sold_product_description)
print()

print("--------------------------------------------------")
print("CREATING NEW TABLE WITH MOST AND LEAST SOLD PRODUCTS")
print("--------------------------------------------------")

# Group by product and sum the sold quantities
sold_quantity_per_product = df.groupby(['StockCode', 'Description'])['Quantity'].sum().reset_index()

# Create a new DataFrame with stock code, product description, and total sold quantity
new_sold_table = pd.DataFrame({
    'StockCode': sold_quantity_per_product['StockCode'],
    'Description': sold_quantity_per_product['Description'],
    'Total_Sold_Quantity': sold_quantity_per_product['Quantity']
})

# Sort the table by total sold quantity in descending order
new_sold_table_sort = new_sold_table.sort_values(by='Total_Sold_Quantity', ascending=False)

# Display the new table
print(new_sold_table_sort.head())  # Display the top 5 most sold products
print(new_sold_table_sort.tail())  # Display the bottom 5 least sold products
print()

'''Calculate the top 10 countries with the highest total quantity'''
#top_countries = df.groupby('Country')['Quantity'].sum().reset_index().nlargest(10, 'Quantity')
#print(tabulate(top_countries, headers=['Country', 'Total Quantity'], tablefmt='pretty'))
#print()



