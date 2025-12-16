from ulid import ULID


class GeneralHelper:

    @classmethod
    def get_ulid(cls) -> str:
        return str(ULID())
