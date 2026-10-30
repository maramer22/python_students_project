import unittest
import os
from DOMAIN.entities import Studenti, Discipline, Nota, MedieStudent
from DOMAIN.validator import ValidatorStudent, ValidatorDisciplina
from REPOS.repo_studenti import RepoStudenti, RepoDiscipline, RepoNote, FisierStudenti, FisierDiscipline, FisierNote
from SERVICES.service_catalog import ServiceStudenti, ServiceDiscipline, ServiceNota, ServiceStatistica


class TestDomain(unittest.TestCase):

    def test_student(self):
        s = Studenti(1, "Popescu", "Ion")
        self.assertEqual(s.get_id(), 1)
        self.assertEqual(s.get_nume(), "Popescu")
        self.assertEqual(s.get_prenume(), "Ion")
        s.set_nume("Ionescu")
        self.assertEqual(s.get_nume(), "Ionescu")
        self.assertEqual(str(s), "Id.student #1 Nume = Ionescu Prenume = Ion")

    def test_disciplina(self):
        d = Discipline(10, "matematica", "Popescu")
        self.assertEqual(d.get_id_dis(), 10)
        self.assertEqual(d.get_nume_disciplina(), "matematica")
        self.assertEqual(d.get_nume_prof(), "Popescu")
        d.set_nume_dis("informatica")
        self.assertEqual(d.get_nume_disciplina(), "informatica")

    def test_nota(self):
        n = Nota(1, 101, 10, 9.5)
        self.assertEqual(n.get_id(), 1)
        self.assertEqual(n.get_id_student(), 101)
        self.assertEqual(n.get_id_disciplina(), 10)
        self.assertEqual(n.get_valoare(), 9.5)
        n.set_valoare(8.0)
        self.assertEqual(n.get_valoare(), 8.0)

    def test_medie_student(self):
        m = MedieStudent(1, "Popescu Ion", 9.25)
        self.assertEqual(m.get_id(), 1)
        self.assertEqual(m.get_nume(), "Popescu Ion")
        self.assertEqual(m.get_media(), 9.25)


class TestRepositoryStudenti(unittest.TestCase):

    def setUp(self):
        self.repo = RepoStudenti()

    def test_add_student(self):
        s = Studenti(1, "Popescu", "Ion")
        self.repo.add(s)
        self.assertEqual(len(self.repo.get_all_stud()), 1)
        self.assertTrue(self.repo.cautare(1))

    def test_add_student_duplicat(self):
        s1 = Studenti(1, "Popescu", "Ion")
        s2 = Studenti(1, "Ionescu", "Maria")
        self.repo.add(s1)
        with self.assertRaises(ValueError):
            self.repo.add(s2)

    def test_remove_student(self):
        s = Studenti(1, "Popescu", "Ion")
        self.repo.add(s)
        student_sters = self.repo.remove(1)
        self.assertEqual(student_sters.get_nume(), "Popescu")
        self.assertEqual(len(self.repo.get_all_stud()), 0)
        self.assertFalse(self.repo.cautare(1))

    def test_remove_student_inexistent(self):
        with self.assertRaises(ValueError):
            self.repo.remove(999)

    def test_update_student(self):
        s_vechi = Studenti(1, "Popescu", "Ion")
        s_nou = Studenti(1, "Ionescu", "Maria")
        self.repo.add(s_vechi)
        student_returnat = self.repo.update(1, s_nou)
        self.assertEqual(student_returnat.get_nume(), "Popescu")
        self.assertEqual(self.repo.get_student_by_id(1).get_nume(), "Ionescu")

    def test_cautare_student(self):
        s = Studenti(1, "Popescu", "Ion")
        self.repo.add(s)
        self.assertTrue(self.repo.cautare(1))
        self.assertFalse(self.repo.cautare(999))


class TestRepositoryDiscipline(unittest.TestCase):

    def setUp(self):
        self.repo = RepoDiscipline()

    def test_add_disciplina(self):
        d = Discipline(10, "matematica", "Popescu")
        self.repo.adddis(d)
        self.assertEqual(len(self.repo.get_all_dis()), 1)
        self.assertTrue(self.repo.cautare_dis(10))

    def test_add_disciplina_duplicata(self):
        d1 = Discipline(10, "matematica", "Popescu")
        d2 = Discipline(10, "informatica", "Ionescu")
        self.repo.adddis(d1)
        with self.assertRaises(ValueError):
            self.repo.adddis(d2)

    def test_remove_disciplina(self):
        d = Discipline(10, "matematica", "Popescu")
        self.repo.adddis(d)
        disciplina_stearsa = self.repo.removedis(10)
        self.assertEqual(disciplina_stearsa.get_nume_disciplina(), "matematica")
        self.assertEqual(len(self.repo.get_all_dis()), 0)

    def test_update_disciplina(self):
        d_veche = Discipline(10, "matematica", "Popescu")
        d_noua = Discipline(10, "informatica", "Ionescu")
        self.repo.adddis(d_veche)
        disciplina_returnata = self.repo.updatedis(10, d_noua)
        self.assertEqual(disciplina_returnata.get_nume_disciplina(), "matematica")
        self.assertEqual(self.repo.get_all_dis()[0].get_nume_disciplina(), "informatica")


class TestServiceStudenti(unittest.TestCase):

    def setUp(self):
        self.repo = RepoStudenti()
        self.validator = ValidatorStudent()
        self.srv_nota = ServiceNota(RepoNote(), None, None)
        self.srv = ServiceStudenti(self.repo, self.validator, self.srv_nota)

    def test_adauga_student_white_box(self):
        self.srv.adauga_student(1, "Popescu", "Ion")
        self.assertEqual(len(self.srv.afisare_student()), 1)

        with self.assertRaises(ValueError):
            self.srv.adauga_student(1, "Ionescu", "Maria")

    def test_sterge_student(self):
        self.srv.adauga_student(1, "Popescu", "Ion")
        student_sters = self.srv.sterge_student(1)
        self.assertEqual(student_sters.get_nume(), "Popescu")
        self.assertEqual(len(self.srv.afisare_student()), 0)

        with self.assertRaises(ValueError):
            self.srv.sterge_student(999)

    def test_modifica_student(self):
        self.srv.adauga_student(1, "Popescu", "Ion")
        s_vechi = self.srv.modifica_student(1, "Ionescu", "Maria")
        self.assertEqual(s_vechi.get_nume(), "Popescu")
        self.assertEqual(self.repo.get_student_by_id(1).get_nume(), "Ionescu")


        with self.assertRaises(ValueError):
            self.srv.modifica_student(999, "Test", "Test")

    def test_sortare_alfabetica(self):
        self.srv.adauga_student(1, "Popescu", "Ion")
        self.srv.adauga_student(2, "Ionescu", "Maria")
        self.srv.adauga_student(3, "Georgescu", "Alex")

        studenti_sortati = self.srv.sortare_alfabetica_studenti()
        self.assertEqual(studenti_sortati[0].get_nume(), "Georgescu")
        self.assertEqual(studenti_sortati[1].get_nume(), "Ionescu")
        self.assertEqual(studenti_sortati[2].get_nume(), "Popescu")

    def test_generare_random(self):
        student = self.srv.genereaza_student()
        self.assertEqual(len(self.srv.afisare_student()), 1)
        self.assertIsNotNone(student.get_id())
        self.assertTrue(len(student.get_nume()) > 0)
        self.assertTrue(student.get_nume()[0].isupper())


class TestServiceDiscipline(unittest.TestCase):

    def setUp(self):
        self.repo = RepoDiscipline()
        self.validator = ValidatorDisciplina()
        self.srv = ServiceDiscipline(self.repo, self.validator)

    def test_adauga_disciplina_white_box(self):
        self.srv.adauga_disciplina(10, "matematica", "Popescu")
        self.assertEqual(len(self.srv.afisare_discipline()), 1)

        with self.assertRaises(ValueError):
            self.srv.adauga_disciplina(11, "fizica", "Ionescu")

        with self.assertRaises(ValueError):
            self.srv.adauga_disciplina(10, "informatica", "Test")

    def test_sterge_disciplina(self):
        self.srv.adauga_disciplina(10, "matematica", "Popescu")
        disciplina_stearsa = self.srv.sterge_disciplina(10)
        self.assertEqual(disciplina_stearsa.get_nume_disciplina(), "matematica")
        self.assertEqual(len(self.srv.afisare_discipline()), 0)

        with self.assertRaises(ValueError):
            self.srv.sterge_disciplina(999)

    def test_modifica_disciplina(self):
        self.srv.adauga_disciplina(10, "matematica", "Popescu")
        d_veche = self.srv.modifica_disciplina(10, "informatica", "Ionescu")
        self.assertEqual(d_veche.get_nume_disciplina(), "matematica")
        self.assertEqual(self.repo.get_all_dis()[0].get_nume_disciplina(), "informatica")

    def test_generare_random(self):
        disciplina = self.srv.genereaza_disciplina_random()
        self.assertEqual(len(self.srv.afisare_discipline()), 1)
        discipline_valide = ["matematica", "informatica", "chimie", "biologie", "romana"]
        self.assertIn(disciplina.get_nume_disciplina(), discipline_valide)

    def test_top_3_discipline(self):
        self.srv.adauga_disciplina(10, "matematica", "Prof1")
        self.srv.adauga_disciplina(11, "matematica", "Prof2")
        self.srv.adauga_disciplina(12, "informatica", "Prof3")
        self.srv.adauga_disciplina(13, "informatica", "Prof4")
        self.srv.adauga_disciplina(14, "chimie", "Prof5")

        top = self.srv.top_3_discipline()
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0], "matematica")
        self.assertEqual(top[1], "informatica")


class TestServiceNote(unittest.TestCase):

    def setUp(self):
        self.repo_stud = RepoStudenti()
        self.repo_dis = RepoDiscipline()
        self.repo_note = RepoNote()

        self.repo_stud.add(Studenti(1, "Popescu", "Ion"))
        self.repo_dis.adddis(Discipline(10, "matematica", "Prof"))

        self.srv_stud = ServiceStudenti(self.repo_stud, ValidatorStudent(), None)
        self.srv_dis = ServiceDiscipline(self.repo_dis, ValidatorDisciplina())
        self.srv = ServiceNota(self.repo_note, self.srv_stud, self.srv_dis)

    def test_adauga_nota_white_box(self):
        self.srv.adauga_nota(1, 10, 9.5)
        self.assertEqual(len(self.srv.afisare_note()), 1)

        with self.assertRaises(ValueError):
            self.srv.adauga_nota(999, 10, 8.0)

        with self.assertRaises(ValueError):
            self.srv.adauga_nota(1, 999, 8.0)

        with self.assertRaises(ValueError):
            self.srv.adauga_nota(1, 10, 0.5)

        with self.assertRaises(ValueError):
            self.srv.adauga_nota(1, 10, 11.0)

    def test_sortare_descrescatoare(self):
        self.srv.adauga_nota(1, 10, 7.0)
        self.srv.adauga_nota(1, 10, 10.0)
        self.srv.adauga_nota(1, 10, 8.5)

        note_sortate = self.srv.sortare_descrescatoare_note()
        self.assertEqual(note_sortate[0].get_valoare(), 10.0)
        self.assertEqual(note_sortate[1].get_valoare(), 8.5)
        self.assertEqual(note_sortate[2].get_valoare(), 7.0)


class TestStatistici(unittest.TestCase):

    def setUp(self):
        self.repo_stud = RepoStudenti()
        self.repo_dis = RepoDiscipline()
        self.repo_note = RepoNote()

        self.repo_stud.add(Studenti(1, "Popescu", "Ion"))
        self.repo_stud.add(Studenti(2, "Ionescu", "Maria"))
        self.repo_stud.add(Studenti(3, "Georgescu", "Alex"))
        self.repo_stud.add(Studenti(4, "Vasilescu", "Dan"))
        self.repo_stud.add(Studenti(5, "Marinescu", "Ana"))

        self.repo_dis.adddis(Discipline(10, "matematica", "Prof1"))
        self.repo_dis.adddis(Discipline(11, "matematica", "Prof2"))
        self.repo_dis.adddis(Discipline(12, "informatica", "Prof3"))

        self.srv_stud = ServiceStudenti(self.repo_stud, ValidatorStudent(), None)
        self.srv_dis = ServiceDiscipline(self.repo_dis, ValidatorDisciplina())
        self.srv_nota = ServiceNota(self.repo_note, self.srv_stud, self.srv_dis)

        self.srv_stud._ServiceStudenti__srv_nota = self.srv_nota

        self.srv_nota.adauga_nota(1, 10, 10.0)
        self.srv_nota.adauga_nota(1, 11, 9.0)
        self.srv_nota.adauga_nota(2, 10, 8.0)
        self.srv_nota.adauga_nota(3, 12, 7.0)

        self.srv_statistica = ServiceStatistica(self.srv_dis, self.srv_nota, self.srv_stud)

    def test_top_3_studenti(self):
        top = self.srv_stud.top_3_studenti()
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].get_id(), 1)
        self.assertGreaterEqual(top[0].get_media(), top[1].get_media())
        self.assertGreaterEqual(top[1].get_media(), top[2].get_media())

    def test_primii_20_la_suta(self):
        rezultat = self.srv_stud.afiseaza_primii_20_la_suta()
        if len(rezultat) > 1:
            self.assertGreaterEqual(rezultat[0].get_media(), rezultat[1].get_media())

    def test_top_final(self):
        rezultat = self.srv_statistica.top_final()
        self.assertEqual(rezultat['materie_top'], "Matematica")
        top_studenti = rezultat['top_studenti']
        self.assertEqual(len(top_studenti), 3)
        self.assertEqual(top_studenti[0]['nume_student'], "Popescu Ion")
        self.assertEqual(top_studenti[0]['numar_note_la_materie_top'], 2)


class TestFisierStudenti(unittest.TestCase):

    def setUp(self):
        self.filename = "test_studenti_temp.txt"
        if os.path.exists(self.filename):
            os.remove(self.filename)
        with open(self.filename, "w") as f:
            f.write("")
        self.repo = FisierStudenti(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_si_citire_fisier(self):
        s = Studenti(1, "Popescu", "Ion")
        self.repo.add(s)
        self.assertEqual(len(self.repo.get_all_stud()), 1)

        with open(self.filename, "r") as f:
            continut = f.read()
            self.assertIn("1", continut)
            self.assertIn("Popescu", continut)

    def test_persistenta_date(self):
        s1 = Studenti(1, "Popescu", "Ion")
        self.repo.add(s1)

        repo2 = FisierStudenti(self.filename)
        self.assertEqual(len(repo2.get_all_stud()), 1)
        self.assertEqual(repo2.get_student_by_id(1).get_nume(), "Popescu")

    def test_remove_si_scriere(self):
        s1 = Studenti(1, "Popescu", "Ion")
        s2 = Studenti(2, "Ionescu", "Maria")
        self.repo.add(s1)
        self.repo.add(s2)

        self.repo.remove(1)
        self.assertEqual(len(self.repo.get_all_stud()), 1)

        repo2 = FisierStudenti(self.filename)
        self.assertEqual(len(repo2.get_all_stud()), 1)
        self.assertFalse(repo2.cautare(1))
        self.assertTrue(repo2.cautare(2))


class TestFisierDiscipline(unittest.TestCase):

    def setUp(self):
        self.filename = "test_discipline_temp.txt"
        if os.path.exists(self.filename):
            os.remove(self.filename)
        with open(self.filename, "w") as f:
            f.write("")
        self.repo = FisierDiscipline(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_si_persistenta(self):
        d = Discipline(10, "matematica", "Popescu")
        self.repo.adddis(d)
        self.assertEqual(len(self.repo.get_all_dis()), 1)

        repo2 = FisierDiscipline(self.filename)
        self.assertEqual(len(repo2.get_all_dis()), 1)
        self.assertEqual(repo2.get_all_dis()[0].get_nume_disciplina(), "matematica")


class TestFisierNote(unittest.TestCase):

    def setUp(self):
        self.filename = "test_note_temp.txt"
        if os.path.exists(self.filename):
            os.remove(self.filename)
        with open(self.filename, "w") as f:
            f.write("")
        self.repo = FisierNote(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_si_persistenta(self):
        n = Nota(1, 101, 10, 9.5)
        self.repo.add(n)
        self.assertEqual(len(self.repo.get_all()), 1)

        repo2 = FisierNote(self.filename)
        self.assertEqual(len(repo2.get_all()), 1)
        self.assertEqual(repo2.get_all()[0].get_valoare(), 9.5)


if __name__ == '__main__':
    unittest.main()