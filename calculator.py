#!/usr/bin/env python3
"""
A simple Python calculator with basic arithmetic operations.
"""

def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract two numbers."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide two numbers."""
    if b == 0:
        return "Error: Division by zero"
    return a / b


def power(a, b):
    """Raise a number to a power."""
    return a ** b


def square_root(a):
    """Calculate the square root of a number."""
    if a < 0:
        return "Error: Cannot calculate square root of negative number"
    return a ** 0.5


def calculator():
    """Main calculator function with user interface."""
    print("=" * 50)
    print("        PYTHON CALCULATOR")
    print("=" * 50)
    print("\nAvailable operations:")
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")
    print("5. Power (**)")
    print("6. Square Root (sqrt)")
    print("7. Exit")
    print("-" * 50)
    
    while True:
        choice = input("\nEnter operation (1/2/3/4/5/6/7): ").strip()
        
        if choice == '7':
            print("\nThank you for using the calculator!")
            break
        
        if choice == '6':
            try:
                num = float(input("Enter a number: "))
                result = square_root(num)
                print(f"√{num} = {result}")
            except ValueError:
                print("Error: Please enter a valid number")
            continue
        
        if choice in ['1', '2', '3', '4', '5']:
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                
                if choice == '1':
                    result = add(num1, num2)
                    print(f"{num1} + {num2} = {result}")
                elif choice == '2':
                    result = subtract(num1, num2)
                    print(f"{num1} - {num2} = {result}")
                elif choice == '3':
                    result = multiply(num1, num2)
                    print(f"{num1} * {num2} = {result}")
                elif choice == '4':
                    result = divide(num1, num2)
                    print(f"{num1} / {num2} = {result}")
                elif choice == '5':
                    result = power(num1, num2)
                    print(f"{num1} ** {num2} = {result}")
            except ValueError:
                print("Error: Please enter valid numbers")
        else:
            print("Error: Invalid choice. Please enter a number between 1 and 7")


if __name__ == "__main__":
    calculator()
