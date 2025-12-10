# ---------- gui.py ----------
from les_classes import Parking, Tarif, Place, Abonnement, ajout_des_donnees_du_client
import uuid
from datetime import datetime, date
import json, glob, os, sys


from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGridLayout, QDialog, QFormLayout, QLineEdit,
    QMessageBox, QSpinBox, QComboBox, QInputDialog, QScrollArea
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

        # ------- Zone gauche = Places parking avec scroll -------
        self.grid_widget = QWidget()
        self.grid = QGridLayout()
        self.grid_widget.setLayout(self.grid)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)      # Important pour que le contenu s'adapte
        scroll.setWidget(self.grid_widget)   # Mettre la grille dans la scroll area
        global_layout.addWidget(scroll, 3)

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
        btnAboCreer = QPushButton("Créer Abonnement")
        btnAboModifier = QPushButton("Modifier Abonnement")
        btnAboProlonger = QPushButton("Prolonger Abonnement")
        btnParam = QPushButton("⚙ Paramètres Tarifs")
        btnSave = QPushButton("💾 Sauvegarder maintenant")

        btnAboCreer.clicked.connect(self.menu_abonnement)
        btnAboModifier.clicked.connect(self.modifier_abonnement_gui)
        btnAboProlonger.clicked.connect(self.prolonger_gui)
        btnParam.clicked.connect(self.menu_tarifs)
        btnSave.clicked.connect(lambda: QMessageBox.information(self,"Sauvegarde",Parking.save_all()))

        right.addWidget(btnAboCreer)
        right.addWidget(btnAboModifier)
        right.addWidget(btnAboProlonger)
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
        # Nettoyage de la grille existante
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w is not None:
                w.deleteLater()

        # Collecte des places réservées par abonnement (ids)
        places_reservees = set()
        for ab in Parking.abonnements():
            if ab.place is not None and ab.date_fin() > date.today():
                places_reservees.add(ab.place)

        # Regrouper les places par étage
        etages = {}
        for p in Parking.places():
            etages.setdefault(p.etage, []).append(p)

        row = 0
        for etage in sorted(etages.keys()):
            # Label étage
            lbl = QLabel(f"Étage {etage}")
            lbl.setStyleSheet("font-weight:bold; font-size:16px; margin-top:10px; margin-bottom:5px")
            self.grid.addWidget(lbl, row, 0, 1, 10, Qt.AlignmentFlag.AlignLeft)
            row += 1

            # Boutons places de cet étage
            for idx, p in enumerate(etages[etage]):
                btn = QPushButton(p.id)
                btn.setFixedSize(70, 70)

                # Déterminer la couleur selon l'état
                color = "green"
                if p.plaque:
                    color = "red"
                elif p.id in places_reservees:
                    color = "blue"

                btn.setStyleSheet(f"border-radius:8px;background:{color};color:white;font-weight:bold")
                btn.clicked.connect(lambda _, place=p: self.clicked_place(place))
                self.grid.addWidget(btn, row + idx // 10, idx % 10)
            # Passer à la ligne suivante après cet étage
            row += (len(etages[etage]) - 1) // 10 + 1


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
            Parking.save_all(),
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
        Parking.save_all()
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
            abo = Abonnement(
                nom.text(),
                prenom.text(),
                plaque.text().strip().upper(),
                duree.value(),
                date.today(),
                place.currentText().strip().upper() if place.currentText() else None
            )
            Parking.save_all()
            # Affichage d'un message personnalisé
            msg = f"Abonnement ajouté pour {abo.nom} {abo.prenom} ({abo.plaque}), durée : {abo.duree} mois, place : {abo.place or 'Aucune'}"
            QMessageBox.information(self,"OK",msg)
            dlg.accept();self.update_all()

        ok.clicked.connect(create)
        dlg.exec()

    # ==================== Prolonger abonnement ==================== #
    def prolonger_gui(self):
        dlg = QDialog(self); form = QFormLayout(dlg)

        abos = Parking.abonnements()
        if not abos:
            QMessageBox.information(self, "Aucun abonnement", "Aucun abonnement n'existe.")
            return

        combo = QComboBox()
        for a in abos:
            combo.addItem(f"{a.id} - {a.nom} {a.prenom} - {a.plaque}", userData=a.id)
        form.addRow("Sélectionnez l'abonnement :", combo)

        nb_mois_spin = QSpinBox(); nb_mois_spin.setRange(1,60); nb_mois_spin.setValue(1)
        form.addRow("Nombre de mois à ajouter :", nb_mois_spin)

        btn_ok = QPushButton("Prolonger"); form.addRow(btn_ok)

        def valider():
            id_abo = combo.currentData()
            nb_mois = nb_mois_spin.value()
            try:
                result = Parking.allonger_abonnement(id=id_abo, nb_mois=nb_mois)
                success = False
                message = ""
                if isinstance(result, (list, tuple)) and len(result) > 1:
                    success = result[0]
                    message = result[1]
                else:
                    message = str(result)
                msg_box = QMessageBox(self)
                if success:
                    msg_box.setIcon(QMessageBox.Icon.Information)
                    msg_box.setWindowTitle("Succès")
                else:
                    msg_box.setIcon(QMessageBox.Icon.Warning)
                    msg_box.setWindowTitle("Erreur")
                msg_box.setText(message)
                msg_box.exec()
                self.update_all()
                dlg.accept()
            except Exception as e:
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Icon.Critical)
                msg_box.setWindowTitle("Exception")
                msg_box.setText(str(e))
                msg_box.exec()

        btn_ok.clicked.connect(valider)
        dlg.exec()
        Parking.save_all()
        

    # ==================== Modifier abonnement ==================== #
    def modifier_abonnement_gui(self):
        from PyQt6.QtWidgets import QInputDialog, QMessageBox
        # Correction : proposer la liste de tous les abonnements (sans filtre date_fin)
        abos = Parking.abonnements()
        if not abos:
            QMessageBox.information(self, "Aucun abonnement", "Aucun abonnement n'existe.")
            return
        # Affiche la liste sous forme "ID - Nom Prénom - Plaque"
        items = [f"{a.id} - {a.nom} {a.prenom} - {a.plaque}" for a in abos]
        idx, ok = QInputDialog.getItem(
            self,
            "Modifier abonnement",
            "Sélectionnez l'abonnement à modifier :",
            items,
            0,
            False
        )
        if not ok or idx is None or idx == "":
            return
        # Récupération de l'id sélectionné
        id_abo = abos[items.index(idx)].id

        # Choix de modification
        choix, ok = QInputDialog.getItem(
            self,
            "Modifier abonnement",
            "Que voulez-vous modifier ?",
            ["Plaque", "Place réservée"],
            0,
            False
        )
        if not ok:
            return

        try:
            if choix == "Plaque":
                nouvelle_plaque, ok2 = QInputDialog.getText(self, "Nouvelle plaque", "Nouvelle plaque :")
                if not ok2 or not nouvelle_plaque:
                    return
                result = Parking.modifier_abonnement(id=id_abo, plaque=nouvelle_plaque)
            elif choix == "Place réservée":
                # On demande la nouvelle place parmi les places libres et la place déjà attribuée à cet abonnement
                abo = next((a for a in Parking.abonnements() if a.id == id_abo), None)
                if not abo:
                    QMessageBox.warning(self, "Erreur", f"Abonnement {id_abo} introuvable")
                    return
                # Liste des places libres + la place déjà attribuée à cet abo (pour garder le choix)
                places_libres_ids = [p.id for p in Parking.places_libres()]
                if abo.place and abo.place not in places_libres_ids:
                    places_libres_ids.append(abo.place)
                nouvelle_place, ok2 = QInputDialog.getItem(
                    self, "Nouvelle place", "Nouvelle place :", places_libres_ids, 0, False
                )
                if not ok2 or not nouvelle_place:
                    return
                result = Parking.modifier_abonnement(id=id_abo, place_id=nouvelle_place)
            else:
                return

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Résultat")
            msg_box.setText(str(result))
            msg_box.exec()
            self.update_all()

        except Exception as e:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("Exception")
            msg_box.setText(str(e))
            msg_box.exec()


    # ==================== Gestion des abonnements existants ==================== #
    def dialog_gestion_abonnement(self):
        # Ici, on affiche une boîte de dialogue pour gérer les abonnements existants
        dlg = QDialog(self)
        form = QFormLayout(dlg)

        # Liste des abonnements existants
        abos = Parking.abonnements() if hasattr(Parking, "abonnements") else []
        if hasattr(Parking, "liste_abonnements"):
            abos = Parking.liste_abonnements()
        # Si abos est une dict, transformer en liste
        if isinstance(abos, dict):
            abos = list(abos.values())

        cb = QComboBox()
        for a in abos:
            display_text = f"{a.nom} {a.prenom}" if hasattr(a, "nom") else str(a)
            cb.addItem(display_text, userData=a.id)
        if not abos:
            cb.addItem("Aucun abonnement")
        form.addRow("Abonnement :", cb)

        btnProlong = QPushButton("Prolonger")
        btnModifier = QPushButton("Modifier")
        btnFermer = QPushButton("Fermer")
        btns = QHBoxLayout()
        btns.addWidget(btnProlong)
        btns.addWidget(btnModifier)
        btns.addWidget(btnFermer)
        form.addRow(btns)

        # Prolonger abonnement
        def prolonger():
            idx = cb.currentIndex()
            if idx < 0 or not abos:
                QMessageBox.warning(self,"Erreur","Aucun abonnement sélectionné.")
                return
            id_abo = cb.currentData()
            nb, ok = QInputDialog.getInt(self, "Prolonger", "Nombre de mois à ajouter :", 1, 1, 60)
            if ok:
                # Appel Parking.allonger_abonnement si disponible
                if hasattr(Parking, "allonger_abonnement"):
                    success, message = Parking.allonger_abonnement(id=id_abo, nb_mois=nb)
                    QMessageBox.information(self, "Résultat", message)
                    self.update_all()
            dlg.accept()

        # Modifier abonnement
        def modifier():
            idx = cb.currentIndex()
            if idx < 0 or not abos:
                QMessageBox.warning(self,"Erreur","Aucun abonnement sélectionné.")
                return
            id_abo = cb.currentData()
            # On propose modification plaque ou place
            modif, ok = QInputDialog.getItem(self, "Modifier", "Modifier :", ["Plaque", "Place"], 0, False)
            if ok:
                if modif == "Plaque":
                    nouvelle_plaque, ok2 = QInputDialog.getText(self, "Nouvelle plaque", "Nouvelle plaque :")
                    if ok2 and hasattr(Parking, "modifier_abonnement"):
                        result = Parking.modifier_abonnement(id=id_abo, plaque=nouvelle_plaque)
                        QMessageBox.information(self, "Résultat", str(result))
                        self.update_all()
                elif modif == "Place":
                    nouvelle_place, ok2 = QInputDialog.getText(self, "Nouvelle place", "Nouvelle place :")
                    if ok2 and hasattr(Parking, "modifier_abonnement"):
                        result = Parking.modifier_abonnement(id=id_abo, place_id=nouvelle_place)
                        QMessageBox.information(self, "Résultat", str(result))
                        self.update_all()
            dlg.accept()

        btnProlong.clicked.connect(prolonger)
        btnModifier.clicked.connect(modifier)
        btnFermer.clicked.connect(dlg.accept)
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