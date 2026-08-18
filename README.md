# Héberger Caarangue Yoon sur GitHub Pages (gratuit)

Ce dossier contient tout ce qu'il faut : `index.html` (la plateforme, renommée
depuis `caarangue-yoon.html` — GitHub Pages sert automatiquement le fichier
`index.html` d'un dépôt), `.nojekyll` (désactive un traitement automatique
de GitHub qui n'est pas nécessaire ici et peut parfois casser des fichiers),
et le nécessaire pour les **alertes presse automatiques** (voir plus bas) :
`.github/workflows/news-alerts.yml`, `scripts/fetch_news_alerts.py`,
`requirements.txt` et `news-alerts.json`.

**Important** : glisse-dépose bien **tout le contenu de ce dossier** (pas
seulement `index.html`) lors de l'upload — sinon les alertes presse ne
fonctionneront pas.

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

## Alertes presse automatiques

Le module "🚨 Alertes accidents" du tableau de bord affiche aussi, en plus
des signalements graves/mortels créés dans l'application, des articles de
presse et vidéos YouTube d'actualité sénégalaise mentionnant un accident de
la circulation.

Fonctionnement : le workflow GitHub Actions `.github/workflows/news-alerts.yml`
s'exécute automatiquement toutes les 2 heures (et peut être lancé
manuellement depuis l'onglet **Actions** du dépôt, bouton **Run workflow**).
Il exécute `scripts/fetch_news_alerts.py`, qui va chercher les derniers
articles/vidéos sur quelques flux RSS de presse sénégalaise (SeneNews,
Sénégal7, PresseAfrik, AllAfrica) et flux YouTube (RTS, TFM), garde ceux qui
contiennent un mot-clé lié aux accidents de la route, et écrit le résultat
dans `news-alerts.json`. Le site lit ensuite ce fichier au chargement.

C'est entièrement gratuit (minutes GitHub Actions incluses avec un dépôt
public) et ne nécessite aucune clé API.

Pour ajuster les sources ou les mots-clés : modifie les listes `FEEDS`,
`YOUTUBE_CHANNELS` et `KEYWORDS` en haut de `scripts/fetch_news_alerts.py`,
commit, et la prochaine exécution du workflow prendra en compte le
changement.

Limite à connaître : c'est un filtre par mots-clés simple, pas une analyse
de sens — il peut occasionnellement laisser passer un faux positif ou
manquer un article formulé différemment. Les identifiants des chaînes
YouTube suivies n'ont pas pu être vérifiés en conditions réelles au moment
de la création de ce fichier (accès réseau restreint côté outil utilisé
pour le générer) : si une chaîne ne remonte jamais rien après quelques
jours, vérifie son `channel_id` (voir commentaire dans le script) et
corrige-le au besoin.

## Comptes & rôles réels (Supabase, gratuit)

Par défaut, la page « Paramètres → Rôle de démonstration » et le bouton
« + Nouveau compte » sont des **simulations** (rien n'est sauvegardé, pas
de vrai mot de passe, pas de vraie sécurité) — c'est explicitement indiqué
sur la page. Le fichier contient déjà tout le code pour activer un
véritable système de comptes, gratuit, via [Supabase](https://supabase.com)
(un service qui fournit une base de données + une authentification sécurisée
gratuitement pour ce genre de projet). Il ne manque que la configuration,
que je ne peux pas faire à ta place (création de compte tiers) :

1. **Crée un compte Supabase** sur [supabase.com](https://supabase.com)
   (gratuit, avec ton email ou GitHub) et crée un nouveau projet (choisis
   une région proche, par ex. Europe). Note le mot de passe de base de
   données que Supabase te propose de générer — garde-le de côté.
2. Une fois le projet créé, va dans **SQL Editor** (menu de gauche), clique
   **New query**, colle **tout le contenu** du fichier `supabase-setup.sql`
   fourni dans ce dossier, puis clique **Run**. Cela crée la table des
   comptes et les règles de sécurité nécessaires.
3. Va dans **Project Settings → API**. Tu y trouveras deux valeurs à me
   transmettre (ou à coller toi-même dans `index.html`) :
   - **Project URL** (ex. `https://xxxxx.supabase.co`)
   - **anon public key** (une longue chaîne commençant par `eyJ...`) — c'est
     une clé **publique**, prévue pour être dans le code du site, ce n'est
     pas un mot de passe.

   ⚠️ Ne partage **jamais** la « `service_role` key » (une autre clé visible
   sur la même page) — celle-ci donne un accès total à la base de données et
   ne doit jamais apparaître dans un site.
4. Dans `index.html`, cherche (tout en haut du `<script>` principal, juste
   après les balises `<script src=...leaflet...>` etc.) :
   ```js
   var SUPABASE_URL = 'REPLACE_ME_SUPABASE_URL';
   var SUPABASE_ANON_KEY = 'REPLACE_ME_SUPABASE_ANON_KEY';
   ```
   et remplace les deux valeurs par celles obtenues à l'étape 3, puis publie
   le fichier mis à jour sur GitHub Pages comme d'habitude.
5. Ouvre le site : un écran de connexion apparaît désormais. Clique
   **Créer un compte**, inscris-toi avec ton propre email. Ton compte est
   créé avec le rôle « Agent de terrain » et le statut « En attente ».
6. Retourne dans Supabase, **SQL Editor**, et exécute (en remplaçant
   l'email par le tien) :
   ```sql
   update public.profiles set role = 'Administrateur', statut = 'Actif'
   where email = 'ton-email@exemple.com';
   ```
   C'est la seule fois où un rôle se change « à la main » dans la base —
   ensuite, tout se fait depuis la page **Comptes & rôles** du site.
7. Recharge le site et connecte-toi : tu es maintenant Administrateur.
   Depuis **Administration → Comptes & rôles**, tu vois la liste réelle des
   comptes (plus les 5 lignes de démonstration) et tu peux changer le rôle
   ou le statut de chacun avec les menus déroulants — les changements sont
   immédiatement sauvegardés dans Supabase.
8. Pour ajouter quelqu'un d'autre : demande-lui de créer lui-même son compte
   via **Créer un compte** sur l'écran de connexion. Son compte apparaît
   dans **Comptes & rôles** avec le statut « En attente » ; attribue-lui le
   rôle voulu et passe son statut à « Actif ».

Tant que `SUPABASE_URL`/`SUPABASE_ANON_KEY` ne sont pas renseignées, le site
continue de fonctionner exactement comme avant (mode démonstration, rôle
choisi manuellement) — aucune régression si tu ne fais pas cette étape tout
de suite.

**Limite à connaître** : la couche gratuite de Supabase suffit largement
pour ce type d'usage (jusqu'à 50 000 utilisateurs actifs mensuels, base de
données incluse), sans carte bancaire à renseigner à l'inscription — mais
comme pour tout service tiers, vérifie les conditions/tarifs actuels sur
supabase.com si le nombre de comptes ou d'utilisation grossit beaucoup.

## Bon à savoir

- C'est un hébergement **gratuit et illimité en durée**, sans carte
  bancaire à renseigner.
- Le dépôt doit rester **public** pour que Pages soit gratuit sur un compte
  GitHub personnel standard (les dépôts privés + Pages gratuits ne sont
  disponibles que sur les comptes GitHub Pro/organisation).
- Cette plateforme reste un fichier HTML autonome pour les **signalements** :
  sans configuration Supabase supplémentaire (voir plus haut, qui ne couvre
  que les comptes/rôles), chaque visiteur a sa propre session en mémoire —
  les signalements créés ne sont pas partagés entre utilisateurs, ni
  sauvegardés d'une visite à l'autre. Si tu veux qu'un signalement créé par
  un agent soit visible par les autres aussi, il faudrait étendre la même
  base Supabase à une table "signalements" — dis-le moi si c'est ce qu'il te
  faut, c'est une suite logique naturelle à ce qui vient d'être mis en place
  pour les comptes.
