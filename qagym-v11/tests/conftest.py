import pytest
import random
from api.client import APIClient
from data.config import settings
from api.endpoints.endpoints import UserEndpoints
from data.payloads.cryptopairs.currency import all_cryptopais
class NoAvailablePairsError(Exception):
    """Вызывается, когда у пользователя нет свободных криптопар."""
    pass

class CleanupContext ():
    def __init__(self) -> None:
        self.ids = {}

@pytest.fixture(scope='session')
def api_client():
    client = APIClient(base_url=settings.API_BASE_URL)
    try:
        yield client
    finally:
        client.session.close()
@pytest.fixture(scope='session')
def all_users(api_client):
    users = api_client.get(UserEndpoints.get_users()).json()
    try:
        yield users
    finally:
        users.clear()
@pytest.fixture(scope='function')
def random_user(all_users, request, api_client):
    """
    Фикстура выбирает пользователя, у которого есть хотя бы одна свободная криптопара.
    Если у всех пользователей пары заняты, вызывает исключение.
    """
    # Перемешиваем пользователей для случайного выбора
    shuffled_users = random.sample(all_users, len(all_users))
    
    for user in shuffled_users:
        # Получаем криптопары пользователя
        url = UserEndpoints.get_crypto_pairs(user['user_id'])
        response = api_client.get(url).json()
        
        # Проверяем наличие свободных пар
        existing_pairs = {
            (pair['crypto_currency'], pair['base_currency']) 
            for pair in response
        }
        available_pairs = all_cryptopais - existing_pairs
        
        if available_pairs:
            print(
                f"\n[DEBUG] Тест {request.node.name}: "
                f"выбран пользователь {user['user_id']} со свободными парами {available_pairs}"
            )
            return user
    
    # Если ни у кого нет свободных пар
    raise NoAvailablePairsError(
        "Нет пользователей со свободными криптопарами!"
        f"Все возможные пары: {all_cryptopais}. "
        f"Всего пользователей: {len(all_users)}"
    )

@pytest.fixture(scope='function')
def user_currencies(api_client, random_user):
    url = UserEndpoints.get_crypto_pairs(random_user['user_id'])
    response = api_client.get(url).json()
    return response

@pytest.fixture(scope='function')
def random_cryptopair(user_currencies, request):
    data = user_currencies
    existing_pairs = set()
    for pair in data:
        existing_pairs.add((pair['crypto_currency'], pair['base_currency']))
    available_pairs = all_cryptopais - existing_pairs
    if not available_pairs:
        raise 
    pair = random.choice(list(available_pairs))
    print(f"\n[DEBUG] Тест {request.node.name}: выбрана пара {pair}")
    # request.node.add_marker(pytest.mark.usefixtures('random_cryptopair'))    
    return pair

@pytest.fixture(scope='function')
def create_cryptopar_dinamic_data(random_user, random_cryptopair):
    #TODO вынести нахуй отсюда хардкод
    dinamic_data = {
        "user_id": random_user["user_id"],
        "crypto_currency": random_cryptopair[0],
        "base_currency": random_cryptopair[1],
        "threshold_value": random.uniform(1.0, 9999999999.9999999999),
        "notify_on": random.choice(["above", "below"]),
    }
    return dinamic_data

@pytest.fixture (scope='function')
def cleanup_cryptopair(api_client, request):
    context = CleanupContext()
    def _register_ids(user_id=None, pair_id=None):
        if user_id: context.ids['user_id'] = user_id
        if pair_id: context.ids['pair_id'] = pair_id
    def _execute_cleanup():
        print(f'\n[DEBUG] Криптопара pair_id:{context.ids["pair_id"]} для пользователя с user_id:{context.ids["user_id"]} после теста удалена')
        if 'pair_id' in context.ids and 'user_id' in context.ids:
            url = UserEndpoints.delete_crypto_pair(
                context.ids['user_id'],
                context.ids['pair_id']
                )
            api_client.delete(url)
    request.addfinalizer(_execute_cleanup)
    return _register_ids

@pytest.fixture(scope='function')
def error_messages():
    class Messages:
        cryptopair = {
            'missing_user_id': 'user not provided',
            'wrong_user_id' : 'No User matches the given query.',
            'wrong_method' : 'Method "{}" not allowed.'
        }
    return Messages
