from lib.quotation.clients.awesome_api import AwesomeAPI
from lib.quotation.clients.rate_api import RateAPI
from lib.quotation.kafka.producer import Producer
from decimal import Decimal


class Quotation:
    """
    Quotation class is the main class that will be executed to get the currency quotation values.
    """

    available_currencies = ["BRL", "USD", "EUR", "CAD", "BTC"]

    def __init__(self, currency_from, currency_to, client=RateAPI, amount=1.0) -> str:
        self.__check_validations(currency_from, currency_to, amount)

        self.currency_from = currency_from
        self.currency_to = currency_to
        self.client = client(self.currency_from, self.currency_to)
        self.amount = amount

    def get(self) -> str:
        """
        Returns the message with currency_from to value in currency_to
        """
        quotation_value = self.__get_quotation_value()
        formatted_quotation = self.__format_quotation(quotation_value)
        self.__produce_message(formatted_quotation)

        return f"{self.amount} {self.currency_from} is equal to {formatted_quotation} {self.currency_to}"

    def __get_quotation_value(self) -> float:
        return self.client.get()

    def __format_quotation(self, quotation) -> str:
        return "{:.2f}".format(Decimal(quotation) * Decimal(self.amount))

    def __produce_message(self, formatted_quotation):
        Producer(
            self.currency_from,
            self.currency_to,
            self.amount,
            formatted_quotation,
            self.client.source(),
        ).produce()

    def __check_validations(self, currency_from, currency_to, amount):
        """
        Check if there is any error validation when instantiate a new object.
        """
        if not type(currency_from) is str:
            raise AttributeError("currency_from must be a string")

        if not type(currency_to) is str:
            raise AttributeError("currency_to must be a string")

        if not currency_from:
            raise AttributeError("currency_from must not be blank")

        if not currency_to:
            raise AttributeError("currency_to must not be blank")

        if amount < 0:
            raise AttributeError("amount must not be negative")

        if not currency_from in self.available_currencies:
            raise AttributeError(
                f"the given {currency_from} currency is not available, available_currencies are {self.available_currencies}"
            )

        if not currency_to in self.available_currencies:
            raise AttributeError(
                f"the given {currency_to} currency is not available, available_currencies are {self.available_currencies}"
            )

        if currency_from == currency_to:
            raise AttributeError("currencies must not be equals")
