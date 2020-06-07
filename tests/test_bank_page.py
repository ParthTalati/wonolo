import pytest
import faker
from app import bank
from app import currencies


class TestAceBank:

    def __init__(self):
        self.bank = bank.AceBank()
        self.currencies = currencies.Currencies
        self.fake = faker.Faker()

    def test_deposit(self):
        account_number = "123456"
        self.bank.deposit_funds(account_number, 100, self.currencies.USD)
        assert self.bank.accounts[account_number] == 150

    def test_withdrawal(self):
        pass

    def test_error_when_withdrawing_more_than_balance(self):
        pass

    def test_deposit_with_negative_amount(self):
        pass

    def test_deposit_eur_adds_balance_in_cad(self):
        pass

    def test_error_when_transferring_more_than_balance(self):
        pass

    def test_balance_not_negative(self):
        pass
