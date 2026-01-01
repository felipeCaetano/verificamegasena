import json
import os
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLineEdit, QTextEdit,
                               QLabel, QMessageBox, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

FILE_NAME = 'bet.json'


class LotteryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Verificador de Mega Sena - Loteria")
        self.setMinimumSize(700, 600)
        self.setup_ui()

    def setup_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Título
        title = QLabel("🎰 Sistema de Apostas")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Grupo: Nova Aposta
        bet_group = QGroupBox("📝 Cadastrar Nova Aposta")
        bet_group.setStyleSheet(
            "QGroupBox { font-weight: bold; padding-top: 10px; }")
        bet_layout = QVBoxLayout()

        bet_instruction = QLabel(
            "Digite os números separados por espaços ou vírgulas (Ex: 1 2 3 4 5 6)")
        bet_instruction.setWordWrap(True)
        bet_layout.addWidget(bet_instruction)

        self.bet_input = QLineEdit()
        self.bet_input.setPlaceholderText("Digite sua aposta aqui...")
        self.bet_input.setMinimumHeight(40)
        bet_layout.addWidget(self.bet_input)

        add_bet_btn = QPushButton("➕ Adicionar Aposta")
        add_bet_btn.setMinimumHeight(40)
        add_bet_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        add_bet_btn.clicked.connect(self.add_new_bet)
        bet_layout.addWidget(add_bet_btn)

        bet_group.setLayout(bet_layout)
        main_layout.addWidget(bet_group)

        # Grupo: Verificar Resultado
        result_group = QGroupBox("🔍 Verificar Resultados")
        result_group.setStyleSheet(
            "QGroupBox { font-weight: bold; padding-top: 10px; }")
        result_layout = QVBoxLayout()

        result_instruction = QLabel(
            "Digite as dezenas sorteadas separadas por espaços ou vírgulas")
        result_instruction.setWordWrap(True)
        result_layout.addWidget(result_instruction)

        self.result_input = QLineEdit()
        self.result_input.setPlaceholderText("Digite o resultado aqui...")
        self.result_input.setMinimumHeight(40)
        result_layout.addWidget(self.result_input)

        verify_btn = QPushButton("✅ Verificar Resultados")
        verify_btn.setMinimumHeight(40)
        verify_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        verify_btn.clicked.connect(self.verify_results)
        result_layout.addWidget(verify_btn)

        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)

        # Área de resultados
        results_label = QLabel("📊 Resultados:")
        results_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        main_layout.addWidget(results_label)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(200)
        self.results_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
            }
        """)
        main_layout.addWidget(self.results_text)

    def add_new_bet(self):
        bet_input = self.bet_input.text().strip()

        if not bet_input:
            QMessageBox.warning(self, "Aviso", "Por favor, digite uma aposta!")
            return

        bet_input = bet_input.replace(',', ' ')

        try:
            aposta = [int(x) for x in bet_input.split()]
            if len(aposta) < 6:
                QMessageBox.warning(
                    self,
                    "Aviso","A aposta deve conter pelo menos 6 números"
                )
                return
            elif len(set(aposta)) < 6:
                QMessageBox.warning(
                    self,
                    "Aviso","A aposta não deve conter números repetidos"
                )
                return
            if any(n < 1 or n > 60 for n in aposta):
                QMessageBox.warning(
                    self,
                    "Aviso","Os números devem estar entre 1 e 60"
                )
                return
        except ValueError:
            QMessageBox.critical(self, "Erro",
                                 "Aposta deve conter apenas números!")
            return

        registro = {"bet": aposta}

        try:
            with open(FILE_NAME, 'a', encoding='utf-8') as f:
                f.write(json.dumps(registro) + '\n')

            QMessageBox.information(self, "Sucesso",
                                    f"✅ Aposta cadastrada com sucesso!\n\nNúmeros: {aposta}")
            self.bet_input.clear()
            self.results_text.append(f"✅ Nova aposta cadastrada: {aposta}\n")
        except Exception as e:
            QMessageBox.critical(self, "Erro",
                                 f"Erro ao salvar aposta: {str(e)}")

    def verify_results(self):
        if not os.path.exists(FILE_NAME):
            QMessageBox.critical(
                self, 'Erro', "Nenhuma aposta cadastrada ainda")
            return
        result_input = self.result_input.text().strip()

        if not result_input:
            QMessageBox.warning(self, "Aviso", "Por favor, digite o resultado!")
            self.results_text.clear()
            return

        try:
            resultado = [int(x) for x in result_input.replace(',', ' ').split()]
            if len(resultado) != 6:
                QMessageBox.critical(
                    self, 'Erro', "O resultado deve conter exatamente 6 "
                                  "números")
                return

            if len(set(resultado)) != 6:
                QMessageBox.critical(
                    self, 'Erro', "O resultado não pode conter números "
                          "repetidos")
                return

            if any(n < 1 or n > 60 for n in resultado):
                QMessageBox.critical(
                    self, 'Erro',"Os números do resultado devem estar entre 1 e 60")
                return
        except ValueError:
            QMessageBox.critical(self, "Erro",
                                 "Os resultados devem ser números!")
            return

        self.results_text.clear()
        self.results_text.append(f"🎯 Resultado do sorteio: {resultado}\n")
        self.results_text.append("=" * 50 + "\n")

        try:
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                apostas_encontradas = False
                for index, line in enumerate(f, 1):
                    try:
                        registro = json.loads(line)
                        bet = registro["bet"]
                        apostas_encontradas = True
                    except (json.JSONDecodeError, KeyError):
                        self.results_text.append(
                            f"⚠️ Aposta inválida na linha {index}, ignorando\n")
                        continue

                    hits = set(bet).intersection(resultado)
                    num_hits = len(hits)

                    self.results_text.append(f"Aposta {index}: {bet}\n")
                    self.results_text.append(
                        f"   ➜ {num_hits} acerto(s): {sorted(hits)}\n")

                    if num_hits < 4:
                        self.results_text.append(
                            "   😢 Que pena! Não foi dessa vez...\n\n")
                    elif num_hits == 4:
                        self.results_text.append(
                            '<span style="color: orange;'
                            'font-weight: bold;">🎉 QUADRA!</span>'
                        )
                    elif num_hits == 5:
                        self.results_text.append(
                            '<span style="color: blue;'
                            'font-weight: bold;">🎉   🎊  QUINA!</span>')
                    elif num_hits == 6:
                        self.results_text.append(
                            '<span style="color: green; font-weight: bold;"> '
                            '🎉 🎊 🏆 SENA! VOCÊ TIROU A SORTE GRANDE! Parabéns!</span><br><br>')

                if not apostas_encontradas:
                    self.results_text.append(
                        "⚠️ Nenhuma aposta encontrada no arquivo.\n")

        except FileNotFoundError:
            QMessageBox.warning(self, "Aviso",
                                "Nenhuma aposta cadastrada ainda!\n\nCadastre uma aposta primeiro.")
            self.results_text.append("⚠️ Arquivo de apostas não encontrado.\n")
        except Exception as e:
            QMessageBox.critical(self, "Erro",
                                 f"Erro ao verificar resultados: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = LotteryApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()