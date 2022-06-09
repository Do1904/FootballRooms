"""
ログイン関連の処理をここに書く
"""
from .abstract import AbstractModel
from hashlib import sha256

class TestModel(AbstractModel):
    """
    ログイン，セッションなどの情報はここに書く
    """

    def __init__(self, config):
        super().__init__(config)

    def fetch_user_by_id(self, userid):
        sql = "SELECT * FROM users  WHERE id=%s"
        return self.fetch_one(sql, userid)

    def login(self, username, password):
        user = self.find_user_by_name_and_password(username, password)
        # 該当するユーザがいなければFalseを返す
        if not user:
            return False, None
        # TODO: セッションに情報を追加
        return True, user

    def find_user_by_name_and_password(self, username, password):
        hashed_password = self.hash_password(password)
        sql = "SELECT * FROM users where username=%s AND password=%s"
        return self.fetch_one(sql, username, hashed_password)
    
    def signup(self, username, password):
        hashed_password = self.hash_password(password)
        sql = "INSERT INTO users (username, password) VALUE (%s, %s);"
        self.execute(sql, username, hashed_password)

    def fetch_user_by_name(self, username):
        sql = "SELECT * FROM users  WHERE username=%s"
        return self.fetch_one(sql, username)

    def logout(self):
        pass
    
    def hash_password(self, password: str):
        return sha256(password.encode()).hexdigest()

    # def fetch_yourclub_by_name(self, favClub):
    #     sql = "SELECT * FROM clubs  WHERE clubs=%s"
    #     return self.fetch_one(sql, favClub)
