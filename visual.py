import sys
from PyQt5.QtWidgets import *
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Нейросеть")
        self.setGeometry(400, 200, 450, 350)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        self.input_label = QLabel("Введите имя нового пользователя:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Имя пользователя...")
        
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_field)
        
        self.btn1 = QPushButton("Добавить пользователя")
        self.btn2 = QPushButton("Тренировать нейросеть")
        self.btn3 = QPushButton("Запустить распознавание")
        self.btn4 = QPushButton("Просмотр пользователей")
        self.btn5 = QPushButton("Выйти")

        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        layout.addWidget(self.btn4)
        layout.addWidget(self.btn5)

        self.output = QLabel("Команда выполнена")
        self.output.setStyleSheet("border: 1px solid gray; padding: 8px; background-color: #f0f0f0;")
        layout.addWidget(self.output)
        
        self.btn1.clicked.connect(self.add_user)
        self.btn2.clicked.connect(self.train)
        self.btn3.clicked.connect(self.recognize)
        self.btn4.clicked.connect(self.photo)
        self.btn5.clicked.connect(self.exit)
        
    def add_user(self):
        name = self.input_field.text()
        if name:
            self.output.setText(f"Команда выполнена: добавлен пользователь '{name}'")
            subprocess.run(['python', 'photo.py', name])
        else:
            self.output.setText("Команда не выполнена: Нет имени")
        
    def train(self):
        subprocess.run(['python', 'encod.py'])
        self.output.setText("Команда выполнена: тренировка нейросети")
        QMessageBox.information(self, "Успешно", "Новые пользователи успешно добавлены в нейросеть")
        
    def recognize(self):
        subprocess.run(['python', 'recognition.py'])
        self.output.setText("Команда выполнена: запуск распознавания")
    def exit(self):
        QApplication.quit()
        QApplication.exit()
    def photo(self):
        subprocess.run(['python', 'rem_photo.py'])
        self.output.setText("Команда выполнена: Просмотр фото")
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())