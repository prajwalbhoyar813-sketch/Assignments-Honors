from abc import ABC, abstractmethod
from typing import Dict, Type

class PaymentMethod(ABC):
    @abstractmethod
    def get_details(self) -> str:
        raise NotImplementedError
    @abstractmethod
    def pay(self, amt: float) -> bool:
        raise NotImplementedError

class RazorpayCardPayment(PaymentMethod):
    def __init__(self, card_no: str, card_name: str):
        self.card_no = card_no
        self.card_name = card_name

    def get_details(self) -> str:
        masked = f"{self.card_no[-4:]}"
        return f"Razorpay Card Payment [{masked}] holder={self.card_name}"

    def pay(self, amt: float) -> bool:
        if amt <= 0:
            return False
        print(f"[Razorpay] Charging card {self.card_no[-4:]} for ${amt}")
        return True

class RazorpayUPIPayment(PaymentMethod):
    def __init__(self, upi: str):
        self.upi = upi
    def get_details(self) -> str:
        return f"Razorpay UPI Payment [{self.upi}]"
    def pay(self, amt: float) -> bool:
        if amt <= 0:
            return False
        print(f"[Razorpay] Requesting ₹{amt} via UPI id {self.upi}")
        return True

class StripeCardPayment(PaymentMethod):
    def __init__(self, card_no: str, card_name: str):
        self.card_no = card_no
        self.card_name = card_name

    def get_details(self) -> str:
        masked = f"{self.card_no[-4:]}"
        return f"Stripe Card Payment [{masked}] holder={self.card_name}"

    def pay(self, amt: float) -> bool:
        if amt <= 0:
            return False
        print(f"[Stripe] Charging card {self.card_no[-4:]} for ${amt}")
        return True

class StripeUPIPayment(PaymentMethod):
    def __init__(self, upi: str):
        self.upi = upi

    def get_details(self) -> str:
        return f"Stripe UPI Payment [{self.upi}]"

    def pay(self, amt: float) -> bool:
        if amt <= 0:
            return False
        print(f"[Stripe] Requesting ${amt} via UPI id {self.upi}")
        return True

class FactoryPaymentMethod(ABC):
    factory: Dict[str, Type[PaymentMethod]] = {}
    @classmethod
    def get_payment_object(cls, method: str, **kw) -> PaymentMethod:
        pay_cls = cls.factory.get(method)
        if pay_cls is None:
            raise ValueError(method)
        return pay_cls(**kw)

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

    def call_get_payment_object(self, method: str, amt: float, **kw) -> bool:
        pay = self._get_factory().get_payment_object(method, **kw)
        return pay.pay(amt)

class RazorpayAggregator(Aggregator):
    def __init__(self, name: str = "Razorpay", fee: float = 2.0):
        super().__init__(name)
        self.fee = fee

    def _get_factory(self) -> Type[FactoryPaymentMethod]:
        return RazorpayFactory

class StripeAggregator(Aggregator):
    def __init__(self, name: str = "Stripe", fee: float = 2.9):
        super().__init__(name)
        self.fee = fee

    def _get_factory(self) -> Type[FactoryPaymentMethod]:
        return StripeFactory

class AggregatorFactory:
    factory: Dict[str, Type[Aggregator]] = {
        "stripe": StripeAggregator,
        "razorpay": RazorpayAggregator,
    }
    @classmethod
    def get_aggregator_object(cls, name: str) -> Aggregator:
        agg_cls = cls.factory.get(name)
        if agg_cls is None:
            raise ValueError(name)
        return agg_cls()

def main():
    print("   Payment menu   ")
    print("\nSelect your choice:")
    print("1. Stripe")
    print("2. Razorpay")
    agg_ch = input("Enter choice: ")

    if agg_ch == "1":
        agg = StripeAggregator()
    elif agg_ch == "2":
        agg = RazorpayAggregator()
    else:
        print("Invalid choice")
        return
    print("\nSelect Method:")
    print("1. Card")
    print("2. UPI")
    met_ch = input("Enter choice: ")

    if met_ch == "1":
        met = "card"
    elif met_ch == "2":
        met = "upi"
    else:
        print("Invalid payment method")
        return
    kw = {}
    if met == "card":
        kw["card_no"] = input("Enter Card Number: ")
        kw["card_name"] = input("Enter Card Holder Name: ")
    else:
        kw["upi"] = input("Enter UPI ID: ")
    amt = float(input("Enter Amount: "))

    print("\nProcessing Payment")
    res = agg.call_get_payment_object(met, amt, **kw)
    print("\n  Payment Result   ")
    print(res)

if __name__ == "__main__":
    main()
