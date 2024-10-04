
Instruccions d'instal.lació

Requeriment: l'ordinador ha de tenir instal.lat el programa Musescore. Aquest programa es pot descarregar gratuitament a:  https://musescore.org/es. Si a l'ordinador no hi ha musescore el programa "Escoltar i cantar"no funcionarà. 

El programa s'ha provat amb Windows11 i Windows7. Desconec com funciona amb una altra versió del sistema operatiu. 

1. Instal.lació
	El programa s'ha escrit en el llenguatge python i la interfície per a interaccionar-hi s'ha fet amb QtDesigner5. Es pot instal.lar a qualsevol directori o subdirectori de l'ordinador. S'hi han de copiar tots els arxius que hi ha dins del repostori. L'arxiu "executable" és intervals.py, els altres son arxius ui generats amb QtDesigner o altres arxius de suport.	

L'arxiu config.txt és molt breu; només conté dues línies. En el meu ordinador el contingut és:
MUSESCORE =C:\Program Files\MuseScore 4\bin\musescore4.exe
FONT=C:\Windows\Fonts\arial.ttf

Heu d'adaptar el contingut de config.txt al vostre ordinador. Obriu-lo amb el bloc de notes (o qualsevol editor de text sense format):
	La primera línia indica on es troba el  programa musescore. L'heu de canviar si en el vostre ordinador es troba en un directori diferent o teniu instal.lada una altra versió del programa. 
	A la segona linia s'indica que el programa farà servir la font de text arial.ttf, que en el meu ordinador es troba en el lloc indicat. Si és necessari, canvieu el lloc on es troba la font en el vostre ordinador i canvieu-la al vostre gust.

	Després de modificar config.txt guardeu-lo com a arxiu de text  sense format (*.txt)

Quan el programa s'executa el primer que fa es confirmar que museescore i la font de text especificats en config.txt existeixen en el lloc que s'ha indicat. Si no és així, s'obre una finestra dient que no s'ha trobat l'arxiu i heu de modificar config.txt amb les "adreces" correctes.

	Notareu que quan executeu el programa apareix el subdirectori "scratchPad"; es tracta d'un subdirectori que el programa crea per guardar-hi arxius temporals que es generen i que s'esborren quan se surt del programa. No li feu cap cas. El programa no fa cap canvi en altres arxius i no recull cap mena d'informació sobre vosaltres ni el que feu, no cal que estigui connectat a internet mentre hi treballeu. Per tot això, si per alguna raó el voleu eliminar de l'ordinador n'hi ha prou amb esborrar el directori que heu creat on hi ha els arxius del programa.

Les instruccions de funcionament són a l'arxiu:
[textajudaIntervals.odt](https://github.com/user-attachments/files/17257609/textajudaIntervals.odt)

