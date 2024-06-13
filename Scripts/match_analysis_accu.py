import json #use json data
import pandas as pd #dataframe manipulation
import matplotlib.pyplot as plt #data visualization

from class_names import df_dash

def data_process(filename): #convert json to a dataframe
    with open(filename, 'r') as archivo:
        dicc_clases = json.load(archivo)
    df = pd.DataFrame.from_dict(dicc_clases, orient='index')
    nueva_fila = pd.DataFrame([df.columns], columns=df.columns)
    df_process = pd.concat([nueva_fila, df], ignore_index=True)
    df_process.columns = ['CLO_C','CLO_M', 'CL_C','CL_M', 'UBERON_C','UBERON_M','BTO_C','BTO_M']
    df_process = df_process.drop(0)
    
    claves=[]
    for clave in dicc_clases.keys():
        claves.append(clave)
    df_process['Label'] = claves #add label column
    
    df_process.fillna("", inplace=True) #replace 'Nonetype' values

    return df_process


def calcular_match(type): #calculate perfect match for each ontology
    if type == 'CL':
        df = data_process('contribution_file_CL.json')
        col_1 = 'CLO'
        col_2 = 'BTO'
    elif type == 'CT':
        df = data_process('contribution_file_CT.json')
        col_1 = 'CL'
        col_2 = 'BTO'
    elif type == 'A':
        df = data_process('contribution_file_A.json')
        col_1 = 'UBERON'
        col_2 = 'BTO'
    elif type == 'dash':
        return 0
    else:
        raise ValueError("Tipo no reconocido")

    perfect_match = 0
    no_perfect_match = 0

    control_1= f'{col_1}_C'
    control_2= f'{col_2}_C'
    prueba_1= f'{col_1}_M'
    prueba_2= f'{col_2}_M'  

    for index, row in df.iterrows():
        string1a = row[control_1]
        string2a = row[prueba_1]
        string1b = row[control_2]
        string2b = row[prueba_2]
        if string1a == string2a and string1b == string2b:
            perfect_match += 1
        else: 
            no_perfect_match += 1

    total = perfect_match + no_perfect_match
    indice_pm= perfect_match / total
    return indice_pm

def calculate_accuracy(type):  #obtain accuracy for each ontology
    if type == 'CL':
        df = data_process('contribution_file_CL.json')
        suffixes = ['CLO', 'CL', 'UBERON', 'BTO']
    elif type == 'CT':
        df = data_process('contribution_file_CT.json')
        suffixes = ['CL', 'UBERON', 'BTO']
    elif type == 'A':
        df = data_process('contribution_file_A.json')
        suffixes = ['UBERON', 'BTO']
    elif type == 'dash':
        df = df_dash
        suffixes = ['CLO', 'CL', 'UBERON', 'BTO']
    else:
        raise ValueError("Tipo no reconocido")

    accuracies = {}
    for suffix in suffixes:
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


def plot_metrics(type): #visualize plots
    accuracy = calculate_accuracy(type)
    df_accuracy = pd.DataFrame([accuracy], index=[0])
    df_accuracy['Perfect_match'] = calcular_match(type)
    num_bars = len(df_accuracy.columns)

    colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon','#D8BFD8']
    ax = df_accuracy.plot(kind='bar', rot=0, figsize=(10, 6), color=colors)

    ax.bar(num_bars-1, df_accuracy['Perfect_match'].values[0], color='red', label='Perfect_match')
    ax.set_ylim(0,1)
    # Configuration
    ax.set_title('Precisión por tipo')
    ax.set_xlabel('Ontologías')
    ax.set_ylabel('Indice de precisión')

    # Text position
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.3f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    # Show graph
    plt.show()

#plot_metrics('CL')
#plot_metrics('CT')
plot_metrics('A')
#plot_metrics('dash')


