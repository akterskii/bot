# from typing import TypeVar, Generic, Set, Dict, Tuple, List, Optional
#
# T1 = TypeVar['T1']
# T2 = TypeVar['T2']
#
#
# class FiniteStateMachine(Generic[T1, T2]):
#     """Class to store state transitions"""
#     def __init__(self):
#         self.states: Set[T1] = set()
#         self.transitions: Dict[T1, Dict[T1, T2]] = {}
#
#     def add_state(self, state: T1):
#         if state not in self.states:
#             self.states.add(state)
#
#     def add_transition(
#             self,
#             initial_state: T1,
#             next_state: T1,
#             transition_metadata: Optional[T2]) -> None:
#         """Docstr"""
#
#         assert initial_state in self.states and next_state in self.states
#         assert (initial_state not in self.transitions or
#                 next_state not in self.transitions[initial_state])
#
#         self.transitions[initial_state] = self.transitions.get(initial_state, {})
#         self.transitions[initial_state][next_state] = (
#             self.transitions[initial_state].get(next_state, T2()))
#         self.transitions[initial_state][next_state].update(
#             transition_metadata)
#
#     def get_next_states(
#             self, initial_state: T1
#     ) -> List[Tuple[T1, T2]]:
#
#         if initial_state not in self.transitions:
#             return []
#         return [(next_state, transition_metadata) for
#                 next_state, transition_metadata in
#                 self.transitions[initial_state].items()]
#
#     def get_transition_info(
#             self, initial_state: T1, next_state: T1) -> Optional[T2]:
#         if initial_state not in self.transitions:
#             return None
#         if next_state not in self.transitions[initial_state]:
#             return None
#         return self.transitions[initial_state][next_state]
#
#     def delete_transition(self, initial_state: T1, next_state: T1) -> bool:
#         if initial_state not in self.transitions:
#             return False
#         if next_state not in self.transitions[initial_state]:
#             return False
#         del self.transitions[initial_state][next_state]
#         return True
#
#     def print_all_transitions(self) -> None:
#         """Output the transitions """
#         for state, transitions in self.transitions.items():
#             print(f"Initial_state: {state}:")
#             for next_state, transition_metadata in transitions:
#                 print(f'  Next state: {next_state}. Transition_metadata: '
#                       f'{transition_metadata}')