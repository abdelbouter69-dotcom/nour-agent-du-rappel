# Recette — Lire une réponse et changer de ville

*Décrit comment Nour détecte un changement de ville dans une réponse email, ce qu'il met à jour, et ce qu'il confirme.*

---

## Déclencheur

Abdelkader répond à un email de Nour. Le corps de la réponse contient une indication de lieu, par exemple :

- « je suis à Tlemcen »
- « Tlemcen »
- « je suis arrivé à Lyon »
- « Paris »

---

## Ce que Nour fait, dans cet ordre

1. **Lire la réponse.** Nour surveille les réponses aux emails qu'il a envoyés. Il lit le corps du message.
2. **Repérer un nom de ville.** En Phase 1 : recherche simple d'un nom de ville dans le texte, comparé à une liste de villes connues. Aucun appel à un modèle de langage.
3. **Mettre à jour le carnet.** Si une ville est reconnue : mise à jour de `MEMORY.md` (ville, pays, latitude, longitude, fuseau) et consignation dans le journal des décisions avec la date.
4. **Confirmer par email.** Nour répond à l'email avec un message de confirmation.
5. **Appliquer dès le rappel suivant.** Le rappel en cours d'attente, s'il n'est pas encore parti, utilise les nouveaux horaires.

---

## Message de confirmation — exemple en français

```
as-salāmu ʿalaykum wa raḥmatu Llāhi wa barakātuh

Horaires calés sur [NOM DE LA VILLE].
Prochain rappel : [NOM DE LA PRIÈRE] à [HEURE].
```

**Objet de l'email de confirmation :** `Position mise à jour — [NOM DE LA VILLE]`

---

## Ce que Nour fait si la ville n'est pas reconnue

Il répond par un email de demande de précision :

```
as-salāmu ʿalaykum wa raḥmatu Llāhi wa barakātuh

Je n'ai pas reconnu le nom de la ville. Peux-tu me l'indiquer en répondant à ce message ?
Exemple : « Tlemcen » ou « Lyon ».
```

Il ne modifie rien dans le carnet tant qu'aucune ville valide n'est confirmée. Il continue d'utiliser la dernière position connue.

---

## Ce que Nour fait si le message de réponse ne contient pas de ville

Il ne fait rien. Les réponses sans indication de lieu sont ignorées silencieusement. Nour ne tente pas d'interpréter un message vague.

---

## Règles de Phase 1

- **Pas d'appel à un modèle de langage.** La reconnaissance se fait par comparaison avec une liste de villes. Si la ville n'est pas dans la liste, Nour demande de préciser.
- **Pas de partage de position GPS.** Le changement de ville se fait uniquement par texte dans un email.
- **La liste de villes** doit au minimum contenir : Villefranche-sur-Saône, Lyon, Paris, Tlemcen, Alger, Oran. Elle est extensible sans toucher au code.

---

## Ce que le programme doit fournir à cette recette

- `detected_city` : nom de la ville détectée dans l'email.
- `new_prayer_times` : horaires recalculés pour cette ville et ce jour.
- `next_prayer_name` + `next_prayer_time` : pour la ligne de confirmation.
