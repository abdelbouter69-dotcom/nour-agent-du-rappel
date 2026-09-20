# Nour — l'Agent du Rappel
## Cahier des charges (conception) — version 3

*Document destiné à être remis à Claude Code pour démarrer la construction.*

---

## 0. En bref (à lire en premier)

On construit un agent IA personnel de rappels, nommé **Nour**, hébergé dans le cloud et joignable partout dans le monde.

**Ce qu'on construit maintenant (Phase 1)** : un système qui envoie automatiquement à une seule personne (Abdelkader) un message 15 à 20 minutes avant chaque prière, contenant le rappel de la prière et le rappel du siwak, avec la salutation complète, dans la bonne langue, et en tenant compte du lieu où il se trouve.

**Ce qu'on ne construit pas encore** : le multicanal complet, le clonage pour d'autres personnes, les agents par projet, la version pour personnes en situation de handicap. Tout cela vient après validation de la Phase 1.

**Consigne de méthode, importante :** ne pas se jeter sur le code. Préparer d'abord les quatre fichiers de fondation décrits en section 5, puis seulement construire.

---

## 1. Présentation générale

**Nom du projet :** l'Agent du Rappel
**Prénom de l'agent :** Nour

**Objectif :** un agent IA personnel capable d'envoyer des rappels, d'écrire des messages et de relancer des personnes. On commence par un modèle unique testé en conditions réelles sur son créateur (Abdelkader), avant de le dupliquer pour d'autres utilisateurs.

**Méthode :** construire petit, tester sur soi, valider, puis élargir. Pas de généralisation avant que le modèle de base fonctionne de façon fiable pendant plusieurs jours d'affilée.

---

## 2. Contrainte fondatrice : un agent qui voyage

Nour doit être **joignable de n'importe où dans le monde**, sans dépendre d'un ordinateur allumé ni d'un réseau local. C'est la contrainte qui structure toute l'architecture :

- Nour tourne **dans le cloud**, en permanence, pas en local sur le PC.
- Il reste joignable depuis le téléphone, en tout lieu et à toute heure.
- Les horaires de prière doivent **suivre les déplacements** : la même journée passée à Villefranche-sur-Saône ou à Tlemcen ne donne pas les mêmes heures.
- Les canaux retenus doivent fonctionner à l'international, sans dépendre d'un opérateur local.

Cette contrainte a une conséquence directe sur les clés d'accès (section 5.3) : elles ne peuvent pas rester sur l'ordinateur personnel, elles vivront sur le serveur.

---

## 3. Automatisation ou agent : ce que Nour doit être

Distinction essentielle, à garder en tête pendant toute la construction :

- Une **automatisation** applique une règle fixe et donne un résultat prévisible. Zéro décision, zéro surprise.
- Un **agent** lit, interprète et choisit selon la situation. Il reçoit un but, pas des étapes.

**La Phase 1 de Nour est une automatisation, et doit le rester.** Un rappel de prière part à une heure calculée, avec un texte de structure fixe. On ne veut surtout pas qu'un modèle improvise l'heure du Maghrib ou reformule la salutation à sa façon. C'est plus fiable, plus simple et sans coût de modèle à chaque envoi.

**La partie agent arrive en Phase 3**, quand Nour devra interpréter : « je suis à Tlemcen » (changer de ville), « reporte de dix minutes », « relance untel » (choisir le ton selon la personne).

Le bon modèle final : **l'agent décide, l'automatisation exécute.** Le code doit donc séparer proprement ces deux couches dès le départ, même si la couche agent reste vide en Phase 1.

### 3.1 Les outils de Nour (ses « bras »)

Un modèle de langage, seul, ne fait rien : il lit du texte et produit du texte. Il ne clique pas, n'envoie rien, ne range rien. Ce qui le rend capable d'agir, ce sont les outils qu'on lui donne.

Ces outils doivent être écrits dès la Phase 1, comme des fonctions autonomes et testables — c'est l'automatisation. En Phase 3, la couche agent viendra simplement les appeler quand elle aura décidé de le faire. Le même outil sert donc aux deux couches, ce qui évite de tout réécrire plus tard.

Les outils de Nour, par ordre de nécessité :

| Outil | Ce qu'il fait | Phase |
|---|---|---|
| `envoyer_message` | Envoie un texte sur le canal retenu | 1 |
| `recuperer_horaires` | Interroge l'API des horaires pour une position et une date | 1 |
| `lire_carnet` / `ecrire_carnet` | Lit et met à jour les réglages et la position courante | 1 |
| `consulter_journal` | Relit ce qui a été envoyé, pour éviter les doublons | 1 |
| `changer_position` | Reçoit un nom de ville (lu dans une réponse email), met à jour le carnet et recalcule les horaires | 1 |
| `reporter_rappel` | Décale un rappel à la demande de l'utilisateur | 3 |
| `ecrire_email` | Rédige et envoie un email pour le compte de l'utilisateur | 2 |
| `relancer_personne` | Envoie un message de relance à un tiers | 2 |

En Phase 3, la couche agent fonctionnera en boucle : elle reçoit un objectif, l'interprète, décide et agit en appelant ces outils, puis vérifie le résultat et recommence si besoin.

---

## 4. Phase 1 — périmètre précis

### 4.1 Ce qui est dans le périmètre

| # | Fonction | Détail |
|---|---|---|
| 1 | Récupération des horaires de prière | Pour la position courante de l'utilisateur, une fois par jour |
| 2 | Envoi d'un rappel avant chaque prière | 15 à 20 minutes avant l'heure (délai réglable) |
| 3 | Rappel du siwak intégré | Dans le même message que le rappel de prière, pas à part |
| 4 | Salutation complète en ouverture | *as-salāmu ʿalaykum wa raḥmatu Llāhi wa barakātuh* |
| 5 | Message en français | Les versions arabe et anglaise sont prévues dans la structure mais peuvent arriver juste après |
| 6 | Un seul canal de communication | Celui retenu en section 6.2 |
| 7 | Un seul utilisateur | Abdelkader, en conditions réelles |
| 8 | Journal des envois | Pour vérifier après coup ce qui est parti, et à quelle heure |

### 4.2 Ce qui est hors périmètre pour l'instant

Multicanal simultané, clonage pour d'autres personnes, interface web d'administration, rappels autres que la prière et le siwak, synthèse vocale, agents séparés par projet, version accessibilité.

Ces éléments sont documentés plus bas pour que l'architecture ne les rende pas impossibles, mais ils **ne doivent pas être développés en Phase 1**.

---

## 5. Les quatre fichiers de fondation (à écrire AVANT de coder)

L'erreur classique est de se jeter sur la construction. On procède comme un architecte : les plans d'abord, les murs ensuite. Quatre fichiers sont à écrire avant la première ligne de code fonctionnel.

### 5.1 Le manuel — `CLAUDE.md`

Le livret d'accueil de Nour, relu au début de chaque session de travail. Il contient :

- Qui est Nour, quel est son rôle, pour qui il travaille.
- Sa manière de s'exprimer : salutation complète en ouverture, ton posé et bref, un rappel et pas un sermon.
- Les langues qu'il parle et dans quel ordre de priorité.
- Ce qu'il ne fait jamais : inventer un horaire, insister au-delà de la prière suivante, envoyer deux fois le même rappel.
- Les règles du projet : Phase 1 = automatisation pure, pas d'appel à un modèle pour un rappel de routine.

### 5.2 Le carnet — `MEMORY.md`

Ce que Nour retient d'une fois sur l'autre, pour ne jamais redemander deux fois la même chose. Dit une fois aujourd'hui, appliqué tout seul demain et les jours suivants. Il contient :

- La ville et les coordonnées courantes de l'utilisateur, et depuis quand.
- Les réglages retenus : délai de rappel, méthode de calcul, école juridique, canal.
- Les décisions prises en cours de route et les problèmes déjà rencontrés.

### 5.3 Le trousseau — `.env`

Une ligne par service, chaque clé ouvrant une porte, jamais partagée ni déposée dans le code.

**Adaptation importante pour Nour :** dans le modèle d'origine, ce fichier ne quitte jamais l'ordinateur personnel. Ici, Nour tourne dans le cloud, donc les clés doivent vivre sur le serveur, dans son gestionnaire de variables d'environnement. Elles ne doivent jamais être écrites dans le code, ni envoyées sur un dépôt de code.

### 5.4 Les recettes — les skills

La méthode est dans la recette, pas dans la tête ni éparpillée dans le code. Pour Nour, au minimum une recette « rédiger un rappel de prière » décrivant la structure exacte du message, la salutation, la place du siwak, le ton, et la variante par langue.

Intérêt concret : le jour où tu veux ajuster le ton, tu modifies la recette et non le programme. Et le jour où tu clones Nour pour quelqu'un d'autre, tu changes la recette sans toucher à la mécanique.

### 5.5 Ordre de travail

1. Écrire le manuel.
2. Écrire le carnet.
3. Mettre en place le trousseau.
4. Écrire les recettes.
5. **Seulement là**, construire.

---

## 6. Briques techniques recommandées

### 6.1 Horaires de prière

**Recommandation : l'API AlAdhan** (`api.aladhan.com`), gratuite et sans clé d'API.

- Endpoint principal : `GET /v1/timings/{date}` avec `latitude`, `longitude`, `method`.
- Variante par ville : `GET /v1/timingsByCity/{date}` avec `city`, `country`.
- Paramètre `method` : choix de la méthode de calcul (liste disponible via `GET /v1/methods`).
- Paramètre `school` : `0` = Shafi'i, `1` = Hanafi (affecte le calcul du 'Asr).

C'est cette API qui permet à Nour de fonctionner **partout dans le monde**, puisqu'elle calcule les horaires à partir de coordonnées géographiques.

**Complément possible : Mawaqit.** Mawaqit n'expose pas d'API publique officielle, mais des API REST communautaires existent (projets open source qui interrogent mawaqit.net et ses 8000+ mosquées). Intérêt : quand Abdelkader est chez lui, Nour peut coller exactement aux horaires de **sa** mosquée plutôt qu'à un calcul théorique. Approche conseillée : Mawaqit quand on est dans une ville couverte et choisie, AlAdhan partout ailleurs et en secours.

### 6.2 Canal de communication — point d'attention important

| Canal | Coût | Mise en place | Verdict |
|---|---|---|---|
| **Email** | Gratuit ou quasi | Simple, via Gmail ou un service SMTP | **Retenu pour la Phase 1** |
| **Telegram** | Gratuit | Créer un bot en quelques minutes, aucune validation | Possible, écarté car peu consulté |
| **WhatsApp** | Payant au message | Compte WhatsApp Business + prestataire + **modèles à faire approuver** | À viser pour la phase de diffusion, pas pour le test |
| **SMS** | Payant, variable selon le pays | Prestataire à contracter | À écarter pour l'instant |

Précision sur WhatsApp : depuis 2025, les messages **envoyés à l'initiative de l'agent** — ce qu'est exactement un rappel de prière — sont facturés à l'unité et doivent passer par des modèles préalablement approuvés. Pour cinq rappels par jour, cela représente environ 1 800 messages par an et par personne : supportable pour une personne, beaucoup moins dès qu'on clone l'agent.

**Décision retenue : l'email pour la Phase 1.** Abdelkader consulte Gmail chaque jour — un rappel qui arrive sur un canal qu'on ne regarde pas ne sert à rien. L'email est gratuit, mondial, et suffisamment précis pour un rappel de prière. WhatsApp reste l'objectif de la phase de diffusion, quand l'agent sera prouvé et destiné à d'autres personnes.

L'architecture doit isoler l'envoi derrière une couche unique, facile à remplacer : passer de l'email à WhatsApp ne devra toucher qu'un seul endroit du code.

### 6.3 Hébergement et déclenchement

**Décision retenue : un petit serveur cloud toujours allumé**, de l'ordre de quelques euros par mois. C'est ce qui garantit à la fois la précision horaire et l'indépendance vis-à-vis du PC personnel.

Deux besoins distincts à y faire tourner :

1. **Une tâche quotidienne** (par exemple à 3 h du matin) qui récupère les horaires du jour et les met en cache.
2. **Un déclencheur précis** qui envoie le message au bon moment, calculé à partir du cache.

À éviter absolument : les planificateurs gratuits dont l'heure d'exécution peut dériver de plusieurs minutes. Pour un rappel calé sur l'heure de prière, cinq minutes de retard rendent l'agent inutile.

Sur les outils d'automatisation visuels type n8n : utiles pour des chaînes de tâches complexes, mais disproportionnés pour cinq rappels par jour. Un petit programme sur un serveur toujours allumé fera la même chose, en plus léger et moins cher. À reconsidérer si Nour devient beaucoup plus riche en tâches.

### 6.4 Stockage

Une base de données légère suffit en Phase 1, mais la structure doit déjà être pensée « multi-utilisateurs » pour que le clonage ultérieur ne demande pas de tout réécrire.

---

## 7. Données à conserver

Par utilisateur : identité et langue préférée, position courante (coordonnées ou ville + pays), fuseau horaire, méthode de calcul et école juridique, délai de rappel, canal et identifiant de contact, prières concernées, date du dernier changement de position.

Par envoi : prière concernée, horaire prévu, horaire réel d'envoi, canal, statut (envoyé / échoué), message d'erreur éventuel.

Ce journal sert autant à diagnostiquer les problèmes qu'à **éviter les doublons** si le système redémarre.

---

## 8. Contenu et forme des messages

- Ouverture systématique par la salutation complète : *as-salāmu ʿalaykum wa raḥmatu Llāhi wa barakātuh*.
- Corps du message : nom de la prière, heure exacte, temps restant.
- Rappel du siwak intégré au même message, formulé avec sobriété.
- Ton : posé, respectueux, bref. Un rappel, pas un cours.
- Structure prévue pour trois langues dès la conception, même si seul le français est livré en Phase 1 : les textes vivent dans la recette et dans un fichier de traductions, jamais écrits en dur dans le code.
- **Voix (pour plus tard, hors Phase 1) :** voix masculine, posée et respectueuse.

---

## 9. Localisation : comment Nour sait où tu es

**Règle posée par l'utilisateur : Nour doit se régler sur la situation géographique du téléphone.** Les horaires doivent suivre l'endroit où il se trouve, pas une ville figée dans un fichier.

**Solution retenue : répondre par email à l'un des messages de Nour.** Quand Abdelkader change de ville, il répond simplement à un email de Nour avec un texte du type « je suis à Tlemcen ». Nour lit cette réponse, reconnaît le nom de la ville, met à jour son carnet et confirme par retour d'email.

Fonctionnement :

1. Abdelkader reçoit un rappel de Nour par email et y répond avec le nom de la nouvelle ville (ex. : « je suis à Tlemcen »).
2. Nour lit la réponse, identifie le nom de la ville, met à jour les coordonnées dans son carnet, et confirme par un email de retour (« horaires calés sur Tlemcen »).
3. Tant qu'aucune nouvelle ville n'est indiquée, Nour garde la dernière connue. Position par défaut au démarrage : Villefranche-sur-Saône.

En Phase 1, la reconnaissance reste volontairement basique (repérer un nom de ville dans le corps de l'email, sans appel à un modèle). L'interprétation fine viendra avec la couche agent, en Phase 3.

**Garde-fou utile :** si la position n'a pas changé depuis longtemps alors que les horaires reçus semblent incohérents avec le fuseau habituel, Nour peut envoyer un email de confirmation plutôt que d'envoyer des rappels potentiellement faux.

---

## 10. Robustesse : que faire quand ça casse

- **Horaires récupérés à l'avance.** Téléchargés une fois par jour et stockés. Si l'API est indisponible au moment d'envoyer, le rappel part quand même, à partir du cache.
- **Si la récupération quotidienne échoue**, réessais espacés, puis repli sur les horaires de la veille en signalant l'approximation dans le message.
- **Si l'envoi échoue**, un réessai sur le même canal dans la minute, puis consignation de l'échec.
- **Pas d'acharnement.** Un rappel manqué reste manqué : au-delà de l'heure de la prière suivante, il n'est plus envoyé. Un agent qui insiste devient un agent qu'on coupe.
- **Alerte silencieuse.** En cas de panne prolongée (plus de 24 h sans envoi réussi), Nour prévient par un second moyen, à définir.

---

## 11. Comment on saura que la Phase 1 est réussie

Critère de validation, à vérifier sur **sept jours consécutifs** :

1. Les cinq rappels quotidiens partent chaque jour, aucun oubli.
2. Chaque message arrive entre 15 et 20 minutes avant l'heure de la prière, avec un écart maximum d'une minute par rapport à l'heure prévue.
3. La salutation complète est présente en ouverture de chaque message.
4. Le rappel du siwak est bien intégré au même message.
5. Au moins un changement de ville est testé sur la période, et les horaires suivent correctement.
6. Le journal des envois ne contient aucun doublon et aucune erreur non traitée.

Tant que ces six points ne sont pas tenus, on ne passe pas à la suite.

---

## 12. Phases suivantes (après validation)

- **Phase 2 — élargir les rappels :** rendez-vous, tâches, relances de personnes, envoi d'emails rédigés par Nour, avec un ton adapté selon le type. C'est aussi le moment d'ajouter une petite page de suivi, consultable depuis le téléphone, pour voir le journal des envois, changer de ville et ajuster les réglages sans passer par le code.
- **Phase 3 — la couche agent :** Nour interprète les messages de l'utilisateur (changement de ville, report, demande de relance). C'est ici que le modèle entre vraiment en jeu.
- **Phase 4 — clonage pour d'autres personnes :** configuration propre à chacun. Cette phase impose de traiter le **consentement** (règles strictes sur WhatsApp et SMS), la **protection des données personnelles**, et le **coût par message**.
- **Phase 5 — agents par projet :** des agents dotés d'une mémoire propre pour chacun des projets d'Abdelkader (Bibliothèque Islamique, Maktaba, Coran phonétique, cours d'arabe). Le modèle pertinent ici est celui d'un agent branché sur une base de notes personnelles, capable de répondre en citant ses sources.

---

## 13. Hors périmètre de ce document

Un **agent séparé et distinct**, destiné aux personnes en situation de handicap, a été évoqué et volontairement écarté de ce projet :

- Pour les personnes aveugles ou malvoyantes : interaction entièrement vocale, message audio ou appel plutôt que texte, réponse par dictée.
- Pour les personnes en fauteuil roulant : rappels spécifiques (rendez-vous médicaux, changements de position, réservation anticipée de transport adapté).

C'est un chantier à part entière, qui sera traité séparément et plus tard.

---

## 14. Choix de développement

- Construction **directement avec Claude Code**, indépendamment des agents reçus de Naiom (Jules, Victor, Sacha, Nina, Léa, Emma), afin de ne pas interférer avec la démarche en cours auprès de Naiom concernant le regroupement de ces agents.
- Développement **étape par étape**, une action à la fois, avec validation à chaque étape avant de passer à la suivante.
- **Les quatre fichiers de fondation d'abord, la construction ensuite.**
