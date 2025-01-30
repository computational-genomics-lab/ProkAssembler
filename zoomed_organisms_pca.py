import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

# Define your data
data = {
    'Data': ['Gloeobacter morelensis MG652769_Assembly_1', 'Gloeobacter morelensis MG652769_Assembly1_meta',
             'Gloeobacter morelensis MG652769_Assembly2', 'Gloeobacter morelensis MG652769_Assembly2_meta',
             'Tolypothrix sp.PCC 7712_Assembly_1', 'Tolypothrix sp. PCC 7712_Assembly_1_meta',
             'Tolypothrix sp. PCC 7712_Assembly_2', 'Tolypothrix sp. PCC 7712_Assembly_2_meta',
             'Phormidium yuhuli AB48_Assembly_1_meta', 'Phormidium yuhuli AB48_Assembly_1',
             'Phormidium yuhuli AB48_Assembly_2', 'Phormidium yuhuli AB48_Assembly_2_meta',
             'Nostoc edaphicum CCNP1411_Assembly_1', 'Nostoc edaphicum CCNP1411_Assembly_1_meta',
             'Nostoc edaphicum CCNP1411_Assembly_2', 'Nostoc edaphicum CCNP1411_Assembly_2_meta',
             'Candidatus Paraprochloron terpiosi LD05_Assembly_1', 'Candidatus Paraprochloron terpiosi LD05_Assembly_1_meta',
             'Candidatus Paraprochloron terpiosi LD05_Assembly_2', 'Candidatus Paraprochloron terpiosi LD05_Assembly_2_meta',
             'Anthocerotibacter panamensis C109_Assembly_1', 'Anthocerotibacter panamensis C109_Assembly_1_meta',
             'Anthocerotibacter panamensis C109_Assembly_2', 'Anthocerotibacter panamensis C109_Assembly_2_meta',
             'Sphaerospermopsis torques-reginae ITEP-024_Assembly_1', 'Sphaerospermopsis torques-reginae ITEP-024_Assembly_1_meta',
             'Sphaerospermopsis torques-reginae ITEP-024_Assembly_2', 'Sphaerospermopsis torques-reginae ITEP-024_Assembly_2_meta',
             'Thermostichus lividus PCC 6715_Assembly_1', 'Thermostichus lividus PCC 6715_Assembly_1_meta',
             'Thermostichus lividus PCC 6715_Assembly_2', 'Thermostichus lividus PCC 6715_Assembly_2_meta',
             'Tolypothrix bouteillei vb52130_Assembly_1', 'Tolypothrix bouteillei vb52130_Assembly_1_meta',
             'Tolypothrix bouteillei vb52130_Assembly_2', 'Tolypothrix bouteillei vb52130_Assembly_2_meta',
             'Myxosarcina sp._Assembly_1', 'Myxosarcina sp._Assembly_1_meta',
             'Myxosarcina sp._Assembly_2', 'Myxosarcina sp._Assembly_2_meta',
             'Scytonema tolypothrichoides VB-61278_Assembly_1', 'Scytonema tolypothrichoides VB-61278_Assembly_1_meta',
             'Scytonema tolypothrichoides VB-61278_Assembly_2', 'Scytonema tolypothrichoides VB-61278_Assembly_2_meta',
             'Scytonema millei VB51128_Assembly_1', 'Scytonema millei VB511283_Assembly_1_meta',
             'Scytonema millei VB511283_Assembly_2', 'Scytonema millei VB511283_Assembly_2_meta',
             'Tolypothrix campylonemoides VB511288_Assembly_1', 'Tolypothrix campylonemoides VB511288_Assembly_1_meta',
             'Tolypothrix campylonemoides VB511288_Assembly_2', 'Tolypothrix campylonemoides VB511288_Assembly_2_meta',
             'cat_1_Assembly_1', 'cat_1_Assembly_1_meta', 'cat_1_Assembly_2', 'cat_1_Assembly_2_meta',
             'cat_2_Assembly_1', 'cat_2_Assembly_1_meta', 'cat_2_Assembly_2', 'cat_2_Assembly_2_meta',
             'cat_4_Assembly_1', 'cat_4_Assembly_1_meta', 'cat_4_Assembly_2', 'cat_4_Assembly_2_meta' ],
    'Completeness': [99.15, 99.15, 99.15, 99.15, 99.11, 99.11, 99.11, 98, 100, 100, 100, 0, 99.7, 99.7, 99.7, 99.7,
                     96.89, 96.89, 96.22, 96.67, 98.29, 0, 98.29, 98.29, 93.33, 90.78, 99.33, 98.11, 0, 0, 99.53, 0,
                     99.66, 99.66, 99.76, 99.52, 99.56, 99.34, 99.56, 99.56, 89.6, 88.88, 99.52, 99.76, 99.76, 99.76,
                     99.76, 88.48, 99.76, 99.76, 97.11, 99.63, 99.97, 99.97, 99.97, 99.97, 99.97, 99.97, 99.97, 99.97, 99.37, 99.97, 99.97, 99.97],
    'Contamination': [0.85, 0.85, 0.85, 0.85, 0, 0, 0, 0, 0.54, 0.54, 0.54, 0, 1.33, 1.33, 1.33, 1.78, 0.52, 0.52, 0.52,
                      1.19, 0.85, 0, 0.85, 0.85, 31.48, 30.02, 0, 0, 0, 0, 0.12, 0, 1.04, 1.29, 1.29, 1.67, 2.4, 2.84, 0.87,
                      0.87, 4.18, 2.49, 1.04, 1.04, 1.19, 1.19, 1.04, 2.34, 1.19, 1.19, 0.8, 1.89, 0.09, 0.09, 0.04, 0.09, 0.45, 0.09, 0.04, 0.09, 3.96,                       6.35, 0.04, 0.04],
    'Heterogeneity': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23.08, 0, 0, 0, 50, 0, 0, 0, 0, 93.88, 92.78, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 36.36, 58.33, 64.29, 0, 0, 76.92, 61.54, 0, 0, 33.33, 33.33, 2.01, 16.67, 33.33, 33.33, 0, 0, 0, 0, 0, 0, 40, 0, 0,                       0, 91.67, 23.08, 0, 0],
    'Contig': [5, 1, 9, 28, 17, 20, 15, 219, 1, 1, 4, 0, 14, 20, 35, 22, 1, 1, 96, 102, 1, 0, 2, 3, 481, 399, 15, 89, 0, 0,
               28, 0, 21, 20, 66, 40, 35, 38, 75, 26, 467, 455, 148, 41, 8, 8, 36, 641, 7, 8, 30, 71, 7, 3, 18, 47, 6, 3, 18, 47, 47, 65, 19, 27],
    'Size': [5, 4.7, 4.8, 4.8, 9.8, 9.8, 9.9, 9.8, 4.6, 4.6, 4.7, 0, 9.5, 9.8, 8.5, 8.3, 3.7, 3.7, 3.5, 3.6, 4, 0, 4.1, 4.1, 7.1,
            6.9, 5.1, 5, 0, 0, 2.6, 0, 11, 11, 11, 12, 6.3, 6.3, 6.1, 6.3, 8.7, 8.6, 9.8, 9.9, 10, 10, 10, 6, 9.9, 10, 9.4, 6.6, 6, 5.6, 5.3, 5.5, 5.6,              5.6, 5.3, 5.5, 5.9, 6.7, 5.3, 5.2],
    'Busco_completeness':[92, 92, 92.3, 92.1, 99.9, 99.9, 99.7, 99.8, 99.4, 99.3, 99.4, 0, 99.7, 99.7, 99.9, 99.9, 92.3, 92.4, 91.6, 92.3, 88.7, 0, 88.7,                          88.7, 88.1, 88.7, 99.4,98.4, 0, 0, 96.6, 0, 99.1, 99.2, 99.6, 99.3, 99.3, 98.7, 99.4, 99.4, 87.6, 86.6, 99.2, 99.5, 99.6, 99.6,                          99.4, 79.6, 99.6, 99.6, 97.8, 98.7, 100, 100, 100, 100, 100, 100, 100, 100, 99.8, 100, 100, 100]



}

for key, value in data.items():
    print(f"Length of '{key}': {len(value)}")

# Create a DataFrame
# Create a DataFrame
df = pd.DataFrame(data)


# Extracting the numerical features for PCA
X = df[['Completeness', 'Contamination', 'Heterogeneity', 'Contig', 'Size', 'Busco_completeness']]

# PCA
pca = PCA(n_components=2)
components = pca.fit_transform(X)

custom_symbols = {
    'Gloeobacter morelensis MG652769_Assembly_1': 'triangle-up',
    'Gloeobacter morelensis MG652769_Assembly1_meta': 'triangle-up',
    'Gloeobacter morelensis MG652769_Assembly2': 'triangle-up',
    'Gloeobacter morelensis MG652769_Assembly2_meta': 'triangle-up',
    'Tolypothrix sp.PCC 7712_Assembly_1': 'triangle-up',
    'Tolypothrix sp. PCC 7712_Assembly_1_meta': 'triangle-up',
    'Tolypothrix sp. PCC 7712_Assembly_2': 'triangle-up',
    'Tolypothrix sp. PCC 7712_Assembly_2_meta': 'triangle-up',
    'Phormidium yuhuli AB48_Assembly_1_meta': 'triangle-up',
    'Phormidium yuhuli AB48_Assembly_1': 'triangle-up',
    'Phormidium yuhuli AB48_Assembly_2': 'triangle-up',
    'Phormidium yuhuli AB48_Assembly_2_meta': 'triangle-up',
    'Nostoc edaphicum CCNP1411_Assembly_1': 'square',
    'Nostoc edaphicum CCNP1411_Assembly_1_meta': 'square',
    'Nostoc edaphicum CCNP1411_Assembly_2': 'square',
    'Nostoc edaphicum CCNP1411_Assembly_2_meta': 'square',
    'Candidatus Paraprochloron terpiosi LD05_Assembly_1': 'square',
    'Candidatus Paraprochloron terpiosi LD05_Assembly_1_meta': 'square',
    'Candidatus Paraprochloron terpiosi LD05_Assembly_2': 'square',
    'Candidatus Paraprochloron terpiosi LD05_Assembly_2_meta': 'square',
    'Anthocerotibacter panamensis C109_Assembly_1': 'diamond',
    'Anthocerotibacter panamensis C109_Assembly_1_meta': 'diamond',
    'Anthocerotibacter panamensis C109_Assembly_2': 'diamond',
    'Anthocerotibacter panamensis C109_Assembly_2_meta': 'diamond',
    'Sphaerospermopsis torques-reginae ITEP-024_Assembly_1': 'circle',
    'Sphaerospermopsis torques-reginae ITEP-024_Assembly_1_meta': 'circle',
    'Sphaerospermopsis torques-reginae ITEP-024_Assembly_2': 'circle',
    'Sphaerospermopsis torques-reginae ITEP-024_Assembly_2_meta': 'circle',
    'Thermostichus lividus PCC 6715_Assembly_1': 'circle',
    'Thermostichus lividus PCC 6715_Assembly_1_meta': 'circle',
    'Thermostichus lividus PCC 6715_Assembly_2': 'circle',
    'Thermostichus lividus PCC 6715_Assembly_2_meta': 'circle',
    'Tolypothrix bouteillei vb52130_Assembly_1': 'square',
    'Tolypothrix bouteillei vb52130_Assembly_1_meta': 'square',
    'Tolypothrix bouteillei vb52130_Assembly_2': 'square',
    'Tolypothrix bouteillei vb52130_Assembly_2_meta': 'square',
    'Myxosarcina sp._Assembly_1': 'diamond',
    'Myxosarcina sp._Assembly_1_meta': 'diamond',
    'Myxosarcina sp._Assembly_2': 'diamond',
    'Myxosarcina sp._Assembly_2_meta':  'diamond',
    'Scytonema tolypothrichoides VB-61278_Assembly_1': 'diamond',
    'Scytonema tolypothrichoides VB-61278_Assembly_1_meta': 'diamond',
    'Scytonema tolypothrichoides VB-61278_Assembly_2': 'diamond',
    'Scytonema tolypothrichoides VB-61278_Assembly_2_meta': 'diamond',
    'Scytonema millei VB51128_Assembly_1': 'circle',
    'Scytonema millei VB511283_Assembly_1_meta': 'circle',
    'Scytonema millei VB511283_Assembly_2': 'circle',
    'Scytonema millei VB511283_Assembly_2_meta': 'circle',
    'Tolypothrix campylonemoides VB511288_Assembly_1': 'circle',
    'Tolypothrix campylonemoides VB511288_Assembly_1_meta': 'circle',
    'Tolypothrix campylonemoides VB511288_Assembly_2': 'circle',
    'Tolypothrix campylonemoides VB511288_Assembly_2_meta': 'circle',
    'cat_1_Assembly_1':'triangle-up',
    'cat_1_Assembly_1_meta':'triangle-up',
    'cat_1_Assembly_2':'triangle-up',
    'cat_1_Assembly_2_meta':'triangle-up',
    'cat_2_Assembly_1':'square',
    'cat_2_Assembly_1_meta':'square',
    'cat_2_Assembly_2':'square',
    'cat_2_Assembly_2_meta':'square',
    'cat_4_Assembly_1':'circle',
    'cat_4_Assembly_1_meta':'circle',
    'cat_4_Assembly_2':'circle',
    'cat_4_Assembly_2_meta':'circle',

 }
    

# Define custom colors for organisms
custom_colors = {
    'Gloeobacter morelensis MG652769_Assembly_1': 'red',
    'Gloeobacter morelensis MG652769_Assembly1_meta': 'blue',
    'Gloeobacter morelensis MG652769_Assembly2': 'blue',
    'Gloeobacter morelensis MG652769_Assembly2_meta': 'blue',
    'Tolypothrix sp.PCC 7712_Assembly_1': 'red',
    'Tolypothrix sp. PCC 7712_Assembly_1_meta': 'grey',
    'Tolypothrix sp. PCC 7712_Assembly_2': 'blue',
    'Tolypothrix sp. PCC 7712_Assembly_2_meta': 'grey',
    'Phormidium yuhuli AB48_Assembly_1_meta': 'blue',
    'Phormidium yuhuli AB48_Assembly_1': 'red',
    'Phormidium yuhuli AB48_Assembly_2': 'blue',
    'Phormidium yuhuli AB48_Assembly_2_meta': 'grey',
    'Nostoc edaphicum CCNP1411_Assembly_1': 'blue',
    'Nostoc edaphicum CCNP1411_Assembly_1_meta': 'red',
    'Nostoc edaphicum CCNP1411_Assembly_2': 'blue',
    'Nostoc edaphicum CCNP1411_Assembly_2_meta': 'blue',
    'Candidatus Paraprochloron terpiosi LD05_Assembly_1': 'blue',
    'Candidatus Paraprochloron terpiosi LD05_Assembly_1_meta': 'red',
    'Candidatus Paraprochloron terpiosi LD05_Assembly_2': 'grey',
    'Candidatus Paraprochloron terpiosi LD05_Assembly_2_meta': 'grey',
    'Anthocerotibacter panamensis C109_Assembly_1': 'blue',
    'Anthocerotibacter panamensis C109_Assembly_1_meta': 'grey',
    'Anthocerotibacter panamensis C109_Assembly_2': 'blue',
    'Anthocerotibacter panamensis C109_Assembly_2_meta': 'red',
    'Sphaerospermopsis torques-reginae ITEP-024_Assembly_1': 'grey',
    'Sphaerospermopsis torques-reginae ITEP-024_Assembly_1_meta': 'grey',
    'Sphaerospermopsis torques-reginae ITEP-024_Assembly_2': 'red',
    'Sphaerospermopsis torques-reginae ITEP-024_Assembly_2_meta': 'grey',
    'Thermostichus lividus PCC 6715_Assembly_1': 'grey',
    'Thermostichus lividus PCC 6715_Assembly_1_meta': 'grey',
    'Thermostichus lividus PCC 6715_Assembly_2': 'red',
    'Thermostichus lividus PCC 6715_Assembly_2_meta': 'grey',
    'Tolypothrix bouteillei vb52130_Assembly_1': 'blue',
    'Tolypothrix bouteillei vb52130_Assembly_1_meta': 'red',
    'Tolypothrix bouteillei vb52130_Assembly_2': 'grey',
    'Tolypothrix bouteillei vb52130_Assembly_2_meta': 'grey',
    'Myxosarcina sp._Assembly_1': 'blue',
    'Myxosarcina sp._Assembly_1_meta': 'blue',
    'Myxosarcina sp._Assembly_2': 'grey',
    'Myxosarcina sp._Assembly_2_meta': 'red',
    'Scytonema tolypothrichoides VB-61278_Assembly_1': 'grey',
    'Scytonema tolypothrichoides VB-61278_Assembly_1_meta': 'grey',
    'Scytonema tolypothrichoides VB-61278_Assembly_2': 'grey',
    'Scytonema tolypothrichoides VB-61278_Assembly_2_meta': 'red',
    'Scytonema millei VB51128_Assembly_1': 'blue',
    'Scytonema millei VB511283_Assembly_1_meta': 'blue',
    'Scytonema millei VB511283_Assembly_2': 'red',
    'Scytonema millei VB511283_Assembly_2_meta': 'grey',
    'Tolypothrix campylonemoides VB511288_Assembly_1': 'blue',
    'Tolypothrix campylonemoides VB511288_Assembly_1_meta': 'blue',
    'Tolypothrix campylonemoides VB511288_Assembly_2': 'red',
    'Tolypothrix campylonemoides VB511288_Assembly_2_meta': 'grey',
    'cat_1_Assembly_1':'red',
    'cat_1_Assembly_1_meta':'grey',
    'cat_1_Assembly_2':'grey',
    'cat_1_Assembly_2_meta':'grey',
    'cat_2_Assembly_1':'red',
    'cat_2_Assembly_1_meta':'red',
    'cat_2_Assembly_2':'blue',
    'cat_2_Assembly_2_meta':'blue',
    'cat_4_Assembly_1':'grey',
    'cat_4_Assembly_1_meta':'grey',
    'cat_4_Assembly_2':'red',
    'cat_4_Assembly_2_meta':'blue',

    #'cat_1_Assembly_1':'red',
    #'cat_1_Assembly_1_meta':'grey',
    #'cat_1_Assembly_2':'grey',
    #'cat_1_Assembly_2_meta':'grey',
    #'cat_2_Assembly_1':'grey',
    #'cat_2_Assembly_1_meta':'red',
    #'cat_2_Assembly_2':'blue',
    #'cat_2_Assembly_2_meta':'blue',
    #'cat_4_Assembly_1':'grey',
    #'cat_4_Assembly_1_meta':'grey',
    #'cat_4_Assembly_2':'red',
    #'cat_4_Assembly_2_meta':'blue',
}

# Create a color list based on the Data column
#colors = [custom_colors[data] for data in df['Data']]

# Creating the scatter plot with custom colors for organisms
fig = px.scatter(components, x=0, y=1, color=df['Data'], color_discrete_map=custom_colors,
                 symbol=df['Data'], symbol_map=custom_symbols,
                 title='PCA Visualization of Organisms')


#fig.update_xaxes(range=[-150, 600]), #tickvals=[-80, -50, -20])
#fig.update_yaxes(range=[-20, 130])


# Update legend title and position
# fig.update_traces(showlegend=True)
# fig.update_layout(legend_title_text='Organisms', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))

# Increase the size of the figure
#fig.update_layout(width=1000, height=1000)
# Update legend title and position
fig.update_traces(showlegend=False)

fig.update_xaxes(range=[-69, -25]), #tickvals=[-60, -50, -20])
fig.update_yaxes(range=[-15, -5])


# Save the plot
fig.write_image("pls.pdf")

