''' 
Dental clinic - python workshop project by Leimar Soto v1.0 - 2026 

A simple CLI application to manage clients, services and payments.

Made with love and care for learning Python programming.
'''



from client import Client
import clinic

import re
from datetime import datetime



# Try to load saved clients from JSON at startup
DATA_FILE = "clients.json"
clients_list: list[Client] = clinic.load_clients(DATA_FILE)



# Simple CLI for the clinic. Functions below handle input and display.


def select_option(message: str, options: list):
    # Show numbered options and return chosen value
    while True:
        print(message)
        for i, op in enumerate(options):
            print(f"  {i + 1}. {op}")
        selection = input("Option: ").strip()
        if selection.isdigit() and 1 <= int(selection) <= len(options):
            return options[int(selection) - 1]
        print("Invalid option, try again.")



def read_id():
    # Read ID: digits only, max 20 characters
    while True:
        id_number = input("ID number (digits only, max 20): ").strip()
        if id_number == "":
            print("ID cannot be empty.")
            continue
        if not id_number.isdigit():
            print("ID must contain digits only.")
            continue
        if len(id_number) > 20:
            print("ID too long (max 20 digits).")
            continue
        return id_number



def read_name():
    # Read and validate full name: letters, spaces, hyphen and apostrophe
    while True:
        name = input("Full name (letters and spaces only): ").strip()
        if name == "":
            print("Name cannot be empty.")
            continue
        if len(name) < 2:
            print("Name too short.")
            continue
        if len(name) > 100:
            print("Name too long (max 100 chars).")
            continue
        valid = True
        for ch in name:
            if not (ch.isalpha() or ch in " -'"):
                valid = False
                break
        if not valid:
            print("Name contains invalid characters.")
            continue
        return name



def read_phone():
    # Read and validate phone number (simple rule)
    pattern = re.compile(r"^\+?[0-9\-\s]{7,}$")
    while True:
        phone = input("Phone: ").strip()
        if phone == "":
            print("Phone cannot be empty.")
            continue
        if not pattern.match(phone):
            print("Invalid phone format. Use digits, spaces or '-' (min 7 chars).")
            continue
        return phone



def read_quantity(service_type: str):
    # Return quantity: some services always use 1
    if service_type in ["Cleaning", "Diagnosis"]:
        return 1
    while True:
        entry = input("Quantity (integer > 0): ").strip()
        if entry.isdigit() and int(entry) > 0:
            return int(entry)
        print("Enter an integer greater than zero.")



def read_date():
    # Read and validate date in DD/MM/YYYY format
    while True:
        date = input("Appointment date (DD/MM/YYYY): ").strip()
        if date == "":
            print("Date cannot be empty.")
            continue
        try:
            datetime.strptime(date, "%d/%m/%Y")
            return date
        except ValueError:
            print("Invalid date. Use DD/MM/YYYY.")



def register_client():
    # Create client from user input and add to list
    print("\nRegister new client")
    c = Client()
    # Ensure unique ID
    while True:
        candidate_id = read_id()
        if any(x.id_number == candidate_id for x in clients_list):
            print("ID already exists. Enter a different ID.")
            continue
        c.id_number = candidate_id
        break
    c.name        = read_name()
    c.phone      = read_phone()
    c.client_type  = select_option("Client type:", clinic.CLIENT_TYPES)
    c.service_type = select_option("Service type:", clinic.SERVICE_TYPES)
    c.quantity      = read_quantity(c.service_type)
    c.priority     = select_option("Priority:", clinic.PRIORITIES)
    c.appointment_date    = read_date()
    clinic.calculate_values(c)
    clients_list.append(c)
    # auto-save after adding
    try:
        clinic.save_clients(DATA_FILE, clients_list)
        saved_msg = " Data saved."
    except Exception:
        saved_msg = " (warning: could not save data)."
    print(f"\nClient registered. Total to pay: ${c.total_fee:,.0f}.{saved_msg}")



def show_statistics():
    # Print simple clinic statistics
    if len(clients_list) == 0:
        print("\nNo clients registered.")
        return
    print(f"\nClinic statistics")
    print(f"  Total clients      : {clinic.total_clients(clients_list)}")
    print(f"  Total revenue      : ${clinic.total_revenue(clients_list):,.0f}")
    print(f"  Extraction clients : {clinic.extraction_clients(clients_list)}")



def show_sorted_clients():
    # Show clients sorted by total value
    if len(clients_list) == 0:
        print("\nNo clients registered.")
        return
    clinic.sort_by_total_fee(clients_list)
    print("\nClients sorted by total (high to low):")
    print(f"  {'ID':<12} {'Name':<25} {'Client Type':<12} {'Service':<12} {'Total':>12}")
    print("  " + "-" * 75)
    for c in clients_list:
        print(f"  {c.id_number:<12} {c.name:<25} {c.client_type:<12} {c.service_type:<12} ${c.total_fee:>10,.0f}")



def find_client():
    # Search for a client by ID and print details
    if len(clients_list) == 0:
        print("\nNo clients registered.")
        return
    id_number = input("\nEnter ID to search: ").strip()
    result = clinic.binary_search_by_id(clients_list, id_number)
    if result is None:
        print("Client not found.")
    else:
        print("\nClient found:")
        print(f"  ID           : {result.id_number}")
        print(f"  Name         : {result.name}")
        print(f"  Phone        : {result.phone}")
        print(f"  Client type  : {result.client_type}")
        print(f"  Service      : {result.service_type}")
        print(f"  Quantity     : {result.quantity}")
        print(f"  Priority     : {result.priority}")
        print(f"  Date         : {result.appointment_date}")
        print(f"  Visit fee    : ${result.visit_fee:,.0f}")
        print(f"  Service fee  : ${result.service_fee:,.0f}")
        print(f"  Total to pay : ${result.total_fee:,.0f}")



def main():
    # Main menu loop
    running = True
    while running:
        print("\n" + "=" * 40)
        print("\n| Dental Clinic - ¡Hi Dr! What would you like to do?")
        print("-" * 30)
        print("| 1. Register client")
        print("| 2. View statistics")
        print("| 3. View clients sorted by total")
        print("| 4. Search client by ID")
        print("| 5. Exit")
        print("\n" + "=" * 40)
        option = input("Select an option: ").strip()

        if option == "1":
            register_client()
        elif option == "2":
            show_statistics()
        elif option == "3":
            show_sorted_clients()
        elif option == "4":
            find_client()
        elif option == "5":
            print("Goodbye!")
            running = False
        else:
            print("Invalid option.")





if __name__ == "__main__":
    main()
