class UserEndpoints:
    @staticmethod
    def create_crypto_pair():
        return '/cryptopair/create/'
    @staticmethod
    def get_crypto_pairs(user_id):
        return f'/cryptopair/get/?user_id={user_id}'
    @staticmethod
    def edit_crypto_pair():
        return '/cryptopair/edit/'
    @staticmethod
    def delete_crypto_pair(user_id, pair_id):
        return f'/cryptopair/delete/?user_id={user_id}&pair_id={pair_id}'
    @staticmethod
    def get_prices():
        return '/get-all-prices/'
    @staticmethod
    def get_users():
        return '/users/'