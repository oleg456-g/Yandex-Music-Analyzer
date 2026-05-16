from yandex_music import Client
from secret import access_token
from sys import exit
import os

def download_tracks(liked_tracks):
    output_dir = 'yandex_music_database'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print(f"Найдено треков для скачивания: {len(liked_tracks)}")
    for i, item in enumerate(liked_tracks, 1):
        track = item.fetch_track()
        if track and track.available:
            artists = "_".join([artist.name for artist in track.artists])
            filename = f"{artists} - {track.title}.mp3"
            filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c in ' .-_()']).strip()
            filepath = os.path.join(output_dir, filename)
            if not os.path.exists(filepath):
                print(f"[{i}/{len(liked_tracks)}] Скачиваю: {filename}...")
                track.download(filepath, codec='mp3', bitrate_in_kbps=192) # 192 или 320 кбит/с
            else:
                print(f"[{i}/{len(liked_tracks)}] Уже скачан: {filename}")
    

def main():
    try:
        client = Client(access_token).init()
    except:
        print("Не смогли зайти в аккаунт")
    else:
        print(f"Успешный вход под аккаунтом: {client.me.account.full_name}")
        liked_tracks = client.users_likes_tracks()
        if not liked_tracks:
            print("Твой плейлист 'Мне нравится' пуст")
            exit()

        print("Скачиваем плейлист 'Мне нравится'...")
        download_tracks(liked_tracks)

if __name__ == '__main__':
    main()