import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd 
import plotly.express as px





def load_data():
    # Définissez les autorisations et l'accès au fichier JSON de clé d'API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("test-wague-9a205da3c6ca.json", scope)

    # Authentification avec les informations d'identification
    gc = gspread.authorize(credentials)

    # Ouvrir la feuille de calcul par son nom ou URL
    # Remplacez "Nom de votre feuille" par le nom de votre propre feuille ou l'URL
    worksheet = gc.open("courtier").sheet1

    # Lire les données de la feuille de calcul
    data = worksheet.get_all_values()

    # Convertir les données en un DataFrame pandas
    df = pd.DataFrame(data[1:], columns=data[0])

    return df

data = load_data()


st.title("Application de données Google Sheets avec Streamlit")




# Afficher les données dans une table
st.write("Données depuis Google Sheets :")
data=pd.DataFrame(data)
st.write(data)




# Convertir la colonne "Ventes" en nombres entiers
data['Ventes'] = data['Ventes'].str.replace(',', '').astype(int)

    # Création d'un graphique à barres avec Matplotlib
# Création d'un graphique à barres avec Matplotlib en spécifiant les couleurs
colors = ['blue', 'green', 'red', 'purple', 'orange', 'pink', 'brown', 'gray', 'cyan', 'magenta']
plt.figure(figsize=(10, 6))
bars = plt.bar(data['Nom'], data['Ventes'], color=colors)
plt.xlabel("Nom")
plt.ylabel("Chiffre d'affaires (en milliers d'euros)")
plt.title("Chiffre d'affaires par courtier")
plt.xticks(rotation=45, ha="right")
st.pyplot(plt)

 # Création d'un graphique à barres horizontal avec Seaborn

fig, ax = plt.subplots()
sns.barplot(x='Ventes', y='Nom', data=data,  ax=ax)
ax.set_xlabel("Chiffre d'affaires (en milliers d'euros)")
ax.set_ylabel('Courtier')
plt.title("Chiffre d'affaires par courtier")
st.pyplot(fig)

# Sélection du courtier pour afficher les détails
selected_courtier = st.selectbox('Sélectionnez un courtier:', data['Nom'])

# Affichage des détails du courtier sélectionné
st.write('Détails du courtier sélectionné:')
selected_data = data[data['Nom'] == selected_courtier]
st.write(selected_data)






# Fonction d'analyse de données
def analyze_data(data):
    # Exemple d'analyse : Calcul de la somme des ventes par courtier
    total_ventes = data.groupby('Nom')['Ventes'].sum().reset_index()
    return total_ventes


st.write(data)

# Analyser les données
st.write("Analyse des ventes par courtier :")
total_ventes = analyze_data(data)
st.write(total_ventes)

# Créer un graphique à barres avec Pandas
bar_chart = st.bar_chart(total_ventes.set_index('Nom'))

# Ajouter des couleurs personnalisées au graphique
bar_chart.plotly_chart({
    'data': [
        {
            'x': total_ventes['Nom'],
            'y': total_ventes['Ventes'],
            'type': 'bar',
            'marker': {'color': ['red', 'green', 'blue', 'yellow', 'purple','red', 'green', 'blue', 'yellow', 'purple','red', 'green', 'blue', 'yellow', 'purple','red', 'green', 'blue', 'yellow', 'purple','red', 'green', 'blue', 'yellow', 'purple','red']}  # Vous pouvez spécifier les couleurs ici
        }
    ],
    'layout': {
        'xaxis': {'title': 'Courtier'},
        'yaxis': {'title': 'Ventes'},
        'title': 'Ventes par courtier'
    }
})















