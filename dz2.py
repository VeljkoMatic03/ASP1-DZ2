import copy as copy

class node:
    def __init__(self,value, parent, child):
        self.value = value
        self.parent = parent
        self.child = child
    def ispravnost(self, zabranjeno, m, n):
        temp = []
        flag = True
        for i in range(n):
            for j in range(0, m-1):
                for k in range(j+1, m):
                    temp.append([self.value[i][j], self.value[i][k]])
        for i in range(len(temp)):
            if temp[i] in zabranjeno:
                flag = False
                break
        return flag

def ucitavanje_stdin():
    while True:
        try:
            m = int(input("Unesite broj grupa pojmova (M): "))
        except ValueError:
            print("Unesite ispravnu vrednost")
        else: break
    while True:
        try:
            n = int(input("Unesite broj pojmova po grupi (N): "))
        except ValueError:
            print("Unesite ispravnu vrednost")
        else: break
    lista_pojmova = []
    print("Unesite pojmove, odvojene zarezima")
    for i in range(m):
        temp = input()
        temp_list = temp.split(",")
        while(len(temp_list)!=n):
            print("Unesite pojmove na ispravan način")
            temp = input()
            temp_list = temp.split(",")
        lista_pojmova.append(temp_list)
    lista_uslova = []
    while True:
        uslov = input()
        if uslov == "":
            break
        lista_uslova.append(uslov)
    return lista_pojmova, lista_uslova, m, n

def ucitavanje_file():
    marker = True
    ime = input("Unesite ime fajla sa ekstenzijom: ")
    while(ime[-4:]!='.txt'):
        ime = input("Unesite ponovo ime fajla: ")
    f = open(ime, 'r')
    linije = f.readlines()
    f.close()
    m = int(linije[0][:-1])
    n = int(linije[1][:-1])
    lista_pojmova = []
    lista_uslova = []
    for i in range(m):
        temp = linije[2+i][:-1]
        temp_lista = temp.split(",")
        if len(temp_lista) != n:
            print("Fajl nije ispravan, unesite podatke drugom metodom.")
            marker = False
            break
        lista_pojmova.append(temp_lista)
    if marker == True:
        for i in range(2+m, len(linije)):
            uslov = linije[i]
            if uslov[-1] == "\n":
                uslov = uslov[:-1]
            lista_uslova.append(uslov)
        return lista_pojmova, lista_uslova, m, n
    else:
        return [], [], m, n

def ucitavanje():
    global pojmovi
    global uslovi
    print("Unesite kako želite da učitate podatke:")
    print("0: Unos putem standardnog ulaza")
    print("1: Unos putem fajla")
    while True:
        izbor = input("Vaš izbor: ")
        try:
            izbor = int(izbor)
        except ValueError:
            print("Pogrešan unos, molim Vas unesite validan broj")
        else:
            if izbor == 0 or izbor == 1:
                break
            else:
                print("Pogrešan unos, molim Vas unesite broj 0 ili broj 1")
    if izbor == 0:
        pojmovi, uslovi, m, n = ucitavanje_stdin()
    elif izbor == 1:
        pojmovi, uslovi, m, n = ucitavanje_file()
        if pojmovi == []:
            print("Fajl koji ste koristili nije ispravan, molim Vas učitajte vrednosti na drugi način")
    return pojmovi, uslovi, m, n

def init(pojmovi, m, n):
    value = []
    for i in range(n):
        info = [pojmovi[0][i]]
        for j in range(m-1):
            info.append(None)
        value.append(info)
    root = node(value, None, [])
    return root

def zabranjeno(uslovi, pojmovi, m):
    zabranjeno = []
    for i in range(len(uslovi)):
        uslov = uslovi[i].split("+")
        if len(uslov) == 1:
            uslov = uslovi[i].split("-")
            zabranjeno.append([uslov[0], uslov[1]])
        elif len(uslov) == 2:
            for i in range(m):
                if uslov[0] in pojmovi[i]:
                    skup = copy.deepcopy(pojmovi[i])
                    skup.remove(uslov[0])
                    for j in range(len(skup)):
                        zabranjeno.append([skup[j], uslov[1]])
    return zabranjeno

def generate(otac, pojmovi, list):
    info = otac.value
    slobodni = copy.deepcopy(pojmovi)
    slobodni = slobodni[1:]
    for i in range(len(info)):
        for j in range(1, len(info[i])):
            if info[i][j] != None:
                slobodni[j-1].remove(info[i][j])
    for i in range(len(info)):
        for j in range(1, len(info[i])):
            if info[i][j] == None:
                for k in range(len(slobodni[j-1])):
                    dete_val = copy.deepcopy(info)
                    dete_val[i][j] = slobodni[j-1][k]
                    dete = node(dete_val, otac, [])
                    otac.child.append(dete)
                    list.append(dete)
    return otac, list


def branching(root, uslovi, pojmovi, m, n):
    zabranjeno_l = zabranjeno(uslovi, pojmovi, m)
    lista_grananja = [root]
    while(lista_grananja != []):
        nova_lista_grananja = []
        for i in range(len(lista_grananja)):
            otac = lista_grananja[i]
            proceed = node.ispravnost(otac, zabranjeno_l, m, n)
            if proceed == False:
                otac.child = []
            elif proceed == True:
                otac, nova_lista_grananja = generate(otac, pojmovi, nova_lista_grananja)
        lista_grananja = nova_lista_grananja
    return root, zabranjeno_l

def start():
    global pojmovi;global uslovi; global m; global n
    pojmovi, uslovi, m, n = ucitavanje()
    root = init(pojmovi, m, n)
    root, zabranjeno_l = branching(root, uslovi, pojmovi, m, n)
    return root, zabranjeno_l, m, n, pojmovi, uslovi

def ispis_resenja(root, zabranjeno_l, m, n):
    lista = [root]
    pomocna = []
    stara = []
    while(len(lista) != 0):
        pomocna.clear()
        for i in range(len(lista)):
            otac = lista[i]
            for j in range(len(otac.child)):
                pomocna.append(otac.child[j])
        stara = copy.deepcopy(lista)
        lista = copy.deepcopy(pomocna)
    skup = []
    for i in range(len(stara)):
        if stara[i].value not in skup and node.ispravnost(stara[i], zabranjeno_l, m, n) == True:
            skup.append(stara[i].value)
    return skup

def ispis_stabla(root):
    f = open("ispis stabla.txt", "w")
    lista = [root]
    print(root.value, end = '', file = f)
    tab = '     '
    counter = 1
    while(lista != []):
        print(tab * counter, file = f)
        pomocna = []
        for i in range(len(lista)):
            for j in range(len(lista[i].child)):
                pomocna.append(lista[i].child[j])
                print(lista[i].child[j].value, end = '', sep = '', file = f)
                if j!=len(lista[i].child) - 1:
                    print(" --- ", end = '', file = f)
                if i != (len(lista) - 1) and lista[i].child[j]!= [] and j==(len(lista[i].child)-1): print(" ; ", end='', file = f)
        lista = pomocna
        counter += 1
        print("", file = f)
        print("----------------------------------------------------------------------", file = f)
    f.close()

def provera(root, zabranjeno, m, n, talon):
    resenja = ispis_resenja(root, zabranjeno, m, n)
    lista_poklapanja = []
    iter = [root]
    while len(lista_poklapanja) == 0:
        help = []
        for i in range(len(iter)):
            if iter[i].value == talon:
                lista_poklapanja.append(iter[i])
            else:
                for j in range(len(iter[i].child)):
                    help.append(iter[i].child[j])
        iter = help
    cnt = 0
    for i in range(len(lista_poklapanja)):
        next = lista_poklapanja[i].child
        prethodno = lista_poklapanja
        while (next != []):
            pomocna = []
            for j in range(len(next)):
                if next[j].child != []:
                    for k in range(len(next[j].child)):
                        pomocna.append(next[j].child[k])
            prethodno = next
            next = pomocna
        vrednosti = []
        for i in range(len(prethodno)):
            if prethodno[i].value not in vrednosti and node.ispravnost(prethodno[i], zabranjeno, m, n) == True:
                vrednosti.append(prethodno[i].value)
        finalna = []
        for i in range(len(vrednosti)):
            if vrednosti[i] in resenja:
                raspored_talona = []
                for k in range(len(talon)):
                    for j in range(len(talon[k])):
                        raspored_talona.append(talon[k][j])
                raspored_resenja = []
                for k in range(len(vrednosti[i])):
                    for j in range(len(vrednosti[i][k])):
                        raspored_resenja.append(vrednosti[i][k][j])
                for k in range(n*m):
                    marker = True
                    if raspored_talona[k] != None and raspored_talona[k] != raspored_resenja[k]:
                        marker = False
                        break
                if marker == True:
                    finalna.append(vrednosti[i])
        cnt = len(finalna)
        if cnt>0: break
    return cnt


def igra(root, pojmovi, m, n, zabranjeno):
    global talon
    talon = root.value
    remaining = n * (m-1)
    pojmovi_rem = pojmovi[1:]
    pojmovi_rem_flat = []
    for i in range(len(pojmovi_rem)):
        for j in range(len(pojmovi_rem[i])):
            pojmovi_rem_flat.append(pojmovi_rem[i][j])
    print("---IGRA---")
    print("Izaberite šta želite da radite:")
    print("0: Odigrajte potez")
    print("1: Proverite da li ste korektno uparili pojmove (za sada)")
    print("2: Proverite da li Vas trenutno stanje vodi ka rešenju")
    print("3: Pomoć prijatelja (automatsko upisivanje jednog polja)")
    print("4: Donesite tvrdnju da igra nema rešenja")
    print("5: Odustanite od igre")
    while remaining != 0:
        try:
            choice = int(input())
            while choice<0 or choice>5:
                choice = int(input("Unesite pravilan broj"))
        except ValueError:
            print("Unesite broj")
        else:
            pass
        if choice == 0:
            print("Unesite koji pojam želite da upišete")
            print("Na raspolaganju su:")
            print(pojmovi_rem_flat)
            while (True):
                izbor = input("Izbor: ")
                if izbor not in pojmovi_rem_flat:
                    print("Unesite pravilan izbor")
                else:
                    break
            pojmovi_rem_flat.remove(izbor)
            for i in range(len(pojmovi)):
                if izbor in pojmovi[i]:
                    red = i
            slobodna_mesta = []
            for i in range(n):
                if talon[i][red] == None:
                    slobodna_mesta.append(i)
            print("Na koje slobodno mesto biste upisali izabrani pojam?")
            print("Slobodne kolone: ")
            print(*slobodna_mesta)
            while True:
                try:
                    kolona = int(input())
                    while kolona not in slobodna_mesta:
                        kolona = int(input("Unesite pravilnu kolonu"))
                except ValueError:
                    print("Unesite pravilnu vrednost")
                else: break
            talon[kolona][red] = izbor
            print("Vrednost je uneta!")
            remaining -= 1
        elif choice == 1:
            cvor = node(talon, None, [])
            test = node.ispravnost(cvor, zabranjeno, m, n)
            if test == True: print("Za sada je sve uneto kako treba!")
            else: print("Niste uneli neki pojam kako treba.")
        elif choice == 2:
            cnt = provera(root, zabranjeno, m, n, talon)
            if node.ispravnost(node(talon, None, []), zabranjeno, m, n) == False or cnt == 0:
                print("Trenutno stanje Vas ne vodi do rešenja")
            else:
                print("Trenutno stanje Vas može odvesti do rešenja")
        elif choice == 3:
            cnt = provera(root, zabranjeno, m, n, talon)
            if cnt == 0:
                print("Nema adekvatnog poteza, pogrešili ste u ranijim potezima")
            else:
                taloni = []
                otac = node(talon, None, [])
                otac, taloni = generate(otac, pojmovi, taloni)
                for i in range(len(taloni)):
                    cnt = provera(root, zabranjeno, m, n, taloni[i].value)
                    if cnt>0:
                        cnt = i
                        break
                talon = taloni[i].value
                for p in range(len(talon)):
                    for q in range(len(talon[p])):
                        if talon[p][q] in pojmovi_rem_flat:
                            pojmovi_rem_flat.remove(talon[p][q])
                remaining -= 1
                print("Odigran potez!")
        elif choice == 4:
            skup = ispis_resenja(root, zabranjeno, m, n)
            if len(skup) == 0:
                print("Bravo, tvrdnja je tačna!")
            else:
                print("Vaša tvrdnja nije tačna.")
        elif choice == 5:
            print(talon)
            print("Kraj igre.")
            break
    if remaining == 0:
        print(talon)
    print("---- KRAJ ----")

while True:
    print("---- MENI ----")
    print("0: Učitavanje igre")
    print("1: Ispis stabla")
    print("2: Ispis svih rešenja")
    print("3: Korisnik igra potez")
    print("4: Terminacija programa")
    try:
        odabir = int(input("Odaberite broj: "))
        while(odabir<0 or odabir>4):
            odabir = int(input("Odaberite ispravan broj: "))
    except ValueError:
        print("Unesite ispravnu vrednost")
    else: pass
    if odabir == 0:
        root, zabranjeno_l, m, n, pojmovi, uslovi = start()
    if odabir == 1:
        ispis_stabla(root)
    if odabir == 2:
        skup = ispis_resenja(root, zabranjeno_l, m ,n)
        for i in range(len(skup)):
            print(skup[i])
    if odabir == 3:
        igra(root, pojmovi, m, n, zabranjeno_l)
    if odabir == 4:
        print("Terminacija programa.")
        break
