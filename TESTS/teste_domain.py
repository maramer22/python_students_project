from DOMAIN.entities import Studenti, Discipline, MedieStudent, Nota

def test_entities():
    s = Studenti(1, "Popescu", "Ion")
    assert s.get_id() == 1
    assert s.get_nume() == "Popescu"
    assert s.get_prenume() == "Ion"

    s.set_nume("Ionescu")
    s.set_prenume("Andrei")
    s.set_id(2)
    assert s.get_nume() == "Ionescu"
    assert s.get_prenume() == "Andrei"
    assert s.get_id() == 2

    d = Discipline(10, "matematica", "Pop")
    assert d.get_id_dis() == 10
    assert d.get_nume_disciplina() == "matematica"
    assert d.get_nume_prof() == "Pop"

    d.set_id_dis(11)
    d.set_nume_dis("informatica")
    d.set_nume_profesor("Ionescu")
    assert d.get_id_dis() == 11
    assert d.get_nume_disciplina() == "informatica"
    assert d.get_nume_prof() == "Ionescu"

    n = Nota(100, 2, 11, 9.5)
    assert n.get_id() == 100
    assert n.get_id_student() == 2
    assert n.get_id_disciplina() == 11
    assert n.get_valoare() == 9.5

    n.set_valoare(10.0)
    assert n.get_valoare() == 10.0
    assert str(n) == "nota cu id 100, student: 2, disciplina: 11, valoare: 10.0"

    m = MedieStudent("Ionescu Andrei", 9.8)
    assert m.get_media() == 9.8
    assert str(m) == "Student: Ionescu Andrei, Media: 9.8"

test_entities()