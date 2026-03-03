# Analyse de Graphe de Bâtiment 🏢

## Description

Ce projet analyse la structure d'un bâtiment modélisée sous forme de **graphe** où :
- **Les nœuds** représentent les **intersections** (carrefours, pièces, jonctions)
- **Les arêtes** représentent les **couloirs** (passages, corridors reliant les intersections)

L'objectif est d'analyser différentes propriétés du bâtiment pour des questions de sécurité, surveillance et accessibilité.

---

## Fonctionnalités principales

### 1. **Intersections Critiques** 🔴
Identifie les nœuds **"points d'articulation"** du bâtiment. Si une intersection critique est fermée, le bâtiment se divise en plusieurs zones isolées.

**Utilité :** Déterminer les zones stratégiques pour les pompiers, évacuations, ou maintenance.

### 2. **Couloirs Vitaux** 🚪
Détecte les arêtes **"isthmes"** du bâtiment. Si un couloir vital est bloqué, le bâtiment se divise en plusieurs zones isolées.

**Utilité :** Identifier les passages critiques pour la circulation.

### 3. **Emplacement optimisé des caméras** 📹
Calcule un **ensemble dominant minimal** : le nombre minimum de caméras nécessaires pour surveiller tout le bâtiment.

Une caméra surveillée à une intersection voit :
- L'intersection elle-même
- Tous les couloirs adjacents

**Utilité :** Optimiser le coût des caméras de surveillance.

### 4. **Zones à fort affluence (ZUC)** 🔥
Trouve toutes les **cliques maximales** du graphe : les groupes d'intersections entièrement interconnectées.

Ces zones représentent des lieux **très densément connectés** où beaucoup de gens circulent.

**Utilité :** Planifier la signalétique, l'éclairage, la sécurité.

### 5. **Propriétés globales du bâtiment** 📊
Affiche des informations générales :
- **Connexité** : Le bâtiment est-il entièrement connecté ?
- **Diamètre** : Distance maximale entre deux intersections
- **Densité** : Densité du réseau de couloirs

---

## Architecture du code

### Structures de données

```python
edges          # Liste des arêtes (couloirs)
nodes          # Ensemble des nœuds (intersections)
Gnx            # Graphe NetworkX
pos            # Positions pour la visualisation
```

### Fonctions utilitaires

| Fonction | Description |
|----------|-------------|
| `is_articulation_point(G, node)` | Vérifie si un nœud est un point d'articulation |
| `is_isthme(G, edge)` | Vérifie si une arête est un isthme |
| `initVF(nodes, edges)` | Crée le voisinage fermé pour chaque nœud |
| `minimum_dominating_set(nodes, edges)` | Calcule l'ensemble dominant minimal (caméras) |
| `creer_pos_pour_edges(edges)` | Génère les positions pour la visualisation |
| `suppDeList(l1, l2)` | Supprime les éléments de l2 de l1 |

### Fonctions d'affichage

| Fonction | Description |
|----------|-------------|
| `afficheInfo()` | Affiche toutes les informations du graphe |
| `afficheInterSect()` | Visualise les intersections critiques |
| `afficheLesCamera()` | Visualise l'emplacement optimal des caméras |
| `afficheZuc()` | Visualise les zones ultra-connectées |
| `afficheLesCouloirsVitaux()` | Visualise les couloirs vitaux |

---

## Usage

### Installation des dépendances

```bash
pip install networkx matplotlib graphviz
```

### Lancer le programme

```bash
python main.py
```

Un menu interactif apparaît :

```
Que Voulez-vous afficher ?
[1] - Information sur le graph
[2] - Intersections Critiques
[3] - Emplacement optimisée des caméra
[4] - Zone à fort affluence
[5] - Couloirs vitaux
[6] - Quittez
```

---

## Exemple de résultat

### Plan du bâtiment
Le bâtiment contient :
- **34 intersections** (nœuds)
- **47 couloirs** (arêtes)
- **Connexité** : OUI (le bâtiment est entièrement connecté)
- **Diamètre** : Distance maximale entre deux intersections

### Visualisation

Les graphiques utilisent un code couleur :
- 🔴 **Rouge** : Point critique / élément important
- ⚫ **Gris** : Éléments normaux
- 🟠 **Autres couleurs** : Zones ultra-connectées

---

## Complexité algorithmique

| Algorithme | Complexité |
|-----------|-----------|
| Points d'articulation | O(V + E) |
| Isthmes | O((V + E) × E) |
| Ensemble dominant minimal | O(3^V) (backtracking) |
| Cliques maximales | Exponentielle |

---

## Améliorations possibles

- [ ] Ajouter des poids aux arêtes (distance en mètres)
- [ ] Calculer les itinéraires optimaux
- [ ] Gérer les étages du bâtiment
- [ ] Interface graphique améliorée
- [ ] Export des résultats en fichier

---

## Auteur

Projet de analyse de graphe - BUT Informatique S2

---

## Licence

Libre d'utilisation pour fins éducatives.