# Pipeline Boltz-2: Predição Estrutural em Larga Escala de Complexos TCR-pMHC (11.000 Estruturas)

Pipeline automatizado e reproduzível para geração de manifestos YAML, inferência estrutural paralela via **SLURM** (com isolamento estrito de CPU/GPU) e consolidação de métricas de confiança (`ipTM`, `pTM`, `confidence_score`) para **11.000 complexos pentaméricos TCR-pMHC** usando **Boltz-2**.

---

## 1. Arquitetura Molecular do Complexo (5 Cadeias)

Cada complexo TCR-pMHC é modelado como um pentâmero completo para preservar a geometria nativa da fenda de apresentação antigênica:

| Cadeia | Componente | Tamanho | Descrição Estrutural |
| :---: | :--- | :---: | :--- |
| **A** | **MHC Classe I (Pesada)** | ~273 aa | Domínios da fenda ($\alpha_1 + \alpha_2$, ~180 aa) fusionados ao domínio constante $\alpha_3$ (93 aa) |
| **B** | **$\beta_2$-Microglobulina ($\beta_2\text{M}$)** | 99 aa | Cadeia leve estabilizadora do complexo MHC-I |
| **C** | **Peptídeo Antigênico** | 8–11 aa | Epítopo apresentado na fenda do MHC |
| **D** | **TCR $\alpha$** | ~110–120 aa | Domínio variável completo da cadeia alfa ($\text{V}\alpha\text{-J}\alpha$) |
| **E** | **TCR $\beta$** | ~115–125 aa | Domínio variável completo da cadeia beta ($\text{V}\beta\text{-D}\beta\text{-J}\beta$) |

---

## 2. Estrutura do Repositório

```text
boltz-tcr-pmhc-11k/
├── examples/
│   ├── sample_input.csv      # Exemplo de linha de entrada com sequências e rótulo
│   └── complex_0001.yaml     # Exemplo de manifesto YAML pentamérico gerado
├── csv_to_boltz.py           # Converte a tabela CSV de sequências em 11.000 arquivos YAML
├── run_boltz_gpu.sh          # Script SLURM com alocação dedicada de GPU e afinidade de CPU (taskset)
├── estatistica_complexos.py  # Varredura recursiva dos JSONs do Boltz-2 e exportação para CSV
├── .gitignore                # Ignora diretórios pesados de saída (.cif, .pdb, msas/)
└── README.md                 # Documentação do pipeline

```

---

## 3. Pré-requisitos e Formato de Entrada

### Ambiente Conda
```bash
conda create -n boltz_env python=3.10 -y
conda activate boltz_env
pip install boltz pandas pyyaml
```

### Tabela CSV de Entrada (`examples/sample_input.csv`)
O script `csv_to_boltz.py` espera colunas contendo as sequências de aminoácidos das cadeias do complexo (`MHC_seq`, `peptide`, `TCR_A_full_variable_seq`, `TCR_B_full_variable_seq`) e o rótulo experimental (`label`: `1` = ligante, `0` = não-ligante).

---

## 4. Fluxo de Execução Passo a Passo

### Etapa 1: Geração dos Manifestos YAML
```bash
conda activate boltz_env
python csv_to_boltz.py
```

### Etapa 2: Submissão Paralela no Cluster via SLURM
O script `run_boltz_gpu.sh` gerencia a fila de execução utilizando `taskset` para evitar contenção de threads entre jobs concorrentes no mesmo nó GPU:
```bash
sbatch run_boltz_gpu.sh
```

### Etapa 3: Consolidação das Métricas Estruturais
Após a conclusão das predições, extrai recursivamente os arquivos `confidence_*.json` e compila a tabela final de métricas (`ipTM`, `pTM`, `complex_plddt`, `complex_ipde`, `confidence_score`):
```bash
python estatistica_complexos.py
```

---

## 5. Interpretação das Métricas de Saída

* **`ipTM` (Interface Predicted TM-score):** Principal métrica para discriminar pares TCR-pMHC ligantes vs. não-ligantes, avaliando a confiança na orientação relativa entre as cadeias na interface de reconhecimento.
* **`pTM` (Predicted TM-score):** Qualidade global do enovelamento do pentâmero completo.
* **`confidence_score`:** Score composto ponderado pelo Boltz-2 combinando `pLDDT` local e `ipTM` de interface.