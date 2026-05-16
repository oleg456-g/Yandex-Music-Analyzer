from yandex_music import Client
import time

def on_code(code):
    print(f'Откройте {code.verification_url} и введите код: {code.user_code}')

def main():
    client = Client()
    token = client.device_auth(on_code=on_code)
    with open("parse_music_database/secret.py", 'w+') as f:
        print(f"# Tokens were got in {time.asctime()}", file=f)
        print(f'access_token = "{token.access_token}"', file=f)
        print(f'refresh_token = "{token.refresh_token}"', file=f)
        print(f'expires_in = {token.expires_in}', file=f)
    client.init()

if __name__ == '__main__':
    main()