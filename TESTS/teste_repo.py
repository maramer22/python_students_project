from REPOS.repo_studenti import RepoStudenti, RepoDiscipline, RepoNote
from DOMAIN.entities import Studenti, Discipline, Nota

def test_repo_studenti():
    repo = RepoStudenti()
    s1 = Studenti(1, "Popescu", "Ion")
    s2 = Studenti(2, "Ionescu", "Andrei")
    repo.add(s1)
    repo.add(s2)
    removed = repo.remove(1)
    assert removed.get_nume() == "Popescu"
    removed2 = repo.remove(2)
    assert removed2.get_nume() == "Ionescu"

def test_repo_discipline():
    repo = RepoDiscipline()
    d1 = Discipline(10, "matematica", "Pop")
    d2 = Discipline(11, "informatica", "Ionescu")
    repo.adddis(d1)
    repo.adddis(d2)
    assert len(repo._RepoDiscipline__discipline) == 2
    removed = repo.removedis(10)
    assert removed.get_nume_disciplina() == "matematica"
    assert len(repo._RepoDiscipline__discipline) == 1
    removed2 = repo.removedis(11)
    assert removed2.get_nume_disciplina() == "informatica"
    assert len(repo._RepoDiscipline__discipline) == 0


def test_repo_studenti_modificare_cautare():
    repo = RepoStudenti()
    s1 = Studenti(1, "Popescu", "Ion")
    repo.add(s1)
    assert repo.cautare(1) is True
    assert repo.cautare(99) is False
    s_nou = Studenti(1, "Georgescu", "Mihai")
    s_vechi = repo.update(1, s_nou)
    assert s_vechi.get_nume() == "Popescu"
    assert repo.get_all_stud()[0].get_nume() == "Georgescu"
    try:
        repo.update(99, s_nou)
        assert False
    except ValueError as e:
        assert "Nu exista student cu id-ul 99" in str(e)


def test_repo_note():
    """Testează operațiile de adăugare, căutare și ștergere pentru note."""
    repo = RepoNote()
    n1 = Nota(100, 1, 10, 8.5)
    repo.add(n1)
    assert len(repo.get_all()) == 1
    try:
        repo.add(n1)
        assert False
    except ValueError as e:
        assert "Exista deja o nota cu acest id!" in str(e)
    assert repo.cautare(100) is True
    assert repo.cautare(99) is False
    removed = repo.remove(100)
    assert removed.get_valoare() == 8.5
    assert len(repo.get_all()) == 0
    try:
        repo.remove(100)
        assert False
    except ValueError as e:
        assert "Nu exista o nota cu acest id!" in str(e)

test_repo_studenti()
test_repo_discipline()
test_repo_note()
test_repo_studenti_modificare_cautare()