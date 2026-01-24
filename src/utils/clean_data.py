import pandas as pd

def clean_my_data(input_file):
    df = pd.read_csv(input_file, sep=';')

    needed_cols = ['id', 'prix_valeur', 'prix_nom', 'region', 'geom']
    df = df[needed_cols]

    df = df.dropna(subset=['prix_valeur', 'region', 'geom'])

    df['prix_valeur'] = pd.to_numeric(df['prix_valeur'], errors='coerce')


    df.to_csv('cleaned_data.csv', index=False)
    print("Le data est nettoyé.")

if __name__ == "__main__":
    clean_my_data('prix-des-carburants-en-france.csv')
    
