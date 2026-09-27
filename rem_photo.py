import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class FacesManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление фото faces")
        self.setGeometry(300, 100, 800, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout()
        central.setLayout(layout)
        
        self.faces_dir = "faces"
        

        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        self.refresh_btn = QPushButton("Обновить список")
        self.refresh_btn.clicked.connect(self.load_files)
        left_layout.addWidget(self.refresh_btn)
        
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.show_photo)
        left_layout.addWidget(self.file_list)
        
        btn_layout = QHBoxLayout()
        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_selected)
        self.close_btn = QPushButton("Закрыть")
        self.close_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.close_btn)
        left_layout.addLayout(btn_layout)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        self.photo_label = QLabel("Выберите фото для просмотра")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        self.photo_label.setMinimumSize(400, 400)
        right_layout.addWidget(self.photo_label)
        
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)
        layout.setStretch(0, 1)
        layout.setStretch(1, 2)
        
        self.load_files()
    
    def get_groups(self):
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)
            return {}
        
        groups = {}
        for file in os.listdir(self.faces_dir):
            file_path = os.path.join(self.faces_dir, file)
            if os.path.isfile(file_path):
                if '#' in file:
                    base = file.split('#')[0]
                else:
                    base = file
                
                if base not in groups:
                    groups[base] = []
                groups[base].append(file)
        
        return groups
    
    def load_files(self):
        self.file_list.clear()
        groups = self.get_groups()
        
        for base_name, files in groups.items():
            if len(files) == 1:
                text = files[0]
            else:
                text = f"{base_name} ({len(files)} файлов)"
            
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, files)
            self.file_list.addItem(item)
    
    def show_photo(self, item):
        files = item.data(Qt.UserRole)
        
        if len(files) > 1:
            file_to_show, ok = QInputDialog.getItem(self, "Выбор фото", 
                                                   "Какое фото показать?",
                                                   files, 0, False)
            if not ok:
                return
        else:
            file_to_show = files[0]
        
        path = os.path.join(self.faces_dir, file_to_show)
        

        pixmap = QPixmap(path)
        if not pixmap.isNull():

            pixmap = pixmap.scaled(self.photo_label.size(), 
                                  Qt.KeepAspectRatio, 
                                  Qt.SmoothTransformation)
            self.photo_label.setPixmap(pixmap)
        else:
            self.photo_label.setText("Не удалось загрузить фото")
    
    def delete_selected(self):
        selected = self.file_list.currentItem()
        if selected:
            files = selected.data(Qt.UserRole)
            for file in files:
                path = os.path.join(self.faces_dir, file)
                os.remove(path)
            self.load_files()
            self.photo_label.clear()
            self.photo_label.setText("Выберите фото для просмотра")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FacesManager()
    window.show()
    sys.exit(app.exec_())