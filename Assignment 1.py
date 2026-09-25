from abc import ABC, abstractmethod
from typing import Dict, Type

class PaymentMethod(ABC):
    @abstractmethod
    def get_details(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def pay(self, amount: float) -> bool:
        raise NotImplementedError

class RazorpayCardPayment(PaymentMethod):
    def __init__(self, card_number: str, card_holder: str):
        self.card_number = card_number
        self.card_holder = card_holder

    def get_details(self) -> str:
        masked = f"**** **** **** {self.card_number[-4:]}"
        return f"Razorpay Card Payment [{masked}] holder={self.card_holder}"

    def pay(self, amount: float) -> bool:
        if amount <= 0:
            return False
        print(f"[Razorpay] Charging card {self.card_number[-4:]} for ₹{amount:.2f}")
        return True


class RazorpayUPIPayment(PaymentMethod):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def get_details(self) -> str:
        return f"Razorpay UPI Payment [{self.upi_id}]"

    def pay(self, amount: float) -> bool:
        if amount <= 0:
            return False
        print(f"[Razorpay] Requesting ₹{amount:.2f} via UPI id {self.upi_id}")
        return True


class StripeCardPayment(PaymentMethod):
    def __init__(self, card_number: str, card_holder: str):
        self.card_number = card_number
        self.card_holder = card_holder

    def get_details(self) -> str:
        masked = f"**** **** **** {self.card_number[-4:]}"
        return f"Stripe Card Payment [{masked}] holder={self.card_holder}"

    def pay(self, amount: float) -> bool:
        if amount <= 0:
            return False
        print(f"[Stripe] Charging card {self.card_number[-4:]} for ${amount:.2f}")
        return True

class StripeUPIPayment(PaymentMethod):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def get_details(self) -> str:
        return f"Stripe UPI Payment [{self.upi_id}]"

    def pay(self, amount: float) -> bool:
        if amount <= 0:
            return False
        print(f"[Stripe] Requesting ${amount:.2f} via UPI id {self.upi_id}")
        return True

class FactoryPaymentMethod(ABC):
    factory: Dict[str, Type[PaymentMethod]] = {}

    @classmethod
    def get_payment_object(cls, method_type: str, **kwargs) -> PaymentMethod:
        payment_class = cls.factory.get(method_type)
        if payment_class is None:
            raise ValueError(method_type)
        return payment_class(**kwargs)

class RazorpayFactory(FactoryPaymentMethod):
    factory: Dict[str, Type[PaymentMethod]] = {
        "card": RazorpayCardPayment,
        "upi": RazorpayUPIPayment,
    }

class StripeFactory(FactoryPaymentMethod):
    factory: Dict[str, Type[PaymentMethod]] = {
        "card": StripeCardPayment,
        "upi": StripeUPIPayment,
    }

class Aggregator(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def _get_factory(self) -> Type[FactoryPaymentMethod]:
        raise NotImplementedError

    def call_get_payment_object(self, method_type: str, amount: float, **kwargs) -> bool:
        payment_method = self._get_factory().get_payment_object(method_type, **kwargs)
        return payment_method.pay(amount)

class RazorpayAggregator(Aggregator):
    def __init__(self, name: str = "Razorpay", processing_fee: float = 2.0):
        super().__init__(name)
        self.processing_fee = processing_fee

    def _get_factory(self) -> Type[FactoryPaymentMethod]:
        return RazorpayFactory

class StripeAggregator(Aggregator):
    def __init__(self, name: str = "Stripe", processing_fee: float = 2.9):
        super().__init__(name)
        self.processing_fee = processing_fee

    def _get_factory(self) -> Type[FactoryPaymentMethod]:
        return StripeFactory

class AggregatorFactory:
    factory: Dict[str, Type[Aggregator]] = {
        "stripe": StripeAggregator,
        "razorpay": RazorpayAggregator,
    }

    @classmethod
    def get_aggregator_object(cls, aggregator_name: str) -> Aggregator:
        aggregator_class = cls.factory.get(aggregator_name)
        if aggregator_class is None:
            raise ValueError(aggregator_name)
        # pyrefly: ignore [missing-argument]
        return aggregator_class()

def main():
    print("=== Payment CLI ===")

    print("\nSelect Aggregator:")
    print("1. Stripe")
    print("2. Razorpay")

    aggregator_choice = input("Enter choice: ")

    if aggregator_choice == "1":
        aggregator = StripeAggregator()
    elif aggregator_choice == "2":
        aggregator = RazorpayAggregator()
    else:
        print("Invalid aggregator choice")
        return

    print("\nSelect Method:")
    print("1. Card")
    print("2. UPI")

    method_choice = input("Enter choice: ")

    if method_choice == "1":
        method = "card"
    elif method_choice == "2":
        method = "upi"
    else:
        print("Invalid payment method")
        return

    kwargs = {}
    if method == "card":
        kwargs["card_number"] = input("Enter Card Number: ")
        kwargs["card_holder"] = input("Enter Card Holder Name: ")
    else:
        kwargs["upi_id"] = input("Enter UPI ID: ")

    amount = float(input("Enter Amount: "))

    print("\nProcessing Payment")

    result = aggregator.call_get_payment_object(method, amount, **kwargs)

    print("\n== Payment Result ==")
    print(result)

if __name__ == "__main__":
    main()
