#!/usr/bin/env python
# -*- coding: utf-8 -*-


#### deklarování proměnných a import funkcí ##### declaration, import

import random
from Tkinter import * #GUI
from PIL import Image, ImageTk  #Zpracování obrázků #image procesing


karta = random.randint(10, 50) #  první karta 
faze = "I" # fáze hry On/Ona (odměny)  I/R/V (úkoly) K=konec
minulafaze = "S" #start, domíchání balíčku dle zdroje karet
ona = 0 # Políčko na kterém stojí, cíl je 15 ##start pozition
on = 0
hraje = random.randint(0, 1) # Los kdo je na řadě (0na/On) 
if hraje == 1:
        rada = "Ona"
else:
        rada = "On"
dal = False #pokračovat přes cílové skore #continue after finish
data= "cs" # img/ pro obrázky cs pro český text,!Změnit i import ## Change task source ("cs" "en" , experimental "img/")
from slice import cs
 ############## Definování funkcí ################ def. functions


def kolo(): # funkce periodicky měníci "hraje" a losující další kartu #### periodicaly change "hraje" and draw card
        global karta, hraje, rada
        if hraje == 1:
                hraje =-1
                rada = "Ona"
                karta = vyberOna.pop(random.randint(0, len(vyberOna)-1)) #výběr karty ##select card
        else:
                hraje =+ 1
                rada = "On"
                karta = vyberOn.pop(random.randint(0, len(vyberOn)-1)) #výběr karty
        schraje.configure(text=rada) # kdo je na řadě do GUI ###  show player in GUI
        if data == "img/":
                photo = ImageTk.PhotoImage(Image.open("slice/%s%d%s.png" % (data, karta, faze))) #aktualizace karty
                img.configure(image=photo)
                img.image=photo #keep reference (kvůli garbage collectoru, špatná implementace v Tk)
        else:
                photo=eval("%s.%s%s[%s]" % (data, faze, rada, karta))
                img.configure(text=(photo), compound=CENTER, font=(None,20), fg="white", wraplength=650)

def jefaze(): #ověření a nastavení "faze" hry ##set phase of game to "faze"
        global hraje, faze, minulafaze
        minulafaze=faze
        if (on or ona) < 6:
                faze = "I"
        elif (on or ona) < 10:
                faze = "R"
        else:
                faze = "V"

def bod(): #přidání bodu pro dle "hraje" ## add point by "hraje"
        global hraje, ona, on
        if hraje == 1:
                ona = ona+1
                scona.configure(text=ona) #zobrazení aktuálního stavu bodů v GUI #show in GUI
        else:
                on = on+1
                scon.configure(text=on)

################## ovládání z příkazové řádky ############# comand line control
##def ukol(): #výběr karty a vyhodnocení splnění
##        while True: #symčka pro vytup od uživatele 0 nebo 1
##                try:
##                        splneno = int(raw_input("Je úkol splněn?")) #vstup uživatele převedený na číslo
##                except ValueError: #enter a písmena
##                        print("zadejte číslo" )
##                else:
##                        if (splneno == 1) or (splneno == 0): # konec smyčky s požadovanou hodnoto ve "splneno"
##                                break
##                        else: print("jen 0 nebo 1" ) #jiná čísla
##        if splneno == 1:
##                bod()
##        elif splneno ==  0:
##                print("Fant - %s" % str(rada))
##                
##        else:
##                print("nikdo" ,splneno)
#####################################################

def balicek(): # obnoví balíček při přechod k další fázi #set new deck when "faze" is changed
        global vyberOna, vyberOn
        if data == "img/":
                if not(faze==minulafaze):
                        vyberOna=range(1,51)
                        vyberOn=range(1,51)
                        print("nový balíček Oba")
                elif len(vyberOna)==0:
                        vyberOna=range(1,51)
                        print("nový balíček jen Ona")
                elif len(vyberOn)==0:
                        vyberOn=range(1,51)
                        print("nový balíček jen On")
        else:
                if not(faze==minulafaze):
                        je=("%s.%sOna" % (data, faze))
                        vyberOna=range(1, (len(eval(je))))
                        je=("%s.%sOn" % (data, faze))
                        vyberOn=range(1, (len(eval(je))))
                        print("nový balíček Oba")
                elif len(vyberOna)==0:
                        je=("%s.%sOna" % (data, faze))
                        vyberOna=range(1, (len(eval(je))))
                        print("nový balíček jen Ona")
                elif len(vyberOn)==0:
                        je=("%s.%sOn" % (data, faze))
                        vyberOn=range(1, (len(eval(je))))
                        print("nový balíček jen On")                        

        
def ok(): #splněno ##task completed
        jefaze()
        balicek()
        kolo()
        if dal == False:
                bod()
        print("\nna řadě %s" % rada)
        print("karta %s" % str(karta)+faze)
        end()

def restart(): #pokračovat ve hře ## continue play after reach finish
		global dal
		bn.configure(state=NORMAL) #aktivace ovládacích prvků
		dal = True
		print("pokracovat")
		

def fant(): #fant ##dare
        jefaze()
        balicek()
        kolo()
        print("karta %s" % str(karta)+faze)

def end(): #zjištění zda není konec hry a případné ukončovací kroky
        if (ona > 15) or (on > 15):
                global faze
                print("konec")
                faze = "K" #konec
                endtxt = Label( hl, text="To je konec hry")
                endtxt.grid(row=3, columnspan=3)
                bk = Button(hl, text="Ukončit", command=(hl.destroy)) #vypínací tlačítko
                br = Button(hl, text="Pokračovat", command=restart) #pokračovat tlačítko
                bk.grid(row=3, column=2, columnspan=2)
                br.grid(row=3, column=0, columnspan=2)
                ba.configure(state=DISABLED) #deaktivace ovládacích prvků
                bn.configure(state=DISABLED)
                if data == "img/":
                        photo=ImageTk.PhotoImage(Image.open("slice/%s%d%s.png" % (data, (random.randint(1, 50)), rada) )) #poslední obrázek
                        img.configure(image=photo)
                        img.image=photo #keep reference
                else:
                        if rada == "On":
                                je=("%s.On" % (data))
                                vyberOn=range(1, (len(eval(je))))
                                karta = vyberOn.pop(random.randint(1, len(vyberOn)-1))
                        else:
                                je=("%s.Ona" % (data))
                                vyberOna=range(1, (len(eval(je))))
                                karta = vyberOna.pop(random.randint(1, len(vyberOna)-1))
                        photo=eval("%s.%s[%s]" % (data, rada, karta))
                        img.configure(text=(photo))


################### GUI ################

hl = Tk() #hlavní okno
hl.title("Love game")
ba = Button(hl, text="OK", command=ok) #hlavní ovládací prvky
bn = Button(hl, text="Fant", command=fant)
bn.grid(row=0, column=2, padx=10, pady=10)
ba.grid(row=0, column=0, padx=10, pady=10)
score = Frame(hl) #rámec v němž je zobrazen stav hry
score.grid(row=1, columnspan=3)
scona = Label(score, width=3, fg="red",text=ona)
scona.grid(row=0, column=0)
scon = Label(score, width=3, fg="blue", text=on)
scon.grid(row=0, column=3)
schraje = Label(score, width=3, bg="white",text=rada)
schraje.grid(row=0, column=1)
balicek()
if data != "img/":
        photo=ImageTk.PhotoImage(Image.open("slice/K.png" )) #úvodní obrázek s místem na text
else:
        photo=ImageTk.PhotoImage(Image.open("slice/S.png" )) #úvodní obrázek

img = Label(hl, image=photo) #label pro obrázek
img.grid(row=4, columnspan=3)
fant()
hl.mainloop()