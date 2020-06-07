from random import randint

import pytest

from app import bank
from app import currencies


class TestAceBank:

    def setup(self):
        self.bank = bank.AceBank()
        self.currencies = currencies.Currencies
        n = 6
        self.new_account_number = ''.join(["{}".format(randint(0, 9)) for _ in range(0, n)])
        self.existing_account = self.new_account_number

    def test_account_created(self):
        self.bank.create_account(self.new_account_number)
        assert self.bank.assert_account_exists(self.new_account_number)

    def test_deposit(self):
        current_balance = self.bank.accounts[self.existing_account]

        self.bank.deposit_funds(self.existing_account, 100, currencies.Currencies.USD)
        updated_balance = self.bank.get_balance(self.existing_account)

        assert updated_balance == current_balance + self.currencies.convert_to_cad(self.currencies.USD, 100)

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

    def test_balance_updated_after_transfer(self):
        pass

