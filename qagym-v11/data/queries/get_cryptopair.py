from utils.utils import generate_number_excluding
import random
def get_user_id_queries(query_name = '', user_ids = None):
    user_ids = user_ids or []
    user_ids = [user.get('user_id') for user in user_ids if user.get('user_id') is not None]
    match query_name:
        case "random_user":
            return random.choice(user_ids)
        case "missing_user_id":
            return ""
        case "wrong_user_id":
            random_id = generate_number_excluding(1000000, 9999999999, user_ids)
            return random_id