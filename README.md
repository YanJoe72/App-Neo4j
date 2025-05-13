# Backend Neo4j – API Flask

Ce projet expose une API REST construite avec **Flask**, connectée à une base de données **Neo4j**. Il permet d’exécuter des requêtes Cypher via des endpoints REST, testables avec Postman.

---

## Prérequis

- Python 3.8+
- Docker
- Postman

---

## 🛠 Installation et démarrage

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/mon-back-neo4j.git
cd mon-back-neo4j
```

### 2. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

### 3. Lancer l'application
```bash
python app.py
```

## Création du conteneur Neo4j
```bash
docker run --name neo4j -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j
```

## 🌐 Interface web Neo4j

- Interface web Neo4j : [http://localhost:7474](http://localhost:7474)
- Identifiants :
  - **Username** : `neo4j`
  - **Password** : `password`

---

## 📬 Tester les routes avec Postman

### 1. Ouvrir Postman

Téléchargez Postman ici : [https://www.postman.com/downloads/](https://www.postman.com/downloads/)

### 2. Importer la collection de requêtes

- Cliquez sur **"Import"**
- Glissez-déposez ou sélectionnez le fichier `.json` de collection fourni (ex : `Curl Query.json`)
- Une fois importée, vous pouvez exécuter directement les requêtes (GET, POST, etc.) vers : [http://localhost:5000](http://localhost:5000)

