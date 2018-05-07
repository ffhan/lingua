from automata import fa


class NFA(fa.FiniteAutomaton):
    '''
    Non-deterministic finite automata.
    '''

    def _check_structure(self):
        #does nothing.
        pass

    def _access(self, value):

        if value not in self.inputs:
            raise ValueError(self._input_error(value))

        # print(value, self.current)

        old_currents = set()

        # print(value)
        for state in sorted(list(self.current)):
            res = state.forward(value)

            # print(state, res)

            # print(state, state._transitions)

            for end in res:
                old_currents.add(self.states[self._get_alias(end.name)])
                # print(end, old_currents)
        # print(old_currents)
        # print("-" * 20)
        self.current = old_currents

class EPSILON_NFA(NFA):

    def __init__(self, states, inputs, start_state, epsilon = '$'):

        inputs.add(epsilon)
        self._epsilon = epsilon

        super().__init__(states, inputs, start_state)

    def _e_closure(self, state, closure = set()):
        if state not in self:
            raise ValueError(self._input_error(state))

        if type(state) is str:
            closure -= {state}
            state = self.states[state]
        closure |= {state}

        for eps in state.forward(self._epsilon):
            if eps not in closure:
                self._e_closure(eps, closure)

        return closure

    def _e_closures(self, *states):
        currents = set(states) if type(states) is not set else states

        for i in states:
            currents |= self._e_closure(i, currents)

        return currents

    def _all_closures(self):

        return self._e_closures(*self.current)

    def _access(self, value):

        super()._access(value)

        self.current = self._all_closures()

    def _process(self, *entry):

        self.current = self._all_closures()

        return super()._process(*entry)


