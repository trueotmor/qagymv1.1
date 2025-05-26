from api.endpoints.endpoints import UserEndpoints
from data.payloads_loader import load_payload
from utils.http_status_codes import HTTPStatus
from data.queries.get_cryptopair import get_user_id_queries
import random
import logging

class TestCryptoPairAPI:
    def test_create_cryptopair(
            self,
            api_client,
            create_cryptopar_dinamic_data,
            cleanup_cryptopair
            ):
        # Очередность действий в тесте
        # 1. Узнать какие ID пользователей доступны для теста 
        # 2. Выбрать пользователя
        # 3. Проверить у выбранного пользователя наличие свобоных криптопар для теста
        # 4. Выбрать криптопару для теста
        # 5. Имея ID пользователя, и криптопару сформировать пэйлоад,
        # добавить в него остальные поля с динамикой
        # 6. При успешном создании криптопары, запомнить ID пользователя и ID криптопары
        # для удаления после теста
        # 7. Произвести проверку полученной криптопары
        # 8. Удалить тестовую криптопару
        
        payload = load_payload(
            "cryptopairs",
            "create_cryptopair",
             create_cryptopar_dinamic_data)
        url = UserEndpoints.create_crypto_pair()
        response = api_client.post(url, json=payload)
        response_data = response.json()
        cleanup_cryptopair(user_id=response_data["user_id"], pair_id=response_data["pair_id"])
        assert response.status_code == HTTPStatus.CREATED
        assert response_data["user_id"] == payload["user_id"]
    
    def test_get_cryptopairs_0(self, api_client, all_users):
        logging.basicConfig(level=logging.DEBUG)
        url = UserEndpoints.get_crypto_pairs(get_user_id_queries('random_user', all_users))
        response = api_client.get(url)
        assert response.status_code == HTTPStatus.OK

    def test_get_cryptopairs_1(self, api_client, all_users):
        logging.basicConfig(level=logging.DEBUG)
        url = UserEndpoints.get_crypto_pairs(get_user_id_queries('random_user', all_users))
        response = api_client.get(url)
        assert response.status_code == HTTPStatus.OK

    def test_get_cryptopair_without_user_id(self, api_client, error_messages):
        logging.basicConfig(level=logging.DEBUG)
        url = UserEndpoints.get_crypto_pairs(get_user_id_queries('missing_user_id'))
        response = api_client.get(url)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["error"] == error_messages.cryptopair['missing_user_id']

    def test_get_cryptopair_with_unregistered_user_id(self, api_client, error_messages, all_users):
        logging.basicConfig(level=logging.DEBUG)
        url = UserEndpoints.get_crypto_pairs(get_user_id_queries('wrong_user_id', all_users))
        response = api_client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["detail"] == error_messages.cryptopair['wrong_user_id']
        
    def test_get_cryptopair_with_wrong_method(self, api_client, error_messages, all_users):
        logging.basicConfig(level=logging.DEBUG)
        random_method = random.choice(['post', 'put', 'patch', 'delete'])
        url = UserEndpoints.get_crypto_pairs(get_user_id_queries('random_user', all_users))                
        response = getattr(api_client, random_method)(url)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        assert response.json()["detail"] == error_messages.cryptopair['wrong_method'].format(random_method.upper())
