# Recette — Rédiger un rappel de prière

*La méthode est dans la recette, pas dans le code. Pour changer le ton ou la formulation, modifier ce fichier — pas le programme.*

**Langue retenue : arabe vocalisé.** Testé en conditions réelles le 2026-09-20 depuis l'adresse de Nour. L'arabe vocalisé passe parfaitement dans l'objet et le corps, les chiffres s'affichent dans le bon ordre au milieu du texte. La translittération et le français restent disponibles dans le code mais ne sont pas utilisés.

---

## Structure du message

Un rappel de prière suit toujours cette structure, dans cet ordre :

```
[SALUTATION]

[CORPS]

[SIWAK ET PARFUM]
```

Aucune section ne peut être omise. Aucune section supplémentaire ne peut être ajoutée en Phase 1.

---

## 1. Salutation

Toujours en ouverture, toujours complète, jamais abrégée :

> السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ

---

## 2. Corps du message

Contient, dans cet ordre :
1. Le nom de la prière en arabe (forme genitive, valable dans l'objet et le corps).
2. L'heure exacte de la prière au format `HH:MM`.
3. Le temps restant avant la prière (en arabe).

**Formulation :**
```
صَلَاةُ [NOM] فِي السَّاعَةِ [HH:MM] — بَعْدَ [MINUTES] دَقِيقَةً.
```

**Noms des prières (forme genitive, identique dans l'objet et le corps) :**

| Prière | Arabe vocalisé |
|---|---|
| Fajr | الْفَجْرِ |
| Dhuhr | الظُّهْرِ |
| Asr | الْعَصْرِ |
| Maghrib | الْمَغْرِبِ |
| Isha | الْعِشَاءِ |

---

## 3. Rappel du siwak et du parfum

Intégré au même message, après le corps, jamais dans un message séparé. Les deux gestes sont rattachés au même moment — avant de prier — parce que cette formulation reste vraie que l'on prie chez soi ou à la mosquée.

**Formulation :**
```
تَذَكَّرِ السِّوَاكَ وَالطِّيبَ قَبْلَ الصَّلَاةِ.
```

---

## Message complet — exemple pour Maghrib (19:45, délai 20 min)

**Objet :**
```
تَذْكِيرٌ بِصَلَاةِ الْمَغْرِبِ — بَعْدَ عِشْرِينَ دَقِيقَةً
```

**Corps :**
```
السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ

صَلَاةُ الْمَغْرِبِ فِي السَّاعَةِ 19:45 — بَعْدَ عِشْرِينَ دَقِيقَةً.

تَذَكَّرِ السِّوَاكَ وَالطِّيبَ قَبْلَ الصَّلَاةِ.
```

---

## Objet de l'email

```
تَذْكِيرٌ بِصَلَاةِ [NOM] — بَعْدَ [MINUTES] دَقِيقَةً
```

---

## Ce que le programme doit fournir à cette recette

- `priere` : clé interne (`Fajr`, `Dhuhr`, `Asr`, `Maghrib`, `Isha`)
- `heure_priere` : heure au format `HH:MM`
- `minutes_restantes` : entier (20 en Phase 1)
- `langue` : `'ar'` (défaut)
