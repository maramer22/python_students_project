import unittest
from SERVICES.service_catalog import ServiceStudenti, ServiceDiscipline, ServiceNota, ServiceStatistica
from REPOS.repo_studenti import RepoStudenti, RepoDiscipline, RepoNote
from DOMAIN.validator import ValidatorStudent, ValidatorDisciplina
from DOMAIN.entities import Studenti, Discipline, Nota, MedieStudent


class TesteServiceCatalog(unittest.TestCase):

    def setUp(self):
        """

        :return: seteaza ce avem nevoie pt fiecare test
        """
        self.repo1 = RepoStudenti()
        self.repo2 = RepoDiscipline()
        self.repo_note = RepoNote()

        self.val1 = ValidatorStudent()
        self.val2 = ValidatorDisciplina()

        self.srv_nota = ServiceNota(self.repo_note, srv_student=None, srv_disciplina=None)
        self.srv_student = ServiceStudenti(self.repo1, self.val1, self.srv_nota)
        self.srv_disciplina = ServiceDiscipline(self.repo2, self.val2)

        self.srv_nota._ServiceNota__srv_student = self.srv_student
        self.srv_nota._ServiceNota__srv_disciplina = self.srv_disciplina

        self.srv_statistica = ServiceStatistica(self.srv_disciplina, self.srv_nota, self.srv_student)

    def test_service_studenti_crud(self):
        """

        :return: testeaza adaugare si stergerestudenti pt service
        """
        self.srv_student.adauga_student(1, "Popescu", "Ion")
        self.srv_student.adauga_student(2, "Ionescu", "Andrei")

        self.assertEqual(len(self.repo1.get_all_stud()), 2)
        removed = self.srv_student.sterge_student(1)
        self.assertEqual(removed.get_nume(), "Popescu")
        self.assertRaisesRegex(ValueError, "Numele trebuie să inceapă cu litera mare", self.srv_student.adauga_student, 3, "popescu", "Mihai")


    def test_service_discipline_crud(self):
        """

        :return: pt testarea la nivel de service a disciplinelor (adaugare/stergere)
        """
        self.srv_disciplina.adauga_disciplina(10, "matematica", "Pop")
        self.srv_disciplina.adauga_disciplina(11, "informatica", "Ionescu")

        self.assertEqual(len(self.repo2.get_all_dis()), 2)

        removed = self.srv_disciplina.sterge_disciplina(10)
        self.assertEqual(removed.get_nume_disciplina(), "matematica")

        self.assertRaisesRegex(ValueError, "Disciplina trebuie sa fie una dintre", self.srv_disciplina.adauga_disciplina, 12, "fizica", "NumeProf")

    def test_service_studenti_modificare_sortare(self):
        """

        :return: teste la modificarea si sortarea studentilor

        """
        self.srv_student.adauga_student(1, "Popescu", "Ion")
        self.srv_student.adauga_student(2, "Ionescu", "Andrei")
        self.srv_student.adauga_student(3, "Georgescu", "Mihai")

        s_vechi = self.srv_student.modifica_student(1, "Petrescu", "Alex")
        self.assertEqual(s_vechi.get_nume(), "Popescu")
        self.assertEqual(self.repo1.get_all_stud()[0].get_nume(), "Petrescu")

        studenti_sortati = self.srv_student.sortare_alfabetica_studenti()
        self.assertEqual(studenti_sortati[0].get_nume(), "Georgescu")

    def test_statistica_top_3_si_final(self):
        """

        :return: testeaza topuri/statistici daca sunt ok
        """

        self.srv_student.adauga_student(1, "Popescu", "Ion")
        self.srv_student.adauga_student(2, "Ionescu", "Andrei")
        self.srv_student.adauga_student(3, "Georgescu", "Mihai")
        self.srv_student.adauga_student(4, "Petrescu", "Alex")

        self.srv_disciplina.adauga_disciplina(10, "matematica", "Prof1")
        self.srv_disciplina.adauga_disciplina(11, "matematica", "Prof2")
        self.srv_disciplina.adauga_disciplina(12, "informatica", "Prof3")

        self.srv_nota.adauga_nota(1, 10, 10.0)
        self.srv_nota.adauga_nota(1, 11, 9.0)
        self.srv_nota.adauga_nota(2, 10, 8.0)
        self.srv_nota.adauga_nota(3, 11, 7.0)
        self.srv_nota.adauga_nota(3, 12, 8.0)

        self.srv_nota.adauga_nota(4, 12, 7.0)

        top_medie = self.srv_student.top_3_studenti()
        self.assertEqual(len(top_medie), 3)
        self.assertEqual(top_medie[0].get_id(), 1)
        self.assertEqual(top_medie[1].get_id(), 2)

        top_dis = self.srv_disciplina.top_3_discipline()
        self.assertEqual(top_dis[0], "matematica")

        top_final = self.srv_statistica.top_final()
        top_final_list = top_final['top_studenti']
        self.assertEqual(top_final['materie_top'], "Matematica")

        self.assertEqual(top_final_list[0]['nume_student'], "Popescu Ion")
        self.assertEqual(top_final_list[0]['numar_note_la_materie_top'], 2)

        self.assertEqual(len(top_final_list), 3)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()