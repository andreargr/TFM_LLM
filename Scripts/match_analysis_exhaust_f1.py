import json #use json data
import pandas as pd #dataframe manipulation
import matplotlib.pyplot as plt #data visualization

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
    else:
        raise ValueError("Tipo no reconocido")

    exhaust = {}
    f1 ={}
    for suffix in suffixes:
        true_col = f'{suffix}_C'
        pred_col = f'{suffix}_M'
        true_pos=0
        false_pos = 0
        false_neg = false_neg_data[suffix]
        if true_col in df.columns and pred_col in df.columns:
            for i in range(len(df)):
                if df.iloc[i][true_col] == df.iloc[i][pred_col]:
                    true_pos += 1
                else : 
                    false_pos +=1
            exhaust_values= true_pos/(true_pos+false_neg)
            f1_values= 2*true_pos/(2*true_pos+false_neg+false_pos)

            exhaust[suffix] = exhaust_values
            f1[suffix] = f1_values
            print(suffix,true_pos,false_pos,false_neg)
        else:
            exhaust[suffix] = None
            f1[suffix] = None
    return exhaust, f1 


def plot_metrics(type,metric): #visualize plots
    exhaust,f1 = calculate_metrics(type)
    if metric == 'exhaust':
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

    if metric == 'f1':
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
    
plot_metrics('CL','exhaust')
plot_metrics('CT','exhaust')
plot_metrics('A','exhaust')

# plot_metrics('CL','f1')
# plot_metrics('CT','f1')
# plot_metrics('A','f1')

