# ui/widgets/plot_widget.py (v5 - Depuração Final)

import pyqtgraph as pg
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                               QPushButton, QListWidgetItem, QLabel)
from PySide6.QtCore import Slot

class PlotWidget(QWidget):
    """
    Widget para plotar sinais CAN em tempo real.
    """
    def __init__(self, dbc_manager, parent=None):
        super().__init__(parent)
        self.dbc_manager = dbc_manager
        self.start_time = None
        self.plotted_signals = {}
        self.colors = ["#00A39A", "#E57373", "#64B5F6", "#FFB74D", "#81C784", "#BA68C8", "#4DD0E1", "#FFF176"]
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        control_panel_widget = QWidget()
        control_panel_widget.setMaximumWidth(250)
        control_panel = QVBoxLayout(control_panel_widget)
        control_panel.addWidget(QLabel("Sinais Disponíveis (DBC)"))
        self.signal_list_widget = QListWidget()
        self.signal_list_widget.itemDoubleClicked.connect(self.add_selected_signal)
        button_layout = QHBoxLayout()
        add_button = QPushButton("Adicionar")
        add_button.clicked.connect(self.add_selected_signal)
        clear_button = QPushButton("Limpar Gráfico")
        clear_button.clicked.connect(self.clear_all_signals)
        button_layout.addWidget(add_button)
        button_layout.addWidget(clear_button)
        control_panel.addWidget(self.signal_list_widget)
        control_panel.addLayout(button_layout)
        
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#1F232A')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setLabel('left', 'Valor')
        self.plot_widget.setLabel('bottom', 'Tempo (s)')
        self.plot_widget.addLegend()
        
        main_layout.addWidget(control_panel_widget)
        main_layout.addWidget(self.plot_widget)

    @Slot()
    def on_dbc_loaded(self):
        self.signal_list_widget.clear()
        self.clear_all_signals()
        signal_names = self.dbc_manager.get_signal_names()
        for name in signal_names:
            self.signal_list_widget.addItem(QListWidgetItem(name))

    @Slot()
    def add_selected_signal(self):
        selected_items = self.signal_list_widget.selectedItems()
        if not selected_items:
            return
        signal_name = selected_items[0].text()
        if signal_name in self.plotted_signals:
            print(f"[Plotter Debug] Sinal '{signal_name}' já está no gráfico.")
            return
        print(f"[Plotter Debug] Adicionando sinal '{signal_name}' ao gráfico.")
        color = self.colors[len(self.plotted_signals) % len(self.colors)]
        curve = self.plot_widget.plot(pen=pg.mkPen(color, width=2), name=signal_name)
        self.plotted_signals[signal_name] = {'x_data': [], 'y_data': [], 'curve': curve}

    @Slot(object)
    def add_data_point(self, msg):
        """ Adiciona um novo ponto de dados ao gráfico, com mensagens de depuração. """
        if not self.plotted_signals:
            return

        if self.start_time is None:
            self.start_time = msg.timestamp
        relative_time = msg.timestamp - self.start_time

        decoded_data = self.dbc_manager.decode_message(msg)
        if not decoded_data:
            return

        # --- LINHA DE DEPURAÇÃO ADICIONADA ---
        # Vamos inspecionar o que o DBCManager está a retornar.
        if msg.arbitration_id == 151: # Mostra apenas para a ID que nos interessa
             print(f"[Plotter Debug] Dados decodificados para ID 151: {decoded_data}")
        # ------------------------------------

        for signal_name, value in decoded_data.items():
            if signal_name in self.plotted_signals:
                print(f"[Plotter Debug] ATUALIZANDO GRÁFICO -> Sinal: {signal_name}, Valor: {value}, Tempo: {relative_time:.2f}")
                self.plotted_signals[signal_name]['x_data'].append(relative_time)
                self.plotted_signals[signal_name]['y_data'].append(value)
                self.plotted_signals[signal_name]['curve'].setData(
                    self.plotted_signals[signal_name]['x_data'],
                    self.plotted_signals[signal_name]['y_data']
                )

    def clear_plot_data(self):
        self.start_time = None
        for signal_name in self.plotted_signals:
            self.plotted_signals[signal_name]['x_data'] = []
            self.plotted_signals[signal_name]['y_data'] = []
            self.plotted_signals[signal_name]['curve'].setData([], [])

    def clear_all_signals(self):
        self.plot_widget.clear()
        self.plotted_signals = {}
        self.start_time = None
        self.plot_widget.addLegend()
