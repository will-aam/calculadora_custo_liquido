# 🧮 Calculadora de Custo Líquido (ICMS + PIS/COFINS)

Este projeto é uma **calculadora fiscal de custo líquido**, focada em simular o impacto de **créditos de ICMS, PIS e COFINS** no custo de mercadorias para revenda.

---

## ✅ Objetivo

Calcular o **custo líquido** de um item a partir de:

- Valor de compra (unitário ou lote)
- Alíquota de ICMS (quando gera crédito)
- Alíquota de PIS (quando gera crédito)
- Alíquota de COFINS (quando gera crédito)
- Informação se a compra gera ou não crédito de:
  - ICMS
  - PIS/COFINS

A calculadora também pode sugerir um **preço mínimo de venda** com base em uma **margem de lucro (%)** aplicada sobre o custo líquido.

---

## 🧩 Arquitetura do projeto

O projeto tem, basicamente, **dois modos de uso**:

1. **Modo terminal (linha de comando)**  
   Arquivo: `calculadora_custo_liquido.py`

   - Roda direto no console
   - Faz perguntas interativas (valor de compra, alíquotas, etc.)
   - Exibe o resultado no próprio terminal

2. **Modo web (navegador)**  
   Arquivo: `app.py` (usando **Streamlit**)
   - Abre uma interface web simples
   - Permite preencher os campos em formulários
   - Mostra o resultado de forma visual (custo líquido, créditos, preço sugerido)

Os dois modos usam a **mesma lógica de cálculo**, apenas com interfaces diferentes.

---

## 🛠️ Tecnologias utilizadas

- **Linguagem:** Python 3.x
- **Bibliotecas principais:**
  - `dataclasses` (organização dos dados)
  - `streamlit` (interface web)

---

## 🚀 Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/will-aam/calculadora_custo_liquido
cd calculadora_custo_liquido
```

---

### 2. Criar e ativar um ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows

# ou no Linux/macOS:
# source venv/bin/activate
```

---

### 3. Instalar dependências

Se for usar só o modo **terminal**, não precisa de nada além do Python.

Se for usar o modo **web**, instale o Streamlit:

```bash
pip install streamlit
```

---

## 🖥️ Modo 1 – Rodar a calculadora no terminal

Arquivo: `calculadora_custo_liquido.py`

```bash
python calculadora_custo_liquido.py
# ou
py calculadora_custo_liquido.py
```

Exemplo de fluxo:

- Informe o valor de compra: `8,50`
- Informe se gera crédito de ICMS: `s`

  - Alíquota de ICMS: `19`

- Informe se gera crédito de PIS/COFINS: `s`

  - PIS: `1,65`
  - COFINS: `7,6`

A saída mostrará:

- Valor de compra
- Crédito de ICMS
- Crédito de PIS
- Crédito de COFINS
- Total de créditos
- **Custo líquido**

Opcionalmente, você pode informar uma **margem de lucro (%)** e a calculadora sugere um **preço mínimo de venda**.

---

## 🌐 Modo 2 – Rodar a calculadora no navegador (Streamlit)

Arquivo: `app.py`

```bash
streamlit run app.py
```

Isso vai abrir o app em uma URL do tipo:

```text
http://localhost:8501
```

Na interface web, você pode:

- Informar valor de compra
- Marcar se a compra gera crédito de ICMS
- Informar alíquota de ICMS (%)
- Marcar se a compra gera crédito de PIS/COFINS
- Informar alíquota de PIS e COFINS (%)
- Informar uma margem de lucro (%)

O app mostra:

- Créditos individuais (ICMS, PIS, COFINS)
- Total de créditos
- **Custo líquido**
- Preço mínimo de venda sugerido (se margem for informada)

---

## 📚 Exemplos de uso (cenários fiscais)

### 1. Gelo comprado de fornecedor do Simples Nacional

- Valor de compra: `4,50`
- Gera crédito de ICMS? `não`
- Gera crédito de PIS/COFINS? `não`

Resultado esperado:

- Créditos = `0,00`
- **Custo líquido = 4,50**

O gelo é tributado na venda, mas **não gera crédito na entrada** (fornecedor Simples).

---

### 2. Mercadoria tributada com crédito de ICMS, PIS e COFINS

Ex.: amendoim, com:

- Valor de compra unitário: `8,50`
- Gera crédito de ICMS? `sim` → `19%`
- Gera crédito de PIS/COFINS? `sim` → PIS `1,65%`, COFINS `7,6%`

Resultado aproximado:

- Crédito de ICMS ≈ `1,6150`
- Crédito de PIS ≈ `0,1403`
- Crédito de COFINS ≈ `0,6460`
- Total de créditos ≈ `2,4013`
- **Custo líquido ≈ 6,0987**

---

## 🔮 Próximos passos / ideias futuras

- Ler automaticamente um **XML de NF-e** e preencher os campos da calculadora.
- Separar:

  - alíquotas e regras de **entrada** (crédito)
  - e regras de **saída** (débito na venda).

- Tratar cenários específicos de:

  - ICMS ST (CST 10, 60)
  - operações isentas (CST 40)
  - fornecedor do Simples x regime normal.

---

## Projeto de estudo e portfólio focado em:

- Tributação (ICMS, PIS, COFINS)
- Formação de custo líquido
