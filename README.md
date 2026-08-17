# Héberger Caarangue Yoon sur GitHub Pages (gratuit)

Ce dossier contient tout ce qu'il faut : `index.html` (la plateforme, renommée
depuis `caarangue-yoon.html` — GitHub Pages sert automatiquement le fichier
`index.html` d'un dépôt) et `.nojekyll` (désactive un traitement automatique
de GitHub qui n'est pas nécessaire ici et peut parfois casser des fichiers).

## Option A — sans ligne de commande (le plus simple)

1. Va sur [github.com](https://github.com) et crée un compte si tu n'en as
   pas (gratuit).
2. Clique sur **New repository** (bouton vert en haut à droite, ou
   [github.com/new](https://github.com/new)).
   - Nom du dépôt : par exemple `caarangue-yoon` (le nom choisi devient une
     partie de l'adresse finale).
   - Laisse-le **Public** (obligatoire pour Pages gratuit sur un compte
     personnel standard).
   - Ne coche aucune case d'initialisation (pas de README, pas de licence).
   - Clique **Create repository**.
3. Sur la page qui s'affiche, clique **uploading an existing file**.
4. Glisse-dépose les deux fichiers de ce dossier (`index.html` et
   `.nojekyll`) dans la zone d'upload.
5. En bas, clique **Commit changes**.
6. Va dans l'onglet **Settings** du dépôt, puis **Pages** (menu de gauche).
7. Sous **Build and deployment → Source**, choisis **Deploy from a branch**.
8. Sous **Branch**, choisis **main** et **/ (root)**, puis **Save**.
9. Attends une à deux minutes, puis rafraîchis la page : l'URL de ton site
   s'affiche en haut (du type
   `https://<ton-pseudo>.github.io/caarangue-yoon/`).

## Option B — avec git (si tu es à l'aise avec la ligne de commande)

```bash
cd caarangue-yoon-pages
git init
git add .
git commit -m "Publication de Caarangue Yoon"
git branch -M main
git remote add origin https://github.com/<ton-pseudo>/caarangue-yoon.git
git push -u origin main
```

Puis répète les étapes 6 à 9 de l'option A (activer Pages dans les réglages
du dépôt).

## Mettre à jour le site plus tard

- **Option A** : reviens dans le dépôt sur GitHub, ouvre `index.html`,
  clique sur l'icône crayon (Edit), colle le nouveau contenu, puis **Commit
  changes**. Le site se met à jour automatiquement en 1-2 minutes.
- **Option B** : remplace le fichier `index.html` localement, puis
  `git add index.html && git commit -m "Mise à jour" && git push`.

## Bon à savoir

- C'est un hébergement **gratuit et illimité en durée**, sans carte
  bancaire à renseigner.
- Le dépôt doit rester **public** pour que Pages soit gratuit sur un compte
  GitHub personnel standard (les dépôts privés + Pages gratuits ne sont
  disponibles que sur les comptes GitHub Pro/organisation).
- Cette plateforme est un fichier HTML autonome, sans base de données
  partagée : chaque visiteur a sa propre session en mémoire (les
  signalements créés ne sont pas partagés entre utilisateurs, ni
  sauvegardés d'une visite à l'autre). Si tu veux qu'un signalement créé
  par un agent soit visible par les autres, il faudra ajouter un vrai
  backend (base de données + API), ce qui dépasse le simple hébergement
  statique — dis-le moi si c'est ce qu'il te faut, on peut regarder les
  options gratuites adaptées (Supabase, Firebase, etc.).
