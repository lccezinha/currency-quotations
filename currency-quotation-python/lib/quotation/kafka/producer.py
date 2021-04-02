from kafka import KafkaProducer
import json


class Producer:
    def __init__(self, currency_from, currency_to, amount, quotation_value, source):
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.amount = amount
        self.quotation_value = quotation_value
        self.source = source
        self.__producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda m: json.dumps(m).encode("ascii"),
        )

    def produce(self):
        data = {
            "currency_from": self.currency_from,
            "currency_to": self.currency_to,
            "amount": self.amount,
            "quotation_value": self.quotation_value,
        }
        self.__producer.send(f"quotation_topic_{self.source}", data)
