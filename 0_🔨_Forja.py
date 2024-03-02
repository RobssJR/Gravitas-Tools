from typing import List
from itertools import combinations
import streamlit as st

class SequenceHammer:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

operations = ['Light', 'Medium', 'Hard', 'Draw', 'Punch', 'Bend', 'Upset', 'Shrink']
values = [-3, -6, -9, -15, 2, 7, 13, 16]

sequence_hammer_list: List[SequenceHammer] = [SequenceHammer(operation, value) for operation, value in zip(operations, values)]

def find_combination(target_value: int, sequence_hammers: List[SequenceHammer], min_combination_size: int) -> List[SequenceHammer]:
    for tamanho_combinacao in range(min_combination_size, len(sequence_hammers) + 1):
        for combinacao in combinations(sequence_hammers, tamanho_combinacao):
            if sum(hammer.value for hammer in combinacao) == target_value:
                return list(combinacao)

    return []

def btn_calc():
    col1, col2 = st.columns(2)
  
    selected_indices = st.session_state.selected_indices
    target_value = -1 * sum(sequence_hammer_list[index].value for index in selected_indices)
    
    result_sequence = find_combination(target_value, sequence_hammer_list, min_combination_size=3)

    if result_sequence:
        col1.write("Combinação encontrada:")
        col1.text(" | ".join([f"{hammer.name}" for hammer in result_sequence]))
        
        selected_names = [sequence_hammer_list[select].name for select in selected_indices][::-1]
        col2.write("Sequencia final:")
        col2.write(f"{' | '.join([f'{hammer.name}' for hammer in result_sequence])} | {' | '.join(selected_names)}")

    else:
        st.write("Nenhuma combinação encontrada.")
        
    st.session_state.selected_indices = []
    st.session_state.selected_names = []

def dynamic_button_selector():
    if 'selected_indices' not in st.session_state:
        st.session_state.selected_indices = []
        
    if 'selected_names' not in st.session_state:
        st.session_state.selected_names = []

    cols = st.columns(4)

    for index, operation in enumerate(operations):
        button_state = cols[index % 4].button(operation)
        if button_state:
            st.session_state.selected_indices.append(index)
            
    st.session_state.selected_names = [sequence_hammer_list[select].name for select in st.session_state.selected_indices]
    st.text(" | ".join(st.session_state.selected_names))

def main():
    dynamic_button_selector()
    
    if st.button('Calcular'):
        btn_calc()

if __name__ == "__main__":
    main()
