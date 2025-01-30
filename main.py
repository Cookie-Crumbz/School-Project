import os
import sys
from datetime import datetime, timedelta
import hashlib
from app_entities import Customer, Package
from ORM import RecordHandler
from SQLHelper import SQLHelper

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input_with_prompt(prompt, validator=None, error_message="Invalid input."):
    while True:
        value = input(prompt).strip()
        if validator is None or validator(value):
            return value
        print(error_message)

def get_user_credentials():
    email = get_input_with_prompt("Enter your email: ", lambda v: '@' in v, "Invalid email format.")
    password = get_input_with_prompt("Enter your password: ")
    return email, hash_password(password)

def fetch_or_sign_up_customer(record_handler, email, hashed_password):
    customers, _ = record_handler.fetch_records(Customer, email, column='email')
    
    if customers:
        customer = customers[0]
        if customer.password == hashed_password:
            return customer
        else:
            print("Incorrect password. Please try again.")
            sys.exit()
            
    else:
        print("No customer found with this email. Please sign up.")
        name = get_input_with_prompt("Enter Customer Name: ")
        phone = get_input_with_prompt("Enter Customer Phone: ")
        address = get_input_with_prompt("Enter Customer Address: ")
        records, _ = record_handler.fetch_all_records(Customer)
        customer_id = max((getattr(record, Customer.get_primary_key()) for record in records), default=0) + 1
        new_customer = Customer(
            customer_id=customer_id,
            name=name,
            email=email,
            phone=phone,
            address=address,
            password=hashed_password
        )
        record_handler.save_record(new_customer)
        print("Customer signed up successfully.")
        return new_customer

def fetch_user_packages(record_handler, customer):
    return record_handler.fetch_records(Package, customer.customer_id, column='customer_id')[0]

def display_home_page(packages):
    print("\nYour Packages:")
    for pkg in packages:
        print(f"Package ID: {pkg.package_id} | Status: {pkg.status} | Expected Delivery: {pkg.expected_delivery_date}")
        
    print("\nCommands:")
    print("1. Deliver - Create a new package for delivery")
    print("2. Details <package_id> - View details of a package")
    print("3. Delete <package_id> - Delete a package")
    print("4. Exit - Exit the program")

def get_package_details():
    while True:
        try:
            source = get_input_with_prompt("Enter Pick-Up Location: ", lambda v: v, "Pick-Up Location cannot be empty.")
            destination = get_input_with_prompt("Enter Destination: ", lambda v: v, "Destination cannot be empty.")
            weight = float(get_input_with_prompt("Enter Weight in kg: ", lambda v: v.isdigit() and float(v) > 0, "Weight must be a positive number."))
            pick_up_date_str = get_input_with_prompt("Enter Pick-Up Date and Time (DD-MM-YYYY HH:MM): ")
            pick_up_date = datetime.strptime(pick_up_date_str, "%d-%m-%Y %H:%M")
            
            print("\nDelivery Options:")
            print("1. Economy: Rs.200/kg, delivery in 10 hours")
            print("2. Express: Rs.300/kg, delivery in 5 hours")
            print("3. Nitro Express: Rs.400/kg, delivery in 1 hour")
            
            option_map = {"1": "economy", "2": "express", "3": "nitro express"}
            option = get_input_with_prompt("Choose an option (1/2/3): ", lambda v: v in option_map, "Invalid option.")
            delivery_option = option_map[option]
            
            cost_multiplier = {"economy": 200, "express": 300, "nitro express": 400}[delivery_option]
            delivery_time = {"economy": 10, "express": 5, "nitro express": 1}[delivery_option]
            cost = weight * cost_multiplier
            expected_delivery_date = pick_up_date + timedelta(hours=delivery_time)
            
            return {
                "source": source,
                "destination": destination,
                "current_location": source,
                "status": "Waiting For Pickup",
                "weight": weight,
                "pick_up_date": pick_up_date,
                "delivery_option": delivery_option,
                "expected_delivery_date": expected_delivery_date,
                "cost": cost
            }
        
        except ValueError as e:
            print(f"Error: {e}")
            print("Please re-enter the details.")

def confirm_package_details(details):
    while True:
        print("\nPackage Summary:")
        print(f"Pick-Up Location: {details['source']}")
        print(f"Destination: {details['destination']}")
        print(f"Weight: {details['weight']} kg")
        print(f"Pick-Up Date: {details['pick_up_date'].strftime('%d-%m-%Y %H:%M')}")
        print(f"Delivery Option: {details['delivery_option']}")
        print(f"Expected Delivery Date: {details['expected_delivery_date'].strftime('%d-%m-%Y %H:%M')}")
        print(f"Cost: Rs. {details['cost']:.2f}")
        
        confirmation = get_input_with_prompt("\nDo you want to save this package? (y/n/edit): ", lambda v: v in ['y', 'n', 'edit'], "Invalid input. Enter 'y', 'n', or 'edit'.")
        if confirmation == 'y':
            return True
        elif confirmation == 'n':
            return False
        elif confirmation == 'edit':
            details = get_package_details()

def save_package(record_handler, customer_id, details):
    if confirm_package_details(details):
        records, _ = record_handler.fetch_all_records(Package)
        package_id = max((getattr(record, Package.get_primary_key()) for record in records), default=0) + 1
        package = Package(
            package_id=package_id,
            customer_id=customer_id,
            **details
        )
        
        record_handler.save_record(package)
        print("Package added successfully.")
        
    else:
        print("Package creation canceled.")

def view_package_details(record_handler, package_id):
    packages, _ = record_handler.fetch_records(Package, package_id)
    if packages:
        pkg = packages[0]
        print(f"Package ID: {package_id}")
        print(f"Pick-Up Location: {pkg.source}")
        print(f"Destination: {pkg.destination}")
        print(f"Current Location: {pkg.current_location}")
        print(f"Status: {pkg.status}")
        print(f"Weight: {pkg.weight} kg")
        print(f"Pick-Up Date: {pkg.pick_up_date}")
        print(f"Delivery Option: {pkg.delivery_option}")
        print(f"Expected Delivery Date: {pkg.expected_delivery_date}")
        print(f"Cost: Rs. {pkg.cost:.2f}")
    else:
        print("Package not found.")

def delete_package(record_handler, package_id):
    packages, _ = record_handler.fetch_records(Package, package_id)
    if packages:
        record_handler.delete_record(packages[0])
        print(f"Package ID {package_id} has been deleted successfully.")
    else:
        print("Package not found.")

def main():
    sql_helper = SQLHelper('127.0.0.1', 'courier_service', 'dhanvin', '123pass', debug=True)
    record_handler = RecordHandler(sql_helper)
    email, hashed_password = get_user_credentials()
    customer = fetch_or_sign_up_customer(record_handler, email, hashed_password)
    
    while True:
        clear_console()
        packages = fetch_user_packages(record_handler, customer)
        display_home_page(packages)
        command = input("Enter command: ").strip().lower().split()
        clear_console()
        
        try:
            if command[0] == 'deliver':
                details = get_package_details()
                save_package(record_handler, customer.customer_id, details)
            elif command[0] == 'details' and len(command) > 1 and command[1].isdigit():
                view_package_details(record_handler, int(command[1]))
            elif command[0] == 'delete' and len(command) > 1 and command[1].isdigit():
                delete_package(record_handler, int(command[1]))
            elif command[0] == 'exit':
                print("Exiting...")
                sql_helper.disconnect()
                sys.exit()
            else:
                print("Invalid command. Please try again.")
                
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
