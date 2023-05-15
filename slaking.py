import sys
import getpass
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QListWidget, QDialog, QDialogButtonBox, QMessageBox, QSizePolicy, QSpacerItem

class NewListDialog(QDialog):
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

    def get_list_name(self):
        return self.new_list_name_input.text()


class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.lists = {}
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.tab_widget = QTabWidget()

        self.general_list_widget = QListWidget()
        self.tab_widget.addTab(self.general_list_widget, "Geral")
        self.lists["Geral"] = self.general_list_widget

        self.layout.addWidget(self.tab_widget)

        self.button_layout = QHBoxLayout()
        self.new_list_button = QPushButton("+")
        self.new_list_button.setFixedSize(23, 23)
        self.tab_widget.setCornerWidget(self.new_list_button)      

        self.remove_list_button = QPushButton("-")
        self.remove_list_button.setFixedSize(23, 23)
        self.tab_widget.setCornerWidget(self.remove_list_button)

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

        self.new_list_button.clicked.connect(self.show_new_list_dialog)
        self.remove_list_button.clicked.connect(self.remove_list)
        self.add_item_button.clicked.connect(self.add_item)
        self.add_item_name_input.returnPressed.connect(self.add_item)

    def show_new_list_dialog(self):
        dialog = NewListDialog(self)
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


    def add_list(self, list_name):
        if list_name and list_name not in self.lists:
            list_widget = QListWidget()
            self.tab_widget.addTab(list_widget, list_name)
            self.lists[list_name] = list_widget

    def add_item(self):
        current_tab_index = self.tab_widget.currentIndex()
        current_list_widget = self.tab_widget.widget(current_tab_index)
        item_name = self.add_item_name_input.text()
        if current_list_widget is not None and item_name:
            current_list_widget.addItem(" - " + item_name.capitalize())
        self.add_item_name_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    todo_list = ToDoList()
    window.setCentralWidget(todo_list)
    user = getpass.getuser()
    window.setWindowTitle(f"Slaking de {user}")
    window.show()
    sys.exit(app.exec_())
