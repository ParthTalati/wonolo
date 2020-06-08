from random import randint

from app.currencies import Currencies


class AceBank:
    def __init__(self):
        self.accounts = {}

    # Method to check if the account exists or not
    def assert_account_exists(self, account_number: str):
        """ This methods checks if an account number is existing or not
        :argument: account_number
        :returns: True, if account exists
        :returns: Exception, if account does not exist
        """

        if account_number not in self.accounts:
            raise Exception(f"Account {account_number} does not exist")
        else:
            return True

    # Method to check that no transaction allowed with negative amount
    @staticmethod
    def assert_positive_amount(amount: float):
        if amount < 0:
            raise Exception("Negative amount not allowed")

    # Method to create a new account
    def create_account(self, account_number: str, balance: float = 0.00) -> str:
        if account_number not in self.accounts:
            self.accounts[account_number] = balance
            return account_number
        else:
            raise Exception("Account already exists")

    # Method to get the balance for the provided account number
    def get_balance(self, account_number: str) -> float:
        self.assert_account_exists(account_number)
        return self.accounts[account_number]

    # Method to deposit amount in C$ currency
    def deposit_funds(
        self, account_number: str, amount: float, currency: Currencies
    ) -> None:
        self.assert_account_exists(account_number)
        self.assert_positive_amount(amount)
        self.accounts[account_number] += currency.convert_to_cad(amount)

    # Method to withdraw money from account (in C$)
    def withdraw_funds(
        self, account_number: str, amount: float, currency: Currencies
    ) -> None:
        self.assert_account_exists(account_number)
        self.assert_positive_amount(amount)
        amount_in_cad = currency.convert_to_cad(amount)
        if amount_in_cad > self.accounts[account_number]:
            raise Exception("Not enough funds")
        self.accounts[account_number] -= amount_in_cad

    # Method to transfer funds from one account to another
    def transfer_funds(
        self, incoming_account_number: str, out_going_account_number: str, amount: float
    ) -> None:
        self.assert_account_exists(incoming_account_number)
        self.assert_account_exists(out_going_account_number)
        self.withdraw_funds(out_going_account_number, amount, Currencies.CAD)
        self.deposit_funds(incoming_account_number, amount, Currencies.CAD)

    @staticmethod
    def generate_new_account_number():
        n = 6
        return ''.join(["{}".format(randint(0, 9)) for _ in range(0, n)])
