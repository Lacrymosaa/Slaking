import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QListWidget, QPushButton, QHBoxLayout, QLineEdit

class ListaAfazeres(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lista de Afazeres")
        self.resize(400, 300)

        # Cria o widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Cria o layout principal
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Cria o QTabWidget
        self.tab_widget = QTabWidget()

        # Cria as abas
        self.tab_dia = QWidget()
        self.tab_semana = QWidget()
        self.tab_geral = QWidget()
        self.tab_aleatoria = QWidget()

        # Adiciona as abas ao QTabWidget
        self.tab_widget.addTab(self.tab_dia, "Dia")
        self.tab_widget.addTab(self.tab_semana, "Semana")
        self.tab_widget.addTab(self.tab_geral, "Geral")
        self.tab_widget.addTab(self.tab_aleatoria, "Aleatória")

        # Cria os layouts para as abas
        self.layout_dia = QVBoxLayout()
        self.layout_semana = QVBoxLayout()
        self.layout_geral = QVBoxLayout()
        self.layout_aleatoria = QVBoxLayout()

        # Cria os QListWidgets para cada aba
        self.list_dia = QListWidget()
        self.list_semana = QListWidget()
        self.list_geral = QListWidget()
        self.list_aleatoria = QListWidget()

        # Adiciona os QListWidgets aos layouts das abas
        self.layout_dia.addWidget(self.list_dia)
        self.layout_semana.addWidget(self.list_semana)
        self.layout_geral.addWidget(self.list_geral)
        self.layout_aleatoria.addWidget(self.list_aleatoria)

        # Configura o layout das abas
        self.tab_dia.setLayout(self.layout_dia)
        self.tab_semana.setLayout(self.layout_semana)
        self.tab_geral.setLayout(self.layout_geral)
        self.tab_aleatoria.setLayout(self.layout_aleatoria)

        # Adiciona o QTabWidget ao layout principal
        self.layout.addWidget(self.tab_widget)

        # Cria um QLineEdit e um QPushButton para adicionar itens à lista
        self.line_edit = QLineEdit()
        self.add_button = QPushButton("Adicionar")

        # Cria um layout horizontal para o QLineEdit e QPushButton
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.line_edit)
        self.button_layout.addWidget(self.add_button)

        # Adiciona o layout horizontal ao layout principal
        self.layout.addLayout(self.button_layout)

        # Conecta o sinal de clique do QPushButton ao slot correspondente
        self.add_button.clicked.connect(self.adicionar_item)

    def adicionar_item(self):
        item = self.line_edit.text()
        current_tab = self.tab_widget.currentWidget()

        if current_tab == self.tab_dia:
            self.list_dia.addItem(item)
        elif current_tab == self.tab_semana:
            self.list_semana.addItem(item)
        elif current_tab == self.tab_geral:
            self.list_geral.addItem(item)
        elif current_tab == self.tab_aleatoria:
            self.list_aleatoria.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    lista_afazeres = ListaAfazeres()
    lista_afazeres.show()
    sys.exit(app.exec_())
