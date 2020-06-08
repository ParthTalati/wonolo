import pytest

from app import bank
from app import currencies


class TestAceBank:
    @pytest.fixture(scope="function")
    def create_account_fixture(self):
        """
        Assumption made : The new account is always created with 100 C$
        """
        self.new_account = self.bank.create_account(self.new_account_number, 100.00)

    @pytest.fixture(scope="function")
    def create_accounts_for_funds_transfer(self):
        self.incoming_account = self.bank.create_account(
            self.incoming_account_number, 100.00
        )
        self.outgoing_account = self.bank.create_account(
            self.new_account_number, 100.00
        )

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.bank = bank.AceBank()
        self.currencies = currencies.Currencies
        self.new_account_number = self.bank.generate_new_account_number()
        self.incoming_account_number = self.bank.generate_new_account_number()

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
        current_balance = self.bank.get_balance(self.new_account)

        self.bank.withdraw_funds(self.new_account, 20, currencies.Currencies.EUR)
        updated_balance = self.bank.get_balance(self.new_account)

        # Balance should be updated in CAD currency
        assert updated_balance == current_balance - self.currencies.convert_to_cad(
            self.currencies.EUR, 20
        )

    def test_error_when_withdrawing_more_than_balance(self, create_account_fixture):
        """
        Test 1 : Account holder can not withdraw more than total balance
        Test 2 : Other currency withdrawal denied when it exceeds the available amount in CAD
        """

        with pytest.raises(Exception) as e:
            # Test 1
            assert not self.bank.withdraw_funds(
                self.new_account, 101.00, currencies.Currencies.CAD
            )
            # Test 2
            assert self.bank.withdraw_funds(
                self.new_account, 95.00, currencies.Currencies.EUR
            )
        assert str(e.value) == "Not enough funds"

    def test_deposit_with_negative_amount(self, create_account_fixture):
        with pytest.raises(Exception) as e:
            assert self.bank.deposit_funds(
                self.new_account, -50.00, currencies.Currencies.CAD
            )
        assert str(e.value) == "Negative amount not allowed"

    def test_deposit_eur_adds_balance_in_cad(self, create_account_fixture):
        current_balance = self.bank.get_balance(self.new_account)
        amount_deposited = 50.00

        self.bank.deposit_funds(
            self.new_account, amount_deposited, currencies.Currencies.EUR
        )
        updated_balance = self.bank.get_balance(self.new_account)

        assert updated_balance == current_balance + self.currencies.convert_to_cad(
            self.currencies.EUR, amount_deposited
        )

    def test_exception_raised_when_transferring_more_than_balance(
        self, create_accounts_for_funds_transfer
    ):
        transfer_amount = 76.00

        with pytest.raises(Exception) as e:
            assert self.bank.transfer_funds(
                self.incoming_account,
                self.outgoing_account,
                transfer_amount,
                currencies.Currencies.USD,
            )
        assert str(e.value) == "Not enough funds"

    def test_balance_updated_after_transfer(self, create_accounts_for_funds_transfer):
        transfer_amount = 50

        # Account balances before transaction
        current_balance_incoming_account = self.bank.get_balance(self.incoming_account)
        current_balance_outgoing_account = self.bank.get_balance(self.outgoing_account)

        # Method to transfer "transfer_amount" from outgoing to incoming account
        self.bank.transfer_funds(
            self.incoming_account,
            self.outgoing_account,
            transfer_amount,
            currencies.Currencies.USD,
        )

        # Account balances after transaction
        updated_balance_incoming_account = self.bank.get_balance(self.incoming_account)
        updated_balance_outgoing_account = self.bank.get_balance(self.outgoing_account)

        # Increase in the balance for incoming account
        assert (
            updated_balance_incoming_account
            == current_balance_incoming_account
            + currencies.Currencies.convert_to_cad(self.currencies.USD, transfer_amount)
        )

        # Decrease in the balance for outgoing account
        assert (
                updated_balance_outgoing_account
                == current_balance_outgoing_account
                - currencies.Currencies.convert_to_cad(self.currencies.USD, transfer_amount)
        )
