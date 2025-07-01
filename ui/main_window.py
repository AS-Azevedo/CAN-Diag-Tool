# ui/main_window.py (v8 - Com Relatório de Erros)

import os
import qtawesome as qta
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget, 
                               QStatusBar, QMenuBar, QMessageBox, QFileDialog)
from PySide6.QtGui import QAction
from PySide6.QtCore import Slot

from core.can_bus_manager import CANBusManager
from core.dbc_manager import DBCManager
from ui.widgets.trace_widget import TraceWidget
from ui.widgets.plot_widget import PlotWidget
from ui.widgets.transmitter_widget import TransmitterWidget

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CAN-Spector Pro")
        self.setWindowIcon(qta.icon('fa5s.microscope', color='#00A39A'))
        self.resize(1200, 800)

        self.can_manager = CANBusManager(self)
        self.dbc_manager = DBCManager(self)

        self.setup_ui()
        self.create_actions()
        self.create_menus()
        self.connect_signals()
        self.update_ui_state(False)

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.tab_widget = QTabWidget()

        self.trace_widget = TraceWidget(self.dbc_manager)
        self.plot_widget = PlotWidget(self.dbc_manager)
        self.transmitter_widget = TransmitterWidget()

        self.tab_widget.addTab(self.trace_widget, qta.icon('fa5s.stream', color='white'), "Trace")
        self.tab_widget.addTab(self.plot_widget, qta.icon('fa5s.chart-line', color='white'), "Plotter")
        self.tab_widget.addTab(self.transmitter_widget, qta.icon('fa5s.paper-plane', color='white'), "Transmitter")
        
        self.layout.addWidget(self.tab_widget)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto. Carregue um ficheiro DBC ou conecte-se a um barramento CAN.")

    def create_actions(self):
        self.load_dbc_action = QAction(qta.icon('fa5s.database', color='#00A39A'), "Carregar DBC...", self)
        self.connect_action = QAction(qta.icon('fa5s.plug', color='#00A39A'), "&Conectar ao Simulador", self)
        self.disconnect_action = QAction(qta.icon('fa5s.unlink', color='#E57373'), "&Desconectar", self)
        self.exit_action = QAction(qta.icon('fa5s.times-circle'), "&Sair", self)
        self.about_action = QAction(qta.icon('fa5s.info-circle'), "&Sobre", self)

    def create_menus(self):
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("&Arquivo")
        file_menu.addAction(self.load_dbc_action)
        file_menu.addSeparator()
        file_menu.addAction(self.connect_action)
        file_menu.addAction(self.disconnect_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        help_menu = self.menu_bar.addMenu("&Ajuda")
        help_menu.addAction(self.about_action)

    def connect_signals(self):
        """ Conecta todos os sinais e slots da aplicação. """
        # Ações do menu
        self.load_dbc_action.triggered.connect(self.load_dbc_file)
        self.connect_action.triggered.connect(self.connect_to_virtual_bus)
        self.disconnect_action.triggered.connect(self.disconnect_from_bus)
        self.exit_action.triggered.connect(self.close)
        self.about_action.triggered.connect(self.show_about_dialog)
        
        # Sinais do CAN Manager
        self.can_manager.message_received.connect(self.trace_widget.add_message)
        self.can_manager.message_received.connect(self.plot_widget.add_data_point)

        # Sinais do DBC Manager
        self.dbc_manager.dbc_loaded.connect(self.on_dbc_loaded)
        self.dbc_manager.dbc_load_error.connect(lambda error: self.status_bar.showMessage(error))
        # --- NOVA CONEXÃO ---
        # Conecta o novo sinal de erro à barra de status.
        self.dbc_manager.decode_error.connect(self.status_bar.showMessage)


    @Slot()
    def on_dbc_loaded(self):
        """ Chamado quando o DBC é carregado, atualiza a UI. """
        self.status_bar.showMessage("DBC carregado com sucesso. Sinais disponíveis no Plotter.")
        self.plot_widget.on_dbc_loaded()

    @Slot()
    def load_dbc_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Selecionar Ficheiro DBC", "", "Ficheiros de Base de Dados CAN (*.dbc)")
        if filepath:
            self.dbc_manager.load_file(filepath)

    @Slot()
    def connect_to_virtual_bus(self):
        """ Inicia a conexão, limpando os dados antigos. """
        self.trace_widget.clear_trace()
        self.plot_widget.clear_plot_data()
        self.can_manager.connect()

    @Slot()
    def disconnect_from_bus(self):
        self.can_manager.disconnect()

    @Slot(bool)
    def update_ui_state(self, is_connected):
        self.connect_action.setEnabled(not is_connected)
        self.disconnect_action.setEnabled(is_connected)

    @Slot()
    def show_about_dialog(self):
        QMessageBox.about(self, "Sobre o CAN-Spector Pro", "<h3>CAN-Spector Pro v1.0 (Fase 2)</h3><p>Analisador de Rede CAN com UI Avançada.</p>")

    def closeEvent(self, event):
        self.disconnect_from_bus()
        event.accept()
