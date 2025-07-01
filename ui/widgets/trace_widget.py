# ui/widgets/trace_widget.py (v6 - Adaptado ao Plotter)

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

class TraceWidget(QWidget):
    """
    Widget que exibe as mensagens CAN em uma tabela, com timestamps relativos.
    """
    def __init__(self, dbc_manager, parent=None):
        super().__init__(parent)
        self.dbc_manager = dbc_manager
        self.start_time = None
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do widget, incluindo o cabeçalho da tabela."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.model = QStandardItemModel(0, 6) 
        self.model.setHorizontalHeaderLabels([
            "Timestamp (s)", "ID (Hex)", "Tipo", "DLC", "Dados (Hex)", "Sinais Decodificados"
        ])

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.verticalHeader().setVisible(False)
        
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        layout.addWidget(self.table_view)

    def add_message(self, msg):
        """
        Adiciona uma nova mensagem CAN à tabela, calculando o timestamp relativo.
        """
        if self.start_time is None:
            self.start_time = msg.timestamp
        relative_time = msg.timestamp - self.start_time

        # --- ALTERAÇÃO: Agora formata o dicionário recebido em texto ---
        decoded_data = self.dbc_manager.decode_message(msg)
        if decoded_data:
            decoded_text = ", ".join([f"{name}: {value:.2f}" for name, value in decoded_data.items()])
        else:
            decoded_text = ""

        timestamp_item = QStandardItem(f"{relative_time:.4f}")
        id_item = QStandardItem(f"{msg.arbitration_id:04X}")
        type_item = QStandardItem("Ext" if msg.is_extended_id else "Std")
        dlc_item = QStandardItem(str(msg.dlc))
        data_item = QStandardItem(msg.data.hex(' ').upper())
        decoded_item = QStandardItem(decoded_text)
        
        id_item.setTextAlignment(Qt.AlignCenter)
        type_item.setTextAlignment(Qt.AlignCenter)
        dlc_item.setTextAlignment(Qt.AlignCenter)

        self.model.appendRow([timestamp_item, id_item, type_item, dlc_item, data_item, decoded_item])
        
        scrollbar = self.table_view.verticalScrollBar()
        if scrollbar.value() == scrollbar.maximum():
            self.table_view.scrollToBottom()

    def clear_trace(self):
        """ Limpa todas as mensagens da tabela e reinicia o tempo de início. """
        self.start_time = None
        self.model.removeRows(0, self.model.rowCount())
