#!/usr/bin/env python3
# coding: utf-8

import sys
import os
import configparser
from pathlib import Path

if hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QLineEdit,
    QGroupBox,
    QMessageBox,
    QRadioButton,
    QButtonGroup,
    QCheckBox,
    QActionGroup,
    QAction,
    QDialog,
    QDialogButtonBox,
    QFrame,
)
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon

from translations import translations
from variant_db import VARIANT_DB


class Translator(QObject):
    def __init__(self):
        super().__init__()
        self.translations = translations

    def tr(self, text, lang="ru"):
        return self.translations.get(lang, {}).get(text, text)


class MIB2FlasherGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.current_language = "ru"
        self.load_icon()
        self.init_ui()

    def load_icon(self):
        try:
            possible_paths = []

            if hasattr(sys, "_MEIPASS"):
                possible_paths.append(os.path.join(sys._MEIPASS, "icon.ico"))

            possible_paths.extend(
                [
                    "icon.ico",
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "icon.ico"
                    ),
                    os.path.join(os.path.dirname(sys.argv[0]), "icon.ico"),
                ]
            )

            icon_loaded = False
            for icon_path in possible_paths:
                if icon_path and os.path.exists(icon_path):
                    try:
                        self.setWindowIcon(QIcon(icon_path))
                        icon_loaded = True
                        break
                    except Exception:
                        continue

            if not icon_loaded:
                print("Icon not found, default will be used")

        except Exception as e:
            print("Icon loading error: {}".format(str(e)))

    def tr(self, text):
        return self.translator.tr(text, self.current_language)

    def init_ui(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu(self.tr("File"))
        self.exit_action = QAction(self.tr("Exit"), self)
        self.exit_action.triggered.connect(self.close)
        file_menu.addAction(self.exit_action)

        language_menu = menubar.addMenu(self.tr("Language"))

        self.ru_action = QAction("Русский", self)
        self.ru_action.triggered.connect(lambda: self.change_language("ru"))
        self.ru_action.setCheckable(True)
        language_menu.addAction(self.ru_action)

        self.en_action = QAction("English", self)
        self.en_action.triggered.connect(lambda: self.change_language("en"))
        self.en_action.setCheckable(True)
        language_menu.addAction(self.en_action)

        self.lang_action_group = QActionGroup(self)
        self.lang_action_group.addAction(self.ru_action)
        self.lang_action_group.addAction(self.en_action)
        self.ru_action.setChecked(True)

        help_menu = menubar.addMenu(self.tr("Help"))
        self.help_action = QAction(self.tr("Online Documentation"), self)
        self.help_action.triggered.connect(self.open_help)
        help_menu.addAction(self.help_action)

        self.forum_action = QAction(self.tr("Support Forum"), self)
        self.forum_action.triggered.connect(self.open_forum)
        help_menu.addAction(self.forum_action)

        self.setWindowTitle(self.tr("MIB2 Universal Flasher Tool"))
        self.setGeometry(100, 100, 900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.variant_group = QGroupBox(self.tr("Target Settings"))
        vbox_variant = QVBoxLayout()
        hbox_variant = QHBoxLayout()
        self.variant_label = QLabel(self.tr("Enter target variant:"))
        self.variant_input = QLineEdit()
        self.variant_input.setPlaceholderText(self.tr("Example: 17203"))
        self.variant_input.setMaxLength(5)
        self.variant_input.textChanged.connect(self.on_variant_changed)
        hbox_variant.addWidget(self.variant_label)
        hbox_variant.addWidget(self.variant_input)
        vbox_variant.addLayout(hbox_variant)
        self.variant_group.setLayout(vbox_variant)
        main_layout.addWidget(self.variant_group)

        self.hwid_group = QGroupBox(self.tr("SWDL"))
        vbox_hwid = QVBoxLayout()
        hbox_hwid = QHBoxLayout()
        self.hwid_label = QLabel(self.tr("SWDL HwVersion:"))
        self.hwid_input = QLineEdit()
        self.hwid_input.setPlaceholderText(self.tr("Example: 20"))
        hbox_hwid.addWidget(self.hwid_label)
        hbox_hwid.addWidget(self.hwid_input)
        vbox_hwid.addLayout(hbox_hwid)
        self.hwid_group.setLayout(vbox_hwid)
        main_layout.addWidget(self.hwid_group)

        self.file_group = QGroupBox(self.tr("Metainfo2.txt File"))
        hbox_file = QHBoxLayout()
        self.file_label = QLabel(self.tr("No file selected"))
        self.file_label.setStyleSheet("color: gray")
        self.file_label.setFixedWidth(600)
        self.browse_btn = QPushButton(self.tr("Browse..."))
        self.browse_btn.clicked.connect(self.browse_file)
        hbox_file.addWidget(self.file_label)
        hbox_file.addWidget(self.browse_btn)
        self.file_group.setLayout(hbox_file)
        main_layout.addWidget(self.file_group)

        self.target_group = QGroupBox(self.tr("Target Parameters (auto-detected)"))
        vbox_target = QVBoxLayout()

        hbox_target_brand = QHBoxLayout()
        self.target_brand_label = QLabel(self.tr("Target brand:"))
        self.target_brand_value = QLabel("")
        hbox_target_brand.addWidget(self.target_brand_label)
        hbox_target_brand.addWidget(self.target_brand_value)
        vbox_target.addLayout(hbox_target_brand)

        hbox_target_platform = QHBoxLayout()
        self.target_platform_label = QLabel(self.tr("Target platform:"))
        self.target_platform_value = QLabel("")
        hbox_target_platform.addWidget(self.target_platform_label)
        hbox_target_platform.addWidget(self.target_platform_value)
        vbox_target.addLayout(hbox_target_platform)

        hbox_target_region = QHBoxLayout()
        self.target_region_label = QLabel(self.tr("Target region:"))
        self.target_region_value = QLabel("")
        hbox_target_region.addWidget(self.target_region_label)
        hbox_target_region.addWidget(self.target_region_value)
        vbox_target.addLayout(hbox_target_region)

        self.target_group.setLayout(vbox_target)
        main_layout.addWidget(self.target_group)

        self.source_group = QGroupBox(self.tr("Source Parameters (from file)"))
        vbox_source = QVBoxLayout()

        hbox_source_brand = QHBoxLayout()
        self.source_brand_label = QLabel(self.tr("Source brand:"))
        self.source_brand_value = QLabel("")
        hbox_source_brand.addWidget(self.source_brand_label)
        hbox_source_brand.addWidget(self.source_brand_value)
        vbox_source.addLayout(hbox_source_brand)

        hbox_source_platform = QHBoxLayout()
        self.source_platform_label = QLabel(self.tr("Source platform:"))
        self.source_platform_value = QLabel("")
        hbox_source_platform.addWidget(self.source_platform_label)
        hbox_source_platform.addWidget(self.source_platform_value)
        vbox_source.addLayout(hbox_source_platform)

        hbox_source_region = QHBoxLayout()
        self.source_region_label = QLabel(self.tr("Source region:"))
        self.source_region_value = QLabel("EU")
        hbox_source_region.addWidget(self.source_region_label)
        hbox_source_region.addWidget(self.source_region_value)
        vbox_source.addLayout(hbox_source_region)

        self.source_group.setLayout(vbox_source)
        main_layout.addWidget(self.source_group)

        self.mode_group = QGroupBox(self.tr("Operation Mode (auto-detected)"))
        vbox_mode = QVBoxLayout()
        self.mode_btn_group = QButtonGroup(self)
        self.cross_mode = QRadioButton(self.tr("Cross-flashing between brands"))
        self.cross_mode.setChecked(True)
        self.cross_mode.setEnabled(False)
        self.mode_btn_group.addButton(self.cross_mode)
        self.zr_to_pq_mode = QRadioButton(self.tr("HMI ZR to PQ flashing"))
        self.zr_to_pq_mode.setEnabled(False)
        self.mode_btn_group.addButton(self.zr_to_pq_mode)
        vbox_mode.addWidget(self.cross_mode)
        vbox_mode.addWidget(self.zr_to_pq_mode)
        self.mode_group.setLayout(vbox_mode)
        main_layout.addWidget(self.mode_group)

        self.log_group = QGroupBox(self.tr("Execution Log"))
        self.log_group.setVisible(False)
        vbox_log = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        vbox_log.addWidget(self.log_output)
        self.log_group.setLayout(vbox_log)
        main_layout.addWidget(self.log_group)

        hbox_actions = QHBoxLayout()
        self.start_btn = QPushButton(self.tr("Execute Conversion"))
        self.start_btn.clicked.connect(self.start_conversion)
        self.start_btn.setEnabled(False)

        self.show_log_btn = QPushButton(self.tr("Show Log"))
        self.show_log_btn.clicked.connect(self.toggle_log_visibility)
        self.show_log_btn.setCheckable(True)

        self.clear_btn = QPushButton(self.tr("Clear Log"))
        self.clear_btn.clicked.connect(self.clear_log)
        self.clear_btn.setVisible(False)

        self.exit_btn = QPushButton(self.tr("Exit"))
        self.exit_btn.clicked.connect(self.close)

        hbox_actions.addWidget(self.start_btn)
        hbox_actions.addWidget(self.show_log_btn)
        hbox_actions.addWidget(self.clear_btn)
        hbox_actions.addWidget(self.exit_btn)
        main_layout.addLayout(hbox_actions)

        self.current_mode = "cross"

    def on_variant_changed(self, text):
        text = text.strip()
        if len(text) == 5 and text.isdigit():
            self.update_from_variant()
        else:
            self.target_brand_value.setText("")
            self.target_platform_value.setText("")
            self.target_region_value.setText("")
            self.start_btn.setEnabled(False)

    def open_help(self):
        import webbrowser

        webbrowser.open("https://www.drive2.ru/users/stasinator/")

    def open_forum(self):
        import webbrowser

        webbrowser.open("https://www.drive2.ru/l/614500832041241045/")

    def update_from_variant(self):
        variant = self.variant_input.text().strip()
        data = VARIANT_DB.get(variant)

        if data:
            self.target_brand_value.setText(data["brand"])
            self.target_platform_value.setText(data["platform"])
            self.target_region_value.setText(data["region"])

            self.log(
                self.tr(
                    "Auto-detected target: brand={}, platform={}, region={}"
                ).format(data["brand"], data["platform"], data["region"])
            )

            if hasattr(self, "source_platform"):
                self.update_operation_mode()
        else:
            self.log(self.tr("Variant not found in database"))
            self.target_brand_value.setText("")
            self.target_platform_value.setText("")
            self.target_region_value.setText("")
            self.start_btn.setEnabled(False)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Select Metainfo2.txt file"),
            "",
            self.tr("Text files (*.txt)"),
        )
        if file_path:
            self.input_file = file_path
            self.file_label.setText(Path(file_path).name)
            self.file_label.setStyleSheet("color: black")
            self.analyze_file_parameters(file_path)

    def analyze_file_parameters(self, file_path):
        try:
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read(file_path, encoding="utf-8")

            if "common" not in config:
                raise ValueError("No [common] section found in file")

            self.source_variants = []
            for key in config["common"]:
                if key.lower().startswith("variant"):
                    variant = config["common"][key].strip('"')
                    if variant in VARIANT_DB:
                        self.source_variants.append(variant)

            if not self.source_variants:
                raise ValueError("No valid variants found in [common] section")

            if config.has_option("common", "Release"):
                release = config.get("common", "Release").strip('"')
                self.log(self.tr("Analyzing Release: {}").format(release))

                parts = release.split("_")
                if len(parts) >= 2:
                    region = parts[1]

                    if region != "EU":
                        QMessageBox.critical(
                            self,
                            self.tr("Error"),
                            self.tr("Region must be EU!")
                            + "\n"
                            + self.tr("Found: {}").format(region),
                        )
                        self.start_btn.setEnabled(False)
                        self.file_label.setStyleSheet("color: red")
                        return
                    else:
                        self.source_region_value.setText(region)
                        self.log(self.tr("Region verification passed: EU"))

                if len(parts) >= 4:
                    brand_map = {"VW": "VW", "SE": "SEAT", "SK": "Skoda"}
                    brand_code = parts[2]
                    self.source_brand = brand_map.get(brand_code)

                    platform_part = parts[3]
                    self.source_platform = platform_part.upper()

                    if self.source_brand and self.source_platform in ["PQ", "ZR"]:
                        self.source_brand_value.setText(self.source_brand)
                        self.source_platform_value.setText(self.source_platform)
                        self.log(
                            self.tr(
                                "Auto-detected source: brand={}, platform={}"
                            ).format(self.source_brand, self.source_platform)
                        )

                        if self.variant_input.text():
                            self.update_operation_mode()
                        return

            raise ValueError("Could not determine source parameters from file")

        except Exception as e:
            self.log(self.tr("Error analyzing file: {}").format(str(e)))
            self.start_btn.setEnabled(False)

    def update_operation_mode(self):
        if not hasattr(self, "source_platform") or not self.variant_input.text():
            return

        target_platform = self.target_platform_value.text()

        if self.source_platform == "ZR" and target_platform == "PQ":
            self.zr_to_pq_mode.setChecked(True)
            self.current_mode = "zr-to-pq"
            self.log(self.tr("Auto-selected ZR→PQ mode"))
        else:
            self.cross_mode.setChecked(True)
            self.current_mode = "cross"
            self.log(self.tr("Auto-selected cross-flash mode"))

        if self.source_platform == "PQ" and target_platform == "ZR":
            self.start_btn.setEnabled(False)
            QMessageBox.warning(
                self,
                self.tr("Error"),
                self.tr("Conversion from PQ to ZR is prohibited!"),
            )
        else:
            self.start_btn.setEnabled(True)

    def find_best_variant_to_replace(self, target_platform):
        if not getattr(self, "source_variants", None):
            return None

        target_data = VARIANT_DB.get(self.variant_input.text().strip())

        perfect_matches = []
        partial_matches = []

        for variant in self.source_variants:
            source_data = VARIANT_DB.get(variant)
            if not source_data or not target_data:
                continue

            if self.current_mode == "cross":
                if source_data["platform"] != target_platform:
                    continue
            elif self.current_mode == "zr-to-pq":
                if source_data["platform"] != "ZR":
                    continue

            if source_data["navi"] != target_data["navi"]:
                continue

            if source_data["dab"] == target_data["dab"]:
                perfect_matches.append(variant)
            else:
                partial_matches.append(variant)

        if len(perfect_matches) > 1:
            self.log(
                self.tr("Found {} perfect matches: {}").format(
                    len(perfect_matches), perfect_matches
                )
            )

            selected_variant = self.show_variant_selection_dialog(
                perfect_matches, self.variant_input.text()
            )

            if selected_variant:
                self.log(self.tr("User selected variant: {}").format(selected_variant))
                return selected_variant
            else:
                raise ValueError(self.tr("Variant selection was cancelled by user"))

        elif perfect_matches:
            self.log(self.tr("Found perfect match: {}").format(perfect_matches[0]))
            return perfect_matches[0]

        elif partial_matches:
            self.log(
                self.tr("Found partial match (DAB differs): {}").format(
                    partial_matches[0]
                )
            )
            return partial_matches[0]

        error_msg = self.tr("No suitable variant found for replacement.") + "\n"
        error_msg += (
            self.tr("Target requirements: platform={}, navi={}, dab={}").format(
                target_platform, target_data["navi"], target_data["dab"]
            )
            + "\n"
        )
        error_msg += self.tr("Available source variants:") + "\n"

        for variant in self.source_variants:
            data = VARIANT_DB.get(variant)
            if data:
                error_msg += f"- {variant}: platform={data['platform']}, navi={data['navi']}, dab={data['dab']}\n"

        raise ValueError(error_msg)

    def show_variant_selection_dialog(self, variants, target_variant):
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("Select Variant to Replace"))
        dialog.setModal(True)

        base_height = 200
        variant_height = 30
        max_height = 600

        calculated_height = min(
            base_height + (len(variants) * variant_height), max_height
        )
        dialog.resize(500, calculated_height)

        layout = QVBoxLayout()

        count_text = self.tr(
            "Found {count} perfect matches for your target variant {target}."
        ).format(count=len(variants), target=target_variant)

        advice_text = self.tr(
            "Usually it doesn't matter which one to replace, but if you encounter issues, you can manually select the replacement variant."
        )

        info_label = QLabel(f"{count_text}\n\n{advice_text}")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        auto_select_checkbox = QCheckBox(
            self.tr("Use auto-selection (recommended)"), dialog
        )
        auto_select_checkbox.setChecked(True)
        layout.addWidget(auto_select_checkbox)

        variants_frame = QFrame()
        variants_frame.setFrameStyle(QFrame.StyledPanel)
        variants_layout = QVBoxLayout()

        variants_label = QLabel(self.tr("Available variants:"))
        variants_layout.addWidget(variants_label)

        radio_group = QButtonGroup(dialog)
        variant_data = []

        for i, variant in enumerate(variants):
            data = VARIANT_DB[variant]
            radio = QRadioButton(
                f"{variant} (brand: {data['brand']}, platform: {data['platform']}, "
                f"navi: {data['navi']}, dab: {data['dab']})"
            )
            radio_group.addButton(radio, i)
            variant_data.append(variant)

            if i == 0:
                radio.setChecked(True)

            variants_layout.addWidget(radio)

        variants_layout.addStretch(1)

        variants_frame.setLayout(variants_layout)
        variants_frame.setEnabled(False)
        layout.addWidget(variants_frame)

        auto_select_checkbox.toggled.connect(variants_frame.setDisabled)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        layout.addWidget(button_box)

        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            if auto_select_checkbox.isChecked():
                return variant_data[0]
            selected_index = radio_group.checkedId()
            if selected_index >= 0:
                return variant_data[selected_index]
            return variant_data[0]
        return None

    def resolve_target_variant(self, source_variant, require_pq=False):
        target_variant = self.variant_input.text().strip()
        target_data = VARIANT_DB.get(target_variant)

        if not target_data:
            raise ValueError(
                self.tr("Target variant {} not found in database").format(
                    target_variant
                )
            )

        if require_pq and target_data["platform"] != "PQ":
            raise ValueError(
                self.tr(
                    "For ZR→PQ mode, target variant must be PQ platform, but found: {}"
                ).format(target_data["platform"])
            )

        source_data = VARIANT_DB[source_variant]
        log_key = (
            "ZR→PQ replacement: {} (navi={}, dab={}) → {} (navi={}, dab={})"
            if require_pq
            else "Replacement: {} (navi={}, dab={}) → {} (navi={}, dab={})"
        )
        self.log(
            self.tr(log_key).format(
                source_variant,
                source_data["navi"],
                source_data["dab"],
                target_variant,
                target_data["navi"],
                target_data["dab"],
            )
        )

        return target_variant

    def check_existing_variant(self, config, target_variant):
        for section in config.sections():
            for key in config[section]:
                if key.lower().startswith("variant"):
                    current_val = config[section][key].strip('"')
                    if current_val == target_variant:
                        return True, section, key
        return False, None, None

    def set_required_version_to_zero(self, config):
        modified_sections = 0

        for section in config.sections():
            if config.has_option(section, "RequiredVersionOfDM"):
                current_value = config.get(section, "RequiredVersionOfDM")
                if current_value.strip('"') == "0":
                    continue
                config.set(section, "RequiredVersionOfDM", '"0"')
                self.log(
                    self.tr("Set RequiredVersionOfDM = 0 in section [{}]").format(
                        section
                    )
                )
                modified_sections += 1

        if modified_sections > 0:
            self.log(
                self.tr("RequiredVersionOfDM set to 0 in {} sections").format(
                    modified_sections
                )
            )
        else:
            self.log(
                self.tr(
                    "RequiredVersionOfDM already set to 0 in all sections or parameter not found"
                )
            )

    def start_conversion(self):
        if not hasattr(self, "input_file"):
            QMessageBox.warning(self, self.tr("Error"), self.tr("No file selected!"))
            return

        hwid = self.hwid_input.text().strip()
        if not hwid:
            QMessageBox.warning(
                self, self.tr("Error"), self.tr("SWDL HwVersion is required!")
            )
            return

        try:
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read(self.input_file, encoding="utf-8")

            target_data = VARIANT_DB.get(self.variant_input.text().strip())
            if not target_data:
                raise ValueError(self.tr("Target variant not found in database"))

            self.target_brand_value.setText(target_data["brand"])
            self.target_platform_value.setText(target_data["platform"])
            self.target_region_value.setText(target_data["region"])

            variant_to_replace = self.find_best_variant_to_replace(
                target_data["platform"]
            )

            if not variant_to_replace:
                raise ValueError(self.tr("No suitable variant found for replacement"))

            target_variant = self.resolve_target_variant(
                variant_to_replace, require_pq=(self.current_mode == "zr-to-pq")
            )

            if variant_to_replace == target_variant:
                raise ValueError(
                    self.tr("Source and target variants are the same: {}").format(
                        target_variant
                    )
                )

            variant_exists, existing_section, existing_key = (
                self.check_existing_variant(config, target_variant)
            )
            if variant_exists:
                raise ValueError(
                    self.tr(
                        "Target variant {} already exists in file (section {}[{}])"
                    ).format(target_variant, existing_section, existing_key)
                )

            backup_file = Path(self.input_file).with_suffix(".bak")
            with backup_file.open("w", encoding="utf-8") as f:
                config.write(f)
            self.log(self.tr("Backup created: {}").format(backup_file))

            changes = []
            for section in config.sections():
                for key in config[section]:
                    if key.lower().startswith("variant"):
                        current_val = config[section][key].strip('"')
                        if current_val == variant_to_replace:
                            config.set(section, key, f'"{target_variant}"')
                            changes.append(
                                (variant_to_replace, target_variant, section, key)
                            )
                            self.log(
                                self.tr("Replaced: {} → {} in section {}[{}]").format(
                                    variant_to_replace, target_variant, section, key
                                )
                            )

            if not changes:
                raise ValueError(self.tr("No variants were replaced"))

            self.link_ids(config, hwid)
            self.log(self.tr("Using HWID: {}").format(hwid))
            self.add_standard_regions(config)
            self.set_required_version_to_zero(config)

            with Path(self.input_file).open("w", encoding="utf-8") as f:
                config.write(f)

            self.log("\n" + "=" * 50)
            self.log(self.tr("Conversion completed successfully!"))
            self.log(
                self.tr("Replaced variant: {} → {}").format(
                    variant_to_replace, target_variant
                )
            )
            self.log(self.tr("Total changes: {}").format(len(changes)))
            self.log("=" * 50)

            QMessageBox.information(
                self,
                self.tr("Success"),
                self.tr(
                    "Conversion completed!\nReplaced variant: {} → {}\nTotal changes: {}\n\nBefore flashing run:\nmibstd2_toolbox > Tools > Patch tsd.mibstd2.system.swdownload"
                ).format(variant_to_replace, target_variant, len(changes)),
            )

        except Exception as e:
            self.log(f"\n[ERROR] {self.tr('Conversion failed:')} {str(e)}")
            QMessageBox.critical(
                self,
                self.tr("Error"),
                self.tr("Conversion failed!\nError: {}").format(str(e)),
            )

    def link_ids(self, config, hwid):
        if not hwid:
            self.log(self.tr("HWID not provided - skipping linking"))
            return

        original_id = None
        for section in config.sections():
            parts = section.split("\\")
            if (
                len(parts) == 5
                and parts[0].lower() == "cpu"
                and parts[1].lower() == "customerupdateinfos"
            ):
                original_id = parts[2]
                self.log(self.tr("Found original ID: {}").format(original_id))
                break

        if not original_id:
            self.log(self.tr("No customerupdateinfos section found"))
            return

        if hwid == original_id:
            self.log(self.tr("HWID matches original ID - no linking needed"))
            return

        self.log(self.tr("Creating link for new ID: {}").format(hwid))

        new_config = configparser.ConfigParser()
        new_config.optionxform = str

        created_links = 0

        for section in config.sections():
            new_config.add_section(section)
            for option in config.options(section):
                new_config.set(section, option, config.get(section, option))

            if f"\\{original_id}\\" in section:
                new_section = section.replace(f"\\{original_id}\\", f"\\{hwid}\\")

                if not new_config.has_section(new_section):
                    new_config.add_section(new_section)
                    new_config.set(new_section, "Link", f'"[{section}]"')
                    created_links += 1
                    self.log(self.tr("Created link: {} → {}").format(original_id, hwid))

        config.clear()
        for section in new_config.sections():
            config.add_section(section)
            for option in new_config.options(section):
                config.set(section, option, new_config.get(section, option))

        if created_links == 0:
            self.log(
                self.tr("No links created - ID already matches or sections not found")
            )

    def add_standard_regions(self, config):
        if "common" not in config:
            return

        regions = {"Region3": '"USA"', "Region4": '"RoA"', "Region5": '"CN"'}

        if config.has_option("common", "RequiredVersionOfDM"):
            config.set("common", "RequiredVersionOfDM", '"0"')

        for region, value in regions.items():
            if not config.has_option("common", region):
                config.set("common", region, value)
                self.log(self.tr("Added region: {} = {}").format(region, value))

    def toggle_log_visibility(self):
        is_visible = not self.log_group.isVisible()
        self.log_group.setVisible(is_visible)
        self.clear_btn.setVisible(is_visible)

        if is_visible:
            self.show_log_btn.setText(self.tr("Hide Log"))
            self.log_output.verticalScrollBar().setValue(
                self.log_output.verticalScrollBar().maximum()
            )
        else:
            self.show_log_btn.setText(self.tr("Show Log"))

    def log(self, message):
        self.log_output.append(message)

        if any(k in message.upper() for k in ("ERROR", "FAILED", "WARNING")):
            if not self.log_group.isVisible():
                self.toggle_log_visibility()
            elif not self.clear_btn.isVisible():
                self.clear_btn.setVisible(True)

    def clear_log(self):
        self.log_output.clear()
        if not self.log_group.isVisible():
            self.clear_btn.setVisible(False)

    def change_language(self, lang):
        if lang == self.current_language:
            return
        self.current_language = lang
        (self.ru_action if lang == "ru" else self.en_action).setChecked(True)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.menuBar().actions()[0].setText(self.tr("File"))
        self.exit_action.setText(self.tr("Exit"))

        self.menuBar().actions()[1].setText(self.tr("Language"))

        self.menuBar().actions()[2].setText(self.tr("Help"))
        self.help_action.setText(self.tr("Online Documentation"))
        self.forum_action.setText(self.tr("Support Forum"))

        self.setWindowTitle(self.tr("MIB2 Universal Flasher Tool"))

        self.variant_group.setTitle(self.tr("Target Settings"))
        self.variant_label.setText(self.tr("Enter target variant:"))
        self.variant_input.setPlaceholderText(self.tr("Example: 17203"))

        self.hwid_group.setTitle(self.tr("SWDL"))
        self.hwid_label.setText(self.tr("SWDL HwVersion:"))
        self.hwid_input.setPlaceholderText(self.tr("Example: 20"))

        self.file_group.setTitle(self.tr("Metainfo2.txt File"))
        self.file_label.setText(self.tr("No file selected"))
        self.browse_btn.setText(self.tr("Browse..."))

        self.target_group.setTitle(self.tr("Target Parameters (auto-detected)"))
        self.target_brand_label.setText(self.tr("Target brand:"))
        self.target_platform_label.setText(self.tr("Target platform:"))
        self.target_region_label.setText(self.tr("Target region:"))

        self.source_group.setTitle(self.tr("Source Parameters (from file)"))
        self.source_brand_label.setText(self.tr("Source brand:"))
        self.source_platform_label.setText(self.tr("Source platform:"))
        self.source_region_label.setText(self.tr("Source region:"))

        self.mode_group.setTitle(self.tr("Operation Mode (auto-detected)"))
        self.cross_mode.setText(self.tr("Cross-flashing between brands"))
        self.zr_to_pq_mode.setText(self.tr("HMI ZR to PQ flashing"))

        self.log_group.setTitle(self.tr("Execution Log"))

        self.start_btn.setText(self.tr("Execute Conversion"))
        self.show_log_btn.setText(
            self.tr("Hide Log") if self.log_group.isVisible() else self.tr("Show Log")
        )
        self.clear_btn.setText(self.tr("Clear Log"))
        self.exit_btn.setText(self.tr("Exit"))

        if self.target_brand_value.text():
            target_variant = self.variant_input.text().strip()
            data = VARIANT_DB.get(target_variant)
            if data:
                self.target_brand_value.setText(data["brand"])
                self.target_platform_value.setText(data["platform"])
                self.target_region_value.setText(data["region"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MIB2FlasherGUI()
    window.show()
    sys.exit(app.exec_())
