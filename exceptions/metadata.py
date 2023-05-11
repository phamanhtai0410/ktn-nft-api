class CollectionNotFoundEx(Exception):
    def __init__(self, msg='Collection Not Found', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_COLLECTION_NOT_FOUND_EX'

    pass
class UserNotInWhitelistEx(Exception):
    def __init__(self, msg='User Not In Whitelist', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_USER_NOT_IN_WHITELIST_EX'

    pass

class NotMintStartTimeYetEx(Exception):
    def __init__(self, msg='Currently Mint Not Active', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NOT_MINT_START_TIME_YET_EX'

    pass

class UserMintLimitAmountEx(Exception):
    def __init__(self, msg='User Mint Limit Amount', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_USER_MINT_LIMIT_AMOUNT_EX'

    pass


class NftIdNotFoundEx(Exception):
    def __init__(self, msg='Nft Id Not Found', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NFT_ID_NOT_FOUND_EX'

    pass

class NftMaxSupplyEx(Exception):
    def __init__(self, msg='Nft Max Supply', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NFT_MAX_SUPPLY_EX'

    pass
