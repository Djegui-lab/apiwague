import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd 
import plotly.express as px
import requests




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






image_pathe = "djegui_wag.jpg"
largeur_image = 200
# Utilisation de st.image pour afficher l'image
st.sidebar.image(image_pathe, caption="AUTEUR /DJEGUI_WAGUE")


st.sidebar.write("Bienvenue dans l'interface utilisateur de mon application d'analyse des données.")
st.sidebar.write("Avec mon application, vous pouvez explorer et tirer des informations exploitables à partir de vos données stockées. Ma solution combine efficacement récupération, affichage et analyse de données pour vous fournir une compréhension approfondie et des statistiques robustes sur vos opérations.")

st.sidebar.write("Caractéristiques clés :")
st.sidebar.write("1. Importation de données en un clic : Vous pouvez rapidement importer des données à partir de vos feuilles de calcul, en éliminant les tracas de la préparation des données.")
st.sidebar.write("2. Visualisation interactive : Notre interface conviviale vous permet de visualiser vos données sous forme de graphiques, de tableaux et de rapports pour une compréhension visuelle.")
st.sidebar.write("3. Statistiques puissantes : Notre application offre une suite complète d'outils d'analyse statistique, vous permettant d'identifier des tendances, de détecter des modèles et de prendre des décisions éclairées.")
st.sidebar.write("4. Personnalisation : Vous pouvez personnaliser votre expérience en choisissant les données à analyser et les statistiques à générer en fonction de vos besoins spécifiques.")
st.sidebar.write("5. Partage de rapports : Vous pouvez partager facilement les résultats de vos analyses avec vos collègues ou collaborateurs pour une collaboration efficace.")




# Image à afficher (le chemin est relatif au script)
image_path = "djegui_wag.jpg"

# Créer deux colonnes (colonne de gauche et colonne de droite)
col1, col2 = st.columns([3, 1])


# Éléments dans la colonne de droite (affiche l'image)
with col2:
    st.image(image_path, caption="AUTEUR / DJEGUI_WAGUE")





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







# Sélection du courtier pour afficher les détails
selected_courtier = st.selectbox('Sélectionnez un courtier:', data_int['Nom'].unique())

# Affichage des détails du courtier sélectionné
st.write('Détails du courtier sélectionné:')
selected_data = data[data['Nom'] == selected_courtier]
st.write(selected_data)




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





# Créez une connexion à la base de données
conn = sqlite3.connect('ma_base_de_donnees.db')
cursor = conn.cursor()

# Calculez la moyenne totale de toutes les ventes
cursor.execute("SELECT AVG(Ventes) FROM Vente")
moyenne_totale = cursor.fetchone()[0]

# Sélectionnez les noms et les moyennes des ventes pour chaque nom
cursor.execute("SELECT Nom, AVG(Ventes) FROM Vente GROUP BY Nom")

# Créez une liste pour stocker les résultats
resultats = []

# Parcourez les résultats et ajoutez les noms dont la moyenne des ventes est supérieure à la moyenne totale à la liste
for row in cursor.fetchall():
    nom, moyenne_ventes = row
    if moyenne_ventes > moyenne_totale:
        resultats.append({"Nom": nom, "Moyenne des ventes": moyenne_ventes})

# Fermez la connexion à la base de données
conn.close()

# Affichez les résultats sous forme de tableau avec le widget st.dataframe
st.write("Les Courtiers dont le chiffre d'affaire moyen est superieur au CA moyen total :")
if resultats:
    df = pd.DataFrame(resultats)
    st.dataframe(df)
else:
    st.write("Aucun résultat trouvé.")






# Créez une connexion à la base de données
conn = sqlite3.connect('ma_base_de_donnees.db')
cursor = conn.cursor()

tendance_vente=cursor.execute('''SELECT strftime('%Y-%m', datetime('now', 'localtime')) AS mois_actuel, SUM(Ventes) AS total_ventes
FROM vente;
''')
avoir= cursor.fetchall()
new_d = pd.DataFrame(avoir, columns=[desc[0] for desc in cursor.description])

if st.button("AFFICHER LE TOTAL DES VENTES "):
     st.write(new_d)

# Fermer la connexion
conn.close()


st.write("")
st.write("")
st.write("")


groupby_column = st.selectbox(
    "QU'AIMERIEZ-VOUS ANALYSER ?",
    (  'Fiches', 'ID','Contrats', 'CB1', 'CB2', 'Prime_mensuelle', 'TotalFrais'),
)


output_columns = ['CB1', 'Ventes']  # Mettez les colonnes que vous voulez ici
# -- GROUP DATAFRAME
df_grouped = defo.groupby(by=[groupby_column], as_index=False)[output_columns].mean()


fig = px.bar(
    df_grouped,
    x=groupby_column,  # Mettez votre colonne ici
    y='Ventes',  # Modifiez la colonne y si nécessaire
    color='CB1',  # Modifiez la colonne de couleur si nécessaire
    color_continuous_scale=['red', 'purple', 'yellow','blue'],
    template='plotly_white',
    title=f'<b> VENTES & CB1 by {groupby_column}</b>'

)
st.subheader("AUTEUR : Mr DJEGUI-WAGUE")

st.plotly_chart(fig)

st.write(f'VENTES & CB1 by {groupby_column} :')

st.dataframe(df_grouped)






# Fonction pour calculer les statistiques pour un courtier donné
def calcule_statistiques_courtier(Nom):
    # Créez une connexion à la base de données (remplacez 'ma_base_de_donnees.db' par le nom de votre base de données)
    conn = sqlite3.connect('ma_base_de_donnees.db')
    cursor = conn.cursor()

    # Recherchez l'ID du courtier en fonction de son nom
    cursor.execute('SELECT ID FROM vente WHERE Nom = ?', (Nom,))
    result = cursor.fetchone()

    if result:
        courtier_id = result[0]
        cursor.execute('SELECT SUM(Ventes), AVG(Ventes), MIN(Ventes), MAX(Ventes), SUM(Fiches), SUM(CB1) FROM vente WHERE ID=?', (courtier_id,))
        rows = cursor.fetchall()
        mlp = pd.DataFrame(rows, columns=["Somme des Ventes", "Moyenne des Ventes", "Minimum des ventes", "Maximum des Ventes", "Total_Fiches","Total_CB1"])
        st.write(f"Statistiques pour {Nom}:")
        st.write(mlp)
    else:
        st.write(f"Aucun résultat trouvé pour le courtier {Nom}.")

    # Fermez la connexion à la base de données
    conn.close()

# Créez une interface utilisateur avec un selectbox pour la sélection du nom
selection = st.selectbox("Courtier :", data_int["Nom"].unique(), key='Nom')

# Appelez la fonction pour calculer les statistiques en fonction de la sélection
calcule_statistiques_courtier(selection)
#calcule_statistiques_courtier("SOUFIANE")
#calcule_statistiques_courtier("DJEGUI")






# Regrouper les données par ID et calculer la somme des ventes pour chaque ID
sales_by_id = data_int.groupby('Nom')['Ventes'].sum().reset_index()

# Liste de couleurs personnalisées pour chaque ID
custom_colors = ['red', 'green', 'blue', 'yellow', 'purple', 'red', 'green', 'blue', 'yellow', 'purple', 
                 'red', 'green', 'blue', 'yellow', 'purple', 'red', 'green', 'blue', 'yellow', 'purple', 'red', 'green', 'blue', 'yellow', 'purple', 'red', 'green', 'blue', 'yellow', 'purple', 'red', 'green', 'blue', 'yellow', 'purple', 'red', 'green', 'blue', 'yellow', 'purple', 'red', 'green', 'blue', 'yellow', 'purple', 'red', 'green', 'blue', 'yellow', 'purple', 'red', 'green', 'blue', 'yellow', 'purple']


# Créer une application Streamlit
st.subheader("Chiffre d'affaires total par Courtier :")

# Créer le graphique interactif à barres avec Plotly et utiliser les couleurs personnalisées
fig = px.bar(sales_by_id, x='Nom', y='Ventes', labels={'Nom': 'Nom', 'Ventes': "Chiffre d'affaires total (en milliers d'euros)"})
fig.update_traces(marker=dict(color=custom_colors))  # Utiliser les couleurs personnalisées

# Afficher le graphique interactif
st.plotly_chart(fig)

# Afficher le tableau de données (en option)
st.dataframe(sales_by_id)

# Pour exécuter l'application Streamlit, utilisez la commande suivante dans votre terminal :
# streamlit run nom_du_fichier.py
st.subheader("Base de données pour chaque nouveau enregistrement : ")
st.write(data_int)





# Charger les données à partir d'un fichier CSV (ou de votre source de données)

# Fonction pour l'analyse
def analyse_courtier(data, nom, colonne_analyse):
    filtered_data = data_int[data_int['Nom'] == nom]
    
    if not filtered_data.empty:
        st.write(f"Résultats de l'analyse pour '{nom}' dans la colonne {colonne_analyse} :")
        st.write(filtered_data)
        
        # Statistiques récapitulatives pour la colonne choisie
        st.subheader(f"Statistiques pour '{nom}' dans la colonne {colonne_analyse} :")
        if colonne_analyse in ['Ventes', 'Fiches', 'CB1', 'CB2','Contrats']:
            st.write(f"Moyenne de {colonne_analyse} : {filtered_data[colonne_analyse].mean()}")
            st.write(f"Somme de {colonne_analyse} : {filtered_data[colonne_analyse].sum()}")
            st.write(f"Médiane de {colonne_analyse} : {filtered_data[colonne_analyse].median()}")
    else:
        st.write(f"Aucun résultat trouvé pour le courtier '{nom}' dans la colonne {colonne_analyse}.")

# Titre de l'application
st.title("Analyse de données robuste :")
st.title("choisir le courtier en fonction de la colonne que vous souhaitez")

# Choix du nom de courtier
selected_name = st.selectbox("Choisissez un nom de courtier :", data_int['Nom'].unique(), key="selected_name")

# Choix de la colonne de filtrage
column_to_filter = st.selectbox("Choisissez la colonne de filtrage :", data_int.columns, key="column_to_filter")

# Appel de la fonction d'analyse
analyse_courtier(data_int, selected_name, column_to_filter)






import streamlit as st
import requests

WEBHOOK_URL = "https://connect.pabbly.com/workflow/sendwebhookdata/IjU3NjUwNTY4MDYzNzA0MzI1MjY0NTUzNzUxMzci_pc"

# Fonction pour envoyer des données au webhook en utilisant l'argument unpacking
def post_to_webhook(**data):
    response = requests.post(WEBHOOK_URL, json=data)
    return response

# Fonction pour réinitialiser les champs du formulaire
def reset_form_state():
    return {"Nom": "", "Ventes": "", "Fiches": "", "Contrats": "", "CB1": "",
            "CB2": "", "Primme_mensuelle": "", "TotalFrais": "", "ID": "", "Statut-Contrat": ""}

# Sidebar content
st.sidebar.title("Ajouter une nouvelle donnée :🚗")

# Initialiser le formulaire dans la session si ce n'est pas déjà fait
if "form_state" not in st.session_state:
    st.session_state.form_state = reset_form_state()

# Form in the sidebar
with st.sidebar.form(key="idea_form"):
    st.session_state.form_state["Nom"] = st.text_input("Name (optional)", value=st.session_state.form_state["Nom"], placeholder="Your Name")
    st.session_state.form_state["Ventes"] = st.text_input("VENTES (optional)", value=st.session_state.form_state["Ventes"], placeholder="Vente_journalière")
    st.session_state.form_state["Fiches"] = st.text_input("FICHES", value=st.session_state.form_state["Fiches"], placeholder="Nombres de Fiches ...")
    st.session_state.form_state["Contrats"] = st.text_input("contrat (optional)", value=st.session_state.form_state["Contrats"], placeholder="Nombres de contrat souscrit")
    st.session_state.form_state["CB1"] = st.text_input("CB1 (optional)", value=st.session_state.form_state["CB1"], placeholder="Montant CB1")
    st.session_state.form_state["CB2"] = st.text_input("CB2 (optional)", value=st.session_state.form_state["CB2"], placeholder="Montant CB2")
    st.session_state.form_state["Primme_mensuelle"] = st.text_input("Montant Prime_mensuelle (optional)", value=st.session_state.form_state["Primme_mensuelle"], placeholder="Prime_mensuelle")
    st.session_state.form_state["TotalFrais"] = st.text_input("total frais (optional)", value=st.session_state.form_state["TotalFrais"], placeholder="Montant Frais")
    st.session_state.form_state["ID"] = st.text_input("ID (optional)", value=st.session_state.form_state["ID"], placeholder="Code_courtier")
    # Multiselect pour Statut-Contrat
    selected_statut_contrat = st.multiselect("Statut-Contrat", ["validé", "retracté"], placeholder="Statut-Contrat")
    st.session_state.form_state["Statut-Contrat"] = selected_statut_contrat

    submit_button = st.form_submit_button(label="Envoyé 🚀")

# Handle form submission
if submit_button:
    if not st.session_state.form_state["Fiches"].strip():
        st.error("Please enter a video idea. 💡")
    else:
        data = st.session_state.form_state
        response = post_to_webhook(**data)
        if response.status_code == 200:
            st.success("Thanks for your submission! 🌟")

            # Réinitialiser les champs du formulaire après la soumission
            st.session_state.form_state = reset_form_state()

            # Mettez à jour les statistiques ici en utilisant les données du formulaire
            # Par exemple, vous pouvez afficher les statistiques dans une zone spécifique de votre application
            st.subheader("Statistiques mises à jour en temps réel")
            st.write(f"Total des fiches : {data['Fiches']}")
            st.write(f"Total des contrats : {data['Contrats']}")
            st.write(f"Total des ventes : {data['Ventes']}")

            # Forcer le réexécution de l'application pour la mise à jour en temps réel
            st.experimental_rerun()

        else:
            st.error("There was an error. Please try again. 🛠️")

# Main content
st.title("🎬 OBTENIR VOTRE DEVIS ")
st.markdown("""
🚗 Commencez Votre Voyage Sans Souci Aujourd'hui!
""")
st.markdown("""
Confidentialité Assurée: Vos données sont sécurisées et traitées avec la plus grande confidentialité. Urgence Assurances s'engage à protéger vos informations.
""")
