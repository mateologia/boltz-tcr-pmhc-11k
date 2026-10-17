import os
import glob
import json
import pandas as pd

# Caminho real onde o Boltz salvou as predições
results_dir = os.path.expanduser('~/boltz_results_all_gpu/boltz_results_boltz_inputs_all/predictions')
data = []

# Busca recursiva de todos os arquivos de confiança JSON
json_files = glob.glob(os.path.join(results_dir, '**', '*confidence*.json'), recursive=True)
if not json_files:
    json_files = glob.glob(os.path.join(results_dir, '**', '*.json'), recursive=True)

print(f'Encontrados {len(json_files)} arquivos de métricas. Consolidando...')

for fpath in json_files:
    target = os.path.basename(os.path.dirname(fpath))
    try:
        with open(fpath, 'r') as jf:
            m = json.load(jf)
            if not isinstance(m, dict):
                continue
            row = {'complexo': target}
            for k, v in m.items():
                if isinstance(v, (int, float, str, bool)):
                    row[k] = v
            # Filtra apenas arquivos que de fato contenham métricas estruturais
            if any(k in row for k in ['iptm', 'ptm', 'complex_plddt', 'mean_plddt', 'plddt', 'confidence_score']):
                data.append(row)
    except Exception:
        continue

df = pd.DataFrame(data)
if not df.empty:
    df.drop_duplicates(subset=['complexo'], inplace=True)
    if 'iptm' in df.columns:
        df.sort_values(by='iptm', ascending=False, inplace=True)
    out_csv = os.path.expanduser('~/boltz_todas_estatisticas.csv')
    df.to_csv(out_csv, index=False)
    print(f'Tabela consolidada salva com sucesso em: {out_csv}')
    print(f'Total de complexos processados na tabela: {len(df)}')
    print('\nTop 5 complexos com melhor ipTM:')
    print(df.head())
else:
    print('Ainda não foram encontrados arquivos de métricas com dados válidos.')
