from random import randint
import db


class CreditCard:
    DEFAULT = 0000
    IIN = 400000
    DATABASE = r"card.s3db"
    ID = 0

    def __init__(self):
        self.id = self.ID
        self.card = ""
        self.pin = self.DEFAULT
        self.word = ""
        self.n_list = []
        self.checksum = ""

    # generate card number via Luhn's Algorithm
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

        if sum(self.n_list) % 10 == 0:
            self.checksum = "0"
        else:
            self.checksum = str(10 - sum(self.n_list) % 10)

        self.card = self.word + self.checksum
        self.pin = str(randint(0000, 9999))
        self.pin = "0" * (4 - len(self.pin)) + self.pin
        CreditCard.ID += 1
        print("Your card has been created")
        return self.card, self.pin

    def show_credentials(self):
        print("Your card number:")
        print(self.card)
        print("Your card PIN:")
        print(self.pin)

    def add_card_to_db(self):
        conn = db.create_connection(self.DATABASE)
        with conn:
            # create a new card
            card = (self.ID, self.card, self.pin, 0)
            db.create_card(conn, card)


if __name__ == "__main__":
    # initialize db
    db.__init_db()

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
            # add card to db
            my_card.add_card_to_db()

        if option == "2":
            print("Enter your card number:")
            card_number = input()
            print("Enter your PIN:")
            pin_number = input()

            authorization = db.log_into_account(card_number, pin_number)

            if authorization:
                print("You have successfully logged in!")
                new_loop = True
                while new_loop:
                    print("1. Balance")
                    print("2. Add income")
                    print("3. Do transfer")
                    print("4. Close account")
                    print("5. Log out")
                    print("0. Exit")

                    new_option = input()
                    if new_option == "1":
                        db.show_card_balance(card_number, 0)
                    if new_option == "2":
                        income = int(input("Add some money: "))
                        db.add_income((income, card_number))
                    if new_option == "3":
                        card_to_transfer = int(input("Input card number to transfer: "))
                        db.do_transfer(card_number, card_to_transfer)
                    if new_option == "4":
                        db.close_account(card_number)
                    if new_option == "5":
                        print("You have successfully logged out!")
                        new_loop = False
                    if new_option == "0":
                        new_loop = False
                        loop = False
                        print("Bye!")
            else:
                print("Wrong card number or PIN!")
