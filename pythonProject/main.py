import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def read_data(file_path):
    return pd.read_excel(file_path)

def set_display_options():
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.max_rows', 10)
    pd.set_option('display.width', None)

def display_console_menu():
    print("Choose a chart:")
    print("1. Top 10 Countries by Total Quantity (Excluding UK)")
    print("2. Top 10 Profits per Product")
    print("3. Top 10 Products per Profit in Respective Country")
    print("4. Two Phenomena: Total Quantity and Quantity in the UK (Excluding UK)")
    print("5. Comparison of Total Profit (Excluding UK) and Profit in the UK")
    print("6. Top 10 Countries by Total CustomerID (Pie Chart)")
    print("7. Top 10 Products based on Total Quantity")
    print("8. Top 10 Countries by Total Quantity (Pie Chart)")
    print("9. Top 10 Countries by Total Profit (Pie Chart)")
    print("10. Bottom 10 Countries by Total Quantity")
    print("11. Exit")

def main():
    print("Data generation")
    data_path = r"C:\Users\teapa\Dropbox\pythonProject\retail.xlsx"
    df = read_data(data_path)
    set_display_options()

    while True:
        display_console_menu()
        choice = input("Enter the number of the chart you want to visualize (1-11): ")

        if choice == '1':
            # Chart 1
            top_countries = df[df['Country'] != 'United Kingdom'].groupby('Country')['Quantity'].sum().nlargest(10)
            top_countries.plot(kind='bar', figsize=(10, 6), color='skyblue')
            plt.title('Top 10 Countries by Total Quantity (Excluding UK)')
            plt.xlabel('Country')
            plt.ylabel('Total Quantity')
            plt.show()

        elif choice == '2':
            # Chart 2
            df['Profit'] = df['Quantity'] * df['UnitPrice']
            profit_per_product = df.groupby(['StockCode', 'Description'])['Profit'].sum().reset_index()
            new_table = pd.DataFrame({
                'StockCode': profit_per_product['StockCode'],
                'Description': profit_per_product['Description'],
                'Profit_Per_Product': profit_per_product['Profit']
            })
            new_table_sort = new_table.sort_values(by='Profit_Per_Product', ascending=False)
            top_table = new_table_sort.nlargest(10, 'Profit_Per_Product')

            plt.figure(figsize=(12, 6))
            plt.bar(top_table['Description'], top_table['Profit_Per_Product'], color='skyblue')
            plt.xlabel('Product Description')
            plt.ylabel('Profit per Product')
            plt.title('Top 10 Profits per Product')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

        elif choice == '3':
            # Chart 3
            df['Profit'] = df['Quantity'] * df['UnitPrice']
            profit_per_product = df.groupby(['StockCode', 'Description', 'Country'])['Profit'].sum().reset_index()
            new_table = pd.DataFrame({
                'StockCode': profit_per_product['StockCode'],
                'Description': profit_per_product['Description'],
                'Country': profit_per_product['Country'],
                'Profit_Per_Product': profit_per_product['Profit']
            })
            new_table_sort = new_table.sort_values(by='Profit_Per_Product', ascending=False)
            top_table = new_table_sort.groupby(['StockCode', 'Description']).head(1).nlargest(10, 'Profit_Per_Product')

            plt.figure(figsize=(12, 6))
            for index, row in top_table.iterrows():
                plt.bar(row['Description'] + ' - ' + row['Country'], row['Profit_Per_Product'], color='skyblue')

            plt.xlabel('Product Description - Country')
            plt.ylabel('Profit per Product')
            plt.title('Top 10 Products per Profit in Respective Country')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

        elif choice == '4':
            # Chart 4
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
            df['Month'] = df['InvoiceDate'].dt.to_period('M')
            total_quantity_all_countries = df[df['Country'] != 'UK'].groupby('Month')['Quantity'].sum()
            quantity_uk = df[df['Country'] == 'United Kingdom'].groupby('Month')['Quantity'].sum()

            fig, ax = plt.subplots(figsize=(12, 6))
            color = 'tab:red'
            ax.set_xlabel('Month')
            ax.set_ylabel('Quantity UK', color=color)
            ax.plot(quantity_uk.index.astype(str), quantity_uk.values, color=color, label='Quantity UK')
            ax.tick_params(axis='y', labelcolor=color)
            ax2 = ax.twinx()
            color = 'tab:blue'
            ax2.set_ylabel('Total Quantity All Countries (Excluding UK)', color=color)
            ax2.plot(total_quantity_all_countries.index.astype(str), total_quantity_all_countries.values,
                     color=color, label='Total Quantity All Countries (Excluding UK)')
            ax2.tick_params(axis='y', labelcolor=color)
            ax2.legend(loc='upper right')
            ax.legend(loc='upper left')
            plt.title('Two Phenomena: Total Quantity and Quantity in the UK (Excluding UK)')
            plt.show()

        elif choice == '5':
            # Chart 5
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
            df['Month'] = df['InvoiceDate'].dt.to_period('M')
            df['TotalProfit'] = df['Quantity'] * df['UnitPrice']
            total_profit_all_countries_except_uk = df[df['Country'] != 'United Kingdom'].groupby('Month')['TotalProfit'].sum()
            profit_uk = df[df['Country'] == 'United Kingdom'].groupby('Month')['TotalProfit'].sum()

            fig, ax1 = plt.subplots(figsize=(12, 6))
            color = 'tab:red'
            ax1.set_xlabel('Month')
            ax1.set_ylabel('Total Profit All Countries (Excluding UK)', color=color)
            ax1.plot(total_profit_all_countries_except_uk.index.astype(str), total_profit_all_countries_except_uk.values,
                     color=color, label='All Countries (Excluding UK)')
            ax1.plot(profit_uk.index.astype(str), profit_uk.values, color='orange', linestyle='dashed',
                     label='Profit UK')
            ax1.tick_params(axis='y', labelcolor=color)
            plt.legend(loc='upper left', bbox_to_anchor=(0.75, 1.0))
            plt.title('Comparison of Total Profit (Excluding UK) and Profit in the UK')
            plt.show()

        elif choice == '6':
            # Chart 6
            customer_id_by_country = df.groupby('Country')['CustomerID'].nunique()
            top_10_countries = customer_id_by_country.nlargest(10)
            percentages = (top_10_countries / top_10_countries.sum()) * 100

            fig, ax = plt.subplots(figsize=(10, 10))
            wedges, texts, autotexts = ax.pie(top_10_countries, labels=None, autopct='', startangle=90,
                                              textprops=dict(color="w"))

            legend_labels = [f'{country}: {percent:.1f}%' for country, percent in
                             zip(top_10_countries.index, percentages)]
            ax.legend(wedges, legend_labels, title='Countries', loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

            ax.axis('equal')
            plt.title('Top 10 Countries by Total CustomerID')
            plt.show()

        elif choice == '7':
            # Chart 7
            quantity_per_product = df.groupby(['StockCode', 'Description'])['Quantity'].sum().reset_index()
            new_table_sort_quantity = quantity_per_product.sort_values(by='Quantity', ascending=False)
            top_table_quantity = new_table_sort_quantity.head(10)

            plt.figure(figsize=(12, 6))
            plt.bar(top_table_quantity['Description'], top_table_quantity['Quantity'], color='skyblue')
            plt.xlabel('Product Description')
            plt.ylabel('Total Quantity')
            plt.title('Top 10 Products based on Total Quantity')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

        elif choice == '8':
            # Chart 8
            total_quantity_by_country = df.groupby('Country')['Quantity'].sum()
            top_10_countries_quantity = total_quantity_by_country.nlargest(10)
            percentages = (top_10_countries_quantity / top_10_countries_quantity.sum()) * 100

            fig, ax = plt.subplots(figsize=(10, 10))
            wedges, texts, autotexts = ax.pie(top_10_countries_quantity, labels=None, autopct='', startangle=90,
                                              textprops=dict(color="w"))

            legend_labels = [f'{country}: {percent:.1f}%' for country, percent in
                             zip(top_10_countries_quantity.index, percentages)]
            ax.legend(wedges, legend_labels, title='Countries', loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

            ax.axis('equal')
            plt.title('Top 10 Countries by Total Quantity')
            plt.show()

        elif choice == '9':
            # Chart 9
            df['TotalProfit'] = df['Quantity'] * df['UnitPrice']
            total_profit_by_country_stock = df.groupby(['Country', 'StockCode'])['TotalProfit'].sum()
            top_10_countries_profit = total_profit_by_country_stock.groupby('Country').sum().nlargest(10)
            percentages = (top_10_countries_profit / top_10_countries_profit.sum()) * 100

            fig, ax = plt.subplots(figsize=(10, 10))
            wedges, texts, autotexts = ax.pie(top_10_countries_profit, labels=None, autopct='', startangle=90,
                                              textprops=dict(color="w"))

            legend_labels = [f'{country}: {percent:.1f}%' for country, percent in
                             zip(top_10_countries_profit.index, percentages)]
            ax.legend(wedges, legend_labels, title='Countries', loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

            ax.axis('equal')
            plt.title('Top 10 Countries by Total Profit')
            plt.show()

        elif choice == '10':
            # Chart 10
            total_quantity_by_country = df.groupby('Country')['Quantity'].sum()
            bottom_10_countries_quantity = total_quantity_by_country.nsmallest(10)

            fig, ax = plt.subplots(figsize=(12, 8))
            bottom_10_countries_quantity.plot(kind='bar', ax=ax, color='skyblue')

            ax.set_xlabel('Country')
            ax.set_ylabel('Total Quantity')
            plt.title('Bottom 10 Countries by Total Quantity')
            plt.xticks(rotation=45, ha='right')

            plt.show()

        elif choice == '11':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 11.")

if __name__ == "__main__":
    main()
