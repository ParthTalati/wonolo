from app.currencies import Currencies


class AceBank:
    def __init__(self):
        self.accounts = {}

    def assert_account_exists(self, account_number: str):
        if account_number not in self.accounts:
            raise Exception(f"Account {account_number} does not exist")

    @staticmethod
    def assert_positive_amount(amount: float):
        if amount < 0:
            raise Exception("Negative amount not allowed")

    def create_account(self, account_number: str, balance: float = 0.00) -> None:
        if account_number not in self.accounts:
            self.accounts[account_number] = balance
        else:
            raise Exception("Account already exists")

    def get_balance(self, account_number: str) -> float:
        self.assert_account_exists(account_number)
        return self.accounts[account_number]

    def deposit_funds(self, account_number: str, amount: float, currency: Currencies) -> None:
        self.assert_account_exists(account_number)
        self.assert_positive_amount(amount)
        self.accounts[account_number] += currency.convert_to_cad(amount)

    def withdraw_funds(self, account_number: str, amount: float, currency: Currencies) -> None:
        self.assert_account_exists(account_number)
        self.assert_positive_amount(amount)
        amount_in_cad = currency.convert_to_cad(amount)
        if amount_in_cad > self.accounts[account_number]:
            raise Exception("Not enough funds")
        self.accounts[account_number] -= amount_in_cad

    def transfer_funds(self, incoming_account_number: str, out_going_account_number: str, amount: float) -> None:
        self.assert_account_exists(incoming_account_number)
        self.assert_account_exists(out_going_account_number)

        self.withdraw_funds(out_going_account_number, amount, Currencies.CAD)
        self.deposit_funds(incoming_account_number, amount, Currencies.CAD)
