import pandas as pd #dataframe manipulation
import matplotlib.pyplot as plt #data visualization

from df_comparation import df_comparation_gpt3_5, df_comparation_gpt4, df_comparation_ft

def get_accuracy(df): #obatin the accuracy for each ontology 
    for columna in df:
        df[columna] = df[columna].fillna('unknown')
    
    suffixes = ['CLO', 'CL', 'UBERON', 'BTO']

    accuracies = {}
    for suffix in suffixes: #for each ontology the accuracy is calculated
        true_col = f'{suffix}_C'
        pred_col = f'{suffix}_M'
        true_pos=0
        false_pos = 0
        if true_col in df.columns and pred_col in df.columns:
            for i in range(len(df)):
                if df.iloc[i][true_col] == df.iloc[i][pred_col]:
                    true_pos += 1
                else : 
                    false_pos +=1
            accuracy= true_pos/(true_pos+false_pos)
            accuracies[suffix] = accuracy
        else:
            accuracies[suffix] = None
    return accuracies

def plot_accuracies(model): #visualization accuracy
    accuracy = get_accuracy(model)
    ontologies = list(accuracy.keys())
    valores = list(accuracy.values())

    colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon']

    plt.figure(figsize=(10, 6))
    plt.bar(ontologies, valores, color=colors)

    #add title and labels 
    plt.xlabel('Ontología')
    plt.title('Precisión de por ontología')
    plt.ylabel('Índice de Precisión')

    #obtain the values for each bar
    for i, valor in enumerate(valores):
        plt.text(i, valor + 0.01, f'{valor:.3f}', ha='center')

    plt.ylim(0, 1) 
    plt.show()

plot_accuracies(df_comparation_ft)
# plot_accuracies(df_comparation_gpt3_5, 'accuracy')
# plot_accuracies(df_comparation_gpt4, 'accuracy')


