from DOMAIN.entities import Studenti, Discipline, Nota, MedieStudent
import random
import string


def bubble_sort(lista, key=None, reverse=False):
    n = len(lista)
    swapped = False
    for j in range (0, n - 1):
        val1 = key(lista[j]) if key else lista[j]
        val2 = key(lista[j + 1]) if key else lista[j + 1]

        if reverse:
            conditie = val1 < val2
        else:
            conditie = val1 > val2

        if conditie:
            lista[j], lista[j + 1] = lista[j + 1], lista[j]
            swapped = True
    if not swapped:
        return
    else:
        bubble_sort(lista, key, reverse)


class ServiceStudenti:

    def __init__(self, repo1, val1, srv_nota):
        self.__repo1 = repo1
        self.__val = val1
        self.__srv_nota = srv_nota

    def get_student_by_id(self, id_dorit: int):
        return self.__repo1.get_student_by_id(id_dorit)

    def adauga_student(self, id_student: int, nume_student: str, prenume_student: str):
        """
        adauga un student
        :param id_student: id_ul studentului, de tip int
        :param nume_student: numele studentului, de tip string
        :param prenume_student: prenumele studentului, de tip string
        :return: eroare daca datele introduse despre studentul dorit nu sunt valide, daca nu doar adauga datele studentului
        """
        student = Studenti(id_student, nume_student, prenume_student)
        self.__val.validate(student)
        self.__repo1.add(student)

    def sterge_student(self, id_de_sters:int):
        """
        sterge datele studentului cu un id dorit
        :param id_student: id-ul studentului care se doreste a fi sters
        :return: studentul sters
        """
        return self.__repo1.remove(id_de_sters)

    def modifica_student(self, id_student: int, nume_nou: str, prenume_nou: str):
        """
        modifica datele referitoare la un studwnt
        :param id_student:id_ul studentului ca carui date se doresc a fi modificate
        :param nume_nou: noul nume, string
        :param prenume_nou: noul prenume, string
        :return: se modifica datele in mmemorie
        """
        student_nou = Studenti(id_student, nume_nou, prenume_nou)
        self.__val.validate(student_nou)
        student_vechi = self.__repo1.update(id_student, student_nou)
        return student_vechi

    def __modifica_student_recursiv(self, lista, id_cautat, nume_nou):
        if len(lista) == 0:
            raise ValueError("Studentul nu exista")
        if lista[0].get_id() == id_cautat:
            lista[0].set_nume(nume_nou)
            return
        self.__modifica_student_recursiv(lista[1:], id_cautat, nume_nou)

    def exista_studentul_cautat(self, id_dorit: int):
        """
        cauta studentul indicat de id
        :param id_dorit: id ul studentului care se doreste a fi cautat
        :return: daca studentul exista sau nu in lista
        """
        return self.__repo1.cautare(id_dorit)

    def afisare_student(self):
        """

        afiseaza studentii existenti
        """
        return self.__repo1.get_all_stud()

    def sortare_alfabetica_studenti(self):
        studenti = self.__repo1.get_all_stud()
        studenti_copie = studenti[:]
        bubble_sort(studenti_copie, key=lambda s: s.get_nume())
        return studenti_copie


    def __genereaza_id_random(self):
        """

        :return: id care nu exisrta deja
        """
        while True:
            id_nou = random.randint(1, 100_000)
            if not self.__repo1.cautare(id_nou):
                return id_nou

    def __genereaza_nume_prenume_random(self, lungime=6):
        """

        :param lungime: lungimea numelui/prenumelui care se vrea generat, de tip int
        :return: genereaza un nume/prenume random
        """
        litere = string.ascii_lowercase
        nume = ""
        for i in range(lungime):
            nume += random.choice(litere)
        return nume.capitalize()

    def genereaza_student(self):
        """

        :return: genereaza datele unui student random
        """
        id_student = self.__genereaza_id_random()
        nume = self.__genereaza_nume_prenume_random()
        prenume = self.__genereaza_nume_prenume_random()
        student = Studenti(id_student, nume, prenume)
        self.__val.validate(student)
        self.__repo1.add(student)
        return student

    def afiseaza_primii_20_la_suta(self):
        """

        :return: afiseaza primii 20% cei mai buni studenti dupa rezultate
        """
        toate_notele = self.__srv_nota.afisare_note()
        note_student = {}

        for nota in toate_notele:
            s_id = nota.get_id_student()
            if s_id not in note_student:
                note_student[s_id] = []
            note_student[s_id].append(nota.get_valoare())

        statistica_completa = []
        studenti_existenti = self.__repo1.get_all_stud()

        for student in studenti_existenti:
            s_id = student.get_id()
            if s_id in note_student:
                note_lista = note_student[s_id]
                media = sum(note_lista)/len(note_lista)
                nume = f"{student.get_nume()}{student.get_prenume()}"
                medie_stud = MedieStudent(s_id, nume, media)
                statistica_completa.append(medie_stud)

        bubble_sort(statistica_completa, key=lambda medie_stud: medie_stud.get_media(), reverse = True)
        total_studenti_cu_note = len(statistica_completa)
        nr_20_la_suta = int(0.2 * total_studenti_cu_note)
        return statistica_completa[:nr_20_la_suta]

    def top_3_studenti(self):
        """

        :return: top 3 studenti cu cea mai amre medie genrerala

        """
        toate_notele = self.__srv_nota.afisare_note()
        note_student = {}
        for nota in toate_notele:
            s_id = nota.get_id_student()
            if s_id not in note_student:
                note_student[s_id] = []
            note_student[s_id].append(nota.get_valoare())

        statistica = []
        for s_id, note_lista in note_student.items():
            student = self.__repo1.get_student_by_id(s_id)
            if student:
                media = sum(note_lista)/len(note_lista)
                nume = f"{student.get_nume()} {student.get_prenume()}"
                medie_stud = MedieStudent(s_id, nume, media)
                statistica.append(medie_stud)

        bubble_sort(statistica, key=lambda medie_stud: medie_stud.get_media(), reverse=True)
        return statistica[:3]




class ServiceDiscipline:
    def __init__(self, repo2, val2):
        self.__repo2 = repo2
        self.__val2 = val2

    def adauga_disciplina(self, id_disciplina: int, nume_disciplina: str, nume_prof:str):
        """
        adauga datele specifice unei discipline
        :param id_disciplina: id-ul disciplinei, de tip int
        :param nume_disciplina: numele disciplinei, de tip string
        :param nume_prof: numele profesorului care preda disciplina, de tip string
        :return: adauga  disciplina
        """
        disciplina = Discipline(id_disciplina, nume_disciplina, nume_prof)
        self.__val2.validatedis(disciplina)
        self.__repo2.adddis(disciplina)

    def sterge_disciplina(self, id_dis_de_sters):
        """
        sterge disciplina aferenta id-ului dorit
        :param id_dis_de_sters: id-ul dorit, de tip int
        :return: disciplina stearsa
        """
        return self.__repo2.removedis(id_dis_de_sters)

    def modifica_disciplina(self, id_dis: int, nume_dis_nou: str, nume_prof_nou: str):
        """
        se modifica datele referiotare la o anumita disciplina
        :param id_dis: id_ul disciplinei care se doreste a fi modificata
        :param nume_dis_nou: noul nume al disciplinei
        :param nume_prof_nou: noul nume al profesorului
        :return: se modifica lista in memorie
        """
        disciplina_noua = Discipline(id_dis, nume_dis_nou, nume_prof_nou)
        self.__val2.validatedis(disciplina_noua)
        disciplina_veche = self.__repo2.updatedis(id_dis, disciplina_noua)
        return disciplina_veche

    def exista_disciplina_dorita(self, id_dorit):
        """
        pt a cauta o disciplina in lista de discipline
        :param id_dorit: id-ul disciplinei care se doreste a fi cautata
        :return: daca exista sau nu disciplina
        """
        return self.__repo2.cautare_dis(id_dorit)

    def afisare_discipline(self):
        return self.__repo2.get_all_dis()

    def genereaza_id(self):
        """

        :return: genereaza id random
        """
        while True:
            id_nou = random.randint(1, 100000)
            if not self.__repo2.cautare_dis(id_nou):
                return id_nou

    def genereaza_nume_random(self, lungime = 7):
        """

        :param lungime: lungimea numelui dorit
        :return: nume randomm
        """
        litere = string.ascii_lowercase
        nume = ""
        for i in range(lungime):
            nume += random.choice(litere)
        return nume.capitalize()

    def genereaza_disciplina_random(self):
        """

        :return: adauga disciplina noua cu val random
        """
        discipline = ["matematica", "informatica", "chimie", "biologie", "romana"]

        id_dis = self.genereaza_id()
        nume_dis = random.choice(discipline)
        profesor = self.genereaza_nume_random()

        disciplina = Discipline(id_dis, nume_dis, profesor)
        self.__val2.validatedis(disciplina)
        self.__repo2.adddis(disciplina)
        return disciplina

    def top_3_discipline(self):
        """

        :return: top 3 discipline care apar cel mai des
        """
        toate_disciplinele = self.__repo2.get_all_dis()
        nume_discipline = [d.get_nume_disciplina().lower() for d in toate_disciplinele]
        cat_de_des_apar = {}
        for nume in nume_discipline:
            if nume in cat_de_des_apar:
                cat_de_des_apar[nume] += 1
            else:
                cat_de_des_apar[nume] = 1
        elemente_lista = list(cat_de_des_apar.items())
        bubble_sort(elemente_lista, key=lambda item: item[1], reverse=True)
        top_discipline = elemente_lista[:3]
        return [nume for nume, frecventa in top_discipline]


class ServiceNota:
    def __init__(self, repo_note, srv_student, srv_disciplina):
        self.__repo_note = repo_note
        self.__srv_student = srv_student
        self.__srv_disciplina = srv_disciplina

    def adauga_nota(self, id_student, id_disciplina, valoare):
        """

        :param id_student: id_ul studentului de tip int, la care se doreste sa se atribuiasca nota
        :param id_disciplina: id_ul disciplinei pt care vse vrea nota
        :param valoare: valoarea notei dorite, de tip float
        :return: atribuie o nota la o disciplina unui student
        """
        if not self.__srv_student.exista_studentul_cautat(id_student):
            raise ValueError("Studentul nu exista.")
        if not self.__srv_disciplina.exista_disciplina_dorita(id_disciplina):
            raise ValueError("Disciplina nu exista. ")
        if not ( 1 <= valoare <= 10):
            raise ValueError("Nota trebuie sa fie intre 1 si 10")

        while True:
            id_nota = random.randint(1, 100000)
            if not self.__repo_note.cautare(id_nota):
                break

        nota = Nota(id_nota, id_student, id_disciplina, valoare)
        self.__repo_note.add(nota)

    def afisare_note(self):
        """

        afiseaza notele din baza de date
        """
        return self.__repo_note.get_all()


    def sortare_descrescatoare_note(self):
        """
        sorteaza descrescator notele
        """
        note = self.__repo_note.get_all()
        note_copie = note[:]
        bubble_sort(note_copie, key=lambda n: n.get_valoare(), reverse=True)
        return note_copie


class ServiceStatistica:
    def __init__(self, srv_disciplina, srv_nota, srv_student):
        self.__srv_disciplina = srv_disciplina
        self.__srv_nota = srv_nota
        self.__srv_student = srv_student

    def top_final(self):
        """

        :return: reordoneaza studentii pe baza mediei obtinute la materia cea mai frecventa
        """
        top_studenti = self.__srv_student.top_3_studenti()
        top_discipline_nume = self.__srv_disciplina.top_3_discipline()
        nume_materie_frecventa = top_discipline_nume[0]
        discipline_cu_nume = self.__srv_disciplina.afisare_discipline()
        id_uri_materie_frecventa = [
            d.get_id_dis()
            for d in discipline_cu_nume
            if d.get_nume_disciplina().lower() == nume_materie_frecventa
        ]
        rezultate_finale = []
        toate_notele = self.__srv_nota.afisare_note()
        for medie_stud in top_studenti:
            s_id = medie_stud.get_id()
            nume_complet = medie_stud.get_nume()
            numar_note_la_materia_frecventa = 0
            for nota in toate_notele:
                if nota.get_id_student() == s_id and nota.get_id_disciplina() in id_uri_materie_frecventa:
                    numar_note_la_materia_frecventa += 1

            rezultate_finale.append(
                {
                    'nume_student': nume_complet,
                    'numar_note_la_materie_top':numar_note_la_materia_frecventa,
                    'media_generala_initiala':medie_stud.get_media()
                }
            )
        bubble_sort(rezultate_finale, key=lambda x: x['numar_note_la_materie_top'], reverse=True)
        return{
                'materie_top': nume_materie_frecventa.capitalize(),
                'top_studenti': rezultate_finale
        }
#un top al disciplinelor, un top al studentilor, dupa top al acelor studenti care au cele mai multe note la aceste materii