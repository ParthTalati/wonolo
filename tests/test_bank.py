import pytest

from app import bank
from app import currencies


class TestAceBank:
    @pytest.fixture(scope="function")
    def create_account_fixture(self):
        self.new_account = self.bank.create_account(self.new_account_number, 100.00)

    @pytest.fixture(scope="function")
    def create_accounts_for_funds_transfer(self):
        self.incoming_account = self.bank.create_account(
            self.new_account_number, 100.00
        )
        self.outgoing_account = self.bank.create_account(
            self.new_account_number, 100.00
        )

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.bank = bank.AceBank()
        self.currencies = currencies.Currencies
        self.new_account_number = self.bank.generate_new_account_number()

    def test_account_created(self):
        self.bank.create_account(self.new_account_number)
        assert self.bank.assert_account_exists(self.new_account_number)

    def test_depositing_money_updates_account_balance(self, create_account_fixture):
        current_balance = self.bank.accounts[self.new_account]

        self.bank.deposit_funds(self.new_account, 100, currencies.Currencies.USD)
        updated_balance = self.bank.get_balance(self.new_account)

        # Balance should be updated in CAD currency
        assert updated_balance == current_balance + self.currencies.convert_to_cad(
            self.currencies.USD, 100
        )

    def test_withdrawing_from_account_updates_account_balance(
        self, create_account_fixture
    ):
        current_balance = self.bank.accounts[self.new_account]

        self.bank.withdraw_funds(self.new_account, 20, currencies.Currencies.EUR)
        updated_balance = self.bank.get_balance(self.new_account)

        # Balance should be updated in CAD currency
        assert updated_balance == current_balance - self.currencies.convert_to_cad(
            self.currencies.EUR, 20
        )

    def test_error_when_withdrawing_more_than_balance(self):
        pass

    def test_deposit_with_negative_amount(self):
        pass

    def test_deposit_eur_adds_balance_in_cad(self):
        pass

    def test_error_when_transferring_more_than_balance(
        self, create_accounts_for_funds_transfer
    ):
        pass

    def test_balance_not_negative(self):
        pass

    def test_balance_updated_after_transfer(self):
        pass
