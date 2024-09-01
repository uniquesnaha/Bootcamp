from alerts import *


def main_menu():
    while True:
        print("\nMenu:")
        print("1. Add Transaction")
        print("2. Check Available Budget")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            user_id = int(input("Enter User ID: "))
            budget_id=int(input("Enter Budget ID: "))
            amount = float(input("Enter Transaction Amount: "))
            add_transaction(user_id,budget_id,amount)
        
        elif choice == '2':
            user_id =int(input("Enter User ID: "))
            budget_id=int(input("Enter Budget ID: "))
            check_available_budget(user_id,budget_id)
        
        elif choice == '3':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main_menu()