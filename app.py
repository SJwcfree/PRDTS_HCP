# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------
# CONFIGURATION DE LA PAGE
# ----------------------------
st.set_page_config(page_title="📊 Tableau de Suivi de la Pauvreté", layout="wide")
st.title("📊 Tableau de Suivi de la Réduction de la Pauvreté Multidimensionnelle (2014 → 2024)")
st.markdown("### 🇲🇦 Analyse régionale du Maroc – Données actualisées 2024")

# ----------------------------
# CHARGEMENT DES DONNÉES
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("pauvrete_regions.csv", sep=';', decimal=',', encoding='latin-1')
    df = df.dropna(subset=['Région'])  # Suppression de la ligne "Total général" si présente
    return df

df = load_data()

# Calculs
df['% Évolution'] = (df['Evo vers P5P6'] / df['CR']) * 100
df['P5P6 Avant (%)'] = (df['avant'] / df['CR']) * 100
df['P5P6 Fin (%)'] = (df['fin22'] / df['CR']) * 100
df['Δ P5P6 (pts)'] = df['P5P6 Fin (%)'] - df['P5P6 Avant (%)']
df['Δ IPM Absolu'] = df['IPM 2014'] - df['IPM 2024']
df['Δ IPM Relatif (%)'] = (df['Δ IPM Absolu'] / df['IPM 2014']) * 100
df['Δ TP Relatif (%)'] = (df['TP 2014'] - df['TP 2024']) / df['TP 2014'] * 100

# ----------------------------
# KPIs NATIONAUX
# ----------------------------
st.subheader("🌍 KPIs Nationaux (2014 → 2024)")

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("🔹 Total Communes (CR)", "1 256", "")
with col2: st.metric("🔹 % Évolution vers P5P6", "53.9%", "↑")
with col3: st.metric("🔹 Part P5P6 (2024)", "48.15%", "↑ +23.15 pts")
with col4: st.metric("🔹 IPM (2024)", "0.0610", "↓ 45.6%")

# ----------------------------
# VISUALISATIONS
# ----------------------------
st.subheader("📈 Évolution Régionale")

# 1. Barres combinées
fig1 = px.bar(df, x='Région', y=['% Évolution', 'P5P6 Fin (%)'],
              title="📊 % Évolution vers P5P6 & Part finale en P5P6",
              barmode='group', text_auto=True, color_discrete_sequence=["#00BFC4", "#F8766D"])
fig1.update_layout(xaxis_tickangle=-45, showlegend=True)
st.plotly_chart(fig1, use_container_width=True)

# 2. Dumbbell IPM
fig2 = px.dumbbell(df, x=['IPM 2014', 'IPM 2024'], y='Région',
                   title="📉 Évolution de l'IPM (2014 → 2024)",
                   color_discrete_sequence=["#F8766D", "#00BFC4"])
fig2.update_layout(xaxis_title="Indice de pauvreté multidimensionnelle")
st.plotly_chart(fig2, use_container_width=True)

# 3. Slope Chart P5P6
fig3 = px.line(df, x='Région', y=['P5P6 Avant (%)', 'P5P6 Fin (%)'],
               title="📈 Évolution de la part des communes en P5P6",
               markers=True, line_shape='spline', text_auto=True)
fig3.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig3, use_container_width=True)

# 4. Waterfall – Augmentation P5P6
st.subheader("🧮 Augmentation de la Part P5P6 (Nationale)")
delta = 604 - 314
fig4 = go.Figure(go.Waterfall(
    x=["P5P6 (2014)", "Augmentation", "P5P6 (2024)"],
    y=[314, delta, 604],
    text=["314", "+290", "604"],
    connector={"line": {"color": "rgb(30, 30, 30)"}}
))
fig4.update_layout(title="Augmentation de la part en P5P6 (2014 → 2024)", 
                   xaxis_title="", yaxis_title="Nombre de communes")
st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# TABLEAU DES RÉGIONS
# ----------------------------
st.subheader("📋 Classements Régionaux")

# Top 3 évolutions
top_evol = df.nlargest(3, '% Évolution')[['Région', '% Évolution', 'Δ P5P6 (pts)', 'Δ IPM Relatif (%)', 'TP 2024']]
st.write("### 🏆 Meilleurs performeurs (Évolution)")
st.dataframe(top_evol.style.format({
    '% Évolution': '{:.1f}%',
    'Δ IPM Relatif (%)': '{:.1f}%',
    'TP 2024': '{:.2f}%'
}))

# Top 3 TP 2024
worst_tp = df.nlargest(3, 'TP 2024')[['Région', 'TP 2024', '% Évolution', 'Δ P5P6 (pts)']]
st.write("### ⚠️ Régions avec TP le plus élevé (2024)")
st.dataframe(worst_tp.style.format({
    'TP 2024': '{:.2f}%',
    '% Évolution': '{:.1f}%',
    'Δ P5P6 (pts)': '{:.1f} pts'
}))

# ----------------------------
# EXPORT & INFO
# ----------------------------
st.markdown("---")
st.markdown("### 🔗 Export & Partage")
st.markdown("- [📥 Télécharger les données au format CSV](pauvrete_regions.csv)")
st.markdown("- [🔗 Lien vers le dashboard en ligne](https://your-dashboard-streamlit.app)")

st.markdown("### 📝 Informatique")
st.code("""
1. Créer un dossier `dashboard-pauvrete-maroc`
2. Copier les fichiers ici
3. Exécuter : pip install streamlit pandas plotly
4. Lancer : streamlit run app.py
""", language="bash")