# Pipeline Boltz-2: Predição Estrutural em Larga Escala de Complexos TCR–pMHC (11.000 Estruturas)

Pipeline automatizado para geração de ficheiros de entrada YAML, submissão paralela via SLURM com isolamento estrito de hardware e compilação de métricas de acurácia estrutural (`ipTM`, `pTM` e `confidence_score`) para 11.000 complexos TCR-pMHC no cluster *Celulose*.

---

## 1. Arquitetura do Complexo (5 Cadeias)
* **Cadeia A (MHC Classe I Pesada - 273 aa):** Região da fenda ($\alpha_1 + \alpha_2$, ~180 aa) fusionada ao domínio constante $\alpha_3$ (93 aa).
* **Cadeia B ($\text{B}_2\text{M}$ - 99 aa):** Microglobulina $\beta_2$ completa.
* **Cadeia C (Peptídeo - 8 a 11 aa):** Epítopo antigénico apresentado.
* **Cadeia D (TCR $\alpha$):** Região variável completa da cadeia alfa.
* **Cadeia E (TCR $\beta$):** Região variável completa da cadeia beta.

---

## 2. Estrutura do Diretório
```text
├── csv_to_boltz.py               # Conversão da tabela CSV em 11.000 YAMLs
├── run_boltz_gpu.sh              # Submissão SLURM com taskset e GPU dedicada
├── estatistica_complexos.py      # Extração recursiva de métricas JSON e geração do CSV
├── .gitignore
└── README.md

##3. Fluxo de Execução

#Geração dos YAMLS
```bash
conda activate boltz_env
python csv_to_boltz.py

#Execução no Cluster via SLURM
```bash
sbatch run_boltz_gpu.sh

#Consolidação das Métricas
```bash
python estatistica_complexos.py
```
