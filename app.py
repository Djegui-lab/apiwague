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


st.title("Application web pour l'analyse de données( en temps réel )")

# Afficher les données dans une table
st.write("AUTEUR : DJEGUI-WAUE")

data=pd.DataFrame(data)
st.write(data)


#convertir tous les colonnes de ma base de données en (int) et ignorer la colonne chaine de caractère
data_complet= data.astype(int, errors='ignore')
data_complet.to_csv("new_csv", index=False)
data_int=pd.read_csv("new_csv")



#supprimer la première colonne 
data_new = data.drop(data.columns[0], axis=1)
# Convertir toutes les colonnes en type int (si possible)
data_new = data_new.astype(int, errors='ignore')
data_new.to_csv("nouveau_data.csv", index=False)
defo= pd.read_csv("nouveau_data.csv")
st.title(" statistique descriptive de la base de données :")
st.dataframe(defo.describe().style.background_gradient(cmap="Reds"))


# Laisser l'utilisateur choisir la colonne de tri
colonne_tri = st.selectbox("Sélectionnez la colonne de tri :", defo.columns)

# Laisser l'utilisateur choisir l'ordre de tri
ordre_tri = st.radio("Sélectionnez l'ordre de tri :", ('Ascendant', 'Descendant'))

# Effectuer le tri en fonction des sélections de l'utilisateur
if ordre_tri == 'Ascendant':
    data_trie = defo.sort_values(by=colonne_tri, ascending=True)
else:
    data_trie = defo.sort_values(by=colonne_tri, ascending=False)

# Afficher les données triées
st.write("Données triées :")
st.write(data_trie)



# matrice de correlation
correlation=defo[["Ventes","Fiches","Contrats","CB1","CB2","Prime_mensuelle","TotalFrais"]].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation,annot=True, cmap='coolwarm',linewidths=0.1)
st.title("Matrice de corellation :")
st.subheader("Ventes__Fiches__Contrats_CB1__CB2_Prime_mensuelle_TotalFrais")
st.pyplot(plt.gcf())






# Convertir la colonne "Ventes" en nombres entiers
#data['Ventes'] = data['Ventes'].str.replace(',', '').astype(int)

    # Création d'un graphique à barres avec Matplotlib
# Création d'un graphique à barres avec Matplotlib en spécifiant les couleurs
colors = ['blue', 'green', 'red', 'purple', 'orange', 'pink', 'brown', 'gray', 'cyan', 'magenta']
plt.figure(figsize=(10, 6))
bars = plt.bar(data_int['Nom'], data_int['Ventes'], color=colors)
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



# Analyser les données
#st.write("Analyse des ventes par courtier :")
total_ventes = analyze_data(data)


# Créer un graphique à barres avec Pandas
bar_chart = st.bar_chart(total_ventes.set_index('Nom'))

# Ajouter des couleurs personnalisées au graphique
bar_chart.plotly_chart({
    'data': [
        {
            'x': total_ventes['Nom'],
            'y': total_ventes['Ventes'],
            'type': 'bar',
            'marker': {'color': ['red', 'green', 'blue', 'yellow', 'purple','red', 'green', 'blue', 'yellow', 'purple','red', 'green', 'blue', 'yellow', 'purple','red', 'green', 'blue', 'yellow', 'purple','red', 'green', 'blue', 'yellow', 'purple','red', 'green', 'blue', 'yellow', 'purple']}  # Vous pouvez spécifier les couleurs ici
        }
    ],
    'layout': {
        'xaxis': {'title': 'Courtier'},
        'yaxis': {'title': 'Ventes'},
        'title': 'Ventes par courtier'
    }
})



import pandas as pd
import sqlite3


# Créer une connexion à la base de données (SQLite en l'occurrence)
conn = sqlite3.connect('ma_base_de_donnees.db')

# Utiliser la fonction to_sql de pandas pour insérer les données dans une table
data_int.to_sql('vente', conn, if_exists='replace', index=False)
# Exécutez une requête SQL pour afficher toutes les données de la table "vente"
cursor = conn.cursor()
cursor.execute('SELECT * FROM vente')
rows = cursor.fetchall()

# Affichez les données dans un DataFrame Streamlit
df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
st.subheader("Base de données Sqlite :")
st.dataframe(df.head())
descriptives= df.describe()

cursor.execute('''SELECT Nom, Ventes FROM vente WHERE Ventes >= (SELECT AVG(Ventes) FROM Vente);''')
recevoir= cursor.fetchall()
# Affichez les données dans un DataFrame Streamlit
new_df = pd.DataFrame(recevoir, columns=[desc[0] for desc in cursor.description])
st.title(" les courtiers qui ont effectués des ventes >= a la moyenne des ventes")
st.subheader(" details des VENTES/COURTIERS :")
st.write(new_df)




tendance_vente=cursor.execute('''SELECT strftime('%Y-%m', datetime('now', 'localtime')) AS mois_actuel, SUM(Ventes) AS total_ventes
FROM vente;
''')
avoir= cursor.fetchall()
new_d = pd.DataFrame(avoir, columns=[desc[0] for desc in cursor.description])

if st.button("AFFICHER LE TOTAL DES VENTES 0CTOBRE-2023"):
    st.write(new_d)


# Fermer la connexion
conn.close()






















