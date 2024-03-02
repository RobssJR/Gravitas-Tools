import json
import streamlit as st

def calcular_materiais(item, quantidade, receitas, materiais_necessarios=None):
    if materiais_necessarios is None:
        materiais_necessarios = {}

    pilha = [(item, quantidade)]

    while pilha:
        item_atual, qtd_atual = pilha.pop()

        if item_atual not in receitas:
            if item_atual in materiais_necessarios:
                materiais_necessarios[item_atual] += qtd_atual
            else:
                materiais_necessarios[item_atual] = qtd_atual
        else:
            if item_atual in materiais_necessarios:
                materiais_necessarios[item_atual] += qtd_atual
            else:
                materiais_necessarios[item_atual] = qtd_atual

                for componente in receitas[item_atual]["itens"]:
                    sub_item = componente["item"]
                    sub_quantidade = componente["qtd"]

                    if "tool" in sub_item.lower():
                        # Sempre considera 1 para itens do tipo "tool"
                        total_sub_quantidade = 1
                    else:
                        total_sub_quantidade = qtd_atual * sub_quantidade

                    pilha.append((sub_item, total_sub_quantidade))

    # Agrupa os itens iguais e soma as quantidades
    materiais_agrupados = {}
    for material, qtd in materiais_necessarios.items():
        if material in materiais_agrupados:
            materiais_agrupados[material] += qtd
        else:
            materiais_agrupados[material] = qtd

    return materiais_agrupados

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
