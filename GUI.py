
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGridLayout, QDialog, QFormLayout, QLineEdit,
    QMessageBox
)
from PyQt6.QtCore import QTimer, Qt, QDateTime
from PyQt6.QtGui import QColor
import sys
from les_classes import Parking

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parking Magique - Dashboard")
        self.resize(1200, 700)

        central = QWidget(); self.setCentralWidget(central)
        layout = QHBoxLayout(); central.setLayout(layout)

        # Left: parking grid
        self.grid_widget = QWidget()
        self.grid = QGridLayout(); self.grid_widget.setLayout(self.grid)
        layout.addWidget(self.grid_widget, 3)

        # Right panel
        right_panel = QVBoxLayout()
        layout.addLayout(right_panel, 1)

        # Date/time
        self.lbl_datetime = QLabel(); self.lbl_datetime.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_panel.addWidget(self.lbl_datetime)

        # Stats
        self.lbl_stats = QLabel(); self.lbl_stats.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_panel.addWidget(self.lbl_stats)

        # Buttons bottom-right
        btn_box = QVBoxLayout()
        self.btn_abonnement = QPushButton("Abonnement")
        self.btn_param = QPushButton("Paramètres")
        btn_box.addWidget(self.btn_abonnement)
        btn_box.addWidget(self.btn_param)
        btn_box.addStretch()
        right_panel.addLayout(btn_box)

        # Timer
        self.timer = QTimer(); self.timer.timeout.connect(self.update_all)
        self.timer.start(2000)

        self.update_all()

    def update_all(self):
        self.update_datetime()
        self.update_stats()
        self.update_grid()

    def update_datetime(self):
        now = QDateTime.currentDateTime()
        self.lbl_datetime.setText(now.toString("dd MMMM yyyy - HH:mm:ss"))

    def update_stats(self):
        total = len(Parking.liste_place())
        libres = len(Parking.places_libres())
        occupees = len(Parking.places_occupees())
        reservees = len(Parking.places_abonnes())
        taux = round(100 * (occupees+reservees) / total, 1) if total else 0
        self.lbl_stats.setText(
            f"Places libres: {libres}\n"
            f"Occupées: {occupees}\n"
            f"Réservées: {reservees}\n"
            f"Taux occupation: {taux}%"
        )

    def update_grid(self):
        # Clear grid
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget(); w.deleteLater()

        places = Parking.places()
        cols = 10
        for idx, p in enumerate(places):
            row = idx // cols
            col = idx % cols

            btn = QPushButton()
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(f"border-radius:20px; background:{self.color_for_place(p)};")
            btn.clicked.connect(lambda _, place=p: self.place_clicked(place))
            self.grid.addWidget(btn, row, col)

    def color_for_place(self, p):
        if p.plaque:
            return "red"
        # places_abonnes returns tuples: (place_obj, plaque)
        for place_obj, plaque in Parking.places_abonnes():
            if place_obj.id == p.id:
                return "blue"
        return "green"

    def place_clicked(self, p):
        if p.plaque:
            self.sortie_dialog(p)
        else:
            self.arrivee_dialog(p)

    def arrivee_dialog(self, p):
        dlg = QDialog(self)
        form = QFormLayout(dlg)
        plaque_edit = QLineEdit()
        form.addRow("Plaque:", plaque_edit)
        ok = QPushButton("Entrée"); form.addRow(ok)

        def do_ok():
            plaque = plaque_edit.text().strip()
            if not plaque:
                QMessageBox.warning(self, "Erreur", "Plaque vide")
                return
            Parking.occuper_place(p.id, plaque)
            dlg.accept(); self.update_all()

        ok.clicked.connect(do_ok)
        dlg.exec()

    def sortie_dialog(self, p):
        dlg = QDialog(self)
        form = QFormLayout(dlg)
        ok = QPushButton("Sortie"); form.addRow(ok)

        def do_ok():
            Parking.liberer_place(p.id)
            dlg.accept(); self.update_all()

        ok.clicked.connect(do_ok)
        dlg.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow(); w.show()
    sys.exit(app.exec())
