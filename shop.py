import csv
from tabulate import tabulate


class Product:
    def _init_(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

class Inventory:
    def _init_(self):
        self.products = {
            101: Product(101, 'Soap', 20, 50),
            102: Product(102, 'Shampoo', 120, 30),
            103: Product(103, 'Toothpaste', 60, 40),
            104: Product(104, 'Rice', 500, 20),
            105: Product(105, 'Sugar', 45, 25)
        }

    def display_inventory(self):
        headers = ["Product ID", "Name", "Price", "Quantity"]
        table = [[p.product_id, p.name, p.price, p.quantity] for p in self.products.values()]
        print(tabulate(table, headers, tablefmt='grid'))

    def add_product(self, product):
        if product.product_id in self.products:
            print("Product ID already exists. Updating quantity instead.")
            self.products[product.product_id].quantity += product.quantity
        else:
            self.products[product.product_id] = product
        print(f"{product.name} added/updated successfully.")

    def update_product(self, product_id, quantity_sold):
        if product_id in self.products:
            product = self.products[product_id]
            if product.quantity >= quantity_sold:
                product.quantity -= quantity_sold
                return True
            else:
                print(f"Insufficient stock for {product.name}.")
                return False
        else:
            print(f"Product with ID {product_id} not found.")
            return False


class Sale:
    def _init_(self, sale_id):
        self.sale_id = sale_id
        self.products_sold = []

    def add_product(self, product_id, name, quantity, total_price):
        self.products_sold.append({
            'product_id': product_id,
            'product_name': name,
            'quantity_sold': quantity,
            'total_price': total_price
        })


class SalesManager:
    def _init_(self):
        self.sales = []

    def record_sale(self, sale):
        self.sales.append(sale)
        print(f"Sale {sale.sale_id} recorded successfully.")

    def display_sales(self):
        headers = ["Sale ID", "Product ID", "Name", "Quantity Sold", "Total Price"]
        table = []
        for sale in self.sales:
            for product in sale.products_sold:
                table.append([
                    sale.sale_id,
                    product['product_id'],
                    product['product_name'],
                    product['quantity_sold'],
                    product['total_price']
                ])
        print(tabulate(table, headers, tablefmt='grid'))


class ShopSystem:
    def _init_(self):
        self.inventory = Inventory()
        self.sales_manager = SalesManager()

    def run(self):
        while True:
            print("\n--- Shop Management System ---")
            print("1. View Inventory")
            print("2. Add Product to Inventory")
            print("3. Record a Sale")
            print("4. View Sales Report")
            print("5. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                self.inventory.display_inventory()
            elif choice == '2':
                self.add_product()
            elif choice == '3':
                self.record_sale()
            elif choice == '4':
                self.sales_manager.display_sales()
            elif choice == '5':
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_product(self):
        try:
            product_id = int(input("Enter product ID: "))
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            self.inventory.add_product(Product(product_id, name, price, quantity))
        except ValueError:
            print("Invalid input. Please enter valid details.")

    def record_sale(self):
        try:
            sale_id = len(self.sales_manager.sales) + 1
            sale = Sale(sale_id)

            while True:
                product_id = int(input("Enter product ID (or 0 to finish): "))
                if product_id == 0:
                    break

                quantity = int(input("Enter quantity sold: "))
                if product_id in self.inventory.products:
                    product = self.inventory.products[product_id]
                    if self.inventory.update_product(product_id, quantity):
                        total_price = product.price * quantity
                        sale.add_product(product_id, product.name, quantity, total_price)
                        print(f"{product.name} added to sale.")
                    else:
                        print(f"Failed to add {product.name} to sale.")
                else:
                    print("Invalid product ID. Try again.")

            if sale.products_sold:
                self.sales_manager.record_sale(sale)
        except ValueError:
            print("Invalid input. Please try again.")


if _name_ == '_main_':
    system = ShopSystem()
    system.run()
