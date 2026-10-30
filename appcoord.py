from DOMAIN.validator import ValidatorStudent, ValidatorDisciplina
from REPOS.repo_studenti import RepoStudenti, RepoDiscipline, RepoNote, FisierStudenti, FisierNote, FisierDiscipline
from SERVICES.service_catalog import ServiceStudenti, ServiceDiscipline, ServiceNota, ServiceStatistica
from UI1.console import Console
from DOMAIN.entities import MedieStudent

repo1 = FisierStudenti("C:/Users/maram/OneDrive/Desktop/LAB7_9/date/date_studenti.txt")
repo2 = FisierDiscipline("C:/Users/maram/OneDrive/Desktop/LAB7_9/date/date_discipline.txt")
repo_note = FisierNote("C:/Users/maram/OneDrive/Desktop/LAB7_9/date/date_note.txt")
val1 = ValidatorStudent()
val2 = ValidatorDisciplina()
srv_nota = ServiceNota(repo_note, srv_student= None, srv_disciplina=None)
srv_student = ServiceStudenti(repo1, val1, srv_nota)
srv_disciplina = ServiceDiscipline(repo2, val2)
srv_statistica = ServiceStatistica(srv_disciplina, srv_nota, srv_student)
srv_nota._ServiceNota__srv_student = srv_student
srv_nota._ServiceNota__srv_disciplina = srv_disciplina

console = Console(srv_student, srv_disciplina, srv_nota, srv_statistica)
console.run()





