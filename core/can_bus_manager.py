# core/can_bus_manager.py (v8 - Com Função de Envio)

import can
import time
from PySide6.QtCore import QObject, Signal, QTimer, Slot

class CANBusManager(QObject):
    """
    Gerencia a conexão e o envio de mensagens.
    Usa um 'loopback manual' para garantir que os dados do simulador
    cheguem à UI, contornando problemas da biblioteca python-can.
    """
    message_received = Signal(object)
    status_updated = Signal(str)
    connection_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bus = None
        self.is_connected = False
        self.simulator_timer = QTimer(self)
        self.simulator_timer.timeout.connect(self.send_simulated_messages)
        self.simulated_ids = [0x100, 0x2A5, 151]
        self.counter = 0

    def connect(self, channel='vcan0', bustype='virtual', bitrate=500000):
        if self.is_connected:
            self.disconnect()
        try:
            self.bus = can.interface.Bus(bustype='virtual', channel='vcan0')
            self.status_updated.emit("Conectado ao simulador (Loopback Manual Ativo)")
            self.simulator_timer.start(250)
            self.is_connected = True
            self.connection_changed.emit(True)
            print("[Info] Conexão estabelecida. Loopback manual está a operar.")
        except Exception as e:
            self.status_updated.emit(f"Erro ao criar barramento virtual: {e}")
            self.is_connected = False
            self.connection_changed.emit(False)

    def disconnect(self):
        if self.simulator_timer.isActive():
            self.simulator_timer.stop()
        if self.bus:
            self.bus.shutdown()
            self.bus = None
        self.is_connected = False
        self.status_updated.emit("Desconectado")
        self.connection_changed.emit(False)

    # --- NOVO SLOT PÚBLICO ---
    @Slot(object)
    def send_message(self, msg: can.Message):
        """ Envia uma mensagem CAN fornecida pela UI. """
        if not self.is_connected or not self.bus:
            self.status_updated.emit("Erro: Não conectado. Não é possível enviar a mensagem.")
            return
        
        try:
            self.bus.send(msg)
            # Emite a mensagem enviada de volta para a UI (para aparecer no trace)
            self.message_received.emit(msg)
            self.status_updated.emit(f"Mensagem {msg.arbitration_id:X} enviada com sucesso.")
        except can.CanError as e:
            self.status_updated.emit(f"Erro ao enviar mensagem: {e}")

    def send_simulated_messages(self):
        """
        Envia mensagens simuladas e emite o sinal 'message_received' manualmente.
        """
        if not self.bus:
            return
        try:
            current_time = time.time()
            msg1 = can.Message(arbitration_id=self.simulated_ids[0], data=[0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88], timestamp=current_time)
            self.bus.send(msg1)
            self.message_received.emit(msg1)

            msg2 = can.Message(arbitration_id=self.simulated_ids[1], data=[self.counter, 0, 0, 0, 0, 0, 0, 0], timestamp=current_time + 0.01)
            self.bus.send(msg2)
            self.message_received.emit(msg2)

            msg3 = can.Message(arbitration_id=self.simulated_ids[2], data=[self.counter, 1, 2, 3, 4, 5, 6, 7], dlc=8, timestamp=current_time + 0.02)
            self.bus.send(msg3)
            self.message_received.emit(msg3)

            self.counter = (self.counter + 1) % 256
        except can.CanError as e:
            self.status_updated.emit(f"Erro no simulador: {e}")
            self.simulator_timer.stop()
