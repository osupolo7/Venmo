from venmo_api import CreditCardTransaction, Page, deserialize, wrap_callback, get_next_page_params
from typing import Union


class CreditCardApi(object):

    def __init__(self, api_client):
        super().__init__()
        self.__api_client = api_client

    def get_transactions(self, callback=None,
                         page_number: int = None,
                         ledger_page_token: str = None) -> Union[Page, None]:
        """
        Get your Venmo Credit Card transactions, newest first, as a <Page> of <CreditCardTransaction>s.
        Venmo returns up to 500 per page; use page.get_next_page() for older ones.
        Pending transactions get a new id once they settle.
        :param callback:
        :param page_number: <int> [optional] cursor, taken from the previous page
        :param ledger_page_token: <str> [optional] cursor, taken from the previous page
        :return:
        """
        params = {}
        if page_number:
            params['page_number'] = page_number
        if ledger_page_token:
            params['ledger_page_token'] = ledger_page_token

        # Prepare the request
        resource_path = '/credit-card/transactions'
        wrapped_callback = wrap_callback(callback=callback,
                                         data_type=CreditCardTransaction)
        # Make the request
        response = self.__api_client.call_api(resource_path=resource_path,
                                              method='GET', params=params,
                                              callback=wrapped_callback)
        # Return None if threaded
        if callback:
            return

        return deserialize(response=response,
                           data_type=CreditCardTransaction).set_method(
            method=self.get_transactions,
            kwargs={},
            next_kwargs=get_next_page_params(response, ['page_number', 'ledger_page_token']))

    def get_transaction(self, transaction_id: str, callback=None) -> Union[CreditCardTransaction, None]:
        """
        Get a single Venmo Credit Card transaction
        :param transaction_id: <str>
        :param callback:
        :return:
        """
        # Prepare the request
        resource_path = f'/credit-card/transactions/{transaction_id}'
        wrapped_callback = wrap_callback(callback=callback,
                                         data_type=CreditCardTransaction)
        # Make the request
        response = self.__api_client.call_api(resource_path=resource_path,
                                              method='GET',
                                              callback=wrapped_callback)
        # Return None if threaded
        if callback:
            return

        return deserialize(response=response, data_type=CreditCardTransaction)
