import face_recognition
import os

# open("encod.txt", 'w')
encod_file = "encod.txt"

def get_existing_users():
    existing_users = set()
    if os.path.exists(encod_file):
        with open(encod_file, "r", encoding="utf-8") as f:
            for line in f:
                if ':' in line:
                    username = line.split(':')[0]
                    if '#' in username:
                        username = username.split('#')[0]
                    existing_users.add(username)
    return existing_users

def user_exists(username, existing_users):
    return username in existing_users

def add_encoding(username, encoding_str):
    with open(encod_file, "a", encoding="utf-8") as file:
        file.write(f"{username}:[{encoding_str}]\n")

existing_users = get_existing_users()
print(f"Существующие пользователи: {existing_users}")
print("-" * 50)

processed_count = 0
skipped_count = 0
new_count = 0

for filename in os.listdir("faces"):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        path = os.path.join("faces", filename)
        
        username = filename.split('.')[0]
        
        if user_exists(username, existing_users):
            print(f"Пропущен (уже существует): {filename} (пользователь: {username})")
            skipped_count += 1
            continue
        
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        
        if len(encodings) > 0:
            emb = encodings[0]
            emb_str = ' '.join([f"{x:.8f}" for x in emb])
            
            add_encoding(filename, emb_str)
            print(f"Сохранен: {filename} (пользователь: {username})")
            new_count += 1
            
            existing_users.add(username)
        else:
            print(f"Лицо не найдено: {filename}")
        
        processed_count += 1

print("-" * 50)
print(f"Всего обработано: {processed_count}")
print(f"Новых добавлено: {new_count}")
print(f"Пропущено (существуют): {skipped_count}")