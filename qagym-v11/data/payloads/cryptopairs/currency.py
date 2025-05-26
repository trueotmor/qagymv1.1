base = ["RUB", "USDT"]
crypto = ["BTC", "ETH", "TON"]

class Currency:
    def __init__(self, base_currencies = None, crypto_currencies = None):

        self.base_currencies =  base_currencies or []
        self.crypto_currencies = crypto_currencies or []

    def add_base_currency(self, currency):        
        if currency not in self.base_currencies:
            self.base_currencies.append(currency)

    def add_crypto_currency(self, currency):        
        if currency not in self.crypto_currencies:
            self.crypto_currencies.append(currency)

    def get_pairs(self):
        return [(crypto, base) for crypto in self.base_currencies for base in self.crypto_currencies]
    
all_cryptopais = set(Currency(crypto, base).get_pairs())

