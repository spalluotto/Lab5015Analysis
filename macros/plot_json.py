import json
import matplotlib.pyplot as plt

file = '/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_H8_May2023/VovsEff_v2.json'
    
data = json.loads(file)

# Estrai le chiavi principali (per esempio "HPK_1E14_LYSO817_T-22C_B")
main_key = next(iter(data))

# Estrai i dati per la chiave principale
sub_data = data[main_key]

# Inizializza le liste per VovEff e current
VovEff = []
current = []

# Itera attraverso le chiavi secondarie per estrarre i dati
for key, values in sub_data.items():
    VovEff.append(float(values[0]))  # il primo elemento è VovEff
    current.append(float(values[2])) # il terzo elemento è current

# Disegna il grafico current vs VovEff
plt.plot(VovEff, current, marker='o')
plt.xlabel('VovEff')
plt.ylabel('Current (mA)')
plt.title('Current vs VovEff')
plt.grid(True)
plt.show()
