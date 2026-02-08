from abc import abstractmethod
from decimal import Decimal
from typing import Protocol, Optional, Dict, Any

# Complete payment processor interface
# The PaymentService depends on this abstraction
class PaymentPort(Protocol):
    # create an authorization/hold on the user's payment method
    @abstractmethod
    def create_hold(
        self,
        amount: Decimal,
        currency: str,
        reference: str,
    ) -> str:
        pass
    # capture a previously authorized payments
    @abstractmethod
    def capture(
        self,
        processor_ref: str,
    ) -> None:
        pass

    # cancel PyamentIntent that won't be used 
    @abstractmethod
    def cancel_payment_intent(
        self,
        processor_ref: str,
    ) -> None:
        pass

    # refund a previously captured or authorized payments
    @abstractmethod
    def refund(
        self,
        processor_ref: str,
        amount: Decimal,
    ) -> str:
        pass

    # create Stripe Checkout Session with manual capture
    @abstractmethod
    def create_checkout_session(
        self,
        booking_id: str,
        user_id: str,
        amount: Decimal,
        currency: str,
        success_url: str,
        cancel_url: str,
        customer_email: str = None,
    ) -> dict:
        pass

    # retrieve Checkout Session details
    @abstractmethod
    def retrieve_checkout_session(
        self,
        session_id: str
    ) -> dict:
        pass 

    # create a PaymentIntent for frontend Stripe Elements
    # returns dict with client_secret and payment_intent_id
    @abstractmethod
    def create_payment_intent(
        self,
        amount: Decimal,
        currency: str,
        reference: str,
        capture_method: str = "manual",
    ) -> Dict[str, Any]:
        raise NotImplementedError

    # confirm a PaymentIntent after frontend collection
    @abstractmethod
    def confirm_payment_intent(
        self,
        payment_intent_id: str,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    # retrieve a PaymentIntent status from processor
    @abstractmethod
    def get_payment_intent(
        self,
        payment_intent_id: str,
    ) -> Optional[Dict[str, Any]]:
        raise NotImplementedError