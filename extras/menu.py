def print_menu():
    print("Please select the desired option of loading your data by entering a number:")
    print(5 * "-", "MENU", 5 * "-")
    print("1. Use a file stored in a 'datasource' directory.")
    print("2. Enter a link to a CSV file.")
    print("3. Exit.")
    while True:
        user_input = input()
        try:
            x = int(user_input)
            if x in (1, 2):
                break
            elif x == 3:
                exit()
            else:
                print("Please select option number 1, 2 or 3. \n")
        except ValueError:
            print("Invalid value provided. \n")
            print("Please select option number 1, 2 or 3. \n")
    return x
