class Settings():
    def __init__(self):
        self.ip_addr = '207.246.79.176'
        self.port = '8000'
    @property
    def API_BASE_URL(self)-> str:
        return f'http://{self.ip_addr}:{self.port}'
        
settings = Settings()