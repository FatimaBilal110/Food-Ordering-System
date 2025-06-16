import db

def show_menu():
    print("\n--- MENU ---")
    for item in db.get_menu():
        print(f"{item[0]}. {item[1]} - Rs.{item[2]:.2f}")

def place_order():
    name = input("Enter your name: ")
    order_id = db.create_order(name)
    total_order_price = 0

    while True:
        try:
            item_id = int(input("Enter item number (or 0 to finish): "))
            if item_id == 0:
                break
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid input. Try again.")
            continue

        price_result = db.get_price(item_id)
        if price_result:
            price = price_result[0]
            total = price * quantity
            total_order_price += total
            db.add_order_item(order_id, item_id, quantity, total)
            print(f"Added {quantity} x item #{item_id} to your order.")
        else:
            print("Item not found.")

    print(f"\n✅ Order placed! Total:Rs.{total_order_price:.2f}")

def view_orders():
    print("\n--- PAST ORDERS ---")
    orders = db.get_all_orders()
    if not orders:
        print("No orders yet.")
        return

    current_order = None
    for row in orders:
        order_id, customer, item, qty, total = row
        if current_order != order_id:
            print(f"\n Order #{order_id} | {customer}")
            current_order = order_id
        print(f"   - {qty} x {item} = Rs.{total:.2f}")

def main():
    db.init_db()

    while True:
        print("\n1. Show Menu\n2. Place Order\n3. View Orders\n4. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            show_menu()
        elif choice == '2':
            show_menu()
            place_order()
        elif choice == '3':
            view_orders()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
     

if __name__ == "__main__":

    main()