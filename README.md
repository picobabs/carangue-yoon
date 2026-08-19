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

## Signalements réels et partagés (Supabase, même base)

En plus des comptes/rôles, les **signalements** (les accidents créés via
« + Nouveau signalement ») sont maintenant, eux aussi, sauvegardés dans la
même base Supabase et partagés entre tous les comptes connectés — un agent
qui crée un signalement le voit apparaître pour un superviseur connecté sur
un autre appareil, et il reste disponible après un rechargement de la page.

Si `SUPABASE_URL`/`SUPABASE_ANON_KEY` sont déjà configurées (voir la section
précédente), il ne reste qu'une seule étape :

1. Dans **Supabase → SQL Editor → New query**, colle **tout le contenu** du
   fichier `supabase-setup-signalements.sql` fourni dans ce dossier, puis
   clique **Run**. Cela crée la table `signalements` et ses règles de
   sécurité (RLS) : tout compte connecté et actif peut voir tous les
   signalements ; chacun ne peut créer un signalement qu'en son propre nom ;
   seuls Superviseur/Administrateur peuvent le valider, le rejeter ou changer
   son statut ; seul un Administrateur peut le supprimer définitivement —
   les mêmes règles que dans l'interface.
2. Publie le `index.html` fourni (déjà mis à jour) sur GitHub Pages comme
   d'habitude. C'est tout — aucune autre configuration.

**Ce qui est déjà réel et partagé** : les données du formulaire de
signalement (lieu, date, gravité, météo, coordonnées GPS, etc.), la création,
la validation/le rejet, et la suppression.

**Ce qui reste local pour l'instant** (par choix, pour avancer par étapes) :
les **photos, croquis et documents joints** à un signalement restent
uniquement dans le navigateur de la personne qui les a ajoutés (pas encore
envoyés à Supabase) ; les données détaillées de **véhicules et victimes**
associées à un signalement restent également en mémoire locale ; de même,
l'**historique de validation** (qui a validé/rejeté et quand) affiché dans le
détail d'un signalement n'est pas encore sauvegardé dans la base — il peut
donc disparaître au rechargement de la page pour un signalement réel. Les
anciennes données de démonstration et l'historique Gendarmerie restent, eux,
des données de référence locales, non migrées. Chacune de ces étapes peut
être ajoutée par la suite de la même façon, si besoin.

## Bon à savoir

- C'est un hébergement **gratuit et illimité en durée**, sans carte
  bancaire à renseigner.
- Le dépôt doit rester **public** pour que Pages soit gratuit sur un compte
  GitHub personnel standard (les dépôts privés + Pages gratuits ne sont
  disponibles que sur les comptes GitHub Pro/organisation).
- Si `SUPABASE_URL`/`SUPABASE_ANON_KEY` sont configurées **et** que
  `supabase-setup-signalements.sql` a été exécuté (voir la section
  « Signalements réels et partagés » plus haut), les signalements sont
  partagés entre utilisateurs et sauvegardés en base. Sans cette étape,
  chaque visiteur garde sa propre session en mémoire (rien de partagé ni
  sauvegardé). Les photos/croquis/documents et les données véhicules/
  victimes restent, dans tous les cas, locales pour l'instant.
