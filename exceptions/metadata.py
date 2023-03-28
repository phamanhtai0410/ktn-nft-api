class CollectionNotFoundEx(Exception):
    def __init__(self, msg='Collection Not Found', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_COLLECTION_NOT_FOUND_EX'

    pass