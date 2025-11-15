from dataclasses import dataclass


@dataclass
class TaxScenario:
    """
    Representa um cenário fiscal simples para cálculo de custo líquido.
    Todos os valores de alíquota devem ser informados em percentual,
    por exemplo: 19 para 19%.
    """
    valor_compra: float          # valor total do item (unitário ou do lote)
    aliq_icms: float             # alíquota de ICMS (%) para crédito (se houver)
    aliq_pis: float              # alíquota de PIS (%) para crédito (se houver)
    aliq_cofins: float           # alíquota de COFINS (%) para crédito (se houver)
    tem_credito_icms: bool       # se essa compra gera crédito de ICMS
    tem_credito_pis_cofins: bool # se essa compra gera crédito de PIS/COFINS


@dataclass
class ResultadoCusto:
    valor_compra: float
    credito_icms: float
    credito_pis: float
    credito_cofins: float
    total_creditos: float
    custo_liquido: float


def calcular_custo_liquido(cenario: TaxScenario) -> ResultadoCusto:
    """
    Calcula o custo líquido de um item a partir do cenário informado.
    A regra aqui é propositalmente simples:
    - crédito de ICMS = valor_compra * aliq_icms, se tem_credito_icms = True
    - crédito de PIS/COFINS = valor_compra * aliq_pis/aliq_cofins,
      se tem_credito_pis_cofins = True
    - custo_líquido = valor_compra - (todos os créditos)
    """

    # Converte % para fator (19 -> 0.19)
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
    """
    Calcula um preço de venda simples aplicando uma margem (%)
    em cima do custo líquido.
    Ex: custo 72,90 com margem 10% -> 72,90 * 1,10 = 80,19
    """
    fator_margem = 1 + (margem_percentual / 100.0)
    return round(custo_liquido * fator_margem, 4)


def parse_float_br(valor_str: str) -> float:
    """
    Converte string como '4,50' ou '4.50' para float 4.5
    """
    valor_str = valor_str.strip().replace(",", ".")
    return float(valor_str)


def perguntar_bool(pergunta: str) -> bool:
    """
    Pergunta algo do tipo 'Tem crédito de ICMS? (s/n)' e retorna True/False.
    """
    while True:
        resp = input(pergunta + " (s/n): ").strip().lower()
        if resp in ("s", "sim"):
            return True
        if resp in ("n", "nao", "não"):
            return False
        print("Resposta inválida, digite 's' ou 'n'.")


def main():
    print("=" * 60)
    print(" CALCULADORA DE CUSTO LÍQUIDO (ICMS + PIS/COFINS) ")
    print("=" * 60)
    print("Obs.: valores podem ser digitados com vírgula ou ponto.\n")

    # 1) Valor de compra (unitário ou do lote)
    valor_compra_str = input("Informe o VALOR DE COMPRA do item (ex: 4,50): ")
    valor_compra = parse_float_br(valor_compra_str)

    # 2) ICMS
    tem_credito_icms = perguntar_bool("Esta compra gera CRÉDITO de ICMS?")
    aliq_icms = 0.0
    if tem_credito_icms:
        aliq_icms_str = input(
            "Informe a alíquota de ICMS para crédito (ex: 19 para 19%): "
        )
        aliq_icms = parse_float_br(aliq_icms_str)

    # 3) PIS/COFINS
    tem_credito_pis_cofins = perguntar_bool(
        "Esta compra gera CRÉDITO de PIS/COFINS?"
    )
    aliq_pis = 0.0
    aliq_cofins = 0.0
    if tem_credito_pis_cofins:
        aliq_pis_str = input(
            "Informe a alíquota de PIS para crédito (ex: 1,65 para 1,65%): "
        )
        aliq_cofins_str = input(
            "Informe a alíquota de COFINS para crédito (ex: 7,6 para 7,6%): "
        )
        aliq_pis = parse_float_br(aliq_pis_str)
        aliq_cofins = parse_float_br(aliq_cofins_str)

    # Monta cenário
    cenario = TaxScenario(
        valor_compra=valor_compra,
        aliq_icms=aliq_icms,
        aliq_pis=aliq_pis,
        aliq_cofins=aliq_cofins,
        tem_credito_icms=tem_credito_icms,
        tem_credito_pis_cofins=tem_credito_pis_cofins,
    )

    # Calcula custo
    resultado = calcular_custo_liquido(cenario)

    print("\n" + "-" * 60)
    print(" RESULTADO DO CÁLCULO ")
    print("-" * 60)
    print(f"Valor de compra........: R$ {resultado.valor_compra:,.4f}")
    print(f"Crédito de ICMS........: R$ {resultado.credito_icms:,.4f}")
    print(f"Crédito de PIS.........: R$ {resultado.credito_pis:,.4f}")
    print(f"Crédito de COFINS......: R$ {resultado.credito_cofins:,.4f}")
    print(f"Total de créditos......: R$ {resultado.total_creditos:,.4f}")
    print(f"CUSTO LÍQUIDO..........: R$ {resultado.custo_liquido:,.4f}")

    # 4) Opcional: sugerir preço de venda com base numa margem
    quer_margem = perguntar_bool(
        "\nDeseja calcular um PREÇO DE VENDA sugerido com base em uma margem (%)?"
    )
    if quer_margem:
        margem_str = input(
            "Informe a margem desejada em % (ex: 10 para 10% de lucro): "
        )
        margem = parse_float_br(margem_str)
        preco_sugerido = calcular_preco_venda(resultado.custo_liquido, margem)
        print("\n" + "-" * 60)
        print(" PREÇO DE VENDA SUGERIDO ")
        print("-" * 60)
        print(f"Margem desejada........: {margem:.2f}%")
        print(f"Preço de venda mínimo..: R$ {preco_sugerido:,.4f}")

    print("\nFim do cálculo. 👋")


if __name__ == "__main__":
    main()
