from alice_app.dao.base_dao import BaseDao
from alice_app.domain.token import Token


class TokenDao(BaseDao):
    def __init__(self, ):
        super(TokenDao, self).__init__('/token/sql/')

    def get_by_login(self, login: str) -> Token:
        sql = self.get_sql('get_by_login.sql')
        return self.query_one(Token, sql, dict(login=login))

    def get_by_access_token(self, access_token: str) -> Token:
        sql = self.get_sql('get_by_access_token.sql')
        return self.query_one(Token, sql, dict(access_token=access_token))

    def get_by_refresh_token(self, refresh_token: str) -> Token:
        sql = self.get_sql('get_by_refresh_token.sql')
        return self.query_one(Token, sql, dict(refresh_token=refresh_token))

    def insert(self, token: Token) -> int:
        sql = self.get_sql('insert.sql')
        return self.execute(sql, token.to_dict())

    def update(self, token: Token) -> int:
        sql = self.get_sql('update_by_id.sql')
        self.execute(sql, token.to_dict())
        return token.id

    def delete(self, token_id: int):
        sql = self.get_sql('delete.sql')
        self.execute(sql, dict(id=token_id))
