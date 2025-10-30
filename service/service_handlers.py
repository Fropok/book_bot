class ServiceHandler:

    @staticmethod
    def get_int_page_callback(callback_data: str) -> int:
        page_int = int(callback_data.split(':')[1])
        return page_int
