import json
import streamlit as st

def calcular_materiais(item, quantidade, receitas):
    if item not in receitas:
        return {item: quantidade}

    materiais_necessarios = {}

    for componente in receitas[item]["itens"]:
        sub_item = componente["item"]
        sub_quantidade = componente["qtd"]
        total_sub_quantidade = quantidade * sub_quantidade

        sub_materiais = calcular_materiais(sub_item, total_sub_quantidade, receitas)

        for sub_material, sub_qtd in sub_materiais.items():
            if sub_material in materiais_necessarios:
                materiais_necessarios[sub_material] += sub_qtd
            else:
                materiais_necessarios[sub_material] = sub_qtd

    return materiais_necessarios

def main():
    st.title("Calculadora de Materiais")

    with open("./db/db.json", "r") as file:
        receitas = json.load(file)

    item_desejado = st.selectbox("Selecione o item desejado:", list(receitas.keys()))

    quantidade_desejada = st.number_input("Insira a quantidade desejada:", min_value=1, value=1, step=1)

    if st.button("Calcular"):
        materiais_necessarios = calcular_materiais(item_desejado, quantidade_desejada, receitas)

        st.subheader(f"Materiais necessários para {quantidade_desejada} {item_desejado}:")
        for material, qtd in materiais_necessarios.items():
            st.write(f"{material}: {qtd}")

if __name__ == "__main__":
    main()
