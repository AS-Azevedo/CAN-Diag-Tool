# ui/widgets/transmitter_widget.py (v2 - Funcional)

import can
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
                               QLineEdit, QCheckBox, QPushButton, QSpinBox, QMessageBox)
from PySide6.QtGui import QIntValidator, QFont
from PySide6.QtCore import Signal, Slot

class TransmitterWidget(QWidget):
    """
    Widget para construir e enviar mensagens CAN.
    """
    # Sinal emitido com um objeto can.Message pronto para ser enviado.
    send_can_message = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """ Configura a interface do widget de transmissão. """
        main_layout = QVBoxLayout(self)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        # --- Linha 1: ID da Mensagem ---
        grid_layout.addWidget(QLabel("ID da Arbitragem (Hex):"), 0, 0)
        self.id_input = QLineEdit("000")
        self.id_input.setFont(QFont("Courier New", 10))
        grid_layout.addWidget(self.id_input, 0, 1)

        self.extended_id_check = QCheckBox("ID Estendido (29-bit)")
        grid_layout.addWidget(self.extended_id_check, 0, 2)

        # --- Linha 2: DLC (Tamanho dos Dados) ---
        grid_layout.addWidget(QLabel("DLC (0-8):"), 1, 0)
        self.dlc_spinner = QSpinBox()
        self.dlc_spinner.setRange(0, 8)
        self.dlc_spinner.setValue(8)
        self.dlc_spinner.valueChanged.connect(self.update_data_fields)
        grid_layout.addWidget(self.dlc_spinner, 1, 1)

        # --- Linha 3: Campos de Dados ---
        grid_layout.addWidget(QLabel("Dados (Hex):"), 2, 0)
        data_layout = QHBoxLayout()
        self.data_inputs = []
        # Validador para aceitar apenas 2 caracteres hexadecimais
        hex_validator = QIntValidator(0, 255) 

        for i in range(8):
            byte_input = QLineEdit("00")
            byte_input.setFont(QFont("Courier New", 10))
            byte_input.setInputMask("HH") # Aceita apenas 2 caracteres hex
            self.data_inputs.append(byte_input)
            data_layout.addWidget(byte_input)
        
        grid_layout.addLayout(data_layout, 2, 1, 1, 2) # Ocupa 2 colunas

        # --- Linha 4: Botão de Envio ---
        self.send_button = QPushButton("Enviar Mensagem")
        self.send_button.setFixedHeight(40)
        self.send_button.clicked.connect(self.on_send_clicked)
        
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.send_button)
        self.setLayout(main_layout)
        
        # Estado inicial dos campos de dados
        self.update_data_fields(self.dlc_spinner.value())

    @Slot(int)
    def update_data_fields(self, dlc):
        """ Habilita/desabilita os campos de dados com base no DLC. """
        for i, field in enumerate(self.data_inputs):
            field.setEnabled(i < dlc)

    @Slot()
    def on_send_clicked(self):
        """ Valida os dados e emite o sinal para enviar a mensagem. """
        try:
            # Valida e converte a ID
            arbitration_id = int(self.id_input.text(), 16)

            # Valida e converte os dados
            dlc = self.dlc_spinner.value()
            data_bytes = []
            for i in range(dlc):
                byte_str = self.data_inputs[i].text()
                if not byte_str: # Se o campo estiver vazio, considera como 0
                    byte_str = "0"
                data_bytes.append(int(byte_str, 16))

            # Cria o objeto can.Message
            message = can.Message(
                arbitration_id=arbitration_id,
                is_extended_id=self.extended_id_check.isChecked(),
                dlc=dlc,
                data=data_bytes
            )

            # Emite o sinal com a mensagem pronta
            self.send_can_message.emit(message)

        except ValueError:
            QMessageBox.critical(self, "Erro de Formato", "ID ou Dados inválidos. Por favor, use apenas caracteres hexadecimais (0-9, A-F).")
        except Exception as e:
            QMessageBox.critical(self, "Erro Inesperado", f"Ocorreu um erro: {e}")
