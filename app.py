import streamlit as st
from dataclasses import dataclass


@dataclass
class TaxScenario:
    valor_compra: float
    aliq_icms: float
    aliq_pis: float
    aliq_cofins: float
    tem_credito_icms: bool
    tem_credito_pis_cofins: bool


@dataclass
class ResultadoCusto:
    valor_compra: float
    credito_icms: float
    credito_pis: float
    credito_cofins: float
    total_creditos: float
    custo_liquido: float


def calcular_custo_liquido(cenario: TaxScenario) -> ResultadoCusto:
    fator_icms = cenario.aliq_icms / 100.0
    fator_pis = cenario.aliq_pis / 100.0
    fator_cofins = cenario.aliq_cofins / 100.0

    credito_icms = cenario.valor_compra * fator_icms if cenario.tem_credito_icms else 0.0
    credito_pis = (
        cenario.valor_compra * fator_pis if cenario.tem_credito_pis_cofins else 0.0
    )
    credito_cofins = (
        cenario.valor_compra * fator_cofins if cenario.tem_credito_pis_cofins else 0.0
    )

    total_creditos = credito_icms + credito_pis + credito_cofins
    custo_liquido = cenario.valor_compra - total_creditos

    return ResultadoCusto(
        valor_compra=cenario.valor_compra,
        credito_icms=round(credito_icms, 4),
        credito_pis=round(credito_pis, 4),
        credito_cofins=round(credito_cofins, 4),
        total_creditos=round(total_creditos, 4),
        custo_liquido=round(custo_liquido, 4),
    )


def calcular_preco_venda(custo_liquido: float, margem_percentual: float) -> float:
    fator_margem = 1 + (margem_percentual / 100.0)
    return round(custo_liquido * fator_margem, 4)


def main():
    st.title("🧮 Calculadora de Custo Líquido (ICMS + PIS/COFINS)")

    st.markdown(
        "Informe os dados da compra abaixo para calcular o **custo líquido** "
        "considerando créditos de ICMS e PIS/COFINS."
    )

    with st.form("form_custo"):
        valor_compra = st.number_input(
            "Valor de compra do item (unitário ou lote)",
            min_value=0.0,
            step=0.01,
            format="%.4f",
        )

        col1, col2 = st.columns(2)

        with col1:
            tem_credito_icms = st.checkbox("Gera crédito de ICMS?", value=False)
            aliq_icms = st.number_input(
                "Alíquota de ICMS (%)",
                min_value=0.0,
                max_value=100.0,
                step=0.01,
                format="%.2f",
            )

        with col2:
            tem_credito_pis_cofins = st.checkbox(
                "Gera crédito de PIS/COFINS?", value=False
            )
            aliq_pis = st.number_input(
                "Alíquota de PIS (%)",
                min_value=0.0,
                max_value=100.0,
                step=0.01,
                format="%.2f",
            )
            aliq_cofins = st.number_input(
                "Alíquota de COFINS (%)",
                min_value=0.0,
                max_value=100.0,
                step=0.01,
                format="%.2f",
            )

        margem = st.number_input(
            "Margem de lucro desejada (%) (opcional)",
            min_value=0.0,
            max_value=1000.0,
            step=0.1,
            format="%.2f",
        )

        submitted = st.form_submit_button("Calcular")

    if submitted:
        cenario = TaxScenario(
            valor_compra=valor_compra,
            aliq_icms=aliq_icms,
            aliq_pis=aliq_pis,
            aliq_cofins=aliq_cofins,
            tem_credito_icms=tem_credito_icms,
            tem_credito_pis_cofins=tem_credito_pis_cofins,
        )

        resultado = calcular_custo_liquido(cenario)

        st.subheader("📊 Resultado do cálculo")
        st.write(f"**Valor de compra:** R$ {resultado.valor_compra:,.4f}")
        st.write(f"**Crédito de ICMS:** R$ {resultado.credito_icms:,.4f}")
        st.write(f"**Crédito de PIS:** R$ {resultado.credito_pis:,.4f}")
        st.write(f"**Crédito de COFINS:** R$ {resultado.credito_cofins:,.4f}")
        st.write(f"**Total de créditos:** R$ {resultado.total_creditos:,.4f}")
        st.markdown(
            f"### 💰 CUSTO LÍQUIDO: **R$ {resultado.custo_liquido:,.4f}**"
        )

        if margem > 0:
            preco_sugerido = calcular_preco_venda(resultado.custo_liquido, margem)
            st.subheader("💵 Preço de venda sugerido")
            st.write(f"**Margem desejada:** {margem:.2f}%")
            st.write(f"**Preço mínimo de venda:** R$ {preco_sugerido:,.4f}")


if __name__ == "__main__":
    main()
