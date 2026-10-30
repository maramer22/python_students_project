from SERVICES.service_catalog import ServiceStudenti, ServiceDiscipline, ServiceNota
from REPOS.repo_studenti import RepoStudenti, RepoDiscipline, RepoNote
from DOMAIN.validator import ValidatorStudent, ValidatorDisciplina
from DOMAIN.entities import Studenti, Discipline

def test_service_studenti():
    repo = RepoStudenti()
    val = ValidatorStudent()
    srv = ServiceStudenti(repo, val)
    srv.adauga_student(1, "Popescu", "Ion")
    srv.adauga_student(2, "Ionescu", "Andrei")
    assert len(repo._RepoStudenti__studenti) == 2
    removed = srv.sterge_student(1)
    assert removed.get_nume() == "Popescu"
    removed2 = srv.sterge_student(2)
    assert removed2.get_nume() == "Ionescu"
    assert len(repo._RepoStudenti__studenti) == 0

def test_service_discipline():
    repo = RepoDiscipline()
    val = ValidatorDisciplina()
    srv = ServiceDiscipline(repo, val)
    srv.adauga_disciplina(10, "matematica", "Pop")
    srv.adauga_disciplina(11, "informatica", "Ionescu")
    assert len(repo._RepoDiscipline__discipline) == 2
    removed = srv.sterge_disciplina(10)
    assert removed.get_nume_disciplina() == "matematica"
    removed2 = srv.sterge_disciplina(11)
    assert removed2.get_nume_disciplina() == "informatica"
    assert len(repo._RepoDiscipline__discipline) == 0


def test_setup_services():
    repo1 = RepoStudenti()
    repo2 = RepoDiscipline()
    repo_note = RepoNote()
    val1 = ValidatorStudent()
    val2 = ValidatorDisciplina()
    srv_nota = ServiceNota(repo_note, srv_student=None, srv_disciplina=None)
    srv_student = ServiceStudenti(repo1, val1, srv_nota)
    srv_disciplina = ServiceDiscipline(repo2, val2)

    srv_nota._ServiceNota__srv_student = srv_student
    srv_nota._ServiceNota__srv_disciplina = srv_disciplina

    return srv_student, srv_disciplina, srv_nota


def test_service_studenti_modificare_cautare_sortare():
    """Testează modificarea, căutarea și sortarea alfabetică a studenților."""
    srv_student = test_setup_services()
    srv_student.adauga_student(1, "Popescu", "Ion")
    srv_student.adauga_student(2, "Ionescu", "Andrei")
    srv_student.adauga_student(3, "Georgescu", "Mihai")
    s_vechi = srv_student.modifica_student(1, "Petrescu", "Alex")
    assert s_vechi.get_nume() == "Popescu"
    assert srv_student._ServiceStudenti__repo1.get_all_stud()[0].get_nume() == "Petrescu"
    assert srv_student.exista_studentul_cautat(2) is True
    assert srv_student.exista_studentul_cautat(99) is False
    studenti_sortati = srv_student.sortare_alfabetica_studenti()
    assert studenti_sortati[0].get_nume() == "Georgescu"


def test_statistica_top_20_la_suta():
    srv_student, srv_disciplina, srv_nota = setup_services()
    srv_student.adauga_student(1, "Popescu", "Ion")
    srv_student.adauga_student(2, "Ionescu", "Andrei")
    srv_student.adauga_student(3, "Georgescu", "Mihai")
    srv_student.adauga_student(4, "Petrescu", "Alex")
    srv_student.adauga_student(5, "Vasilescu", "Maria")
    srv_disciplina.adauga_disciplina(10, "matematica", "Prof1")
    srv_nota.adauga_nota(1, 10, 10.0)
    srv_nota.adauga_nota(1, 10, 9.0)
    srv_nota.adauga_nota(2, 10, 8.0)
    srv_nota.adauga_nota(3, 10, 6.0)
    srv_nota.adauga_nota(4, 10, 7.0)
    srv_nota.adauga_nota(5, 10, 8.0)

    top_studenti = srv_student.afiseaza_primii_20_la_suta()

    assert len(top_studenti) == 1
    assert top_studenti[0].get_media() == 9.5
    assert "PopescuIon" in str(top_studenti[0])

test_setup_services()
test_service_studenti()
test_service_discipline()
test_service_studenti_modificare_cautare_sortare()
test_statistica_top_20_la_suta()
