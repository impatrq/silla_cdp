class StateMachine():
    def __init__(self, firstState: tuple):
        self.__executer = {}
        self.__firstState = firstState[0]
        self.__state = firstState[0]

        self.__executer[firstState[0]] = firstState[1]

    @property
    def State(self):
        return self.__state

    @State.setter
    def State(self, state: int):
        self.__state = state

    @property
    def Executer(self):
        return self.__executer

    def change_first_state(self, new_state: tuple):
        del self.__executer[self.__firstState]
        self.__executer[new_state[0]] = new_state[1]
        self.__firstState = new_state[0]

    def add_state(self, state: tuple):
        self.__executer[state[0]] = state[1]

    def add_states(self, states: list):
        for tup in states:
            self.add_state(tup)

    def delete_state(self, state: int):
        del self.__executer[state]

    def delete_states(self, states: list):
        for state in states:
            self.delete_state(state)

    def start(self):
        self.__executer[self.__firstState]()
        self.next_state()

    def next_state(self):
        self.__executer[self.__state]()
