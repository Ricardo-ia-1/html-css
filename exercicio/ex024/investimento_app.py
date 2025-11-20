import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout,
    QFileDialog, QSplitter, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class InvestimentoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📈 Cronograma de Investimentos")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📊 Cronograma de Investimentos")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        # Entradas
        self.entrada_valor_inicial = QLineEdit()
        self.entrada_valor_inicial.setPlaceholderText("Valor inicial (R$)")
        self.entrada_aporte_mensal = QLineEdit()
        self.entrada_aporte_mensal.setPlaceholderText("Aporte mensal (R$)")
        self.entrada_taxa = QLineEdit()
        self.entrada_taxa.setPlaceholderText("Taxa de juros mensal (%)")
        self.entrada_meses = QLineEdit()
        self.entrada_meses.setPlaceholderText("Duração (em meses)")

        for input_field in [
            self.entrada_valor_inicial,
            self.entrada_aporte_mensal,
            self.entrada_taxa,
            self.entrada_meses,
        ]:
            layout.addWidget(input_field)

        # Botões
        botoes_layout = QHBoxLayout()
        botao_calcular = QPushButton("Gerar Cronograma")
        botao_calcular.clicked.connect(self.gerar_cronograma)

        botao_exportar = QPushButton("Exportar para CSV")
        botao_exportar.clicked.connect(self.exportar_para_csv)

        botao_salvar_grafico = QPushButton("Salvar Gráfico como PNG")
        botao_salvar_grafico.clicked.connect(self.salvar_grafico_png)

        botoes_layout.addWidget(botao_calcular)
        botoes_layout.addWidget(botao_exportar)
        botoes_layout.addWidget(botao_salvar_grafico)
        layout.addLayout(botoes_layout)

        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Mês", "Aporte", "Juros", "Saldo"])

        # Gráfico
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        # Layout responsivo com QSplitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        frame_tabela = QFrame()
        frame_grafico = QFrame()

        tabela_layout = QVBoxLayout()
        tabela_layout.addWidget(self.tabela)
        frame_tabela.setLayout(tabela_layout)

        grafico_layout = QVBoxLayout()
        grafico_layout.addWidget(self.canvas)
        frame_grafico.setLayout(grafico_layout)

        splitter.addWidget(frame_tabela)
        splitter.addWidget(frame_grafico)
        splitter.setSizes([400, 400])  # Tamanho inicial

        layout.addWidget(splitter)
        self.setLayout(layout)

    def gerar_cronograma(self):
        try:
            valor_inicial = float(self.entrada_valor_inicial.text())
            aporte_mensal = float(self.entrada_aporte_mensal.text())
            taxa = float(self.entrada_taxa.text())
            meses = int(self.entrada_meses.text())

            saldo = valor_inicial
            self.cronograma = []
            saldos = []

            for mes in range(1, meses + 1):
                saldo += aporte_mensal
                juros = saldo * (taxa / 100)
                saldo += juros
                self.cronograma.append((mes, aporte_mensal, juros, saldo))
                saldos.append(saldo)

            self.tabela.setRowCount(meses)
            for i, (mes, aporte, juros, saldo_total) in enumerate(self.cronograma):
                self.tabela.setItem(i, 0, QTableWidgetItem(str(mes)))
                self.tabela.setItem(i, 1, QTableWidgetItem(f"R$ {aporte:.2f}"))
                self.tabela.setItem(i, 2, QTableWidgetItem(f"R$ {juros:.2f}"))
                self.tabela.setItem(i, 3, QTableWidgetItem(f"R$ {saldo_total:.2f}"))

            self.plotar_grafico(saldos)

        except ValueError:
            self.tabela.setRowCount(1)
            self.tabela.setItem(0, 0, QTableWidgetItem("Erro"))
            self.tabela.setItem(0, 1, QTableWidgetItem("Verifique"))
            self.tabela.setItem(0, 2, QTableWidgetItem("os dados"))
            self.tabela.setItem(0, 3, QTableWidgetItem("digitados"))

    def plotar_grafico(self, saldos):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(range(1, len(saldos) + 1), saldos, marker='o', color='#0077cc')
        ax.set_title("Evolução do Saldo")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Saldo (R$)")
        ax.grid(True)
        self.canvas.draw()

    def salvar_grafico_png(self):
        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar Gráfico", "", "PNG Files (*.png)")
        if caminho:
            self.figure.savefig(caminho)

    def exportar_para_csv(self):
        if not hasattr(self, 'cronograma') or not self.cronograma:
            return

        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar CSV", "", "CSV Files (*.csv)")
        if caminho:
            with open(caminho, mode='w', newline='', encoding='utf-8') as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow(["Mês", "Aporte", "Juros", "Saldo"])
                for linha in self.cronograma:
                    escritor.writerow([linha[0], f"{linha[1]:.2f}", f"{linha[2]:.2f}", f"{linha[3]:.2f}"])

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f2f6fc;
                font-family: Arial;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0077cc;
                background-color: #e6f0ff;
            }
            QPushButton {
                background-color: #0077cc;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #0077cc;
                color: white;
                padding: 4px;
                font-weight: bold;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = InvestimentoApp()
    janela.show()
    sys.exit(app.exec_())