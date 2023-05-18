import sys
import getpass
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QListWidget, QDialog, QDialogButtonBox, QMessageBox

class NewList(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Slaking criará uma lista!")
        self.layout = QVBoxLayout()
        self.new_list_name_input = QLineEdit()
        self.layout.addWidget(QLabel("Nome da Nova Lista:"))
        self.layout.addWidget(self.new_list_name_input)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout.addWidget(button_box)
        self.setLayout(self.layout)
        # Conectar evento closeEvent ao método delete_checked_items
        self.closeEvent = lambda event: self.delete_checked_items()

    def get_list_name(self):
        return self.new_list_name_input.text()
    # Responsavel por pegar o nome da nova lista na classe e retorna-la para ser aderida na janela
    


class Slaking(QWidget):
    def __init__(self):
        super().__init__()
        self.lists = {}
        self.setup_ui()
        # Conecta a função update_current_list na troca de abas
        self.tab_widget.currentChanged.connect(self.update_current_list)

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.tab_widget = QTabWidget()

        self.button_container = QWidget()
        self.button_layout = QHBoxLayout(self.button_container)
        self.button_layout.setAlignment(Qt.AlignLeft)
        # Botões de nova lista e remover lista
        self.new_list_button = QPushButton("+")
        self.new_list_button.setFixedSize(23, 23)
        self.remove_list_button = QPushButton("-")
        self.remove_list_button.setFixedSize(23, 23)
        self.button_layout.addWidget(self.new_list_button)
        self.button_layout.addWidget(self.remove_list_button)

        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.button_container)

        self.add_item_widget = QWidget()
        self.add_item_layout = QHBoxLayout()

        self.add_item_name_label = QLabel("Item:")
        self.add_item_name_input = QLineEdit()
        self.add_item_button = QPushButton("Adicionar Item")

        self.add_item_layout.addWidget(self.add_item_name_label)
        self.add_item_layout.addWidget(self.add_item_name_input)
        self.add_item_layout.addWidget(self.add_item_button)
        self.add_item_widget.setLayout(self.add_item_layout)

        self.layout.addWidget(self.add_item_widget)

        self.setLayout(self.layout)

        # Conecta as funções aos botões
        self.new_list_button.clicked.connect(self.show_new_list_dialog)
        self.add_item_button.clicked.connect(self.add_item)
        self.remove_list_button.clicked.connect(self.remove_list)
        self.add_item_name_input.returnPressed.connect(self.add_item)

        # Parte do código responsável por fazer o evento doubleclick marcar o item da lista
        def connect_item_double_clicked():
            current_list_widget = self.tab_widget.currentWidget()
            if current_list_widget is not None:
                current_list_widget.itemDoubleClicked.connect(self.toggle_item_strikeout)
        
        self.tab_widget.currentChanged.connect(connect_item_double_clicked)
        connect_item_double_clicked()

    # Chama a classe NewList para criar uma nova lista e chama add_list para que ela seja adicionada as abas
    def show_new_list_dialog(self):
        dialog = NewList(self)
        if dialog.exec_() == QDialog.Accepted:
            list_name = dialog.get_list_name()
            self.add_list(list_name)

    def remove_list(self):
        current_tab_index = self.tab_widget.currentIndex()
        current_list_widget = self.tab_widget.widget(current_tab_index)
        current_list_name = self.tab_widget.tabText(current_tab_index)
        if current_list_widget is not None:
            message_box = QMessageBox()
            message_box.setWindowTitle("Remover Lista")
            message_box.setText(f"Deseja remover a lista '{current_list_name}'?")
            message_box.setIcon(QMessageBox.Warning)
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message_box.setDefaultButton(QMessageBox.No)
            if message_box.exec_() == QMessageBox.Yes:
                self.tab_widget.removeTab(current_tab_index)
                self.lists.pop(current_list_name)  # Remove a lista do dicionário

                # Remove a lista do arquivo JSON
                with open("lists.json", "r") as file:
                    data = json.load(file)
                if current_list_name in data:
                    data.pop(current_list_name)
                    with open("lists.json", "w") as file:
                        json.dump(data, file)

    def add_list(self, list_name):
        if list_name not in self.lists:
            list_widget = QListWidget()
            self.tab_widget.addTab(list_widget, list_name) # Adiciona aba 
            self.lists[list_name] = list_widget 

    def add_item(self):
        current_tab_index = self.tab_widget.currentIndex()
        current_list_widget = self.tab_widget.widget(current_tab_index)
        item_name = self.add_item_name_input.text()
        if current_list_widget is not None and item_name:
            current_list_widget.addItem(" - " + item_name.capitalize())
            self.save_lists()
        self.add_item_name_input.clear()

    def toggle_item_strikeout(self, item):
        font = item.font()
        if font.strikeOut():
            font.setStrikeOut(False)
        else:
            font.setStrikeOut(True)
        item.setFont(font)

        # Remove os itens marcados da lista quando o programa for fechado
        app = QApplication.instance()
        app.aboutToQuit.connect(self.remove_marked_items)

    def update_current_list(self, index):
        current_list_widget = self.tab_widget.currentWidget()
        if current_list_widget is not None:
            # Limpa a conexão com o sinal itemDoubleClicked para evitar duplicação
            current_list_widget.itemDoubleClicked.disconnect()
            # Conecta o sinal itemDoubleClicked com a função toggle_item_strikeout
            current_list_widget.itemDoubleClicked.connect(self.toggle_item_strikeout)
    
    def remove_marked_items(self):
        for list_widget in self.lists.values():
            for i in reversed(range(list_widget.count())):
                item = list_widget.item(i)
                if item.font().strikeOut():
                    list_widget.takeItem(i)
        self.save_lists()

    def save_lists(self):
        data = {}
        for list_name, list_widget in self.lists.items():
            items = [list_widget.item(i).text() for i in range(list_widget.count())]
            data[list_name] = items

        with open("lists.json", "w") as file:
            json.dump(data, file)

    def load_lists(self):
        try:
            with open("lists.json", "r") as file:
                data = file.read()
                if data:
                    data = json.loads(data)
                    for list_name, items in data.items():
                        list_widget = QListWidget()
                        for item in items:
                            list_widget.addItem(item)
                        self.tab_widget.addTab(list_widget, list_name)
                        self.lists[list_name] = list_widget
        except (FileNotFoundError, json.JSONDecodeError):
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    todo_list = Slaking()
    todo_list.load_lists() # Carrega as listas salvas anteriormente
    window.setCentralWidget(todo_list)
    user = getpass.getuser()
    window.setWindowTitle(f"Slaking de {user}")
    window.show()
    sys.exit(app.exec_())