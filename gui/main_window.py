from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from core.scanner import ModScanner
from core.metadata_parser import MetadataParser
from core.classifier import Classifier
from core.analyzers.classes import ClassAnalyzer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minecraft Mod Analyzer")
        self.resize(1100, 700)

        self.mods_folder = ""

        self.build_ui()

    def build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        title = QLabel("Minecraft Mod Analyzer")
        title.setStyleSheet("font-size:24px;font-weight:bold;")
        layout.addWidget(title)

        # -------------------------

        row = QHBoxLayout()

        self.path_box = QLineEdit()
        self.path_box.setReadOnly(True)

        browse_btn = QPushButton("Seleccionar carpeta")
        browse_btn.clicked.connect(self.select_folder)

        row.addWidget(self.path_box)
        row.addWidget(browse_btn)

        layout.addLayout(row)

        # -------------------------

        self.scan_btn = QPushButton("Analizar Mods")
        self.scan_btn.clicked.connect(self.scan_mods)

        layout.addWidget(self.scan_btn)

        # -------------------------

        self.summary = QLabel("Mods analizados: 0")
        layout.addWidget(self.summary)

        # -------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Mod",
            "Loader",
            "Tipo",
            "Confianza",
            "Dependencias"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Selecciona la carpeta de mods"
        )

        if folder:

            self.mods_folder = folder
            self.path_box.setText(folder)

    def scan_mods(self):

        if not self.mods_folder:

            QMessageBox.warning(
                self,
                "Error",
                "Selecciona primero una carpeta."
            )

            return

        try:

            scanner = ModScanner(self.mods_folder)
            parser = MetadataParser()
            classifier = Classifier()
            analyzer = ClassAnalyzer()

            mods = scanner.scan()

            self.table.setRowCount(0)

            self.summary.setText(
                f"Mods analizados: {len(mods)}"
            )

            for mod in mods:

                metadata = parser.parse(mod.path)

                analysis = analyzer.analyze(mod.path)

                result = classifier.classify(
                    metadata,
                    analysis
                )

                row = self.table.rowCount()

                self.table.insertRow(row)

                self.table.setItem(
                    row,
                    0,
                    QTableWidgetItem(
                        metadata.name or mod.name
                    )
                )

                self.table.setItem(
                    row,
                    1,
                    QTableWidgetItem(
                        metadata.loader
                    )
                )

                self.table.setItem(
                    row,
                    2,
                    QTableWidgetItem(
                        result.side
                    )
                )

                self.table.setItem(
                    row,
                    3,
                    QTableWidgetItem(
                        f"{result.confidence}%"
                    )
                )

                depends = ", ".join(metadata.depends)

                self.table.setItem(
                    row,
                    4,
                    QTableWidgetItem(depends)
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )
