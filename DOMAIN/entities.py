class Studenti:
    def __init__(self, id_student: int, nume_student: str, prenume_student: str):
        self.__id = id_student
        self.__nume_student = nume_student
        self.__prenume_student = prenume_student

    def get_id(self):
        return self.__id

    def get_nume(self):
        return self.__nume_student

    def get_prenume(self):
        return self.__prenume_student

    def set_nume(self, nume_nou):
        self.__nume_student = nume_nou

    def set_prenume(self, prenume_nou):
        self.__prenume_student = prenume_nou

    def set_id(self, id_nou):
        self.__id = id_nou


    def __str__(self):
        return f"Id.student #{self.__id} Nume = {self.__nume_student} Prenume = {self.__prenume_student}"


class Discipline:
    def __init__(self, id_disciplina: int, nume_disciplina: str, nume_prof: str):
        self.__id_dis = id_disciplina
        self.__nume_dis = nume_disciplina
        self.__nume_profesor = nume_prof

    def get_id_dis(self):
        return self.__id_dis

    def get_nume_disciplina(self):
        return self.__nume_dis

    def get_nume_prof(self):
        return self.__nume_profesor

    def set_id_dis(self, id_dis_nou):
        self.__id_dis = id_dis_nou

    def set_nume_dis(self, nume_dis_nou):
        self.__nume_dis = nume_dis_nou

    def set_nume_profesor(self, nume_prof_nou):
        self.__nume_profesor = nume_prof_nou

    def __str__(self):
        return f"Id.disciplina {self.__id_dis} Nume disciplina = {self.__nume_dis} Nume profesor = {self.__nume_profesor}"


class Nota:
    def __init__(self, id_nota: int, id_student: int, id_disciplina: int, valoare:float):
        self.__id = id_nota
        self.__id_student = id_student
        self.__id_disciplina = id_disciplina
        self.__valoare = valoare

    def get_id(self):
        return self.__id
    def get_id_student(self):
        return self.__id_student
    def get_id_disciplina(self):
        return self.__id_disciplina
    def get_valoare(self):
        return self.__valoare

    def set_valoare(self, valoare_noua:float):
        self.__valoare = valoare_noua

    def __str__(self):
        return f"nota cu id {self.__id}, student: {self.__id_student}, disciplina: {self.__id_disciplina}, valoare: {self.__valoare}"


class MedieStudent():
    def __init__(self,id_student:int, nume, media):
        self.__nume = nume
        self.__media = media
        self.__id = id_student
    def get_id(self):
        return self.__id

    def get_nume(self):
        return self.__nume

    def get_media(self):
        return self.__media

    def __str__(self):
        return f"Student: {self.__nume}, Media: {self.__media}"

