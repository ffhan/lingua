import automata.dfa as dfa
import automata.state as st
import automata.packs as pk
import copy

class DeterministicPDA(dfa.DFA): # the correct implementation would be to inherit from abstract PA.

    def __init__(self, text, parser, empty_symbol = '$'):

        super().__init__(text, parser)

        self.start_symbol = parser.start_stack
        self.stack = pk.Stack(self.start_symbol)

        self.stack_alphabet = parser.stack_alphabet

        self.inputs.add(empty_symbol)
        self.empty_symbol = empty_symbol

        self.failed_state = st.PushState('fail', 0, epsilon = empty_symbol)
        self.processed_all = True

    def _check_structure(self):
        pass #not checking anything. should be checking if every symbol, input and state is registered within pda.

    @property
    def accepted(self):
        if self.processed_all:
            return self.current in self.accepted_states
        return False

    def reset(self):
        super().reset()
        # self.current = self.start_state
        self.processed_all = True
        self.stack.clear()
        self.stack.push(self.start_symbol)

    def _access(self, value):
        def error_print(msg):
            print(msg, self.current, value, symbol, self.stack)
        go_on = True
        if self.stack.size == 0:
            self.current = self.failed_state
            # error_print('Stack size 0')
            return True

        symbol = self.stack.pop()

        current = self.current.clean_forward(pk.InputPack(self.empty_symbol, symbol))
        # print(self.current, self.empty_symbol, symbol, current, self.stack)

        if current == set():
            current = self.current.clean_forward(pk.InputPack(value, symbol))
            # print(self.current, value, symbol, current, self.stack)
            if current == set():
                self.current = self.failed_state
                # error_print('Both failed')
                return True
        else:
            go_on = False
        current, stack = current.unpack

        self.stack += stack.exclude(self.empty_symbol)

        self.current = current
        # print('Go on: {}'.format(go_on), self.stack, self.current)
        return go_on

    def _access_epsilon(self):

        if self.stack.size == 0:
            return False
        symbol = self.stack.pop()

        current = self.current.clean_forward(pk.InputPack(self.empty_symbol, symbol))
        # print(self.current, self.empty_symbol, symbol, current, self.stack)

        if current == set():
            return False

        current, stack = current.unpack

        self.stack += stack.exclude(self.empty_symbol)
        self.current = current
        return True

    def _process(self, *entry):
        record = pk.Records()
        entry = list(entry)

        while len(entry) > 0: # go through epsilon transitions until the stack is depleted or there aren't any possible moves left.
            record.add_record(pk.PushRecordPack(self.current, self.accepted, self.stack))
            # print(entry)
            if self.current == self.failed_state:
                self.processed_all = False
                break
            value = entry.pop(0)

            if not self._access(value):
                entry.insert(0, value)
        # self.processed_all = True
        if self.processed_all:
            record.add_record(pk.PushRecordPack(self.current, self.accepted, self.stack))

            while (not self.accepted) and self._access_epsilon():
                record.add_record(pk.PushRecordPack(self.current, self.accepted, self.stack))

        self.records.add_record(record)

        # print(self.records)