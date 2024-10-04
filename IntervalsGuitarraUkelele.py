from music21 import *
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
from PIL import Image
import winsound
import time

instrument =""  # "G" guitarra, "U" Ukelele
# Guitarra
notesAfinacioGuitarra = "E3 A3 D4 G4 B4 E5"   # afinacio de la guitarra de la 6a a la 1a
numCordesGuitarra = 6   # per la guitarra 6
# Ukelele
notesAfinacioUkelele = "G4 C5 E5 A5"   # afinacio de la guitarra de la 6a a la 1a
numCordesUkelele = 4   # per la guitarra 6

# variables globals que s'assignaran als valors de la guitarra o ukelele
notesAfinacioStandard =""
numCordes=0
notacio =""  # "A":  C,D,E...... anglosaxona , "L": Do, Re...llatina

sostingutABemoll ={"F#": "G-", "G#": "A-", "A#": "B-", "C#":"D-", "D#":"E-"}
bemollASostingut ={"G-": "F#", "A-":"G#", "B-":"A#", "D-":"C#", "E-":"D#"}


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# en tot el programa l'index 0 de la 1a columna de les llistes correspon a la numCordesa coorda i l'index 5 a la 1a corda
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class triaInstrument(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("triaInstrument.ui",self)
        self.botoInstrument.clicked.connect(self.instrumentTriat)


    def instrumentTriat(self):
        global numCordes
        global notesAfinacioStandard
        global instrument
        global notacio

        if self.BGuitarra.isChecked():
            numCordes= numCordesGuitarra
            notesAfinacioStandard = notesAfinacioGuitarra
            instrument = "G"
        if self.BUkelele.isChecked():
            numCordes = numCordesUkelele
            notesAfinacioStandard = notesAfinacioUkelele
            instrument ="U"
        if self.RBNotacioA.isChecked():
                notacio="A"
        if self.RBNotacioL.isChecked():
                notacio="L"
        self.close()



class finestraAjuda(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ajudaGuitarra.ui", self)
        self.BSortirAjuda.clicked.connect(self.sortirAjuda)
    def sortirAjuda(self):
        self.close()

def notacioDoaC(ss):
    diccionariInvers = {"D": "C", "R": "D", "M": "E", "F": "F", "Sol": "G", "L": "A", "Si": "B"}
    # rep un string amb les notes en format Do, Re, Mi  i les passa a format C, D...
    nouText=""
    index=0
    while index < len(ss):
        if ss[index] in ["D", "R", "M", "F", "L"] : # excepte Si i Sol
            trad = diccionariInvers[ss[index]]
            nouText=nouText+trad
            index= index+2  # 2 lletres
        elif ss[index] =="S":
            if ss[index+1]=="o": #"Sol"
                nouText=nouText+"G"
                index=index+3 # 3 lletres
            elif ss[index+1]=="i": # Si
                nouText = nouText + "B"
                index = index + 2  # 2 lletres
        else:
            nouText = nouText+ss[index]
            index=index+1
    return nouText

def notacioCaDo(ss):
    diccionari = {"C": "Do", "D": "Re", "E": "Mi", "F": "Fa", "G": "Sol", "A": "La", "B": "Si"}
    # rep un string amb les notes en format C,D..i les passa a format Do, Re...
    nouText=""
    for i in range(0,len(ss)):
        if ss[i] in ["D", "E", "F", "G", "A", "B", "C"]:
            trad = diccionari[ss[i]]
            nouText=nouText+trad
        else:
            nouText=nouText+ss[i]
    return nouText


def indexACorda(index):
        # transforma l'index de columna dels arrays a corda
        corda =numCordes-index
        return corda

def cordaAIndex(corda):
        # donada una corda torna l'index de la columna dels arrays
        index=numCordes-corda
        return index

def afegirALlista(text, llista1, llista2):
    temp=[]
    temp.append(text)
    temp.append(llista1)
    llista2.append(temp)
    return llista2

def buidaPaperera():
    # buida el directori temporal de morralla
    dir_esborrar = os.path.join(os.getcwd(), "scratchPath")
    llistaArxius = os.listdir(dir_esborrar)
    for arxiu in llistaArxius:
        nomArxiu = os.path.join(os.getcwd(), "scratchPath", arxiu)
        os.remove(nomArxiu)

def llegirConfiguracio():
    # llegeix l'arxiu config.txt per sober on es troba musescore
    with open("./config.txt", "r") as file:
        for line in file.readlines():
            print(line)
            if line.startswith("MUSESCORE"):
                temp=line.find("=")
                ssttMusescore=line[temp+1:-1]
                print(ssttMusescore)
            #  La font no es fara servir en aquest programa
            if line.startswith("FONT"):
                temp=line.find("=")
                ssttFont=line[temp+1:-1]
                print(ssttFont)
    return ssttMusescore, ssttFont

def beep():
    # de winsound. Pita : frequencia, durada
    winsound.Beep(600, 250)
    time.sleep(0.25)


class App(QMainWindow):

    LNotesCordesOct=[]  # llista de 7 llistes de les notes de les diferents cordes amb octava,
                        # ojo que l'index comença a 0 pero no es fara servir
    LNotesCordes =[]    # el mateix pero sense octava, nomes nota i alteracio.
                        # ALERTA: la unica alteracio es el # sino es complica molt buscar
    clau= ""  # clau de tonalitat
    nomArrel = ""   # nom de l'arrel
    acordTocar=[]  # l'acord que es tocarà
    def __init__(self,parent):
        super().__init__()
        tm = triaInstrument()
        tm.show()
        tm.exec()
        if instrument =="G":
            loadUi("Intervals guitarra1.4.ui",self)

        elif instrument=="U":
            loadUi("Intervals ukelele1.4.ui", self)

        self.setWindowTitle("Intervals i acords en el màstil de la guitarra o ukelele. Adolf Cortel 2024")
        # self.showMaximized() #self.setFixedSize(830,600)   # mida fixa de la finestra per no desajustar la taula
        if instrument=="G":
            self.CBArrelABaixos.toggled.connect(self.dibuixarIntervals)
        if instrument =="G":
           textLabel = notesAfinacioGuitarra
        if instrument == "U":
            textLabel = notesAfinacioUkelele

            if notacio =="L":
                textLabel = notacioCaDo(textLabel)
            self.LabelAfinaNormal.setText(textLabel)

        self.inicialitzaLlistesComu()
        self.ompleNotesMastil()
        self.tabWidget.setStyleSheet('''
                       QTabBar::tab:!selected {background-color: rgb(170,200,170);}
                       QTabBar::tab:selected  {background-color: pink; }
                       QWidget {background-color: rgb(230,230,230);}
                                           ''')  # això funciona be !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.tabWidget.setCurrentIndex(1)
        # aqui es llegeixen els parametres i es pinten els intervals
        self.tabWidget.currentChanged.connect(self.dibuixarIntervals)

        self.grupBotons3.buttonClicked.connect(self.dibuixarIntervals)
        self.grupBotons5.buttonClicked.connect(self.dibuixarIntervals)
        self.grupBotons7.buttonClicked.connect(self.dibuixarIntervals)
        self.grupBotons9.buttonClicked.connect(self.dibuixarIntervals)
        self.grupBotons11.buttonClicked.connect(self.dibuixarIntervals)
        self.grupBotons13.buttonClicked.connect(self.dibuixarIntervals)
        self.grupBotons246.buttonClicked.connect(self.dibuixarIntervals)
        self.botoTocarSeleccio.clicked.connect(self.transferir)    # transfereix les notes marcades d'un mastil a un altre
        self.botoAcabar.clicked.connect(self.tancar)
        self.BAjuda.clicked.connect(self.obrirAjuda)
        self.RBBemolls.toggled.connect(self.dibuixarIntervals)
        self.RBSostinguts.toggled.connect(self.dibuixarIntervals)
        self.CBNotes.currentIndexChanged.connect(self.dibuixarIntervals)
        self.CBTipusAcord.currentIndexChanged.connect(self.buscaPosicions)
        self.CBTipus7.currentIndexChanged.connect(self.buscaPosicions)
        self.CBAltres.currentIndexChanged.connect(self.buscaPosicions)
        if notacio=="L":
            textTemp= notacioCaDo(notesAfinacioStandard)
            self.LAfinacio.setText(textTemp)
        elif notacio =="A":
            self.LAfinacio.setText(notesAfinacioStandard)
        self.grupAfinacio.buttonClicked.connect(self.reiniciaLlistes)
        self.LAfinacio.editingFinished.connect(self.reiniciaLlistes)
        self.testDirectoris()
        self.dibuixarIntervals()  # mira quina pestanya esta triada

    def obrirAjuda(self):
        fA=finestraAjuda()
        fA.show()
        fA.exec()


    def reiniciaLlistes(self):
        self.inicialitzaLlistesComu()
        self.ompleNotesMastil()
        self.dibuixarIntervals()

    def finestraProblemes(self, s):
        QMessageBox.about(self, "Problema!! Verificar els noms d'arxius dins config.txt", s)

    def testDirectoris(self):
        # crea el subdirectori scratchPath per la morralla si es que no eisteix
        try:
            os.mkdir("scratchPath")
        except:
            print("problemes amb l'arxiu")
        nom= os.path.join(os.getcwd(),"scratchPath")
        environment.set("directoryScratch", nom)
        global ssMusescore
        global ssFont
        ssMusescore, ssFont = llegirConfiguracio()
        if os.path.exists(ssMusescore):
            environment.set("musescoreDirectPNGPath", ssMusescore)
        else:
            self.finestraProblemes(" No es troba l'arxiu: "+ssMusescore)
            self.tancar()

    def alteracioNota(self, nomNota, alteracio):
        # si la nota te # o -, se li posa  l'alteracio
        # retorna un string amb la nota amb l'alteracio correcta
        nouNom= nomNota
        if len(nomNota) > 1:
            if alteracio =="#" and nomNota[1] == "-":  # si hi ha un bemoll
                nouNom = bemollASostingut[nomNota]
            if alteracio =="-" and nomNota[1] == "#":  # si hi ha un bemoll
                nouNom = sostingutABemoll[nomNota]
                nouNom =nouNom.replace("-","b")
        return nouNom

    def canviaAlteracions(self,ss):
        # es canvien totes les alteracions iNTERNAMENT a LNotesCordes a #
        # en el que es veu a la taula les alteracions son les que s'han triat amb els Rbotons
        for c in range(len(self.LNotesCordes)):  # totes les  cordes
            NotesCorda= self.LNotesCordes[c]
            #print(NotesCorda)
            for t in range(len(NotesCorda)):  # per cada nota de la corda
                if len(NotesCorda[t])>1:
                      if NotesCorda[t][1] =="-":  # si hi ha un bemoll
                            equiv = bemollASostingut[NotesCorda[t]]
                            self.LNotesCordes[c][t]= equiv

    def inicialitzaLlistesComu(self):
        # al mastil s'hi posen totes les notes sense octava
        # si hi ha bemolls es passen a sostinguts (en la representacio interna només # no bemolls
        # llegir notes afinacio
        while len(self.LNotesCordesOct)>0:
            self.LNotesCordesOct.pop()
        while len(self.LNotesCordes) >0:
            self.LNotesCordes.pop()

        if self.BAfinacioStandard.isChecked():
            llistaN = list(notesAfinacioStandard.split(" "))
            notesAfinacio = llistaN.copy()
        if self.BAfinacioUsuari.isChecked():
            if notacio == "L":
                textTemp = notacioDoaC(self.LAfinacio.text())
                llistaN = list(textTemp.split(" "))
                notesAfinacio = llistaN.copy()
            if notacio =="A":
                llistaN = list(self.LAfinacio.text().split(" "))
                notesAfinacio = llistaN.copy()


        self.taulaMastil.setEditTriggers(QTableWidget.NoEditTriggers)
        for i in range(len(notesAfinacio)):  # notes afiniacio de les cordes
            notesCordaOctava=[]  # llista notes d'una corda concreta
            escalaCrom =scale.ChromaticScale(notesAfinacio[i])
            NotesCordaOctava= [str(p) for p in escalaCrom.getPitches()]
            self.LNotesCordesOct.append(NotesCordaOctava)  # l'index 0 correspon a la corda 6 en guitarra
        for i in range(len(self.LNotesCordesOct)):
            NotesCorda=self.LNotesCordesOct[i]
            llistaTemp=[]
            for k in range(len(NotesCorda)):
                temp= NotesCorda[k]
                temp2 =temp[0:-1]
                llistaTemp.append(temp2)
            self.LNotesCordes.append(llistaTemp)
        self.canviaAlteracions("#")
    def destacarFiles(self, taula):
        # marca els trasts a 0 i 7 amb un groc fluix
        for j in range(taula.columnCount()):
            taula.item(0, j).setBackground(QtGui.QColor(250,250,200))
            taula.item(7, j).setBackground(QtGui.QColor(250,250,200))

    def posNota(self, nota, corda):
        # torna el trast que correspon a nota en una corda
        trast = self.LNotesCordes[cordaAIndex(corda)].index(nota)
        return trast
    def ompleNotesMastil(self):
        # omple el mastil1 amb totes les notes sense octava i destaca les files 0 i 7
        # ALERTA: es posa # o - al gust de l'usuari, internament tot va amb #
        self.taulaMastil.clearContents()  # no Clear sino ClearContents, esborra el que hi ha seleccionat
        for c in range(self.taulaMastil.columnCount()):  # de l''index 0 (ultima corda) a l'index 5 (1a corda)
            for t in range(0, 13):
                item = self.LNotesCordes[c][t]
                if self.RBSostinguts.isChecked():
                    item = self.alteracioNota(item,"#")
                if self.RBBemolls.isChecked():
                    item = self.alteracioNota(item,"-")
                if notacio=="L":
                    item = notacioCaDo(item)
                self.taulaMastil.setItem(t, c, QTableWidgetItem(item))
        # destacar el trast 0 i el 7
        self.destacarFiles(self.taulaMastil)

    def buscaNotes(self, nota):
        # torna una llista de tuples(columna, fila) amb les posicions de la nota en el mastil

        llista=[]
        for i in range(0, numCordes):
            for t in range(0,13):        # en tot el mastil
                if self.LNotesCordes[i][t] == nota:
                    pos=(i,t)
                    if numCordes==6: # no per l'ukelele
                        if nota == self.nomArrel: # si es l'arrel tracte especial
                            if i not in [3,4,5]:
                                llista.append(pos)
                            else:
                                if not self.CBArrelABaixos.isChecked():
                                    llista.append(pos)

                        else:
                            llista.append(pos)
                    else:
                        llista.append(pos)

        return llista

    def prepararLlista(self, num, nomA):
        # num: semitons de l'interval des de l'arrel
        # nomA: nom dela nota
        # torna la llista de les notes en una corda separades num ST de l'arrel
        interv = interval.Interval(num)
        nota = interv.transposeNote(note.Note(nomA))
        nomNota = str(nota.pitch)  # str necessari per passar de l'objecte Pich a string
        if len(nomNota) > 1:  # hi ha bemoll es passa a #
            if nomNota[1] == "-":
                nomNota = bemollASostingut[nomNota]
        llista = self.buscaNotes(nomNota)  # es busca la llista de posicions ambel nom de la nota
        return llista

    def dibuixarIntervals(self):
        self.clau=""
        self.netejaImatge()

        if self.tabWidget.currentIndex()==0:
            self.buscaPosicions()
        if self.tabWidget.currentIndex()==1:
            self.buscaPosicions2()
    def buscaPosicions(self):
        # ha de fer un reset de tot l'anterior en el mastil1
        notaAlt= self.CBNotes.currentText() # nota amb alteracio
        tonalitat = self.CBTipusAcord.currentText()
        if tonalitat in ["Menor", "Disminuit"]:
            notaAlt = notaAlt.lower()
        print(notaAlt)
        self.clau = key.Key(notaAlt)  # es crea la clau com a self
        self.ompleNotesMastil()
        llistaPosArrels=[]
        llistaPos2m=[]
        llistaPos2M=[]
        llistaPos3m=[]
        llistaPos3M=[]
        llistaPos4J=[]
        llistaPos5dim=[] # tritò
        llistaPos5J=[]
        llistaPos5aug=[]
        llistaPos6m=[]    # igual que 5a aug
        llistaPos6M=[]
        llistaPos7m=[]
        llistaPos7M=[]
        llistaPos7dim=[]  # és igual que 6
        llistaPos9=[]
        llistaPos9b=[]
        llistaPos9s=[]
        llistaPosSus4=[]
        llistaPosSus2=[]
        llistaPos11=[]
        llistaPos13=[]
        llistaPos69=[]

        llistaAcord=[] # llista de llistes de tot el que s'ha d'escriure
        # primer l'arrel
        # per cada interval definit dins l'acord es genera una llista amb les posicions de les notes de l'interval
        # cada llista es va afegint precedida del seu nom
        self.nomArrel = self.CBNotes.currentText() # nom de la nota amb alteracio

        llistaPosArrels = self.buscaNotes(self.nomArrel)

        # torna llista (corda/trast) de la nota en altres cordes,
        # en trasts no massa allunyats (<=3) si s'ha triat l'opcio

        # a llista acord es van afegir les llistes amb totes les posicions que s'han d0integrar a l'acord
        llistaAcord = afegirALlista ("arrel", llistaPosArrels,llistaAcord)

        # es preparen les llistes de 3M, 3m i 5a que son les que es fan servir mé
        llistaPos3M = self.prepararLlista(4, self.nomArrel)
        llistaPos3m = self.prepararLlista(3, self.nomArrel)
        llistaPos5J = self.prepararLlista(7, self.nomArrel)
        # l'arrel s'afegeix sempre
        if self.CBTipusAcord.currentText() == "Major":
            # afegir 3aMajor i 5a
            if self.CBAltres.currentText() not in ["sus4", "sus2"]: # si es sus als majors no es posa 3a
                # si hi ha sus4 o sus2 no es posa la tercera
                llistaAcord = afegirALlista ("3M", llistaPos3M,llistaAcord)
            llistaAcord = afegirALlista ("5J", llistaPos5J,llistaAcord)

        elif self.CBTipusAcord.currentText() == "Menor":
            # afegir 3a menor i 5a
            if self.CBAltres.currentText() not in ["Sus4", "Sus2"]:
                # si hi ha sus4 o sus2 no es posa la tercera
                llistaAcord = afegirALlista ("3m", llistaPos3m,llistaAcord)
            llistaAcord = afegirALlista ("5J", llistaPos5J,llistaAcord)

        elif self.CBTipusAcord.currentText() == "sus4":
            llistaPosSus4= self.prepararLlista(5, self.nomArrel)
            llistaAcord = afegirALlista ("sus4", llistaPosSus4,llistaAcord)
            llistaAcord = afegirALlista ("5J", llistaPos5J,llistaAcord)

        elif self.CBTipusAcord.currentText() == "sus2":
            llistaPosSus2= self.prepararLlista(2, self.nomArrel)
            llistaAcord = afegirALlista ("sus2", llistaPosSus2,llistaAcord)
            llistaAcord = afegirALlista ("5J", llistaPos5J,llistaAcord)

        elif self.CBTipusAcord.currentText() == "Augmentat":
            # afegir 3a major i 5a aug
            llistaAcord = afegirALlista ("3M", llistaPos3M,llistaAcord)
            llistaPos5aug = self.prepararLlista(8, self.nomArrel)
            llistaAcord = afegirALlista ("5a", llistaPos5aug,llistaAcord)

        elif self.CBTipusAcord.currentText() == "Disminuit":  # 5d es un trito
            llistaPos5dim = self.prepararLlista(6, self.nomArrel)
            llistaAcord = afegirALlista ("3m", llistaPos3m,llistaAcord)
            llistaAcord = afegirALlista ("5d", llistaPos5dim,llistaAcord)

        elif self.CBTipusAcord.currentText() == "3 major i 5 bemoll":  # 5d es un trito
            llistaPos5dim = self.prepararLlista(6, self.nomArrel)
            llistaAcord = afegirALlista ("3M", llistaPos3M,llistaAcord)
            llistaAcord = afegirALlista ("5d", llistaPos5dim,llistaAcord)

        elif self.CBTipusAcord.currentText() == "Arrel i 3a major":
            llistaAcord = afegirALlista ("3M", llistaPos3M,llistaAcord)

        elif self.CBTipusAcord.currentText() == "Arrel i 3a menor":
            llistaAcord = afegirALlista ("3m", llistaPos3m,llistaAcord)

        elif self.CBTipusAcord.currentText() == "Arrel i 5a justa":
            llistaAcord = afegirALlista ("5J", llistaPos5J,llistaAcord)

        elif self.CBTipusAcord.currentText() == "Arrel i 4a justa":
            llistaPos4J = self.prepararLlista(5, self.nomArrel)
            llistaAcord = afegirALlista ("4J", llistaPos4J,llistaAcord)

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if self.CBTipus7.currentText() == "7":
            llistaPos7= self.prepararLlista(10, self.nomArrel)
            llistaAcord = afegirALlista ("7", llistaPos7,llistaAcord)

        elif self.CBTipus7.currentText() == "7M":
            llistaPosM7= self.prepararLlista(11, self.nomArrel)
            llistaAcord = afegirALlista ("7M", llistaPosM7,llistaAcord)

        elif self.CBTipus7.currentText() == "7 dim":
            llistaPos7dim= self.prepararLlista(9, self.nomArrel)
            llistaAcord = afegirALlista ("7d", llistaPos7dim,llistaAcord)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        if self.CBAltres.currentText() == "2m":
            llistaPos2m= self.prepararLlista(1, self.nomArrel)
            llistaAcord = afegirALlista ("2m", llistaPos2m,llistaAcord)

        elif self.CBAltres.currentText() == "2M":
            llistaPos2M= self.prepararLlista(2, self.nomArrel)
            llistaAcord = afegirALlista ("2M", llistaPos2M,llistaAcord)

        elif self.CBAltres.currentText() == "4J":
            llistaPos6= self.prepararLlista(5, self.nomArrel)
            llistaAcord = afegirALlista ("4J", llistaPos6,llistaAcord)

        elif self.CBAltres.currentText() == "tritò":
            llistaPos6= self.prepararLlista(6, self.nomArrel)
            llistaAcord = afegirALlista ("tritò", llistaPos6,llistaAcord)

        elif self.CBAltres.currentText() == "6M":
            llistaPos6M= self.prepararLlista(9, self.nomArrel)
            llistaAcord = afegirALlista ("6M", llistaPos6M,llistaAcord)

        elif self.CBAltres.currentText() == "6m":
            llistaPos6m= self.prepararLlista(8, self.nomArrel)
            llistaAcord = afegirALlista ("6m", llistaPos6m,llistaAcord)

        elif self.CBAltres.currentText() == "9":
            llistaPos9= self.prepararLlista(14, self.nomArrel)
            llistaAcord = afegirALlista ("9", llistaPos9,llistaAcord)

        elif self.CBAltres.currentText() == "69":
            llistaPos6M= self.prepararLlista(9, self.nomArrel)
            llistaAcord = afegirALlista ("6M", llistaPos6M,llistaAcord)

            llistaPos9= self.prepararLlista(14, self.nomArrel)
            llistaAcord = afegirALlista ("9", llistaPos9,llistaAcord)

        elif self.CBAltres.currentText() == "9b":
            llistaPos9b= self.prepararLlista(1, self.nomArrel)
            llistaAcord = afegirALlista ("9b", llistaPos9b,llistaAcord)
        elif self.CBAltres.currentText() == "9#":
            llistaPos9s= self.prepararLlista(3, self.nomArrel)
            llistaAcord = afegirALlista ("9#", llistaPos9s,llistaAcord)

        elif self.CBAltres.currentText() == "11":
            llistaPos11= self.prepararLlista(5, self.nomArrel)
            llistaAcord = afegirALlista ("11", llistaPos11,llistaAcord)

        elif self.CBAltres.currentText() == "13":
            llistaPos13= self.prepararLlista(9, self.nomArrel)
            llistaAcord = afegirALlista ("13", llistaPos13,llistaAcord)
        self.dibuixaPosicions(llistaAcord)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def buscaPosicions2(self):
        notaAlt= self.CBNotes.currentText() # nota amb alteracio
        tonalitat = self.CBTipusAcord.currentText()
        #self.clau = key.Key(notaAlt)  # es crea la clau en la tonalitat major
        self.ompleNotesMastil()
        llistaPosArrels=[]

        llistaPos2M, llistaPos3m, llistaPos3M = [], [], []
        llistaPos4J, llistaPos6M= [], []
        llistaPos5dim, llistaPos5J, llistaPos5aug = [], [], []
        llistaPos7m, llistaPos7M, llistaPos7dim = [], [], []
        llistaPos9, llistaPos9b, llistaPos9s = [], [], []
        llistaPos11, llistaPos11b, llistaPos11s = [], [], []
        llistaPos13, llistaPos13b, llistaPos13s = [], [], []
        llistaAcord=[] # llista de llistes de tot el que s'ha d'escriure
        # primer l'arrel
        # per cada interval definit dins l'acord es genera una llista amb les posicions de les notes de l'interval
        # cada llista es va afegint precedida del seu nom
        self.nomArrel = self.CBNotes.currentText() # nom de la nota amb alteracio

        llistaPosArrels = self.buscaNotes(self.nomArrel)
        llistaAcord = afegirALlista ("arrel", llistaPosArrels,llistaAcord)
        llistaPos2M = self.prepararLlista(2, self.nomArrel)
        llistaPos3m = self.prepararLlista(3, self.nomArrel)
        llistaPos3M = self.prepararLlista(4, self.nomArrel)
        llistaPos4J = self.prepararLlista(5, self.nomArrel)
        llistaPos5dim = self.prepararLlista(6, self.nomArrel)
        llistaPos5J = self.prepararLlista(7, self.nomArrel)
        llistaPos5aug = self.prepararLlista(8, self.nomArrel)
        llistaPos6M = self.prepararLlista(9, self.nomArrel)
        llistaPos7dim = self.prepararLlista(9, self.nomArrel)
        llistaPos7m = self.prepararLlista(10, self.nomArrel)
        llistaPos7M = self.prepararLlista(11, self.nomArrel)
        llistaPos9b = self.prepararLlista(1, self.nomArrel)
        llistaPos9 = self.prepararLlista(2, self.nomArrel)  # grau 9 == 2
        llistaPos9s = self.prepararLlista(3, self.nomArrel)
        llistaPos11b = self.prepararLlista(4, self.nomArrel)
        llistaPos11 = self.prepararLlista(5, self.nomArrel) # grau 11 ==4
        llistaPos11s = self.prepararLlista(6, self.nomArrel)
        llistaPos13b = self.prepararLlista(8, self.nomArrel)
        llistaPos13 = self.prepararLlista(9, self.nomArrel) # grau 13 ==6
        llistaPos13s = self.prepararLlista(10, self.nomArrel)

        if self.B2M.isChecked():
            llistaAcord = afegirALlista("2M", llistaPos2M, llistaAcord)
        if self.B3m.isChecked():
            llistaAcord = afegirALlista("3m", llistaPos3m, llistaAcord)
        if self.B3M.isChecked():
            llistaAcord = afegirALlista("3M", llistaPos3M, llistaAcord)
        if self.B4J.isChecked():
            llistaAcord = afegirALlista("4J", llistaPos4J, llistaAcord)
        if self.B5dim.isChecked():
            llistaAcord = afegirALlista("5d", llistaPos5dim, llistaAcord)
        if self.B5J.isChecked():
            llistaAcord = afegirALlista("5J", llistaPos5J, llistaAcord)
        if self.B5aug.isChecked():
            llistaAcord = afegirALlista("5a", llistaPos5aug, llistaAcord)
        if self.B6M.isChecked():
            llistaAcord = afegirALlista("6M", llistaPos6M, llistaAcord)
        if self.B7dim.isChecked():
            llistaAcord = afegirALlista("7d", llistaPos7dim, llistaAcord)
        if self.B7M.isChecked():
            llistaAcord = afegirALlista("7M", llistaPos7M, llistaAcord)
        if self.B7m.isChecked():
            llistaAcord = afegirALlista("7", llistaPos7m, llistaAcord)
        if self.B9.isChecked():
            llistaAcord = afegirALlista("9", llistaPos9, llistaAcord)
        if self.B9b.isChecked():
            llistaAcord = afegirALlista("9b", llistaPos9b, llistaAcord)
        if self.B9s.isChecked():
            llistaAcord = afegirALlista("9#", llistaPos9s, llistaAcord)
        if self.B11.isChecked():
            llistaAcord = afegirALlista("11", llistaPos11, llistaAcord)
        if self.B11b.isChecked():
            llistaAcord = afegirALlista("11b", llistaPos11b, llistaAcord)
        if self.B11s.isChecked():
            llistaAcord = afegirALlista("11#", llistaPos11s, llistaAcord)
        if self.B13.isChecked():
            llistaAcord = afegirALlista("13", llistaPos13, llistaAcord)
        if self.B13b.isChecked():
            llistaAcord = afegirALlista("13b", llistaPos13b, llistaAcord)
        if self.B13s.isChecked():
            llistaAcord = afegirALlista("13#", llistaPos13s, llistaAcord)
        self.dibuixaPosicions(llistaAcord)

    def pintaLlista(self, nom, LL, color):
        # marca les posicions al mastil1 amb el nom dins l'acord (arrel, 3a...) i el color que s'envia
        for item in LL:
            c, f =item
            col1,col2,col3= color
            hiHa = self.taulaMastil.item(f,c).text()
            self.taulaMastil.setItem(f, c , QTableWidgetItem(hiHa +"/"+nom))
            self.taulaMastil.item(f,c).setBackground(QtGui.QColor(col1,col2,col3))

    def dibuixaPosicions(self, LLAcords):
        # rep una llista de llistesB , a cada llistaB hi ha un nom i la llista de posicions
        # pinta cadascuna de les subllistes amb un color diferent
        for item in LLAcords:
            if item[0] == "arrel":
                self.pintaLlista("arrel", item[1], (255, 0, 0))
            elif item[0] == "2m":
                 self.pintaLlista("2m", item[1], (255, 0, 255))
            elif item[0] == "2M":
                self.pintaLlista("2M", item[1], (255, 20, 255))
            elif item[0] == "3M":
                self.pintaLlista("3M", item[1], (255, 255, 0))
            elif item[0] == "3m":
                self.pintaLlista("3m", item[1], (255, 150, 0))
            elif item[0] == "4J":
                self.pintaLlista("4J", item[1], (255, 60, 255))
            elif item[0] == "5J":
                self.pintaLlista("5J", item[1], (0, 255, 0))
            elif item[0] == "5a":
                self.pintaLlista("5a", item[1], (180, 255, 180))
            elif item[0] == "5d":
                self.pintaLlista("5d", item[1], (0, 180, 0))
            elif item[0] == "6m":
                self.pintaLlista("6m", item[1], (50, 180, 50))
            elif item[0] == "6M":
                self.pintaLlista("6M", item[1], (50, 180, 50))
            elif item[0] == "7":
                self.pintaLlista("7", item[1], (100, 100, 200))
            elif item[0] == "7M":
                self.pintaLlista("7M", item[1], (170, 170, 255))
            elif item[0] == "7d":
                self.pintaLlista("7d", item[1], (0, 0, 200))
            elif item[0] == "9":
                self.pintaLlista("9", item[1], (200, 150, 200))
            elif item[0] == "9b":
                self.pintaLlista("9b", item[1], (200, 150, 200))
            elif item[0] == "9#":
                self.pintaLlista("9#", item[1], (200, 150, 200))
            elif item[0] == "11":
                self.pintaLlista("11", item[1], (200, 150, 150))
            elif item[0] == "11b":
                self.pintaLlista("11b", item[1], (200, 150, 150))
            elif item[0] == "11#":
                self.pintaLlista("11#", item[1], (200, 150, 150))
            elif item[0] == "13":
                self.pintaLlista("13", item[1], (200, 70, 200))
            elif item[0] == "13b":
                self.pintaLlista("13b", item[1], (200, 70, 200))
            elif item[0] == "13#":
                self.pintaLlista("13#", item[1], (200, 70, 200))
            # sus4, sus2, 11 i 13, del mateix color

            elif item[0] == "sus4":
                self.pintaLlista("sus4", item[1], (255, 40, 255))
            elif item[0] == "sus2":
                self.pintaLlista("sus2", item[1], (255, 80, 255))

            elif item[0] == "69":
                self.pintaLlista("69", item[1], (255, 40, 255))
            elif item[0] == "tritò":
                self.pintaLlista("tritò", item[1], (255, 60, 255))
            # els afegits nous

    def resetAcord(self):
        # cada vegada que es prem el boto de Tocar seleccio es fa reset de l'acord anterior
        # i es tornen a llegir les tecles seleccionades
        while len(self.acordTocar)>0:
            self.acordTocar.pop()
    def netejaImatge(self):
        # esborra el canvas
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.set_axis_off()
        self.MplWidget.canvas.flush_events()
        self.MplWidget.canvas.draw()
    def mostrarImatge(self, nomArxiu):
        # mostra la imatge al canvas
        self.im1 = Image.open(nomArxiu)  # .resize((800,600))
        self.netejaImatge()
        self.MplWidget.canvas.axes.imshow(self.im1)
        self.MplWidget.canvas.draw()
    def ferAcord(self, acord):
        # a acord on hi ha la sequència de notes:mostra la partitura i la toca
        # toca acord o arpegi segons el valor a CBArpegiAcord
        acord2 =acord.copy()
        acordFet=chord.Chord(acord)
        acordFet.duration.type= "whole"
        nom= acordFet.commonName
        acordFet.addLyric(nom)
        acord2.reverse()
        acordFet2=chord.Chord(acord2)
        streamMeu=stream.Stream()

        if self.clau !="":
            streamMeu.append(self.clau)
        if self.CBArpegiAcord.currentText() == "Acord":
            streamMeu.append(acordFet)
        else:
            for n in acord:
                nota=note.Note(n)
                streamMeu.append(nota)
            rr= note.Rest()
            rr.duration.quarterLength=1
            streamMeu.append(rr)
            for n in acord2:
                nota=note.Note(n)
                streamMeu.append(nota)
        nom = streamMeu.write("musicxml.png")
        self.mostrarImatge(nom)
        self.MplWidget.canvas.flush_events()
        sp=midi.realtime.StreamPlayer(streamMeu)
        sp.play()

    def transferir(self):
        # les cel.les seleccionades del mastil1 es copien a una llista
        # i es marquen amb color blau
        self.resetAcord()
        text=""
        llistaItems= self.taulaMastil.selectedItems()
        if len(llistaItems)>0:
            for item in llistaItems:
                 # retorna la corda i el trast de cada casella marcada

                print(item.column(), item.row())
                nota = self.LNotesCordesOct[item.column()][item.row()]
                self.acordTocar.append(nota)
                nota2 = self.LNotesCordes[item.column()][item.row()]
                if self.RBSostinguts.isChecked():
                    if nota2.find("-") != -1:
                        nota2=bemollASostingut[nota2]
                if self.RBBemolls.isChecked():
                    if nota2.find("#") != -1:
                        nota2 = sostingutABemoll[nota2]
                if nota2.find("-") !=-1:
                    nota2= nota2.replace("-","b")
                text= text+ nota2+ " "

            if notacio=="L":
                text= notacioCaDo(text)
            self.labelAcord.setText(text)
            print(self.acordTocar)
        self.ferAcord(self.acordTocar)

    def tancar(self):
        buidaPaperera()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(app)
    ex.show()
    sys.exit(app.exec_())

