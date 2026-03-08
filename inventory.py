from tabulate import tabulate

# ========The beginning of the class==========
class Shoe:
    # Initialise attributes of shoes
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Returns the cost of the shoes.
    def get_cost(self):
        return self.cost

    # Returns the quantity of the shoes.
    def get_quantity(self):
        return self.quantity

    # This method returns a string representation of a class.
    def __str__(self):
        return (f"Country: {self.country}, Code: {self.code}, Product: {self.product},"
                f" Cost: {self.cost}, Quantity: {self.quantity}")

# =============Shoe list===========
# list to store a list of objects of shoes.
shoe_list = []

# ==========Functions outside the class==============
#Read lines from the file and insert objects to shoe_list
def read_shoes_data():
    try:
        # Open inventory.txt file
        with open("inventory.txt", "r") as file:
            # Skip header in the file
            next(file)

            # Create Shoe objects from each line in the file,
            # Then insert them to shoe_list
            for line in file:
                temp = line.strip().split(",")
                shoe_list.append(Shoe(temp[0], temp[1],
                                      temp[2], int(temp[3]),int(temp[4])))

    # try-except for any issues to catch if file doesn't exist or
    # the file including wrong indexes(if index is not 5 )
    except FileNotFoundError:
        print("Error : inventory.txt file is not available\n")
    except IndexError:
        print("Error: Please check your file as it is "
              "including different indexes\n")

#Create new Shoe object with getting details from user and
#append new object to shoe_list.
def capture_shoes():
    # Ask user below details to create new shoe
    try:
        new_country = input("Please enter country of the shoe: ")
        new_code = input("Please enter code of the shoe: ")
        new_product = input("Please enter the product of the shoe: ")
        new_cost = int(input("Please enter the cost of the shoe: "))
        new_quantity = int(input("Please enter the quantity of the shoe: "))

        # add new shoe to the shoe_list
        shoe_list.append(Shoe(new_country, new_code,
                              new_product, new_cost, new_quantity))

        #This is not in the task but I added new shoe to inventory file
        with open("inventory.txt", "a") as file:
            file.write(f"{new_country},{new_code},{new_product},{new_cost},{new_quantity}\n")
    except ValueError:
        print("Cost and Quantity must be a number!")


#iterate over the shoes list and show them in a table
def view_all():
    table = []

    # shoe_list keeps data as Shoe Objects. For table it doesn't work.
    # So, inserting each shoe details to table
    for shoe in shoe_list:
        table.append([shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity])

    # table format with tabulate to show shoe_list objects details
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    print(tabulate(table, headers=headers))

# find the shoe object with the lowest quantity and re-stock it
def re_stock():
    #find minimum quantity product and print
    min_shoe = min(shoe_list, key=lambda x: x.quantity)
    print(f"Minimum stock:\nProduct: {min_shoe.product}"
          f"\nQuantity: {min_shoe.quantity}\n")

    # ask user if he wants to add more stock
    user_input = (input(
        f"Would you like to re-stock {min_shoe.product}? (Yes/No): ")
                  .lower())

    #check if user answered with yes or no to continue
    while user_input != "yes" and user_input != "no":
        user_input = input(f"Would you like to re-stock {min_shoe.product}? (Yes/No) : ").lower()

    try:
        #Ask user how many more to add this product, print new quantity
        if user_input == "yes":
            re_st = int(input("Please enter new stock: "))
            min_shoe.quantity = min_shoe.quantity + re_st
            print(f"Updated quantity: {min_shoe.quantity}\n")


            # Read file to update new quantity for this product in the file
            with open("inventory.txt", "r") as f:
                lines = f.readlines()

            #find the product index in the file
            index_to_update = None
            for i, line in enumerate(lines):
                country, code, product, cost, quantity = line.strip().split(",")
                if product == min_shoe.product:
                    index_to_update = i
                    break

            # Update the line if found
            if index_to_update is not None:
                lines[index_to_update] = (
                    f"{min_shoe.country},{min_shoe.code},{min_shoe.product},"
                    f"{min_shoe.cost},{min_shoe.quantity}\n")

            # UPDATE LINE IN THE FILE
            with open("inventory.txt", "w") as file:
                file.writelines(lines)
                print(f"{min_shoe.product} quantity updated successfully.\n")
        else:
            print("You didn't want to update your stock\n")

    except ValueError:
        print("Stock must be a number!")


# Search shoe with shoe code and print.
def search_shoe():
    search_code = input("Please enter the shoe code to search: ").strip()
    found = False

    for shoe in shoe_list:
        if shoe.code == search_code:
            print(f"\nProduct details are like below \n{shoe}\n")
            found = True
            break

    if not found:
        print("Shoe not found.")

# calculate the total value for each item and print
def value_per_item():
    table = []
    for shoe in shoe_list:
        total = shoe.quantity * shoe.cost
        table.append([shoe.product, total])

    # table format with tabulate
    headers = ["Product", "Value"]
    print(tabulate(table, headers=headers))
    print("\n")


# Find highest quantity product and print this shoe as being for sale
def highest_qty():
    high_shoe = max(shoe_list, key=lambda x: x.quantity)
    print(f"This shoe is in sale :  {high_shoe.product}\n")


# ==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''
user_inp = True
read_shoes_data()

while user_inp:
    try:
        choice_shoe = input(
            "A : Add new shoe to your list.\n"
            "B : View all shoes table.\n"
            "C : Re-stock shoes.\n"
            "D : Search shoe with code.\n"
            "E : View value of items.\n"
            "F : Highest quantity item for sale.\n"
            "Q : Close the program.\n"
            "Please type one of the above options:").lower()
        print("")

        if choice_shoe == "a":
            capture_shoes()
        elif choice_shoe == "b":
            view_all()
        elif choice_shoe == "c":
            re_stock()
        elif choice_shoe == "d":
            search_shoe()
        elif choice_shoe == "e":
            value_per_item()
        elif choice_shoe == "f":
            highest_qty()
        elif choice_shoe == "q":
            print("Program closed. BYE!")
            user_inp = False

        else:
            print("Try again!\n")

    except ValueError:
        print("Try again.. You entered wrong answer..")
