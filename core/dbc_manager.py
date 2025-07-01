# core/dbc_manager.py (v6 - Com Relatório de Erros)

import cantools
from PySide6.QtCore import QObject, Signal

class DBCManager(QObject):
    """
    Gerencia o carregamento e a decodificação de mensagens CAN usando um arquivo DBC.
    """
    dbc_loaded = Signal()
    dbc_load_error = Signal(str)
    # --- NOVO SINAL ADICIONADO AQUI ---
    # Emite uma mensagem quando uma mensagem específica não pode ser decodificada.
    decode_error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = None

    def load_file(self, filepath):
        """ Carrega um arquivo de banco de dados CAN (.dbc). """
        if not filepath:
            return
        try:
            self.db = cantools.database.load_file(filepath, strict=False)
            print(f"DBC '{filepath}' carregado com sucesso (modo não-estrito).")
            self.dbc_loaded.emit()
        except Exception as e:
            self.db = None
            error_message = f"Erro crítico ao carregar DBC: {e}"
            print(error_message)
            self.dbc_load_error.emit(error_message)

    def get_signal_names(self):
        """ Retorna uma lista ordenada e única de todos os nomes de sinais no DBC. """
        if not self.db:
            return []
        signal_names = []
        for msg in self.db.messages:
            for signal in msg.signals:
                signal_names.append(signal.name)
        return sorted(list(set(signal_names)))
            
    def decode_message(self, msg):
        """
        Decodifica uma mensagem CAN e retorna um dicionário de sinais.
        Emite um sinal de erro se a decodificação falhar.
        """
        if not self.db:
            return None
        try:
            decoded_signals = self.db.decode_message(msg.arbitration_id, msg.data)
            return decoded_signals
        except KeyError:
            # Ignora silenciosamente se a ID não estiver no DBC.
            return None
        except Exception as e:
            # Emite o sinal de erro em vez de falhar silenciosamente.
            error_msg = f"Erro de decodificação na ID {msg.arbitration_id}: {e}"
            self.decode_error.emit(error_msg)
            return None
