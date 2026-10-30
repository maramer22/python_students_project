class Console:
    def __init__(self, srv_student, srv_disciplina, srv_nota,srv_statistica ):
        self.__srv_student = srv_student
        self.__srv_disciplina = srv_disciplina
        self.__srv_nota = srv_nota
        self.__srv_statistica = srv_statistica

    @staticmethod #nu poate accesa atributele clasei
    def print_menu():
        print("1. Adauga student")
        print("2. Adauga disciplina")
        print("3. Sterge student dupa id")
        print("4. Sterge disciplina dupa id")
        print("5. Afiseaza toti studentii")
        print("6. Afiseaza toate disciplinele")
        print("7. Modifica student")
        print("8. Modifica disciplina")
        print("11. Cauta un student in lista dupa id")
        print("12. Cauta o disciplina in lista dupa id")
        print("13. Genereaza studenti")
        print("14. Genereaza disciplina")
        print("15. Creati o nota")
        print("16. Afiseaza toate notele")
        print("17. Afiseaza studentii ordonati alfabetic")
        print("18. Afiseaza notele ordonate descrescator")
        print("19. Statistica cu primii 20% cei mai buni elevi dupa medie")
        print("20. Top 3 elevi in functie de cea mai frecventa materie")
        print("E. Exit")

    @staticmethod
    def __print_studenti(lista_studenti):
        if not lista_studenti:
            print("Nu exista studenti in baza de date")
        else:
            print("Lista de studenti:")
            for student in lista_studenti:
                print(student)

    @staticmethod
    def __print_discipline(lista_discipline):
        if not lista_discipline:
            print("Nu exista discipline in baza de date")
        else:
            print("Lista de discipline:")
            for disciplina in lista_discipline:
                print(disciplina)


    def __add_ui_student(self):
        s_id = input("ID student:")
        nume_student = input("Numele studentului")
        prenume_student = input("Prenumele studentului:")

        try:
            s_id = int(s_id)
            self.__srv_student.adauga_student(s_id, nume_student, prenume_student)
        except ValueError as e:
            print(str(e))
        else:
            print("Studentul a fost adaugat cu succes")

    def __add_ui_disciplina(self):
        d_id = input("ID disciplina:")
        nume_disciplina = input("Numele disciplinei: ")
        nume_prof_disciplina = input("Numele profesorului care preda disciplina:")

        try:
            d_id = int(d_id)
            self.__srv_disciplina.adauga_disciplina(d_id, nume_disciplina, nume_prof_disciplina)
        except ValueError as e:
            print(str(e))
        else:
            print("Disciplina adaugata cu succes")

    def verif_daca_exista_student(self):
        id_cautat = int(input("Introduceti id-ul studentului pe care vreti sa il cautati:"))
        if self.__srv_student.exista_studentul_cautat(id_cautat):
            print("Studentul exista!")
        else:
            print("Studentul nu exista!")

    def verif_daca_exista_disciplina(self):
        id_cautat = int(input("Introduceti id-ul disciplinei cautate "))
        if self.__srv_disciplina.exista_disciplina_dorita(id_cautat):
            print("Disciplina exista în sistem")
        else:
            print("Disciplina nu exista")


    def __delete_ui(self):
        s_id = input("Introduceti id-ul studentului de sters:")
        try:
            s_id = int(s_id)
            student_sters = self.__srv_student.sterge_student(s_id)
            print(f"{student_sters} a fost sters")
        except ValueError as e:
            print(str(e))

    def __delete_ui_disciplina(self):
        d_id = input("Introduceti id-ul disciplinei de sters:")
        try:
            d_id = int(d_id)
            disciplina_sters = self.__srv_disciplina.sterge_disciplina(d_id)
            print(f"{disciplina_sters} a fost stearsa")
        except ValueError as e:
            print(str(e))

    def __modifica_ui_student(self):
        s_id = int(input("ID student de modificat: "))
        nume_nou = input("Noul nume: ")
        prenume_nou = input("Noul prenume: ")
        student_vechi = self.__srv_student.modifica_student(s_id, nume_nou, prenume_nou)
        print(f"Studentul {student_vechi} a fost modificat.")

    def __modifica_ui_disciplina(self):
        d_id = int(input("ID disciplina de modificat: "))
        nume_dis_nou = input("Numele disciplinei nou: ")
        nume_prof_nou = input("Numele profesorului nou: ")
        disciplina_veche = self.__srv_disciplina.modifica_disciplina(d_id, nume_dis_nou, nume_prof_nou)
        print(f"Disciplina {disciplina_veche} a fost modificata.")

    def __afiseaza_studenti(self):
        studenti = self.__srv_student.afisare_student()
        print("Studentii actuali sunt: ")
        for s in studenti:
            print(s)

    def __afiseaza_discipline(self):
        discipline = self.__srv_disciplina.afisare_discipline()
        print("Disciplinele actuale sunt : ")
        for d in discipline:
            print(d)
    def genereaza_student_random_ui(self):
        nr = int(input("Introduceti cati studenti vreti sa generati:"))
        for i in range(nr):
            student = self.__srv_student.genereaza_student()
            print(f"{i+1}:{student}")

    def genereaza_disciplina_random_ui(self):
        nr = int(input("Introduceti cate discipline vreti sa introduceti: "))
        for i in range(nr):
            disciplina = self.__srv_disciplina.genereaza_disciplina_random()
            print(f"{i+1}: {disciplina}")

    def __adauga_nota_ui(self):
        try:
            studenti = self.__srv_student.afisare_student()
            if not studenti:
                print("Nu exista studenti")
                return
            print("Studenti disponibili:")
            for s in studenti:
                print(s)
            id_student = int(input("Introduceti id-ul studentului:"))
            if not self.__srv_student.exista_studentul_cautat(id_student):
                print("Studentul acesta nu exista!")
                return

            discipline = self.__srv_disciplina.afisare_discipline()
            if not discipline:
                print("Nu exisra discipline in baza de date")
                return
            print("Discipline disponibile:")
            for d in discipline:
                print(d)
            id_disciplina = int(input("Introduceti id-ul disciplinei: "))
            if not self.__srv_disciplina.exista_disciplina_dorita(id_disciplina):
                print("Disciplina nu exista")
                return

            valoare = float(input("Introduceti nota de la 1 la 10: "))
            if not (1 <= valoare <= 10):
                print("Nota trebuie sa fie intre 1 si 10")
                return

            nota = self.__srv_nota.adauga_nota(id_student, id_disciplina, valoare)
            print(f"Nota {valoare} pentru studentul {id_student} la disciplina {id_disciplina} a fost introdusa")

        except ValueError as ve:
            print(f"Eroare : {ve}")


    def __afiseaza_note(self):
        note = self.__srv_nota.afisare_note()
        if not note:
            print("Nu exista note in baza de date")
        else:
            print("Notele acordate sunt: ")
            for n in note:
                print(n)

    def __afiseaza_studenti_sortati(self):
        studenti = self.__srv_student.sortare_alfabetica_studenti()
        print("Studentii ordonati alfabetic sunt:")
        if not studenti:
            print("Nu exista studenti de afisat")
        else:
            for s in studenti:
                print(s)

    def __afiseaza_note_sortate(self):
        note = self.__srv_nota.sortare_descrescatoare_note()
        print("Notele ordonate descrescator sunt:")
        if not note:
            print("Nu exista note de afișat")
        else:
            print("Notele ordonate descrescator:")
            for n in note:
                print(n)

    def __afiseaza_primii_20(self):

            statistics = self.__srv_student.afiseaza_primii_20_la_suta()

            if not statistics:
                print("Nu s-au gasit studenti cu note")
                return
            print("Primii 20% studenti dupa medii:")
            for i, medie_stud in enumerate(statistics):
                print(f"Locul {i+1}: {medie_stud}")

    def __afiseaza_top_final(self):
        try:
            rezultat = self.__srv_statistica.top_final()
            materie = rezultat['materie_top']
            top_studenti = rezultat['top_studenti']

            if not top_studenti:
                print("Nu s-a putut genera topul")
            else:
                print("Topul cerut:")
                for i, student_data in enumerate(top_studenti):
                    nume = student_data['nume_student']
                    numar_note = student_data['numar_note_la_materie_top']
                    medie_initiala = student_data['media_generala_initiala']
                    print(f"Locul {i+1}: {nume}, nr note la {materie}: {numar_note} cu media generala {medie_initiala}")

        except ValueError:
            print("Eroare")








    def run(self):
        while True:
            Console.print_menu()
            option = input(">>>").strip()
            if option == "1":
                self.__add_ui_student()
            elif option == "2":
                self.__add_ui_disciplina()
            elif option == "3":
                self.__delete_ui()
            elif option == "4":
                self.__delete_ui_disciplina()
            elif option == "7":
                self.__modifica_ui_student()
            elif option == "8":
                self.__modifica_ui_disciplina()
            elif option == "11":
                self.verif_daca_exista_student()
            elif option == "12":
                self.verif_daca_exista_disciplina()
            elif option == "5":
                self.__afiseaza_studenti()
            elif option == "6":
                self.__afiseaza_discipline()
            elif option == "13":
                self.genereaza_student_random_ui()
            elif option == "14":
                self.genereaza_disciplina_random_ui()
            elif option == "15":
                self.__adauga_nota_ui()
            elif option == "16":
                self.__afiseaza_note()
            elif option == "17":
                self.__afiseaza_studenti_sortati()
            elif option == "18":
                self.__afiseaza_note_sortate()
            elif option == "19":
                self.__afiseaza_primii_20()
            elif option == "20":
                self.__afiseaza_top_final()

            else:
                print("Optiune invalida")

