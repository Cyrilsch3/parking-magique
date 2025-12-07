# ---------- gui.py ----------
from les_classes import Parking, Tarif, Place, Abonnement, ajout_des_donnees_du_client
from datetime import datetime, date
import json, glob, os, sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGridLayout, QDialog, QFormLayout, QLineEdit,
    QMessageBox, QSpinBox, QComboBox
)
from PyQt6.QtCore import QTimer, Qt, QDateTime


# ------------------ Chargement des données comme la version console ------------------
def charger_parking_depuis_fichier(fichier):
    from les_classes import Parking, Tarif, Place, Abonnement
    with open(fichier, "r", encoding="utf-8") as f:
        data = json.load(f)

    # = Places =
    Parking.set_places([])
    for p in data.get("places", []):
        place = Place(p["etage"], p["zone"], p["numero"], p["type_place"], p.get("plaque"))
        if p.get("temp"): place.temp = datetime.fromisoformat(p["temp"])

    # = Abonnements =
    Parking.set_abonnements([])
    for a in data.get("abonnements", []):
        Abonnement(a["nom"], a["prenom"], a["plaque"], a["duree"],
                   datetime.fromisoformat(a["date_debut"]).date(),
                   a.get("place"))

    # = Tarifs =
    tarifs = data.get("tarifs", {})
    from les_classes import Tarif
    if "gratuit_minutes" in tarifs: Tarif.set_gratuit_minutes(tarifs["gratuit_minutes"])
    if "prix_premiere_heure" in tarifs: Tarif.set_prix_premiere_heure(tarifs["prix_premiere_heure"])
    if "prix_deuxieme_heure" in tarifs: Tarif.set_prix_deuxieme_heure(tarifs["prix_deuxieme_heure"])
    if "prix_heures_suivantes" in tarifs: Tarif.set_prix_heures_suivantes(tarifs["prix_heures_suivantes"])
    if "prix_max_10h" in tarifs: Tarif.set_prix_max_10h(tarifs["prix_max_10h"])
    if "prix_abonnement_simple" in tarifs: Tarif.set_prix_abonnement_simple(tarifs["prix_abonnement_simple"])
    if "prix_abonnement_reserver" in tarifs: Tarif.set_prix_abonnement_reserver(tarifs["prix_abonnement_reserver"])


def charger_dernier_backup():
    fichiers = glob.glob("parking_*.json")
    if not fichiers:
        ajout_des_donnees_du_client()
        return

    def date_of(f):
        try:
            return datetime.strptime(f.replace("parking_","").replace(".json",""),"%Y-%m-%d_%H-%M-%S")
        except:
            return datetime.min

    fichiers.sort(key=date_of)
    charger_parking_depuis_fichier(fichiers[-1])


charger_dernier_backup()

# ============================================================================ #
#                             WINDOW PRINCIPALE GUI                             #
# ============================================================================ #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏠 Parking Magique")
        self.resize(1200,700)

        central = QWidget(); self.setCentralWidget(central)
        global_layout = QHBoxLayout(); central.setLayout(global_layout)

        # ------- Zone gauche = Places parking -------
        self.grid_widget = QWidget()
        self.grid = QGridLayout(); self.grid_widget.setLayout(self.grid)
        global_layout.addWidget(self.grid_widget,3)

        # ------- Zone Droite = Stats + Boutons -------
        right = QVBoxLayout()
        global_layout.addLayout(right,1)

        # Date & heure
        self.lbl_time = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.lbl_time.setStyleSheet("font-size:18px; font-weight:bold")
        right.addWidget(self.lbl_time)

        # Statistiques parking
        self.lbl_stats = QLabel()
        self.lbl_stats.setStyleSheet("font-size:14px")
        right.addWidget(self.lbl_stats)

        # Boutons
        btnAbo = QPushButton("📋 Gérer Abonnements")
        btnParam = QPushButton("⚙ Paramètres Tarifs")
        btnSave = QPushButton("💾 Sauvegarder maintenant")

        btnAbo.clicked.connect(self.menu_abonnement)
        btnParam.clicked.connect(self.menu_tarifs)
        btnSave.clicked.connect(lambda: QMessageBox.information(self,"Sauvegarde",Parking.save_all()))

        right.addWidget(btnAbo)
        right.addWidget(btnParam)
        right.addWidget(btnSave)
        right.addStretch()

        # Refresh automatique
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(1500)

        self.update_all()


    # ========================= UPDATE ========================= #
    def update_all(self):
        self.lbl_time.setText(QDateTime.currentDateTime().toString("dd/MM/yyyy - HH:mm:ss"))
        self.update_stats()
        self.update_grid()

    def update_stats(self):
        t = len(Parking.liste_place())
        libres = len(Parking.places_libres())
        occ = len(Parking.places_occupees())
        res = len(Parking.places_abonnes())
        tx = round((occ+res)/t*100,1) if t else 0

        self.lbl_stats.setText(f"""
📊 Statistiques Parking
-------------------------
Places libres : {libres}
Occupées      : {occ}
Réservées     : {res}
Taux          : {tx} %
        """)

    # ========================= AFFICHAGE GRILLE ========================= #
    def update_grid(self):
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget(); w.deleteLater()

        for idx,p in enumerate(Parking.places()):
            btn = QPushButton(p.id)
            btn.setFixedSize(70,70)

            # Design place
            if p.plaque: color = "red"     # occupée
            elif any(p.id==pl.id for pl,_ in Parking.places_abonnes()): color="blue" # réservée abo
            else: color="green"            # libre

            btn.setStyleSheet(f"border-radius:8px;background:{color};color:white;font-weight:bold")

            btn.clicked.connect(lambda _,place=p:self.clicked_place(place))
            self.grid.addWidget(btn, idx//10, idx%10)


    # ==================== Action clic sur place ===================== #
    def clicked_place(self,p:Place):
        if p.plaque: self.sortie(p)
        else:        self.entree(p)


    # ==================== Entrée véhicule ==================== #
    def entree(self,p):
        dlg = QDialog(self)
        form = QFormLayout(dlg)
        txt = QLineEdit(); form.addRow("Plaque :",txt)
        ok = QPushButton("Valider entrée"); form.addRow(ok)

        ok.clicked.connect(lambda:(
            QMessageBox.information(self,"Info", Parking.occuper_place(p.id,txt.text())),
            dlg.accept(),
            self.update_all()
        ))
        dlg.exec()


    # ==================== Sortie véhicule ==================== #
    def sortie(self, p):
        # ----------------- calcul durée stationnement ----------------- #
        if not p.temp:
            QMessageBox.warning(self,"Erreur","La place n'a pas d'heure d'entrée enregistrée.")
            return

        entree = p.temp
        duree = (datetime.now() - entree).total_seconds() / 3600   # en heures

        # ----------------- libération réelle ----------------- #
        result = Parking.liberer_place(p.id)
        # result peut être [True, msg] ou autre
        msg = ""
        prix = None
        if isinstance(result, (list, tuple)) and len(result) > 1:
            msg = result[1]
            # On tente d'extraire le prix du message si présent
            import re
            m = re.search(r'prix\s*:\s*([\d\.]+)', msg)
            if m:
                prix = float(m.group(1))
        else:
            msg = str(result)

        # Calcul du prix si pas trouvé dans le message
        if prix is None:
            # Récupération des tarifs
            g = Tarif.gratuit_minutes() / 60
            h1 = Tarif.prix_premiere_heure()
            h2 = Tarif.prix_deuxieme_heure()
            hsuiv = Tarif.prix_heures_suivantes()
            hmax = Tarif.prix_max_10h()

            if duree <= g:
                prix = 0
            elif duree <= 1:
                prix = h1
            elif duree <= 2:
                prix = h1 + h2
            elif duree <= 10:
                prix = h1 + h2 + (duree-2)*hsuiv
            else:
                prix = hmax

        QMessageBox.information(
            self,"Sortie véhicule",
            f"{msg}\nDurée : {duree:.2f}h\nPrix à payer : {prix:.2f} €"
        )

        self.update_all()

    # ==================== Gestion abonnements ==================== #
    def menu_abonnement(self):
        dlg = QDialog(self); form = QFormLayout(dlg)

        nom=QLineEdit(); prenom=QLineEdit(); plaque=QLineEdit()
        duree=QSpinBox(); duree.setRange(1,60)
        place=QComboBox(); place.addItems(["" ]+[p.id for p in Parking.places_libres()])

        form.addRow("Nom",nom); form.addRow("Prénom",prenom)
        form.addRow("Plaque",plaque); form.addRow("Durée (mois)",duree)
        form.addRow("Place réservée",place)

        ok=QPushButton("Créer abonnement"); form.addRow(ok)

        def create():
            # Création de l'abonnement, capture message si besoin
            abo = Abonnement(nom.text(),prenom.text(),plaque.text(),
                       duree.value(),date.today(),
                       place.currentText() or None)
            # Affichage d'un message personnalisé
            msg = f"Abonnement ajouté pour {abo.nom} {abo.prenom} ({abo.plaque}), durée : {abo.duree} mois, place : {abo.place or 'Aucune'}"
            QMessageBox.information(self,"OK",msg)
            dlg.accept();self.update_all()

        ok.clicked.connect(create)
        dlg.exec()


    # ==================== Menu tarifs ==================== #
    def menu_tarifs(self):
        dlg = QDialog(self); form=QFormLayout(dlg)

        inputs={}
        for nom,val in {
            "Gratuit minutes":Tarif.gratuit_minutes(),
            "Prix 1ère heure":Tarif.prix_premiere_heure(),
            "Prix 2ème heure":Tarif.prix_deuxieme_heure(),
            "Heures suivantes":Tarif.prix_heures_suivantes(),
            ">10h":Tarif.prix_max_10h(),
            "Abo simple":Tarif.prix_abonnement_simple(),
            "Abo réservé":Tarif.prix_abonnement_reserver(),
        }.items():
            box=QSpinBox(); box.setMaximum(999); box.setValue(int(val))
            inputs[nom]=box; form.addRow(nom,box)

        ok=QPushButton("Enregistrer"); form.addRow(ok)

        def save():
            Tarif.set_gratuit_minutes(inputs["Gratuit minutes"].value())
            Tarif.set_prix_premiere_heure(inputs["Prix 1ère heure"].value())
            Tarif.set_prix_deuxieme_heure(inputs["Prix 2ème heure"].value())
            Tarif.set_prix_heures_suivantes(inputs["Heures suivantes"].value())
            Tarif.set_prix_max_10h(inputs[">10h"].value())
            Tarif.set_prix_abonnement_simple(inputs["Abo simple"].value())
            Tarif.set_prix_abonnement_reserver(inputs["Abo réservé"].value())
            QMessageBox.information(self,"OK","Tarifs mis à jour")
            dlg.accept()

        ok.clicked.connect(save)
        dlg.exec()


# ------------------ lancement app ------------------
if __name__ == '__main__':
    app=QApplication(sys.argv)
    w=MainWindow(); w.show()
    sys.exit(app.exec())
