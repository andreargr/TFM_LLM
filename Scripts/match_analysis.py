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

def calculate_metrics(type): #obtain exhaustivity or f1-score for each ontology
    if type == 'CL':
        df = data_process('contribution_file_CL.json')
        suffixes = ['CLO', 'CL', 'UBERON', 'BTO']
        false_neg_data = {'CLO':1,'CL':0,'UBERON':2,'BTO':4}
    elif type == 'CT':
        df = data_process('contribution_file_CT.json')
        suffixes = ['CL', 'UBERON', 'BTO']
        false_neg_data = {'CLO':0,'CL':1,'UBERON':0,'BTO':16}
    elif type == 'A':
        df = data_process('contribution_file_A.json')
        suffixes = ['UBERON', 'BTO']
        false_neg_data = {'CLO':0,'CL':0,'UBERON':0,'BTO':1}
    elif type == 'dash':
        df = df_dash
        suffixes = ['CLO', 'CL', 'UBERON', 'BTO']
        false_neg_data = None
    else:
        raise ValueError("Tipo no reconocido")

    accuracies ={}
    exhaust = None if type == 'dash' else {}
    f1 = None if type == 'dash' else {}
    
    for suffix in suffixes:
        true_col = f'{suffix}_C'
        pred_col = f'{suffix}_M'
        true_pos=0
        false_pos = 0
        false_neg = 0 if false_neg_data is None else false_neg_data[suffix]
        if true_col in df.columns and pred_col in df.columns:
            for i in range(len(df)):
                if df.iloc[i][true_col] == df.iloc[i][pred_col]:
                    true_pos += 1
                else : 
                    false_pos +=1
            if type != 'dash':
                exhaust_values= true_pos/(true_pos+false_neg)
                f1_values= 2*true_pos/(2*true_pos+false_neg+false_pos)
                exhaust[suffix] = exhaust_values
                f1[suffix] = f1_values
            accuracy= true_pos/(true_pos+false_pos)
            accuracies[suffix] = accuracy
        else:
            if type != 'dash':
                exhaust[suffix] = None
                f1[suffix] = None
            accuracies[suffix] = None
    return accuracies, exhaust, f1 

def plot_metrics(type): #visualize plots
    accuracy, exhaust, f1 = calculate_metrics(type)
    metric=input("Indique 1 si quiere visualizar la precisión. \n Indique 2 si desea visualizar la exhaustividad. \n Indique 3 si desea visualizar F1-score. \n")
    if metric == '1':
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
    elif metric == '2':
        if exhaust is None:
            print("Exhaust metrics not calculated for type: dash")
            return
        df_exhaust = pd.DataFrame([exhaust], index=[0])

        colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon','#D8BFD8']
        ax = df_exhaust.plot(kind='bar', rot=0, figsize=(10, 6), color=colors)
        ax.set_ylim(0,1.2)
        # Configuration
        ax.set_title('Exhaustividad por tipo')
        ax.set_xlabel('Ontologías')
        ax.set_ylabel('Exhaustividad')

        # Text position
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.3f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
        # Show graph
        plt.show()
    elif metric == '3':
        if f1 is None:
            print("F1-score metrics not calculated for type: dash")
            return
        df_f1 = pd.DataFrame([f1], index=[0])

        colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon','#D8BFD8']
        ax = df_f1.plot(kind='bar', rot=0, figsize=(10, 6), color=colors)

        ax.set_ylim(0,1)
        # Configuration
        ax.set_title('F1-score por tipo')
        ax.set_xlabel('Ontologías')
        ax.set_ylabel('F1-score')

        # Text position
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.3f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
        # Show graph
        plt.show()


# plot_metrics('CL')
# plot_metrics('CT')
# plot_metrics('A')
plot_metrics('dash')


