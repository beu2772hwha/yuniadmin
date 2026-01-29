from __future__ import annotations


def get_stylesheet(name: str) -> str:
    theme = name.lower().strip()
    if theme == "light":
        return _LIGHT
    if theme == "yuni":
        return _YUNI
    return _DARK


_DARK = """
* {
    font-family: "Segoe UI", "Inter", "Arial";
    font-size: 12pt;
}
QMainWindow, QDialog {
    background: #0b1120;
    color: #e2e8f0;
}
QWidget {
    background-color: #0b1120;
    color: #e2e8f0;
}
QTabWidget::pane {
    border: 1px solid #1e293b;
    border-radius: 12px;
    margin-top: 8px;
    background: #0a1324;
}
QTabBar::tab {
    background: #0f1b35;
    color: #cbd5f5;
    padding: 10px 18px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 6px;
}
QTabBar::tab:selected {
    background: #1f2a44;
    color: #f8fafc;
}
QLabel {
    color: #e2e8f0;
}
QLineEdit, QSpinBox, QComboBox {
    background: #0a142b;
    border: 1px solid #1f2a44;
    border-radius: 8px;
    padding: 8px 12px;
    color: #f8fafc;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #60a5fa;
    background: #0b1833;
}
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #2563eb, stop:1 #22d3ee);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 10px 16px;
    font-weight: 600;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #1d4ed8, stop:1 #0ea5e9);
}
QPushButton:pressed {
    background: #1e40af;
}
QTableWidget {
    background: #0a142b;
    alternate-background-color: #0c1730;
    border: 1px solid #1e293b;
    gridline-color: #1e293b;
    border-radius: 12px;
}
QHeaderView::section {
    background: #0f1b35;
    color: #dbeafe;
    padding: 8px 10px;
    border: 0px;
    font-weight: 600;
}
QTableWidget::item:selected {
    background: #1f2a44;
    color: #f8fafc;
}
QScrollBar:vertical {
    background: #0b1120;
    width: 12px;
    margin: 0px;
    border-radius: 6px;
}
QScrollBar::handle:vertical {
    background: #334155;
    min-height: 24px;
    border-radius: 6px;
}
QScrollBar::handle:vertical:hover {
    background: #475569;
}
QCheckBox {
    spacing: 8px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #475569;
    background: #0a142b;
}
QCheckBox::indicator:checked {
    background: #22d3ee;
    border: 1px solid #22d3ee;
}
QMessageBox {
    background: #0b1120;
}
"""

_LIGHT = """
* {
    font-family: "Segoe UI", "Inter", "Arial";
    font-size: 12pt;
}
QMainWindow, QDialog {
    background: #f8fafc;
    color: #0f172a;
}
QWidget {
    background-color: #f8fafc;
    color: #0f172a;
}
QTabWidget::pane {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    margin-top: 8px;
    background: #ffffff;
}
QTabBar::tab {
    background: #e2e8f0;
    color: #0f172a;
    padding: 10px 18px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 6px;
}
QTabBar::tab:selected {
    background: #ffffff;
    color: #0f172a;
}
QLineEdit, QSpinBox, QComboBox {
    background: #ffffff;
    border: 1px solid #cbd5f5;
    border-radius: 8px;
    padding: 8px 12px;
    color: #0f172a;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #2563eb;
}
QPushButton {
    background: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 10px 16px;
    font-weight: 600;
}
QPushButton:hover {
    background: #1d4ed8;
}
QTableWidget {
    background: #ffffff;
    alternate-background-color: #f1f5f9;
    border: 1px solid #e2e8f0;
    gridline-color: #e2e8f0;
    border-radius: 12px;
}
QHeaderView::section {
    background: #e2e8f0;
    color: #0f172a;
    padding: 8px 10px;
    border: 0px;
    font-weight: 600;
}
QTableWidget::item:selected {
    background: #dbeafe;
    color: #0f172a;
}
"""

_YUNI = """
* {
    font-family: "Segoe UI", "Inter", "Arial";
    font-size: 12pt;
}
QMainWindow, QDialog {
    background: #0a0f1e;
    color: #e2e8f0;
}
QWidget {
    background-color: #0a0f1e;
    color: #e2e8f0;
}
QTabWidget::pane {
    border: 1px solid #1b2a4a;
    border-radius: 14px;
    margin-top: 8px;
    background: #0b1429;
}
QTabBar::tab {
    background: #121a33;
    color: #a5b4fc;
    padding: 10px 18px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 6px;
}
QTabBar::tab:selected {
    background: #1a2547;
    color: #f8fafc;
}
QLineEdit, QSpinBox, QComboBox {
    background: #0b1429;
    border: 1px solid #1f2a44;
    border-radius: 10px;
    padding: 8px 12px;
    color: #f8fafc;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #38bdf8;
    background: #0f1b3b;
}
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #2563eb, stop:0.5 #22d3ee, stop:1 #10b981);
    color: #ffffff;
    border: none;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 700;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #1d4ed8, stop:0.5 #0ea5e9, stop:1 #059669);
}
QTableWidget {
    background: #0b1429;
    alternate-background-color: #0f1b3b;
    border: 1px solid #1b2a4a;
    gridline-color: #1b2a4a;
    border-radius: 14px;
}
QHeaderView::section {
    background: #121a33;
    color: #e0e7ff;
    padding: 8px 10px;
    border: 0px;
    font-weight: 700;
}
QTableWidget::item:selected {
    background: #1f2a44;
    color: #f8fafc;
}
"""
