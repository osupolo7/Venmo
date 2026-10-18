from venmo_api import string_to_date, BaseModel, JSONSchema
from enum import Enum


class CreditCardTransaction(BaseModel):

    def __init__(self, transaction_id, reference_number, status, amount_cents, transaction_type,
                 description, merchant_name, category, created_at, scheduled_date, paid_by,
                 detail_url, is_authorized_user_transaction, authorized_user_initials, json=None):
        """
        Venmo Credit Card transaction model
        :param transaction_id: <str> Changes when a pending transaction settles.
        :param reference_number: <str> None while pending.
        :param status: <str> 'pending' or 'settled'
        :param amount_cents: <int> Positive for charges (purchases), negative for credits (payments, refunds).
        :param transaction_type: <str> e.g. 'purchase', 'payment'
        :param description: <str> Statement description
        :param merchant_name: <str> None for card payments
        :param category: <str> Venmo's merchant category, e.g. 'dining_and_nightlife'
        :param created_at: <date> Transaction date
        :param scheduled_date: <date> Scheduled date of a future card payment
        :param paid_by:
        :param detail_url: <str> API path of the transaction details
        :param is_authorized_user_transaction: <bool>
        :param authorized_user_initials: <str>
        :param json: full_json
        """
        super().__init__()

        self.id = transaction_id
        self.reference_number = reference_number
        self.status = status

        self.amount_cents = amount_cents
        self.amount = amount_cents / 100
        self.transaction_type = transaction_type
        self.description = description
        self.merchant_name = merchant_name
        self.category = category

        self.created_at = created_at
        self.scheduled_date = scheduled_date
        self.paid_by = paid_by
        self.detail_url = detail_url

        self.is_authorized_user_transaction = is_authorized_user_transaction
        self.authorized_user_initials = authorized_user_initials
        self._json = json

    @classmethod
    def from_json(cls, json):
        """
        Create a new CreditCardTransaction from the given json.
        :param json:
        :return:
        """

        if not json:
            return

        parser = JSONSchema.cc_transaction(json)

        return cls(transaction_id=parser.get_transaction_id(),
                   reference_number=parser.get_reference_number(),
                   status=parser.get_status(),
                   amount_cents=parser.get_amount(),
                   transaction_type=parser.get_transaction_type(),
                   description=parser.get_description(),
                   merchant_name=parser.get_merchant_name(),
                   category=parser.get_category(),
                   created_at=string_to_date(parser.get_created_at()),
                   scheduled_date=string_to_date(parser.get_scheduled_date()),
                   paid_by=parser.get_paid_by(),
                   detail_url=parser.get_detail_url(),
                   is_authorized_user_transaction=parser.get_is_authorized_user_transaction(),
                   authorized_user_initials=parser.get_authorized_user_initials(),
                   json=json)


class CreditCardTransactionStatus(Enum):
    PENDING = 'pending'
    SETTLED = 'settled'


class CreditCardTransactionType(Enum):
    PURCHASE = 'purchase'
    PAYMENT = 'payment'
