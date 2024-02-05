class TesteAula:
    def __init__(self):
        self.__nome_aluno = None
        self.__horario_aula = None
        self.__sala = None

    @property
    def nome_aluno(self):
        return self.__nome_aluno

    @nome_aluno.setter
    def nome_aluno(self, new_nome_aluno):
        self.__nome_aluno = new_nome_aluno

    @property
    def horario_aula(self):
        return self.__horario_aula

    @horario_aula.setter
    def horario_aula(self, new_horario_aula):
        self.__horario_aula = new_horario_aula

    @property
    def sala(self):
        return self.__sala

    @sala.setter
    def sala(self, new_sala):
        self.__sala = new_sala

    def registrar_aluno(self):
        self.nome_aluno = input('Nome do aluno: ')
        self.horario_aula = input('Horario da aula: ')
        self.sala = int(input("Numero da sala: "))

    def dados_aluno(self):
        to_string(self.nome_aluno, self.horario_aula, self.sala)


def to_string(nome, horario, sala):
    return print(f'Nome aulo: {nome}\nHorario da aula: {horario}\nNumero da sala de aula: {sala}')


def init_app():
    t = TesteAula()
    t.registrar_aluno()
    t.dados_aluno()


if __name__ == '__main__':
    init_app()
