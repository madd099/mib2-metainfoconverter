# coding: utf-8

import sys
import os
import configparser
from pathlib import Path

if hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)

from PySide6.QtWidgets import (
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
    QMessageBox,
    QRadioButton,
    QButtonGroup,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QCompleter,
)
from PySide6.QtCore import Qt, QObject, QSize, QPropertyAnimation, QEasingCurve, Property, QRect, QStringListModel
from PySide6.QtGui import QIcon, QColor, QPainter, QFont, QAction, QActionGroup, QPen, QPixmap

from translations import translations
from variant_db import VARIANT_DB

VERSION = "2.0"

STYLE = """
* {
    font-family: "Segoe UI", "Inter", "Roboto", sans-serif;
    font-size: 13px;
    color: #1c1c1e;
    outline: none;
}
QMainWindow, QDialog {
    background: #f4f5f7;
}
QMenuBar {
    background: #ffffff;
    border-bottom: 1px solid #e4e6ea;
    padding: 2px 8px;
}
QMenuBar::item {
    padding: 6px 12px;
    background: transparent;
    border-radius: 6px;
}
QMenuBar::item:selected {
    background: #eef1f5;
}
QMenu {
    background: #ffffff;
    border: 1px solid #e4e6ea;
    border-radius: 8px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 24px 6px 16px;
    border-radius: 5px;
}
QMenu::item:selected {
    background: #e8f0fe;
    color: #1a56db;
}
QMenu::indicator {
    width: 14px;
    height: 14px;
}
QMenu::separator {
    height: 1px;
    background: #eceef1;
    margin: 4px 8px;
}

QLabel#windowTitle {
    font-size: 16px;
    font-weight: 700;
    color: #111827;
}
QLabel#versionBadge {
    background: #e8f0fe;
    color: #1a56db;
    font-size: 11px;
    font-weight: 600;
    border-radius: 11px;
    padding: 2px 10px;
    margin-left: 4px;
}
QLabel#unitIcon {
    font-size: 26px;
}

QFrame[card="true"] {
    background: #ffffff;
    border: 1px solid #e4e6ea;
    border-radius: 12px;
}
QLabel[cardTitle="true"] {
    font-size: 13px;
    font-weight: 600;
    color: #374151;
}
QLabel[hint="true"] {
    color: #8a919c;
    font-size: 12px;
}
QLabel[fieldName="true"] {
    color: #6b7280;
    min-width: 110px;
}
QLabel[fieldValue="true"] {
    font-weight: 600;
}
QLabel#statusChipNeutral {
    background: #eef1f5;
    color: #6b7280;
    border-radius: 10px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 600;
}
QLabel#statusChipOk {
    background: #e5f6ec;
    color: #18794e;
    border-radius: 10ps;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 600;
}
QLabel#statusChipError {
    background: #fdecec;
    color: #c92a2a;
    border-radius: 10px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 600;
}

QLineEdit {
    background: #ffffff;
    border: 1.5px solid #d7dbe0;
    border-radius: 8px;
    padding: 8px 12px;
    selection-background-color: #bcd4fb;
}
QLineEdit:hover { border-color: #b8c0cc; }
QLineEdit:focus { border-color: #1a56db; }
QLineEdit:disabled {
    background: #f2f3f5;
    color: #9aa1ab;
}

QPushButton {
    background: #eef1f5;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 500;
}
QPushButton:hover { background: #e2e6ec; }
QPushButton:pressed { background: #d6dbe3; }
QPushButton:disabled {
    background: #f2f3f5;
    color: #b0b6bf;
}

QPushButton[accent="true"] {
    background: #1a56db;
    color: #ffffff;
    font-weight: 600;
    padding: 10px 20px;
}
QPushButton[accent="true"]:hover { background: #1e66f5; }
QPushButton[accent="true"]:pressed { background: #1648b5; }
QPushButton[accent="true"]:disabled {
    background: #c3ccdc;
    color: #f4f6fa;
}

QPushButton[success="true"] {
    background: #18794e;
    color: #ffffff;
    font-weight: 600;
    padding: 10px 20px;
}
QPushButton[success="true"]:hover { background: #1d9260; }

QRadioButton { spacing: 8px; }
QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 10px;
    border: 2px solid #b8c0cc;
    background: #ffffff;
}
QRadioButton::indicator:hover { border-color: #1a56db; }
QRadioButton::indicator:checked {
    border: 2px solid #1a56db;
    background: #1a56db;
}
QRadioButton:disabled { color: #9aa1ab; }
QRadioButton::indicator:disabled {
    border-color: #d7dbe0;
    background: #f2f3f5;
}

QCheckBox { spacing: 8px; }

QTextEdit {
    background: #ffffff;
    border: 1.5px solid #d7dbe0;
    border-radius: 8px;
    padding: 8px;
    font-family: "Consolas", "Cascadia Mono", monospace;
    font-size: 12px;
}
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: #cdd2d9;
    min-height: 30px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover { background: #b0b6bf; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 2px;
}
QScrollBar::handle:horizontal {
    background: #cdd2d9;
    min-width: 30px;
    border-radius: 5px;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

QToolTip {
    background: #111827;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 5px 9px;
}
"""


class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(44, 26)
        self.setCursor(Qt.PointingHandCursor)
        self._offset = 3.0
        self._anim = QPropertyAnimation(self, b"offset", self)
        self._anim.setDuration(140)
        self._anim.setEasingCurve(QEasingCurve.InOutQuad)

    def get_offset(self):
        return self._offset

    def set_offset(self, value):
        self._offset = value
        self.update()

    offset = Property(float, get_offset, set_offset)

    def sizeHint(self):
        return QSize(44, 26)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setChecked(not self.isChecked())
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        radius = h / 2.0

        checked = self.isChecked()
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#1a56db") if checked else QColor("#c8cdd5"))
        p.drawRoundedRect(QRect(0, 0, w, h), radius, radius)

        target = (w - radius * 2 - 3.0) if checked else 3.0
        if abs(self._offset - target) > 0.5 and self._anim.state() != QPropertyAnimation.Running:
            self._anim.stop()
            self._anim.setStartValue(self._offset)
            self._anim.setEndValue(target)
            self._anim.start()

        knob = h - 6
        p.setBrush(QColor("#ffffff"))
        p.drawEllipse(int(self._offset), 3, knob, knob)
        p.end()


class FlagButton(QWidget):
    FILES = {
        "ru": "free-icon-russia-555451.png",
        "us": "free-icon-united-states-206626.png",
    }

    def __init__(self, kind, on_click, parent=None):
        super().__init__(parent)
        self.kind = kind
        self.on_click = on_click
        self.active = False
        self.setFixedSize(34, 22)
        self.setCursor(Qt.PointingHandCursor)
        self.pixmap = self._load_pixmap()

    def _load_pixmap(self):
        name = self.FILES.get(self.kind)
        candidates = []
        if hasattr(sys, "_MEIPASS"):
            candidates.append(os.path.join(sys._MEIPASS, name))
        candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), name))
        candidates.append(name)
        for c in candidates:
            if os.path.exists(c):
                pm = QPixmap(c)
                if not pm.isNull():
                    return pm
        return None

    def set_active(self, active):
        self.active = active
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.on_click()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        w, h = self.width(), self.height()
        if self.pixmap is not None:
            scaled = self.pixmap.scaled(
                w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            p.setOpacity(1.0 if self.active else 0.35)
            p.drawPixmap((w - scaled.width()) // 2, (h - scaled.height()) // 2, scaled)
            p.setOpacity(1.0)
        p.end()


class Card(QFrame):
    def __init__(self, title=None):
        super().__init__()
        self.setProperty("card", True)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(20, 16, 20, 18)
        self._layout.setSpacing(10)
        if title:
            t = QLabel(title)
            t.setProperty("cardTitle", True)
            self._layout.addWidget(t)
            self.title_label = t
        else:
            self.title_label = None

    def content(self):
        return self._layout

    def set_title(self, text):
        if self.title_label:
            self.title_label.setText(text)


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
        self.log_visible = False
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
            for icon_path in possible_paths:
                if icon_path and os.path.exists(icon_path):
                    try:
                        self.setWindowIcon(QIcon(icon_path))
                        return
                    except Exception:
                        continue
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

        special_menu = menubar.addMenu(self.tr("Special"))
        self.links_only_action = QAction(self.tr("Links replacement only"), self)
        self.links_only_action.setCheckable(True)
        self.links_only_action.toggled.connect(self.on_links_only_toggled)
        special_menu.addAction(self.links_only_action)

        self.patches_menu = special_menu.addMenu(self.tr("HMI ZR-PQ patches"))
        self.clock_patch_action = QAction(self.tr("Future date patch"), self)
        self.clock_patch_action.triggered.connect(self.open_clock_patcher)
        self.patches_menu.addAction(self.clock_patch_action)

        self.volume_patch_action = QAction(self.tr("Volume slider patch"), self)
        self.volume_patch_action.triggered.connect(self.open_volume_patch)
        self.patches_menu.addAction(self.volume_patch_action)

        help_menu = menubar.addMenu(self.tr("Help"))
        self.help_action = QAction(self.tr("Online Documentation"), self)
        self.help_action.triggered.connect(self.open_help)
        help_menu.addAction(self.help_action)

        self.forum_action = QAction(self.tr("Support Forum"), self)
        self.forum_action.triggered.connect(self.open_forum)
        help_menu.addAction(self.forum_action)

        self.github_action = QAction(self.tr("GitHub"), self)
        self.github_action.triggered.connect(self.open_github)
        help_menu.addAction(self.github_action)

        # Corner language switcher RU/EN (flags) + version badge
        self.lang_widget = QWidget(menubar)
        lang_layout = QHBoxLayout(self.lang_widget)
        lang_layout.setContentsMargins(0, 0, 8, 0)
        lang_layout.setSpacing(6)
        self.version_badge = QLabel(" v" + VERSION + " ")
        self.version_badge.setObjectName("versionBadge")
        self.version_badge.setFixedHeight(22)
        self.version_badge.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.ru_flag = FlagButton("ru", lambda: self.change_language("ru"), self.lang_widget)
        self.us_flag = FlagButton("us", lambda: self.change_language("en"), self.lang_widget)
        lang_layout.addWidget(self.version_badge)
        lang_layout.addWidget(self.ru_flag)
        lang_layout.addWidget(self.us_flag)
        self.ru_flag.set_active(True)
        menubar.setCornerWidget(self.lang_widget, Qt.TopRightCorner)

        self.setWindowTitle(self.tr("MIB2 Universal Flasher Tool"))
        self.resize(860, 760)
        self.setMinimumWidth(860)

        central = QWidget()
        self.setCentralWidget(central)
        main = QVBoxLayout(central)
        self._main_layout = main
        main.setContentsMargins(24, 18, 24, 18)
        main.setSpacing(12)

        header = QHBoxLayout()
        header.addStretch(1)
        main.addLayout(header)

        self.unit_card = Card(self.tr("Target Settings"))
        ucl = self.unit_card.content()

        row_variant = QHBoxLayout()
        row_variant.setSpacing(10)
        self.variant_label = QLabel(self.tr("Enter target variant:"))
        self.variant_input = QLineEdit()
        self.variant_input.setPlaceholderText(self.tr("Example: 17203"))
        self.variant_input.setMaxLength(5)
        self.variant_input.setClearButtonEnabled(True)
        self.variant_input.textChanged.connect(self.on_variant_changed)
        row_variant.addWidget(self.variant_label)
        row_variant.addWidget(self.variant_input, 1)
        ucl.addLayout(row_variant)

        completer_model = QStringListModel(self)
        items = []
        for v, d in VARIANT_DB.items():
            items.append(
                "{}   {} · {} · {} · NAVI {} · DAB {}".format(
                    v,
                    d["brand"],
                    d["platform"],
                    d["region"],
                    "✓" if d["navi"] == "yes" else "✗",
                    "✓" if d["dab"] == "yes" else "✗",
                )
            )
        completer_model.setStringList(items)

        self.variant_completer = QCompleter(completer_model, self)
        self.variant_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.variant_completer.setFilterMode(Qt.MatchContains)
        self.variant_completer.setCompletionMode(QCompleter.PopupCompletion)
        self.variant_completer.setMaxVisibleItems(6)
        popup = self.variant_completer.popup()
        popup.setStyleSheet("""
QListView {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 6px;
    font-size: 13px;
    outline: 0;
}
QListView::item {
    padding: 10px 14px;
    border-radius: 8px;
    margin: 1px 2px;
    color: #1e293b;
}
QListView::item:hover {
    background: #f1f5f9;
}
QListView::item:selected {
    background: #e0e7ff;
    color: #1d4ed8;
    font-weight: 600;
}
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 4px 2px;
}
QScrollBar::handle:vertical {
    background: #cbd5e1;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
""")
        self.variant_input.setCompleter(self.variant_completer)
        self.variant_completer.activated.connect(self.on_completer_activated)

        chips_row = QHBoxLayout()
        chips_row.setSpacing(8)

        self.target_chip_main = QLabel("")
        self.target_chip_main.setObjectName("statusChipInfo")
        self.target_chip_main.setVisible(False)
        chips_row.addWidget(self.target_chip_main)

        self.target_chip_navi = QLabel("")
        self.target_chip_navi.setVisible(False)
        chips_row.addWidget(self.target_chip_navi)

        self.target_chip_dab = QLabel("")
        self.target_chip_dab.setVisible(False)
        chips_row.addWidget(self.target_chip_dab)

        chips_row.addStretch(1)
        ucl.addLayout(chips_row)

        row_hwid = QHBoxLayout()
        row_hwid.setSpacing(10)
        self.hwid_label = QLabel(self.tr("SWDL HwVersion:"))
        self.hwid_input = QLineEdit()
        self.hwid_input.setPlaceholderText(self.tr("Example: 20"))
        row_hwid.addWidget(self.hwid_label)
        row_hwid.addWidget(self.hwid_input, 1)
        ucl.addLayout(row_hwid)

        main.addWidget(self.unit_card)

        self.file_card = Card(self.tr("Metainfo2.txt File"))
        fcl = self.file_card.content()

        row_file = QHBoxLayout()
        row_file.setSpacing(10)
        self.file_label = QLabel(self.tr("No file selected"))
        self.file_label.setProperty("hint", True)
        self.file_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.browse_btn = QPushButton(self.tr("Browse..."))
        self.browse_btn.clicked.connect(self.browse_file)
        row_file.addWidget(self.file_label)
        row_file.addWidget(self.browse_btn)
        fcl.addLayout(row_file)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setStyleSheet("color: #eceef1;")
        self.file_sep = sep2
        fcl.addWidget(sep2)

        self.source_hint = QLabel()
        self.source_hint.setProperty("cardTitle", True)
        fcl.addWidget(self.source_hint)

        chips_row_src = QHBoxLayout()
        chips_row_src.setSpacing(8)

        self.source_chip_main = QLabel("")
        self.source_chip_main.setObjectName("statusChipInfo")
        self.source_chip_main.setVisible(False)
        chips_row_src.addWidget(self.source_chip_main)

        chips_row_src.addStretch(1)
        fcl.addLayout(chips_row_src)
        main.addWidget(self.file_card)

        self.mode_card = Card(self.tr("Conversion Type"))
        mcl = self.mode_card.content()

        self.mode_summary = QLabel("—")
        self.mode_summary.setStyleSheet(
            "background: #f7f8fa; color: #475569; border: 1.5px dashed #cbd5e1;"
            " border-radius: 10px; padding: 14px 18px; font-size: 18px; font-weight: 600;"
        )
        self.mode_summary.setAlignment(Qt.AlignCenter)
        mcl.addWidget(self.mode_summary)

        self.mode_btn_group = QButtonGroup(self)
        self.cross_mode = QRadioButton(self.tr("Cross-flashing between brands"))
        self.cross_mode.setChecked(True)
        self.cross_mode.setEnabled(False)
        self.cross_mode.setVisible(False)
        self.mode_btn_group.addButton(self.cross_mode)
        self.zr_to_pq_mode = QRadioButton(self.tr("HMI ZR to PQ flashing"))
        self.zr_to_pq_mode.setEnabled(False)
        self.zr_to_pq_mode.setVisible(False)
        self.mode_btn_group.addButton(self.zr_to_pq_mode)
        main.addWidget(self.mode_card)

        row_run = QHBoxLayout()
        row_run.setSpacing(12)
        self.start_btn = QPushButton(self.tr("Execute Conversion"))
        self.start_btn.setProperty("accent", True)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.start_btn.setMinimumHeight(42)
        self.start_btn.clicked.connect(self.start_conversion)
        self.start_btn.setEnabled(False)
        row_run.addWidget(self.start_btn)
        main.addLayout(row_run)

        row_log_head = QHBoxLayout()
        row_log_head.setSpacing(10)
        self.log_caption = QLabel(self.tr("Execution Log"))
        self.log_caption.setProperty("cardTitle", True)
        self.log_toggle = ToggleSwitch()
        self.log_toggle.toggled.connect(self.toggle_log_visibility)
        row_log_head.addWidget(self.log_caption)
        row_log_head.addStretch(1)
        row_log_head.addWidget(self.log_toggle)
        main.addLayout(row_log_head)

        self.log_card = Card()
        self.log_card.setVisible(False)
        self.log_card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        lcl = self.log_card.content()
        lcl.setContentsMargins(12, 12, 12, 12)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.log_output.setMinimumHeight(120)
        lcl.addWidget(self.log_output)
        row_log_btns = QHBoxLayout()
        row_log_btns.addStretch(1)
        self.clear_btn = QPushButton(self.tr("Clear Log"))
        self.clear_btn.clicked.connect(self.clear_log)
        row_log_btns.addWidget(self.clear_btn)
        lcl.addLayout(row_log_btns)
        main.addWidget(self.log_card)

        main.addStretch(1)

        self.source_hint.setText(self.tr("Source Parameters (from file)"))

        self.current_mode = "cross"

    def _set_target_chips(self, data):
        main_text = "{} · {} · {}".format(data["brand"], data["platform"], data["region"])
        self.target_chip_main.setText(main_text)
        self.target_chip_main.setStyleSheet(
            "background:#e8f0fe; color:#1a56db; border-radius:10px; padding:5px 12px;"
            " font-size:13px; font-weight:600;"
        )
        self.target_chip_main.setVisible(True)

        ok_style = (
            "background:#e5f6ec; color:#18794e; border-radius:10px; padding:5px 12px;"
            " font-size:12px; font-weight:600;"
        )
        no_style = (
            "background:#fdecec; color:#c92a2a; border-radius:10px; padding:5px 12px;"
            " font-size:12px; font-weight:600;"
        )

        navi_ok = data["navi"] == "yes"
        self.target_chip_navi.setText("NAVI {}".format("✓" if navi_ok else "✗"))
        self.target_chip_navi.setStyleSheet(ok_style if navi_ok else no_style)
        self.target_chip_navi.setVisible(True)

        dab_ok = data["dab"] == "yes"
        self.target_chip_dab.setText("DAB {}".format("✓" if dab_ok else "✗"))
        self.target_chip_dab.setStyleSheet(ok_style if dab_ok else no_style)
        self.target_chip_dab.setVisible(True)

    def _hide_target_chips(self):
        for w in (self.target_chip_main, self.target_chip_navi, self.target_chip_dab):
            w.setVisible(False)

    def _set_source_chips(self, brand, platform, region):
        self.source_chip_main.setText("{} · {} · {}".format(brand, platform, region))
        self.source_chip_main.setStyleSheet(
            "background:#e8f0fe; color:#1a56db; border-radius:10px; padding:5px 12px;"
            " font-size:13px; font-weight:600;"
        )
        self.source_chip_main.setVisible(not self.links_only_action.isChecked())

    def on_completer_activated(self, text):
        variant_id = text.split()[0] if text else ""
        if variant_id.isdigit() and len(variant_id) == 5:
            self.variant_input.blockSignals(True)
            self.variant_input.setText(variant_id)
            self.variant_input.blockSignals(False)
            self.update_from_variant()

    def on_variant_changed(self, text):
        text = text.strip()
        if len(text) == 5 and text.isdigit():
            self.variant_completer.popup().hide()
            self.variant_completer.setCompletionPrefix("")
            self.update_from_variant()
        else:
            self._hide_target_chips()
            self.start_btn.setEnabled(False)

    def open_help(self):
        import webbrowser

        webbrowser.open("https://www.drive2.ru/users/stasinator/")

    def open_forum(self):
        import webbrowser

        webbrowser.open("https://www.drive2.ru/l/614500832041241045/")

    def open_github(self):
        import webbrowser

        webbrowser.open("https://github.com/madd099/mib2-metainfoconverter")

    def open_volume_patch(self):
        import webbrowser

        webbrowser.open("https://www.drive2.ru/b/708474166721917664/")

    def open_clock_patcher(self):
        pw = getattr(self, "_patcher_window", None)
        if pw is None or pw.lang != self.current_language:
            from clock_patcher import AutoHexPatcherGUI

            pw = AutoHexPatcherGUI(self.current_language)
            pw.setWindowIcon(self.windowIcon())
            self._patcher_window = pw
        pw.show()
        pw.raise_()
        pw.activateWindow()

    def on_links_only_toggled(self, checked):
        self._apply_links_only_ui(checked)
        if checked:
            self.log(self.tr("Links replacement only mode enabled"))
        else:
            self.log(self.tr("Links replacement only mode disabled"))

    def _apply_links_only_ui(self, checked):
        widgets = (
            self.variant_label,
            self.variant_input,
            self.target_chip_main,
            self.target_chip_navi,
            self.target_chip_dab,
            self.mode_card,
            self.source_hint,
            self.source_chip_main,
            self.file_sep,
        )
        for w in widgets:
            w.setVisible(not checked)
        self.unit_card.set_title(
            self.tr("HwVersion") if checked else self.tr("Target Settings")
        )
        self.start_btn.setText(
            self.tr("Change HwVersion")
            if checked
            else self.tr("Execute Conversion")
        )
        self._refresh_start_enabled()

    def _refresh_start_enabled(self):
        if self.links_only_action.isChecked():
            self.start_btn.setEnabled(hasattr(self, "input_file"))
        elif hasattr(self, "source_platform") and self.variant_input.text().strip() in VARIANT_DB:
            self.update_operation_mode()
        else:
            self.start_btn.setEnabled(False)

    def update_from_variant(self):
        variant = self.variant_input.text().strip()
        data = VARIANT_DB.get(variant)

        if data:
            self._set_target_chips(data)
            self.log(
                self.tr(
                    "Auto-detected target: brand={}, platform={}, region={}"
                ).format(data["brand"], data["platform"], data["region"])
            )

            if hasattr(self, "source_platform"):
                self.update_operation_mode()
        else:
            self.log(self.tr("Variant not found in database"))
            self._hide_target_chips()
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
            self.file_label.setProperty("hint", False)
            self.file_label.setStyleSheet("color:#1c1c1e;")
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
                        self._refresh_start_enabled()
                        return
                    else:
                        self.log(self.tr("Region verification passed: EU"))

                if len(parts) >= 4:
                    brand_map = {"VW": "VW", "SE": "SEAT", "SK": "Skoda"}
                    brand_code = parts[2]
                    self.source_brand = brand_map.get(brand_code)

                    platform_part = parts[3]
                    self.source_platform = platform_part.upper()

                    if self.source_brand and self.source_platform in ["PQ", "ZR"]:
                        self._set_source_chips(
                            self.source_brand, self.source_platform, region
                        )
                        self.log(
                            self.tr(
                                "Auto-detected source: brand={}, platform={}"
                            ).format(self.source_brand, self.source_platform)
                        )

                        if self.variant_input.text():
                            self.update_operation_mode()
                        else:
                            self._refresh_start_enabled()
                        return

            raise ValueError("Could not determine source parameters from file")

        except Exception as e:
            self.log(self.tr("Error analyzing file: {}").format(str(e)))
            self._refresh_start_enabled()

    def update_operation_mode(self):
        if not hasattr(self, "source_platform") or not self.variant_input.text():
            return

        target_data = VARIANT_DB.get(self.variant_input.text().strip())
        if not target_data:
            return
        target_platform = target_data["platform"]
        target_brand = target_data["brand"]

        if self.source_platform == "ZR" and target_platform == "PQ":
            self.zr_to_pq_mode.setChecked(True)
            self.current_mode = "zr-to-pq"
            self.mode_summary.setText(
                self.tr("⚡ Прошивка {} ZR HMI в {} PQ").format(self.source_brand, target_brand)
            )
            self.log(self.tr("Auto-selected ZR→PQ mode"))
        else:
            self.cross_mode.setChecked(True)
            self.current_mode = "cross"
            self.mode_summary.setText(
                "🔁 {} {} → {} {}".format(
                    target_brand, target_platform, self.source_brand, self.source_platform
                )
            )
            self.log(self.tr("Auto-selected cross-flash mode"))

        if self.source_platform == "PQ" and target_platform == "ZR":
            self.start_btn.setEnabled(False)
            self.mode_summary.setText(
                "⛔ {} PQ → {} ZR {}".format(target_brand, self.source_brand, self.tr("prohibited"))
            )
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
        dialog.resize(520, calculated_height)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

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
        variants_frame.setProperty("card", True)
        variants_layout = QVBoxLayout(variants_frame)
        variants_layout.setContentsMargins(14, 10, 14, 10)
        variants_layout.setSpacing(6)

        variants_label = QLabel(self.tr("Available variants:"))
        variants_label.setProperty("cardTitle", True)
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

        variants_frame.setEnabled(False)
        layout.addWidget(variants_frame)

        auto_select_checkbox.toggled.connect(variants_frame.setDisabled)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

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

        links_only = self.links_only_action.isChecked()

        try:
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read(self.input_file, encoding="utf-8")

            if links_only:
                backup_file = Path(self.input_file).with_suffix(".bak")
                with backup_file.open("w", encoding="utf-8") as f:
                    config.write(f)
                self.log(self.tr("Backup created: {}").format(backup_file))

                self.link_ids(config, hwid)
                self.log(self.tr("Using HWID: {}").format(hwid))

                with Path(self.input_file).open("w", encoding="utf-8") as f:
                    config.write(f)

                self.log("\n" + "=" * 50)
                self.log(self.tr("Conversion completed successfully!"))
                self.log(self.tr("Using HWID: {}").format(hwid))
                self.log("=" * 50)

                QMessageBox.information(
                    self,
                    self.tr("Success"),
                    self.tr("Линки успешно созданы!"),
                )
                return

            target_data = VARIANT_DB.get(self.variant_input.text().strip())
            if not target_data:
                raise ValueError(self.tr("Target variant not found in database"))

            self._set_target_chips(target_data)

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
            is_hmizr = self.current_mode == "zr-to-pq"
            for section in config.sections():
                if is_hmizr:
                    section_lower = section.lower()
                    allowed = (
                        section_lower == "common"
                        or (section_lower.startswith("cpu") and "hmizr" in section_lower)
                    )
                    if not allowed:
                        continue
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

            success_msg = self.tr(
                "Conversion completed!\nReplaced variant: {} → {}\nTotal changes: {}\n\nBefore flashing run:\nmibstd2_toolbox > Tools > Patch tsd.mibstd2.system.swdownload"
            ).format(variant_to_replace, target_variant, len(changes))

            if self.current_mode == "zr-to-pq":
                success_msg += "\n\n" + self.tr(
                    'После прошивки для исправления багов HMI используйте "HMI ZR-PQ патчи" из меню "Специальные"'
                )

            QMessageBox.information(self, self.tr("Success"), success_msg)

        except PermissionError as e:
            protected_file = getattr(e, "filename", None) or self.input_file
            self.log(f"\n[ERROR] {self.tr('Conversion failed:')} {str(e)}")
            self.log(self.tr("File is write-protected: {}").format(protected_file))
            QMessageBox.critical(
                self,
                self.tr("Error"),
                self.tr(
                    'Файл защищён от записи!\nСнимите атрибут "только чтение" с файла:\n{}\n\n(правый клик по файлу → Свойства → снимите галочку "Только чтение") и повторите конвертацию.'
                ).format(protected_file),
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

    def toggle_log_visibility(self, checked=None):
        if checked is None:
            checked = not self.log_card.isVisible()
        self.log_visible = checked
        self.log_card.setVisible(checked)
        if self.log_toggle.isChecked() != checked:
            self.log_toggle.blockSignals(True)
            self.log_toggle.setChecked(checked)
            self.log_toggle.blockSignals(False)
        if checked:
            self.log_output.verticalScrollBar().setValue(
                self.log_output.verticalScrollBar().maximum()
            )
            self._expand_to_log()
        else:
            self._collapse_to_compact()

    def _expand_to_log(self):
        screen = self.screen().availableGeometry()
        desired_h = 1080
        max_h = int(screen.height() - self.frameGeometry().height() + self.geometry().height() - 20)
        target_h = min(desired_h, max_h)
        self.setMinimumHeight(target_h)
        self.resize(self.width(), target_h)

    def _collapse_to_compact(self):
        self.setMinimumHeight(0)
        self.resize(self.width(), 760)

    def log(self, message):
        self.log_output.append(message)
        if any(k in message.upper() for k in ("ERROR", "FAILED", "WARNING")):
            if not self.log_card.isVisible():
                self.toggle_log_visibility(True)

    def clear_log(self):
        self.log_output.clear()

    def change_language(self, lang):
        if lang == self.current_language:
            return
        self.current_language = lang
        self.ru_flag.set_active(lang == "ru")
        self.us_flag.set_active(lang == "en")
        self.retranslate_ui()

    def retranslate_ui(self):
        menus = self.menuBar().actions()
        menus[0].setText(self.tr("File"))
        self.exit_action.setText(self.tr("Exit"))
        menus[1].setText(self.tr("Special"))
        self.links_only_action.setText(self.tr("Links replacement only"))
        self.patches_menu.setTitle(self.tr("HMI ZR-PQ patches"))
        self.clock_patch_action.setText(self.tr("Future date patch"))
        self.volume_patch_action.setText(self.tr("Volume slider patch"))
        menus[2].setText(self.tr("Help"))
        self.help_action.setText(self.tr("Online Documentation"))
        self.forum_action.setText(self.tr("Support Forum"))
        self.github_action.setText(self.tr("GitHub"))

        self.setWindowTitle(self.tr("MIB2 Universal Flasher Tool"))

        self.unit_card.set_title(
            self.tr("HwVersion")
            if self.links_only_action.isChecked()
            else self.tr("Target Settings")
        )
        self.variant_label.setText(self.tr("Enter target variant:"))
        self.variant_input.setPlaceholderText(self.tr("Example: 17203"))
        self.hwid_label.setText(self.tr("SWDL HwVersion:"))
        self.hwid_input.setPlaceholderText(self.tr("Example: 20"))

        self.file_card.set_title(self.tr("Metainfo2.txt File"))
        if not hasattr(self, "input_file"):
            self.file_label.setText(self.tr("No file selected"))
        self.browse_btn.setText(self.tr("Browse..."))

        self.source_hint.setText(self.tr("Source Parameters (from file)"))

        self.mode_card.set_title(self.tr("Conversion Type"))

        self.start_btn.setText(
            self.tr("Change HwVersion")
            if self.links_only_action.isChecked()
            else self.tr("Execute Conversion")
        )
        self.log_caption.setText(self.tr("Execution Log"))
        self.clear_btn.setText(self.tr("Clear Log"))

        target_variant = self.variant_input.text().strip()
        data = VARIANT_DB.get(target_variant)
        if data:
            self._set_target_chips(data)

        if hasattr(self, "source_platform"):
            self.update_operation_mode()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    window = MIB2FlasherGUI()
    window.show()
    sys.exit(app.exec())
