# coding: utf-8

import os
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QGroupBox,
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QDesktopServices

from translations import translations


class AutoHexPatcherGUI(QMainWindow):
    def __init__(self, lang="ru"):
        super().__init__()
        self.lang = lang

        self.START_ADDR = 0x5B00
        self.END_ADDR = 0x6000
        self.SEARCH_BYTE = 0x04
        self.REPLACE_BYTE = 0x03
        self.SIGNATURES = {
            "SEAT Non Nav": "b2 2c 00 04 11 1e 01 11 01 01 11",
            "SEAT Nav": "b2 2b 00 04 11 1e 01 11 01 01 11",
            "SKODA/VW Non Nav": "b2 2c 00 04 11 38 02 10 74 11 73",
            "SKODA/VW Nav": "b2 2b 00 04 11 38 02 10 74 11 73",
        }

        self.file1_path = None
        self.file2_path = None

        self.setWindowTitle(
            "MIB STD2 HMIOFFCLOCKVIEW PATCHER for SEAT/SKODA/VW ZR-PQ Converts v1.1"
        )
        self.setGeometry(100, 100, 900, 800)
        self.setup_ui()

    def tr(self, text):
        return translations.get(self.lang, {}).get(text, text)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        title_label = QLabel("MIB STD2 HMIOFFCLOCKVIEW DATE PATCHER")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(
            "padding: 15px; background-color: #2c3e50; color: white; border-radius: 10px;"
        )
        layout.addWidget(title_label)

        desc_label = QLabel(
            self.tr(
                "Автоматический патчер для скрытия виджета даты\nна экране часов в режиме ожидания\nдля PQ юнитов с HMI от ZR прошивок\n"
            )
        )
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("padding: 10px; font-size: 12px;")
        layout.addWidget(desc_label)

        link_layout = QHBoxLayout()
        link_layout.addStretch()

        website_link = QLabel(
            '<a href="https://www.drive2.ru/l/712453299302827334" style="color: #3498db; text-decoration: none; font-size: 11px;">'
            + self.tr("🌐 Подробнее на Drive2.ru")
            + "</a>"
        )
        website_link.setOpenExternalLinks(True)
        website_link.linkActivated.connect(self.open_website)
        website_link.setToolTip(self.tr("Перейти на статью на Drive2.ru"))
        website_link.setCursor(Qt.PointingHandCursor)

        link_layout.addWidget(website_link)
        link_layout.addStretch()
        layout.addLayout(link_layout)

        files_group = QGroupBox(self.tr("Файлы Hocv.jxe для обработки"))
        self.files_group = files_group
        files_layout = QVBoxLayout(files_group)

        file1_layout = QHBoxLayout()
        self.file1_label = QLabel(self.tr("Файл Hocv_08DA85708EEB9B2F_CA54.jxe"))
        self.file1_label.setStyleSheet(
            "padding: 8px; border: 2px solid #3498db; border-radius: 5px;"
        )
        self.file1_label.setMinimumHeight(40)

        self.browse_btn1 = QPushButton(self.tr("📁 Файл 1"))
        self.browse_btn1.clicked.connect(lambda: self.browse_file(1))
        self.browse_btn1.setStyleSheet(
            """
            QPushButton {
                padding: 10px;
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )

        file1_layout.addWidget(self.file1_label, 3)
        file1_layout.addWidget(self.browse_btn1, 1)
        files_layout.addLayout(file1_layout)

        file2_layout = QHBoxLayout()
        self.file2_label = QLabel(self.tr("Файл Hocv_08DA85708EEB9B2F_DA1F.jxe"))
        self.file2_label.setStyleSheet(
            "padding: 8px; border: 2px solid #3498db; border-radius: 5px;"
        )
        self.file2_label.setMinimumHeight(40)

        self.browse_btn2 = QPushButton(self.tr("📁 Файл 2"))
        self.browse_btn2.clicked.connect(lambda: self.browse_file(2))
        self.browse_btn2.setStyleSheet(
            """
            QPushButton {
                padding: 10px;
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )

        file2_layout.addWidget(self.file2_label, 3)
        file2_layout.addWidget(self.browse_btn2, 1)
        files_layout.addLayout(file2_layout)

        layout.addWidget(files_group)

        self.run_btn = QPushButton(self.tr("🚀 Запуск"))
        self.run_btn.clicked.connect(self.auto_patch)
        self.run_btn.setStyleSheet(
            """
            QPushButton {
                padding: 15px;
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """
        )
        self.run_btn.setMinimumHeight(50)
        self.run_btn.setEnabled(False)
        layout.addWidget(self.run_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid #34495e;
                border-radius: 5px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
            }
        """
        )
        layout.addWidget(self.progress_bar)

        log_label = QLabel(self.tr("Лог выполнения:"))
        log_label.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Courier", 9))
        self.log_text.setStyleSheet(
            """
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
            }
        """
        )
        layout.addWidget(self.log_text, 1)

        self.statusBar().showMessage(self.tr("Готов к работе"))

        self.log("=== MIB STD2 HMIOFFCLOCKVIEW PATCHER 1.1 ===")
        self.log(
            self.tr("• Область поиска: 0x{:04X} - 0x{:04X}").format(
                self.START_ADDR, self.END_ADDR
            )
        )
        self.log(
            self.tr("• Замена: 0x{:02X} → 0x{:02X}").format(
                self.SEARCH_BYTE, self.REPLACE_BYTE
            )
        )
        self.log(self.tr("• Сигнатуры: SEAT, SKODA, VW (ZR Navi/Non Navi)"))
        self.log(self.tr("\nВыберите файлы и нажмите 'Запуск'"))

    def open_website(self, link):
        QDesktopServices.openUrl(QUrl(link))

    def browse_file(self, file_number):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Выберите файл {}").format(file_number),
            "",
            self.tr("Все файлы (*)"),
        )

        if file_path:
            if file_number == 1:
                self.file1_path = file_path
                self.file1_label.setText(os.path.basename(file_path))
            else:
                self.file2_path = file_path
                self.file2_label.setText(os.path.basename(file_path))

            if self.file1_path and self.file2_path:
                self.run_btn.setEnabled(True)

            self.log(self.tr("\n📄 Выбран файл {}: {}").format(file_number, file_path))

    def log(self, message):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
        QApplication.processEvents()

    def check_files_selected(self):
        if not self.file1_path or not self.file2_path:
            QMessageBox.warning(self, self.tr("Ошибка"), self.tr("Выберите оба файла!"))
            return False
        return True

    def auto_patch(self):
        if not self.check_files_selected():
            return

        reply = QMessageBox.question(
            self,
            self.tr("Подтверждение"),
            self.tr("Выбраны файлы:\n\n• Файл 1: {}\n• Файл 2: {}\nПродолжить?").format(
                self.file1_path, self.file2_path
            ),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self.log(self.tr("\n🔍 Начинаю автоматический поиск и замену..."))
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)
        self.run_btn.setEnabled(False)

        try:
            total_patched = 0

            files = [
                (1, self.file1_path, self.tr("Файл 1")),
                (2, self.file2_path, self.tr("Файл 2")),
            ]

            for file_num, file_path, file_name in files:
                self.log(self.tr("📂 Обработка {}:").format(file_name))

                file_patched = 0
                found_signatures = []

                for sig_name, sig_hex in self.SIGNATURES.items():
                    signature = bytes.fromhex(sig_hex.replace(" ", ""))
                    patched = self.patch_file_signature(
                        file_path, signature, sig_name, file_name
                    )

                    if patched > 0:
                        file_patched += patched
                        found_signatures.append(sig_name)

                if file_patched > 0:
                    found_str = ", ".join(found_signatures)
                    self.log(
                        self.tr("✅ Для {} найдены сигнатуры: {}").format(
                            file_name, found_str
                        )
                    )
                    self.log(self.tr("   Заменено байт: {}").format(file_patched))
                    total_patched += file_patched
                else:
                    self.log(
                        self.tr("❌ Для {} сигнатуры не найдены").format(file_name)
                    )

                self.progress_bar.setValue(50 if file_num == 1 else 100)

            self.log("\n" + "=" * 50)
            if total_patched > 0:
                self.log(
                    self.tr("🎉 ОБЩИЙ ИТОГ: Исправлено {} файл(а)").format(total_patched)
                )
                self.statusBar().showMessage(
                    self.tr("Завершено. Исправлено {} файл(а)").format(total_patched)
                )
                QMessageBox.information(
                    self,
                    self.tr("Успех"),
                    self.tr("Патчинг завершен!\nИсправлено {} файл(а).").format(
                        total_patched
                    ),
                )
            else:
                self.log(self.tr("😞 ОБЩИЙ ИТОГ: Сигнатуры не найдены в обоих файлах"))
                self.statusBar().showMessage(self.tr("Сигнатуры не найдены"))
                QMessageBox.warning(
                    self,
                    self.tr("Внимание"),
                    self.tr(
                        "Сигнатуры не найдены в указанных файлах.\nПроверьте правильность файлов."
                    ),
                )

        except Exception as e:
            self.log(self.tr("💥 Ошибка: {}").format(str(e)))
            QMessageBox.critical(
                self,
                self.tr("Ошибка"),
                self.tr("Произошла ошибка:\n{}").format(str(e)),
            )

        finally:
            self.progress_bar.setVisible(False)
            self.run_btn.setEnabled(True)

    def patch_file_signature(self, file_path, signature, sig_name, file_name):
        patched_count = 0

        try:
            with open(file_path, "r+b") as file:
                file.seek(self.START_ADDR)
                area_data = file.read(self.END_ADDR - self.START_ADDR)

                pos = 0
                found_any = False

                while pos < len(area_data):
                    match_pos = area_data.find(signature, pos)
                    if match_pos == -1:
                        break

                    abs_position = self.START_ADDR + match_pos

                    if not found_any:
                        self.log(
                            self.tr(
                                "   Найдена сигнатура {} по адресу: 0x{:04X}"
                            ).format(sig_name, abs_position)
                        )
                        found_any = True

                    for offset, byte in enumerate(signature):
                        if byte == self.SEARCH_BYTE:
                            patch_addr = abs_position + offset
                            file.seek(patch_addr)
                            file.write(bytes([self.REPLACE_BYTE]))
                            patched_count += 1

                    pos = match_pos + 1

                if found_any and patched_count > 0:
                    self.log(
                        self.tr("   Для {} заменено байт: {}").format(
                            sig_name, patched_count
                        )
                    )

        except Exception as e:
            self.log(
                self.tr("   Ошибка при обработке {} в {}: {}").format(
                    sig_name, file_name, str(e)
                )
            )

        return patched_count


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AutoHexPatcherGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
