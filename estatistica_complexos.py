python3 -c "
import pandas as pd
import os

# Carrega a tabela consolidada gerada anteriormente
input_csv = os.path.expanduser('~/boltz_todas_estatisticas.csv')
output_csv = os.path.expanduser('~/tabela_confiabilidade_11k.csv')

df = pd.read_csv(input_csv)

# Colunas desejadas: complexo, iptm, ptm e confiabilidade
target_cols = ['complexo', 'iptm', 'ptm', 'confidence_score']

# Garante que pega apenas as colunas que existem no arquivo
cols_to_use = [col for col in target_cols if col in df.columns]

# Se a coluna de plddt estiver presente, você pode incluí-la se desejar
tabela_filtrada = df[cols_to_use].copy()

# Ordena por confidence_score (ou iptm) decrescente
if 'confidence_score' in tabela_filtrada.columns:
    tabela_filtrada.sort_values(by='confidence_score', ascending=False, inplace=True)
elif 'iptm' in tabela_filtrada.columns:
    tabela_filtrada.sort_values(by='iptm', ascending=False, inplace=True)

# Salva a nova tabela limpa na sua home da Celulose
tabela_filtrada.to_csv(output_csv, index=False)

print(f'Tabela criada com sucesso em: {output_csv}')
print(f'Total de complexos na tabela: {len(tabela_filtrada)}')
print('\nPrimeiras 10 linhas da tabela:')
print(tabela_filtrada.head(10).to_string(index=False))
"
