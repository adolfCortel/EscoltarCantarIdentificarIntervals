from music21 import *
import random
import os
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import time
import winsound
from PIL import Image

nomsIntervals = ["2m", "2M", "3m", "3M", "4J", "trito", "5J", "6m", "6M", "7m", "7M", "8J"]
llistaIntervals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

nomsIntervalsMaj = ["2M", "3M", "4J", "5J", "6M", "7M", "8J"]
llistaIntervalsMaj = [2, 4, 5, 7, 9, 11, 12]

nomsIntervalsMen = ["2m", "3m", "trito", "6m", "7m"]
llistaIntervalsMen = [1, 3, 6, 8, 10]

# diccionari amb els semitons de cada interval
nomsIntervalsAsc= {"2m":1,"2M":2, "3m":3, "3M":4, "4J":5, "trito":6,"5J":7, "6m":8,"6M":9, "7m":10, "7M":11, "8J":12}
totesNotes=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

class finestraAjuda(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ajudaIntervals.ui", self)
        self.BSortirAjuda.clicked.connect(self.sortirAjuda)
    def sortirAjuda(self):
        self.close()



def beep():
    # de winsound. Pita : frequencia, durada
    winsound.Beep(600, 250)
    time.sleep(0.25)


def buidaPaperera():
    # buida el directori temporal de morralla
    dir_esborrar = os.path.join(os.getcwd(), "scratchPath")
    llistaArxius = os.listdir(dir_esborrar)
    for arxiu in llistaArxius:
        nomArxiu = os.path.join(os.getcwd(), "scratchPath", arxiu)
        os.remove(nomArxiu)

def llegirConfiguracio1():
    # llegeix config.txt per saber on ha d'anar a buscar musescore
    with open("./config.txt", "r") as file:
        for line in file.readlines():

            if line.startswith("MUSESCORE"):
                temp = line.find("=")
                ssttMusescore = line[temp + 1:-1]

    return ssttMusescore


class App(QMainWindow):
    streamMeu=[]
    nota = "C"  # primera nota interval MAJUSC+alteracio
    nota2 = ""  # l'altra nota de l'interval
    octava = "4"  # str amb numero de l'octava
    intervalMeu = ""  # interval que s'ha triat per escoltar i cantar
    STintervalQueSona = 0  # nombre de semitons de l'interval que es toca i que s'ha d'endevinar
       # el nom de l'interval que ha sonat sera: nomsIntervals[llistaIntervals[self.STintervalQueSona-1]

    tocat = False  # es posa a true quan ha sonat l'interval
    kS = ""  # key signature
    nProves, nEncerts = 0, 0  # en endevinar compta les proves i els encerts

    aleatoriVell = 0  # per evitar repeticions en els numeros aleatoris
    errors = ""  # llista dels errors que s'han fet, per controlar on es falla més

    def __init__(self,parent):
        super().__init__()
        loadUi("totsIntervals.ui",self)
        self.setWindowTitle("Escoltar, cantar i identificar  intervals musicals .Adolf Cortel 2024")
        self.botoAcabar.clicked.connect(self.tancar)
        self.BRepetir.clicked.connect(self.repetir)
        self.BOida.clicked.connect(self.oida)  # boto toca interval
        self.BReset.clicked.connect(self.reinicia)
        self.CBArrelAleatoria.clicked.connect(self.notaVisible)
        self.grupBotons.buttonClicked.connect(self.onClicked)
        self.BAjuda.clicked.connect(self.obrirAjuda)
        self.testDirectoris()
        self.tabWidget.setStyleSheet('''
                        QTabBar::tab:!selected {background-color: rgb(170,200,170);}
                        QTabBar::tab:selected  {background-color: pink; }
                        QWidget {background-color: rgb(230,230,230);}
                                            ''')
        self.tabWidget.setCurrentIndex(0)
        self.reinicia()

    def obrirAjuda(self):
        fA = finestraAjuda()
        fA.show()
        fA.exec()

    def finestraProblemes(self, s):
        # s'obre una finestra per avisar d'un problema
        QMessageBox.about(self, s)


    def testDirectoris(self):
        # crea el subdirectori scratchPath per a posar la morralla si es que no eisteix
        # llegeix l'arxiu de configuració per saber on es Musescore
        nom_dir = os.path.join(os.getcwd(),"scratchPath")
        if not os.path.exists(nom_dir):
            try:
                os.mkdir("scratchPath")
            except:
                print("problema en la creacio de scratchPath")
        nom_dir= os.path.join(os.getcwd(),"scratchPath")
        environment.set("directoryScratch", nom_dir)
        ssMusescore = llegirConfiguracio1()
        if os.path.exists(ssMusescore):
            environment.set("musescoreDirectPNGPath", ssMusescore)
        else:
            self.finestraProblemes(" No es troba l'arxiu: "+ssMusescore)
            self.tancar()
    def onClicked(self, button):
        # Quan s'apreta un boto d'un interval:
        #  si la tab es Escoltar i cantar es fa una cosa si es identificar una altra
        if self.tabWidget.currentIndex() == 0: # escoltar i cantar
            self.onClickedEscoltarCantar(button)
        if self.tabWidget.currentIndex() == 1:
            self.onClickedIdentificar(button)

    def netejaImatge(self):
        # esborra el canvas
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.set_axis_off()
        self.MplWidget.canvas.flush_events()
        self.MplWidget.canvas.draw()

    def mostrarImatge(self,nomArxiu):
        # mostra la imatge de la partitura
        im1 = Image.open(nomArxiu)  # .resize((800,600))
        self.netejaImatge()
        self.MplWidget.canvas.axes.imshow(im1)
        self.MplWidget.canvas.draw()

    def notaVisible(self):
        if self.CBArrelAleatoria.isChecked():
            self.CBNota.setEnabled(False)
        else:
            self.CBNota.setEnabled(True)
    def tria_nota1(self):
        if self.CBArrelAleatoria.isChecked():
            num = random.randint(0, 11)  # randint >> enter de 0 a 11 (inclosos)
            self.nota = note.Note(totesNotes[num] + self.CBOctava.currentText())  # 4: es tocara a la octava triada
        else:
            self.nota = note.Note(self.CBNota.currentText() + self.CBOctava.currentText())


    def onClickedEscoltarCantar(self, button):
        # toca l'interval triat, ascendent o descendent,  a partir de la nota arrel
        self.tocat=False
        self.netejaImatge()
        boto = str(button.objectName())
        boto = boto[1:]  # es treu la lleta B del davant del nom
        self.tria_nota1()
        self.nota.duration.type = "half"

        if self.CBAscDescOida.currentText() == "Ascendent":
            self.intervalMeu = interval.Interval(nomsIntervalsAsc[boto])
        else:
            # es treu el nombe de semitons del diccionari
            # si l'interval es descendent s'ha de multiplicar l'ascendent per -1
            intDes = int(nomsIntervalsAsc[boto] * (-1))
            self.intervalMeu = interval.Interval(intDes)

        self.nota2 = self.intervalMeu.transposeNote(self.nota)
        self.nota2.duration.type = "half"
        self.streamMeu = stream.Stream()

        if self.CBAcord.currentText() == "Arpegi":
            self.streamMeu.append(self.nota)
            rr = note.Rest()
            rr.duration.type = "half"
            self.streamMeu.append(rr)
            self.streamMeu.append(self.nota2)
        else:  # acord"
            acord = []
            acord.append(self.nota)
            acord.append(self.nota2)
            acordFet = chord.Chord(acord)
            self.streamMeu.append(acordFet)
        if self.CBVeurePartitura.isChecked():
            nom = self.streamMeu.write("musicxml.png")
            self.mostrarImatge(nom)
            self.MplWidget.canvas.flush_events()
        sp = midi.realtime.StreamPlayer(self.streamMeu)
        sp.play()
        self.tocat =True

    def onClickedIdentificar(self, button):
        # quan el tab es identificar
        # quan es prem un boto es mira si l'interval coincideix amb el que ha sonat
        # i el nom de l'interval que ha sonat  és nomsIntervals[self.STintervalQueSona- 1]
        if self.tocat:
            # només es considera si s'ha apretat un boto si ja s'ha tocat l'interval
            boto = str(button.objectName())
            boto=boto[1:] # es treu la lleta B del davant
            self.LTriat.setText(boto)
            self.LTriat.repaint()
            # self.STintervalQueSona es els semitons de l'interval que ha sonat
            nomSonat = nomsIntervals[self.STintervalQueSona - 1]
            self.LResultat.setText(nomSonat)
            self.LResultat.repaint()
            self.nProves = self.nProves + 1
            self.NProves.setText(str(self.nProves))
            if boto == nomSonat:
                self.nEncerts = self.nEncerts + 1
                self.NEncerts.setText(str(self.nEncerts))
            else:
                beep()
                self.errors = self.errors + boto + ", "
                self.LErrades.setText(self.errors)
                self.LErrades.repaint()
            self.tocat = False

    def esborraTextos(self):
        self.LTriat.setText("")
        self.LTriat.repaint()
        self.LResultat.setText("")
        self.LResultat.repaint()
    def reinicia(self):
        # fa reset de tots els resultats
        self.esborraTextos()
        self.nProves, self.nEncerts = 0, 0
        self.NProves.setText(str(self.nProves))
        self.NProves.repaint()
        self.NEncerts.setText(str(self.nEncerts))
        self.NEncerts.repaint()
        self.errors = ""
        self.LErrades.setText(self.errors)
        self.LErrades.repaint()
        self.tocat = False

    def repetir(self):
        # torna a tocar l'ultim stream
        if len(self.streamMeu)>0:
            sp = midi.realtime.StreamPlayer(self.streamMeu)
            sp.play()


    def quinIntervalSonara(self):
        # posa un valor als nombre de semitons a self.STIntervalQue Sona
        # # retorna la segona nota de l'interval que sonarà
        # tria aleatoriament el nombre de semitons d'un interval i el guarda a self.STintervalQueSona

        if self.RBMajors.isChecked():
            numLlista = 6
        elif self.RBMenors.isChecked():
            numLlista = 4
        else:
            numLlista = 11

        # aleatorivell es per no repetir l'anterior
        aleatori = random.randint(0, numLlista)
        while aleatori == self.aleatoriVell:
            aleatori = random.randint(0, numLlista)
        self.aleatoriVell = aleatori
        # STintervalQueSona nombre de semitons de l'interval que sonara

        if self.RBMajors.isChecked():
            self.STintervalQueSona = llistaIntervalsMaj[aleatori]
        elif self.RBMenors.isChecked():
            self.STintervalQueSona = llistaIntervalsMen[aleatori]
        else:
            self.STintervalQueSona = llistaIntervals[aleatori]
        # self.STintervalQueSona és el nombre de semitons  on esta la segona nota
        # i el nom de l'interval és troba amb : nomsIntervals[self.STintervalQueSona- 1]
        intervalTemp = interval.Interval(self.STintervalQueSona)
        # intervalTemp variable interna per definir un interval a music21
        # torna la segona nota de l'interval
        return intervalTemp.transposeNote(self.nota)

    def oida(self):
        # quan es prem "Toca Interval" dins la tab Identificar
        # genera l'interval o acord i el fa sonar
        self.tocat = False
        self.esborraTextos()
        # agafar la primera nota
        self.tria_nota1()
        # armadura major corresponent a la primera nota
        self.kS = key.Key(self.CBNota.currentText())
        # ara la segona nota que sonara
        self.nota2 = self.quinIntervalSonara()  # tria les dues notes de l'interval a self.nota i self.nota2 i
        self.streamMeu = stream.Stream()

        if self.CBAcord.currentText() == "Acord":
            acord = []
            self.nota.duration.type = "half"
            acord.append(self.nota)
            self.nota2.duration.type = "half"
            acord.append(self.nota2)
            acordFet = chord.Chord(acord)
            self.streamMeu.append(acordFet)
        else:  # es tocarà l'arpegi
            if self.CBAscDescOida.currentText() == "Ascendent":
                capOn = "A"
            if self.CBAscDescOida.currentText() == "Descendent":
                capOn = "D"
            if self.CBAscDescOida.currentText() == "Aleatori":
                numAl = random.randint(0, 1)
                lletra = ["A", "D"]
                capOn = lletra[numAl]

            if capOn == "A":
                self.streamMeu.append(self.nota)
                self.streamMeu.append(self.nota2)
            else:
                self.streamMeu.append(self.nota2)
                self.streamMeu.append(self.nota)
        sp = midi.realtime.StreamPlayer(self.streamMeu)
        sp.play()
        self.tocat = True
        # fins aqui, ha tocat

    def tancar(self):
        # tanca el programa però abans buida la morralla
        buidaPaperera()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(app)
    ex.show()
    sys.exit(app.exec_())