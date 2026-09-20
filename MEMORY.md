# MEMORY.md — Carnet de Nour

*Ce que Nour retient d'une session à l'autre. Dit une fois, appliqué tout seul les jours suivants. Mis à jour à chaque changement de réglage ou de position.*

---

## 1. État courant

| Paramètre | Valeur | Depuis |
|---|---|---|
| Ville | Villefranche-sur-Saône | Valeur par défaut au démarrage |
| Pays | France | — |
| Latitude | 45.9800 | — |
| Longitude | 4.7122 | — |
| Fuseau horaire | Europe/Paris | — |
| Méthode de calcul | 99 (custom) — Fajr 12°, Isha fixe 90 min après Maghrib | 2026-09-19, calibrage API |
| École juridique | 0 — Shafi'i (ombre simple) | 2026-09-19, calibrage API |
| Correction horaires | tune=0,-3,0,4,-4,0,0,0,0 (Fajr -3 min, Dhuhr +4 min, Asr -4 min) | 2026-09-19, vérifié sur 4 saisons |
| Délai de rappel | 20 minutes avant la prière | 2026-09-19, décision d'Abdelkader |
| Canal Phase 1 | Email (Gmail) | Décision initiale |
| Langue | Arabe vocalisé | Décision révisée 2026-09-20, tests concluants |
| Prières concernées | Fajr, Dhuhr, Asr, Maghrib, Isha | Décision initiale |

---

## 2. Journal des décisions

| Date | Décision | Raison |
|---|---|---|
| 2026-09-19 | Canal retenu : email à la place de Telegram | Abdelkader consulte Gmail chaque jour, ouvre rarement Telegram |
| 2026-09-20 | Langue retenue : arabe vocalisé (pas translittération, pas français) | Testé en conditions réelles depuis l'adresse de Nour : l'arabe vocalisé passe partout, objet et corps, chiffres dans le bon ordre |
| 2026-09-19 | Adresse expéditrice : compte Gmail dédié à Nour, pas le compte personnel | Le mot de passe d'application donne accès à toute la boîte — compte dédié = risque isolé, adresse identifiable, réutilisable en Phase 4 |
| 2026-09-20 | Compte email dédié à Nour créé et configuré. .env complet. | Brique 3 débloquée. |
| 2026-09-19 | Changement de ville par réponse email | Email est le seul canal Phase 1 ; le partage de position Telegram est écarté |
| 2026-09-19 | Position par défaut : Villefranche-sur-Saône | Lieu de résidence principal |
| 2026-09-19 | Phase 1 = automatisation pure, sans appel à un modèle | Fiabilité et coût : un rappel de routine ne justifie pas un appel LLM |
| 2026-09-19 | Méthode de calcul : API AlAdhan méthode 99 (custom), Fajr=12°, Isha fixe 90 min, école Shafi'i (0) | Calibrage sur référence réelle Villefranche-sur-Saône 19/09/2026 |
| 2026-09-19 | Correction tune=0,-3,0,4,-4,0,0,0,0 validée sur 4 saisons (Fajr -3, Dhuhr +4, Asr -4) | Décalage constant quelle que soit la saison — correction fiable toute l'année |
| 2026-09-19 | Délai de rappel : 20 minutes | Décision d'Abdelkader |

---

## 3. Questions encore ouvertes

Ces points n'ont pas encore été tranchés. Ils doivent l'être avant ou pendant la construction, pas après.

### 3.1 Méthode de calcul et école juridique — RESOLUE

Calibrage effectué le 2026-09-19 sur les horaires de référence de Villefranche-sur-Saône.

**Réglage retenu (complet et définitif) :**
- Méthode : `99` (custom AlAdhan)
- `methodSettings` : `12,null,90 min` — Fajr angle 12° (méthode UOIF France), Isha fixe 90 minutes après Maghrib
- École : `0` (Shafi'i — ombre simple)
- `tune` : `0,-3,0,4,-4,0,0,0,0` — corrections Fajr -3 min, Dhuhr +4 min, Asr -4 min

**Validation saisonnière (2026-09-19) :**
Vérification sur 4 dates (21/12, 21/03, 21/06, 21/09) : les trois corrections sont exactement constantes (-3/-4/+4) quelle que soit la saison. La correction tune est fiable toute l'année. L'intervalle Maghrib→Isha reste 90 minutes exactes après correction sur les quatre dates.

**Précision finale après tous les réglages (référence 19/09/2026) :**
- Fajr : 0 min ✓ (06:16)
- Dhuhr : 0 min ✓ (13:39)
- Asr : 0 min ✓ (16:58)
- Maghrib : 0 min ✓ (19:45)
- Isha : 0 min ✓ (21:15)

### 3.2 Traitement du Fajr — QUESTION OUVERTE

En été à Villefranche-sur-Saône, le Fajr tombe vers 04h00, ce qui placerait le rappel vers 03h40. Faut-il un traitement différent pour le Fajr ?

**Options à trancher :**
- Délai plus court pour le Fajr uniquement (ex. : 10 min au lieu de 20 min)
- Plage horaire minimum en dessous de laquelle Nour n'envoie rien (ex. : pas de rappel avant 05h00)
- Aucun traitement particulier — le rappel part à 03h40 comme prévu

**Question :** est-ce que Abdelkader veut être réveillé à 03h40 en été, ou le Fajr mérite-t-il une règle à part ?

Ne pas coder avant décision.

### 3.3 Délai exact de rappel — RÉSOLUE

**Décision :** 20 minutes pour toutes les prières (sauf Fajr si la question 3.2 est tranchée autrement).

### 3.4 Second moyen d'alerte en cas de panne prolongée
Le cahier des charges prévoit qu'en cas de panne de plus de 24 h sans envoi réussi, Nour prévient "par un second moyen, à définir".

**Lien avec le piège Gmail :** un mot de passe d'application Google est automatiquement révoqué si Abdelkader change son mot de passe de compte. Dans ce cas, Nour ne peut plus envoyer d'email — il ne peut donc pas se signaler lui-même via ce canal. Le second moyen d'alerte doit fonctionner **indépendamment de Gmail** pour couvrir exactement ce cas.

**Question :** quel est ce second moyen ? Il doit être indépendant de Gmail (SMS, autre adresse email sur un service différent, notification push, etc.).
