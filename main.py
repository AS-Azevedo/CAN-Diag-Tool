# main.py (v4 - Final)

import sys
import os
from PySide6.QtWidgets import QApplication

# Passo 1: Garantir que o Python encontra os nossos pacotes 'core' e 'ui'.
# Adiciona o diretório raiz do projeto ao caminho de busca do Python.
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Passo 2: Importar a nossa janela principal.
# Esta linha só funciona porque fizemos o Passo 1.
from ui.main_window import MainWindow

def load_stylesheet(app):
    """Carrega a nossa folha de estilos customizada."""
    try:
        stylesheet_path = os.path.join(project_root, "assets", "dark_theme.qss")
        with open(stylesheet_path, "r") as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Aviso: 'assets/dark_theme.qss' não encontrado. Usando estilo padrão.")
    except Exception as e:
        print(f"Erro ao carregar folha de estilos: {e}")

def main():
    """
    O ponto de entrada que cria e executa a aplicação.
    """
    # Cria a instância da aplicação.
    app = QApplication(sys.argv)

    # Carrega o nosso tema visual.
    load_stylesheet(app)

    # Cria a janela principal.
    window = MainWindow()

    # Mostra a janela.
    window.show()

    # Inicia o loop de eventos do Qt e espera até que o utilizador feche a janela.
    # O sys.exit garante uma saída limpa.
    sys.exit(app.exec())

# Este é o ponto de partida padrão para um script Python.
# Garante que a função main() só é chamada quando executamos "python main.py".
if __name__ == "__main__":
    main()
