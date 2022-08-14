from venmo_api import string_to_timestamp, BaseModel, User, Comment, get_phone_model_from_json, JSONSchema
from enum import Enum


class CreditCardTransaction(BaseModel):

    def __init__(self, transaction_id, status, name, amount, category, created_at,
                 transaction_type, reference_number, description, detail_url,
                 paid_by, scheduled_date, json=None):
        """
        Credit Card Transaction model
        :param transaction_id:
        :param status:
        :param name:
        :param amount:
        :param category:
        :param created_at:
        :param transaction_type:
        :param reference_number:
        :param description:
        :param detail_url:
        :param paid_by:
        :param scheduled_date:
        """
        super().__init__()

        self.id = story_id
        self.payment_id = payment_id

        self.date_completed = date_completed
        self.date_created = date_created
        self.date_updated = date_updated

        self.payment_type = payment_type
        self.amount = amount
        self.audience = audience
        self.status = status

        self.note = note
        self.device_used = device_used
        self.comments = comments

        self.actor = actor
        self.target = target
        self._json = json

    @classmethod
    def from_json(cls, json):
        """
        Create a new Transaction from the given json.
        This only works for transactions, skipping refunds and bank transfers.
        :param json:
        :return:
        """

        if not json:
            return

        parser = JSONSchema.cc_transaction(json)

        return cls(transaction_id=parser.get_transaction_id(),
                   status=parser.get_status(),
                   name=parser.get_name(),
                   amount=parser.get_amount(),
                   category=parser.get_category(),
                   created_at=parser.get_created_at(),
                   transaction_type=parser.get_transaction_type(),
                   reference_number=parser.get_reference_number(),
                   description=parser.get_description(),
                   detail_url=parser.get_detail_url(),
                   paid_by=parser.get_paid_by(),
                   scheduled_date=parser.get_scheduled_date(),
                   json=json)


class TransactionType(Enum):
    PAYMENT = 'payment'
    # merchant refund
    REFUND = 'refund'
    # to/from bank account
    TRANSFER = 'transfer'
    # add money to debit card
    TOP_UP = 'top_up'
    # debit card purchase
    AUTHORIZATION = 'authorization'
    # debit card atm withdrawal
    ATM_WITHDRAWAL = 'atm_withdrawal'

    DISBURSEMENT = 'disbursement'
