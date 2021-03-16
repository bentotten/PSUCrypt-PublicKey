# CS585 Cryptography
# Ben Totten
# My Take on rijndael 


def main():
    menu()


def menu():
    print("~~~ MENU ~~~\n")
    print("1) Key Generation\n2) Encryption \n3) Decryption\n")
    selection = input("Input: ")
    
    while selection != "1" and selection != "2" and selection != "3":
        print("\nPlease input option 1, 2, or 3\n")
        selection = input("Input: ")

    print(selection)





if __name__ == "__main__":
    main()
    