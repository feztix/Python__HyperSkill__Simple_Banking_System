# Write your code here

from random import randint


class CreditCard:
    DEFAULT = 0000
    IIN = 400000

    def __init__(self):
        self.card = ""
        self.pin = self.DEFAULT
        self.word = ""
        self.n_list = []
        self.checksum = ""

    def generate_card(self):
        self.word = str(randint(000000000, 999999999))
        self.word = str(self.IIN) + "0" * (9 - len(self.word)) + self.word

        self.n_list = [int(x) for x in self.word]

        for _, n in enumerate(self.n_list):
            if self.n_list.index(n, _) % 2 == 0:
                self.n_list[self.n_list.index(n, _)] = n * 2
        for _, n in enumerate(self.n_list):
            if n > 9:
                self.n_list[self.n_list.index(n, _)] = n - 9
        # self.checksum = str(10 - sum(self.n_list) % 10)

        if sum(self.n_list) % 10 == 0:
            self.checksum = "0"
        else:
            self.checksum = str(10 - sum(self.n_list) % 10)

        self.card = self.word + self.checksum
        self.pin = str(randint(0000, 9999))
        self.pin = "0" * (4 - len(self.pin)) + self.pin
        print("Your card has been created")
        return self.card, self.pin

    def show_credentials(self):
        print("Your card number:")
        print(self.card)
        print("Your card PIN:")
        print(self.pin)


if __name__ == "__main__":
    cred_dict = {}
    loop = True
    while loop:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")

        option = input(">")

        if option == "0":
            loop = False
            print("Bye!")

        if option == "1":
            my_card = CreditCard()
            cardID, pinID = my_card.generate_card()
            cred_dict[cardID] = pinID
            my_card.show_credentials()

        if option == "2":
            print("Enter your card number:")
            card_number = input()
            print("Enter your PIN:")
            pin_number = input()

            if card_number in cred_dict.keys():
                if cred_dict[card_number] == pin_number:
                    print("You have successfully logged in!")
                    new_loop = True
                    while new_loop:
                        print("1. Balance")
                        print("2. Log Out")
                        print("0. Exit")

                        new_option = input()
                        if new_option == "1":
                            print("Balance: 0")
                        if new_option == "2":
                            print("You have successfully logged out!")
                            new_loop = False
                        if new_option == "0":
                            new_loop = False
                            loop = False
                            print("Bye!")
                else:
                    print("Wrong card number or PIN!")
            else:
                print("Wrong card number or PIN!")