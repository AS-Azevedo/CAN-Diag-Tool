# CAN-Spector Pro
### Analisador de Rede CAN com UI Avançada

**CAN-Spector Pro** é uma ferramenta de diagnóstico de redes CAN desenvolvida em Python com PySide6, projetada com foco numa arquitetura de software limpa, uma interface de utilizador moderna e uma experiência de utilizador (UX) excecional. A aplicação serve como uma peça de portfólio de alta qualidade, demonstrando competências em engenharia de software, sistemas embarcados e design de UI.

## ✨ Funcionalidades

O projeto foi desenvolvido até à conclusão da Fase 2, com as seguintes funcionalidades implementadas:

* **Trace em Tempo Real:** Visualização de mensagens CAN recebidas, com timestamps relativos, ID, DLC e dados brutos.
* **Decodificação de DBC:** Carregue um ficheiro `.dbc` para decodificar as mensagens CAN em tempo real, exibindo os sinais e os seus valores diretamente na tabela de trace.
* **Plotter de Sinais:** Selecione e visualize múltiplos sinais decodificados num gráfico em tempo real, permitindo uma análise visual dos dados da rede.
* **Transmissor de Mensagens:** Construa e envie mensagens CAN customizadas, especificando a ID (standard ou estendida), DLC e até 8 bytes de dados.
* **Interface Customizável:** Um tema escuro moderno e coeso, implementado através de uma folha de estilos QSS externa, garantindo um controlo total sobre a aparência.
* **Feedback ao Utilizador:** Uma barra de status informa o utilizador sobre o estado da conexão, carregamento de ficheiros e erros de decodificação.

## 🛠️ Stack de Tecnologia

* **Linguagem:** Python 3.11+
* **Interface Gráfica (GUI):** PySide6
* **Core Lógico:**
  * `python-can`: Para a comunicação com o barramento CAN (real e virtual).
  * `cantools`: Para o parsing e a decodificação de ficheiros DBC.
  * `pyqtgraph`: Para a plotagem de gráficos de alta performance.
* **Estilo e Ícones:**
  * QSS (Qt Style Sheets) para uma estilização customizada.
  * `qtawesome` com Feather Icons para ícones limpos e modernos.

## 📂 Estrutura do Projeto

A aplicação segue uma arquitetura modular para garantir a manutenibilidade e a clareza do código:

```
CAN-Spector-Pro/
|
|-- main.py             # Ponto de entrada da aplicação
|
|-- core/
|   |-- __init__.py
|   |-- can_bus_manager.py  # Gestor de conexão e comunicação CAN
|   |-- dbc_manager.py      # Gestor de carregamento e decodificação de DBC
|
|-- ui/
|   |-- __init__.py
|   |-- main_window.py      # Janela principal que organiza os widgets
|   |-- widgets/
|   |   |-- __init__.py
|   |   |-- trace_widget.py       # Painel da tabela de trace
|   |   |-- plot_widget.py        # Painel do gráfico
|   |   |-- transmitter_widget.py # Painel para enviar mensagens
|
|-- assets/
|   |-- dark_theme.qss      # Folha de estilos customizada
|
|-- requirements.txt
|-- README.md