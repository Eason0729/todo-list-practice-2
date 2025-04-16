from sqlalchemy.orm.query import Query


class Paginate:
    page: int
    per_page: int

    def __init__(self, per_page: int = 0):
        self.page = 0
        self.per_page = per_page

    @staticmethod
    def from_token(token: str) -> "Paginate":
        page_size, page_number = token.split("-")

        paginate = Paginate()
        paginate.per_page = int(page_size)
        paginate.page = int(page_number)

        return paginate

    def to_token(self) -> str:
        return f"{self.per_page}-{self.page}"

    def apply(self, query: Query) -> Query:
        return query.limit(self.per_page).offset(self.page * self.per_page)

    def next_page(self) -> int:
        return self.page + 1
