class BrightMenu:

    def show_main_menu(self) -> int:

        while True:

            print()
            print("=" * 34)
            print("Main Menu")
            print("=" * 34)

            print("1. Continue Learning")
            print("2. View Objectives")
            print("3. View Resources")
            print("4. View Exercises")
            print("5. Take Assessment")
            print("6. View Progress")
            print("7. Exit")

            try:
                return int(input("\n> ").strip())

            except ValueError:
                print("\nPlease enter a number between 1 and 7.")