class ValidatorStudent:
    def validate(self, s):
        """

        :param s: studentul la care se face referire, de tip Student
        :return: verifica daca datele introduse pentrun un student sunt valide
        """
        errors = []


        if s.get_nume() == "":
            errors.append("Numele nu poate fi vid")
        elif not s.get_nume()[0].isupper():
            raise ValueError("Numele trebuie sa inceapa cu litera mare")
        if s.get_prenume() == "":
            errors.append("Prenumele nu poate fi vid")
        elif not s.get_prenume()[0].isupper():
            raise ValueError("Prenumele trebuie sa inceapa cu litera mare")
        if not s.get_nume()[0].isupper():
            raise ValueError("Numele trebuie să inceapă cu litera mare")
        if not s.get_prenume()[0].isupper():
            raise ValueError("Prenumele trebuie să înceapă cu literă mare")
        if len(errors) > 0:
            raise ValueError('\n'.join(errors))

class ValidatorDisciplina:
    def validatedis(self, d):
        """

        :param d: disciplina la care se face referire, de tip Disciplina
        :return: verifica daca datele introduse pentru o disciplina sunt ok
        """
        errors = []

        if d.get_nume_disciplina() == "":
            errors.append("Numele nu poate fi vid")
        if d.get_nume_prof() == "":
            errors.append("Prenumele nu poate fi vid")
        if not d.get_nume_prof()[0].isupper():
            raise ValueError("Numele trebuie să inceapă cu litera mare")
        if d.get_nume_disciplina() not in ['matematica', 'informatica', 'chimie', 'biologie', 'romana']:
            errors.append("Disciplina trebuie sa fie una dintre matematica, informatica, chimie, biologie sau romana")
        if len(errors) > 0:
            raise ValueError('\n'.join(errors)) #ca sa ridice problemele din value error

class ValidatorNota:
    def validatornota(self, nota):

        """

        :param nota: nota la care se face referire
        :return: verifica daca datele introduse pentru nota sunt ok
        """
        errors = []
        try:
            valo = float(nota.get_valoare())
        except:
            errors.append("Nota trebuie sa fie un numar!")
            raise ValueError('\n'.join(errors))
        if valo < 1 or valo >10:
            errors.append("Nota trebuie sa fie intre 1 si 10")
        if len(errors) > 0:
            raise ValueError('\n'.join(errors))