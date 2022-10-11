# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""


class TxRecorded(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 300
        self.msg = 'This tx has been recorded. Please see the results in your transaction history.'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_TX_RECORDED'

    pass


class TxPayment(Exception):
    def __init__(self,msg="Order not found in payment queue.", *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_PAYMENT'

    pass
