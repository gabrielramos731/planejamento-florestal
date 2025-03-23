def numpy_to_python(obj):
    '''Converte np.int e np.float para int e float dos dados do dicionário'''
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    
def python_to_numpy(dicionario):
    '''Converte int e float para np.int e np.float dos dados do dicionário'''
    for chave, subdict in dicionario.items():
        for subchave, valor in subdict.items():
            if isinstance(valor, int):
                subdict[subchave] = np.int64(valor)
            elif isinstance(valor, float):
                subdict[subchave] = np.float64(valor)
                
    dicionario = {np.int64(key): valor for key, valor in dicionario.items()}
    return dicionario

# Converte e salva em json
caminho = 'v3_experimentos.json'
with open(caminho, 'w', encoding='utf-8') as arquivo:
    json.dump(v3_num_calc_vpl, arquivo, ensure_ascii=False, indent=4, default=numpy_to_python)

# Lê json
with open(caminho, 'r', encoding='utf-8') as arquivo:
    v3_teste = python_to_numpy(json.load(arquivo))

# ---

v3_teste_ojb = experimento(v3_teste)
v3_teste_ojb.calcula_estatisticas()

# ---

fig, axs = plt.subplots(3,1, figsize=(8,16))
plt.rcParams.update({'font.size': 10})
plt.sca(axs[0])
v3_teste_ojb.plota_experimento(medida='media', vizinhanca='Aleatória')
plt.sca(axs[1])
v3_teste_ojb.plota_experimento(medida='media', vizinhanca='Localizada')
plt.sca(axs[2])
v3_teste_ojb.plota_experimento(medida='media', vizinhanca='Sistemática')

plt.show()

# ---

# Melhores métodos de cada vizinhança

v1_mm_media = []
for chave, subdict in v3_teste_ojb.estatisticas.items():
    for subchave, valor in subdict.items():
        if subchave == 'mm':
            v1_mm_media.append(valor.get('media'))
            
v2_pm_media = []
for chave, subdict in v3_teste_ojb.estatisticas.items():
    for subchave, valor in subdict.items():
        if subchave == 'pm':
            v2_pm_media.append(valor.get('media'))
            
v3_pm_media = []
for chave, subdict in v3_teste_ojb.estatisticas.items():
    for subchave, valor in subdict.items():
        if subchave == 'pm':
            v3_pm_media.append(valor.get('media'))