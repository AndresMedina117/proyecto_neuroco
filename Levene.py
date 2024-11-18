import pandas as pd
from scipy.stats import levene

ruta_archivo = "/home/luistorrest/Documents/Projects/Research/Volumetry MRI/proyecto_neuroco/HIPOCAMPO_AMIGDALA_ASEG_BIOMARCADORES_SUIZA.xlsx"  # Reemplazar con la ruta real del archivo
excel_file = pd.ExcelFile(ruta_archivo)
aseg_stats = pd.read_excel(excel_file, sheet_name="aseg_stats")

filtered_data = aseg_stats[aseg_stats['Measure:volume'].str.contains('CTR|DCL', na=False)]

filtered_data['Group'] = filtered_data['Measure:volume'].str.extract('(CTR|DCL)')

volumetric_columns = filtered_data.columns[1:-1] 

levene_results = {}

for column in volumetric_columns:
    group_data = [filtered_data[filtered_data['Group'] == group][column].dropna()
                  for group in ['CTR', 'DCL']]
    
    if all(len(g) > 1 for g in group_data):
        stat, p_value = levene(*group_data)
        levene_results[column] = p_value


sorted_levene_results = dict(sorted(levene_results.items(), key=lambda x: x[1]))


sorted_levene_top10 = {k: v for k, v in list(sorted_levene_results.items())[:10]}



print("Prueba de Levene - Homogeneidad de Varianzas :")
for structure, p_value in sorted_levene_top10.items():
    print(f"{structure}: p-value = {p_value:.5f}")
