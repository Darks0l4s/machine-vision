import subprocess
text = "1. Добавить пользователя\n2. Синхронизировать распознование\n3. Распознование\n4. Выйти\n"
while (True):
    enter = input(text)
    if enter=="1":
        subprocess.run(['python', 'photo.py'])
    if enter=="2":
        subprocess.run(['python', 'encod.py'])
    if enter=="3":
        subprocess.run(['python', 'recognition.py'])
    if enter=="4":
        print("Пока")
        break
