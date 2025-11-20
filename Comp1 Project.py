def print_welcome_message():

    print("=" * 40)
    print("              CALCULATOR              ")
    print("=" * 40)
    print("This calculator can perform:")
    print(" - Addition")
    print(" - Subtraction")
    print(" - Multiplication")
    print(" - Division")
    print("-" * 40)


def print_menu():

    print("\nPlease choose an operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Exit")


def get_user_choice():
    """
    Ask the user to enter a menu choice and return it as an integer.
    Handles invalid input and keeps asking until a valid choice is entered.
    """
    while True:
        choice = input("Enter your choice (1-5): ")

        if choice.isdigit():
            choice_int = int(choice)
            if 1 <= choice_int <= 5:
                return choice_int
            else:
                print("Invalid choice. Please enter a number from 1 to 5.")
        else:
            print("Invalid input. Please enter a numeric value.")


def get_number(prompt):
    """
    Asks the user to enter a number and return it as a float.
    Handles invalid numeric input using a loop.
    """
    while True:
        value = input(prompt)

        try:
            number = float(value)
            return number
        except ValueError:
            print("That is not a valid number. Please try again.")


def add(a, b):
    """
    Return the sum of a and b.
    """
    return a + b


def subtract(a, b):
    """
    Return the result of a - b.
    """
    return a - b


def multiply(a, b):
    """
    Return the product of a and b.
    """
    return a * b


def divide(a, b):
    """
    Return the result of a / b.
    Handles division by zero by raising a ValueError.
    """
    if b == 0:
        raise ValueError("Error: Division by zero is not allowed.")

def perform_operation(choice):
    """
    Based on the user's choice, ask for numbers and perform the operation.
    Prints the result or any error messages.
    """
    if choice == 5:
        return

    print("\nEnter the numbers for the operation:")

    num1 = get_number("First number: ")
    num2 = get_number("Second number: ")

    result = None
    symbol = ""

    try:
        if choice == 1:
            result = add(num1, num2)
            symbol = "+"
        elif choice == 2:
            result = subtract(num1, num2)
            symbol = "-"
        elif choice == 3:
            result = multiply(num1, num2)
            symbol = "*"
        elif choice == 4:
            result = divide(num1, num2)
            symbol = "/"

        print(f"\nResult: {num1} {symbol} {num2} = {result}")

    except ValueError as error:
        print(error)


def ask_to_continue():
    """
    Ask the user if they want to perform another calculation.
    True if yes, False if no.
    """

    while True:
        answer = input("\nDo you want to perform another calculation? (y/n): ")
        answer = answer.strip().lower()

        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def main():

    print_welcome_message()

    while True:
        print_menu()
        choice = get_user_choice()

        if choice == 5:
            print("\nThank you for using the calculator. Goodbye!")
            break

        perform_operation(choice)

        if not ask_to_continue():
            print("\nThank you for using the calculator. Goodbye!")
            break


if __name__ == "__main__":
    main()