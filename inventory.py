from csv import DictReader, DictWriter
from msvcrt import getwch
from os import system
from time import sleep


class Product:
    def __init__(self, id: str, name: str, desc: str, price: str, quantity: str) -> None:
        self.id = id
        self.name = name
        self.desc = desc
        self.price = price
        self.quantity = quantity


    def __str__(self) -> str:           
        return f" #{self.id} | {self.name} | {self.desc} | {self.price} | {self.quantity}"  


class Inventory:
    def __init__(self, products=None, source_file=str) -> None: 
        if products is None:
            products = []
        self.products = products
        self.source_file = source_file

    
    def check_inventory(self):
        system("cls")
        if not len(self.products):
            print("Inventory is empty")

        for index, product in enumerate(self.products): 
            print(f"{index + 1}.) {product}")


    def get_product(self, id): 
        for product in self.products: 
            if product.id == int(id):
                return product
        return None


    def create_unquie_id(self) -> int : 
        unquie_id = max([product.id for product in self.products]) + 1
        return unquie_id


    def remove_product(self, id): 
        # go though each product item and return the one with provided id
        removed_product = self.get_product(id)
        self.products.remove(removed_product)


    def add_product(self, name, desc, price, quantity):
        new_id = self.create_unquie_id()
        self.products.append(Product(new_id, name, desc, price, quantity))
        self.save_to_inventory()


    def edit_product(self, id, name, desc, price, quantity): 
        product_to_edit = None

        for product in self.products:
            if product.id == id:
                product_to_edit = product
                break
        
        product_to_edit.name = name
        product_to_edit.desc = desc
        product_to_edit.price = price
        product_to_edit.quantity = quantity


    def save_to_inventory(self):
        with open(self.source_file, mode="w") as csvfile:
            fieldnames = ["id", "name", "desc", "price", "quantity"]
            writer = DictWriter(csvfile, fieldnames)

            writer.writeheader()
            for product in self.products:
                writer.writerow({
                    "id": product.id,
                    "name": product.name,
                    "desc": product.desc,
                    "price": product.price,
                    "quantity": product.quantity
                })


    @staticmethod
    def load_inventory(filename): 
        products = []
    
        with open(filename, 'r') as file:
            reader = DictReader(file)

            for row in reader:
                id = int(row['id'])
                name = row['name']
                desc = row['desc']

                try:
                    price = float(row['price'])
                except: 
                    price = "[INVALID PRICE]"

                try:
                    quantity = int(row['quantity'])
                except: 
                    quantity = "[INVALID QUANTITY]"
                
                products.append(Product(id, name, desc, price, quantity))

        return products


def getwch_input(label):
    print(label)
    user_input = getwch()
    return user_input


def validate_int(input): 
    try: 
        return int(input)
    except ValueError: 
        return False


system("cls")

products_file_path = "products.csv"
loaded_products = Inventory.load_inventory(products_file_path)

inventory = Inventory(loaded_products, products_file_path) # initialize inventory with loaded products
message = ""
ID_REQUIRED_COMMANDS = ["R", "E"]


# main program loop
while True:
    # view inventory and eventual messages (like warnings, errors)
    inventory.check_inventory()
    print(message + "\n" if len(message) else "")

    user_command= getwch_input("(A)dd | (R)emove | (E)dit a product: ").upper()  # prompt the user for a command

    if user_command in ID_REQUIRED_COMMANDS:
        product_id = validate_int(getwch_input("Enter product ID: "))

        if not product_id or not inventory.get_product(product_id):  
            message = "Not valid input"
            continue
        
        # remove product
        elif user_command == "R": 
            inventory.remove_product(product_id)
        

        # edit product
        elif user_command == "E":
            placeholder = inventory.get_product(product_id)

            name = input(f"New product name: ({placeholder.name}): ")
            desc = input("New product description: ")
            price = input("New product price: ")
            quantity = input("New product quantity: ")

            inventory.edit_product(product_id, name, desc, price, quantity)

        inventory.save_to_inventory()
            

    # add product
    elif user_command == "A": 
        system("cls")

        name  = input("Product name: ")
        desc  = input("Product desc: ")
        price = input("Product price: ")
        quantity = input("Product quantity: ")

        inventory.add_product(name, desc, price, quantity)









    



