from DOMAIN.entities import Studenti, Discipline, Nota

class RepoStudenti():

    def __init__(self):
        self.__studenti = {}

    def get_student_by_id(self, id_stud: int):
        return self.__studenti.get(id_stud)

    def add(self, student: Studenti):
        """
        adauga datele unui student
        :param student: studentul de adaugat
        :return: studentul a fost adaugat
        """
        if student.get_id() in self.__studenti:
            raise ValueError("Exista deja un student cu acest id!")
        self.__studenti[student.get_id()] = student


    def remove(self, id_stud: int):
        """

        Sterge studentul cu un id dat
        :param id_stud:  id-ul studentului de sters
        :return: studentul sters

        """
        if not id_stud in self.__studenti:
            raise ValueError(f"Nu exista student cu id-ul {id_stud}")
        student_sters = self.__studenti[id_stud]
        del self.__studenti[id_stud]
        return student_sters

    def update(self, id_stud: int, student_nou: Studenti):
        """
        pt a modifica un student din lista
        :param id_stud: id-ul studentului a carui date se doresc a fi modificate
        :param student_nou: studentul nou
        :return: datele modificate ale studentului dorit
        """
        if id_stud not in self.__studenti:
            raise ValueError(f"Nu exista student cu id-ul {id_stud}")
        student_vechi = self.__studenti[id_stud]
        self.__studenti[id_stud] = student_nou
        return student_vechi

    def cautare(self, id_stud: int):
        """
        pt a cauta un student dupa id
        :param id_stud: id_ul studentului care se doreste a fi cautat
        :return: true sau false, daca se gaseste studentul dorit sau nu
        """
        return id_stud in self.__studenti

    def cautare_recursiva(self, lista_studenti, id_stud: int):
        """
        cauta recursiv sa vada daca un student exista sau nu
        """
        if len(lista_studenti) == 0:
            return False
        student_curent = lista_studenti[0]

        if student_curent.get_id() == id_stud:
            return True

        return self.cautare_recursiva(lista_studenti[1:], id_stud)

    def get_all_stud(self):
        """

        :return: toti studentii existenti
        """
        return list(self.__studenti.values())



class RepoDiscipline():
    def __init__(self):
        self.__discipline = {}

    def adddis(self, disciplina: Discipline):
        """
        adauga datele unei discipline
        :param disciplina: disiplina care se doreste a fi adaugata
        :return: disciplina adaugata
        """
        if disciplina.get_id_dis() in self.__discipline:
            raise ValueError("Exista deja o disciplina cu acest id!")
        self.__discipline[disciplina.get_id_dis()] = disciplina

    def removedis(self, id_dis:int):
        """
        sterge disciplina cu un id dat
        :param id_dis: id-ul disciplinei care sa doreste a fi stearsa
        :return: disciplina stearsa
        """
        if not id_dis in self.__discipline:
            raise ValueError("Nu exista o disciplina cu acest id")
        disciplina_sters = self.__discipline[id_dis]
        del self.__discipline[id_dis]
        return disciplina_sters

    def updatedis(self, id_dis: int, disciplina_noua: Discipline):
        """

        :param id_dis: id_ul disciplinei care se doreste a fi modificata, de tip int
        :param disciplina_noua: disciplina modificata, de tip Disciplina
        :return: disciplina modificata
        """
        if id_dis not in self.__discipline:
            raise ValueError(f"Nu exista disciplina cu id-ul {id_dis}")
        disciplina_veche = self.__discipline[id_dis]
        self.__discipline[id_dis] = disciplina_noua
        return disciplina_veche

    def cautare_dis(self, id_cautat):
        """
        pt cautarea unei anumite discipline dupa id
        :param id_cautat: id_ul disciplinei care se doreste a fi cautata
        :return: daca se gaseste sau nu disciplina respectiva
        """
        return id_cautat in self.__discipline

    def get_all_dis(self):
        """

        :return: toate disciplinele existente
        """
        return list(self.__discipline.values())


class RepoNote:
    def __init__(self):
        self.__note = {}

    def add(self, nota:Nota):
        """

        :param nota: nota, de tip Nota
        :return:
        """
        if nota.get_id() in self.__note:
            raise ValueError("Exista deja o nota cu acest id!")
        self.__note[nota.get_id()] = nota

    def remove(self, id_nota: int):
        """

        :param id_nota:id-ul notei care se doreste a fi stearsa
        :return: nota stearsa din baza de date
        """
        if id_nota not in self.__note:
            raise ValueError("Nu exista o nota cu acest id!")
        nota = self.__note[id_nota]
        del self.__note[id_nota]
        return nota

    def cautare(self, id_nota: int):
        """

        :param id_nota: id_ul notei care se doreste a fi cautata, de tip int
        :return:
        """
        return id_nota in self.__note

    def get_all(self):
        """

        :return: lista cu toate notele
        """
        return list(self.__note.values())

class FisierStudenti(RepoStudenti):
    def __init__(self, fisier):
        super().__init__()
        self.__fisier = fisier
        self.__citeste_fisier()
    def __citeste_fisier(self):
        try:
            with open(self.__fisier, 'r') as f:

                for l in f:
                    l = l.strip()
                    if l:
                        impartire = l.split(';')
                        if len(impartire) == 3:
                            try:
                                id_student = int(impartire[0])
                                nume_student = (impartire[1])
                                prenume_student = impartire[2]
                                student = Studenti(id_student, nume_student, prenume_student)
                                super().add(student)
                            except ValueError as e:
                                print(f"Eroare la citirea studentului din fisier (ID duplicat sau invalid): {e}")
                                pass
        except FileNotFoundError:
            pass

    def __scrie_stud_fisier(self):
        with open(self.__fisier, 'w') as f: # w pt modul scriere
            for student in super().get_all_stud():
                f.write(f"{student.get_id()};{student.get_nume()};{student.get_prenume()}\n")

    def add(self, student: Studenti):
        super().add(student)
        self.__scrie_stud_fisier()

    def remove(self, id_stud:int):
        student_sters = super().remove(id_stud)
        self.__scrie_stud_fisier()
        #suprascrie in fisier
        return student_sters

    def update(self, id_stud: int, student_nou: Studenti):
        student_vechi = super().update(id_stud, student_nou)
        self.__scrie_stud_fisier()
        return student_vechi

class FisierDiscipline(RepoDiscipline):
    def __init__(self, fisier):
        super().__init__()
        self.__fisier = fisier
        self.__citeste_fisier()

    def __citeste_fisier(self):
        try:
            with open(self.__fisier, 'r') as f:
                for l in f:
                    l = l.strip()
                    if l:
                        impartire = l.split(';')
                        if len(impartire) == 3:
                            id_dis = int(impartire[0])
                            nume_dis = impartire[1]
                            nume_prof = impartire[2]
                            disciplina = Discipline(id_dis, nume_dis, nume_prof)
                            super().adddis(disciplina)

        except FileNotFoundError:
            pass


    def __scrie_dis_fisier(self):
         with open(self.__fisier, 'w') as f:
            for disciplina in super().get_all_dis():
                f.write(f"{disciplina.get_id_dis()};{disciplina.get_nume_disciplina()};{disciplina.get_nume_prof()}\n")


    def adddis(self, disciplina: Discipline):
        super().adddis(disciplina)
        self.__scrie_dis_fisier()


    def removedis(self, id_dis: int):
        disciplina_stearsa = super().removedis(id_dis)
        self.__scrie_dis_fisier()
        return disciplina_stearsa


    def updatedis(self, id_dis: int, disciplina_noua: Discipline):
        disciplina_veche = super().updatedis(id_dis, disciplina_noua)
        self.__scrie_dis_fisier()
        return disciplina_veche


class FisierNote(RepoNote):
    def __init__(self, fisier):
        super().__init__()
        self.__fisier = fisier
        self.__citeste_fisier()

    def __citeste_fisier(self):
        try:
            with open(self.__fisier, 'r') as f:
                for l in f:
                    l = l.strip()
                    if l:
                        impartire = l.split(';')
                        if len(impartire) == 4:
                            id_nota = int(impartire[0])
                            id_student = int(impartire[1])
                            id_disciplina = int(impartire[2])
                            valoare = float(impartire[3])
                            nota = Nota(id_nota, id_student, id_disciplina, valoare)
                            super().add(nota)
        except FileNotFoundError:
            pass

    def __scrie_note_fisier(self):
        with open(self.__fisier, 'w') as f:
            for nota in super().get_all():
                f.write(f"{nota.get_id()};{nota.get_id_student()};{nota.get_id_disciplina()};{nota.get_valoare()}\n")

    def add(self, nota: Nota):
        super().add(nota)
        self.__scrie_note_fisier()

    def remove(self, id_nota: int):
        nota_stearsa = super().remove(id_nota)
        self.__scrie_note_fisier()
        return nota_stearsa












