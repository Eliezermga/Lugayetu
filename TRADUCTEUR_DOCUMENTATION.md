# Documentation Scientifique : Traduction Automatique Ruund-Français avec mBART

## Table des Matières
1. [Introduction](#introduction)
2. [Architecture Générale](#architecture-générale)
3. [Section 1 : Initialisation et Chargement des Données](#section-1--initialisation-et-chargement-des-données)
4. [Section 2 : Prétraitement du Texte](#section-2--prétraitement-du-texte)
5. [Section 3 : Filtrage et Nettoyage du Corpus](#section-3--filtrage-et-nettoyage-du-corpus)
6. [Section 4 : Configuration du Modèle](#section-4--configuration-du-modèle)
7. [Section 5 : Tokenisation et Préparation des Données](#section-5--tokenisation-et-préparation-des-données)
8. [Section 6 : Division Train/Validation/Test](#section-6--division-trainvalidationtest)
9. [Section 7 : Configuration de l'Entraînement](#section-7--configuration-de-lentraînement)
10. [Section 8 : Entraînement du Modèle](#section-8--entraînement-du-modèle)
11. [Section 9 : Évaluation et Inférence](#section-9--évaluation-et-inférence)
12. [Concepts Théoriques Clés](#concepts-théoriques-clés)
13. [Conclusions](#conclusions)

---

## Introduction

Ce notebook implémente un système complet de **traduction automatique neuronale (NMT - Neural Machine Translation)** du Ruund vers le Français. L'objectif est d'entraîner un modèle capable de traduire automatiquement des phrases d'une langue source (Ruund) vers une langue cible (Français) en utilisant les architectures d'apprentissage profond les plus modernes.

### Contexte
- **Langue Source** : Ruund (une langue minoritaire/endangered language)
- **Langue Cible** : Français
- **Modèle Utilisé** : mBART-large-50 (Multilingual BART)
- **Corpus** : Corpus parallèle Ruund-Français provenant de Hugging Face

---

## Architecture Générale

Le pipeline de traduction suit une architecture **séquence-à-séquence (Seq2Seq)** standard :

```
┌─────────────────┐
│  Texte Ruund    │
└────────┬────────┘
         │ Tokenisation + Embedding
         ▼
    ┌─────────┐
    │ Encoder │ (mBART)
    └────┬────┘
         │ Représentations Latentes
         ▼
    ┌─────────┐
    │ Decoder │ (mBART)
    └────┬────┘
         │ Génération de Tokens
         ▼
┌─────────────────────┐
│ Texte Français      │
│ (Traduction)        │
└─────────────────────┘
```

Les principales étapes sont :
1. **Prétraitement** : Normalisation du texte brut
2. **Tokenisation** : Conversion du texte en tokens numériques
3. **Encodage** : Transformation des tokens en représentations latentes
4. **Décodage** : Génération des tokens de traduction
5. **Post-traitement** : Conversion des tokens en texte final

---

## Section 1 : Initialisation et Chargement des Données

### Objectif
Préparer l'environnement de travail et charger le corpus parallèle pour l'entraînement.

### Code Principal
```python
!pip install -q datasets pandas sentencepiece evaluate sacrebleu transformers[torch] accelerate

from datasets import load_dataset
import pandas as pd
import evaluate
from huggingface_hub import login

HF_TOKEN = userdata.get('HF_TOKEN')
login(token=HF_TOKEN)
ds = load_dataset("eliezermga/ruund-french-parallel-corpus")
df = pd.DataFrame(ds['train'])
```

### Explication Détaillée

#### 1.1 Bibliothèques Utilisées

| Bibliothèque | Fonction |
|---|---|
| **datasets** | Gestion des corpus de données structurés |
| **pandas** | Manipulation et analyse des données tabulaires |
| **sentencepiece** | Tokenisation subword (BPE/SentencePiece) |
| **evaluate** | Calcul des métriques (BLEU, ROUGE, etc.) |
| **sacrebleu** | Implémentation standard de la métrique BLEU |
| **transformers** | Modèles pré-entraînés (BERT, mBART, etc.) |
| **torch** | Framework de deep learning |
| **accelerate** | Optimisation et distribution de l'entraînement |

#### 1.2 Chargement du Corpus

Le corpus est chargé depuis le hub Hugging Face. La structure est :
- **Format** : Dataset HuggingFace
- **Contenu** : Paires parallèles (source=Ruund, cible=Français)
- **Split** : 'train' (contient l'ensemble d'entraînement)

Après conversion en DataFrame Pandas, chaque ligne contient deux colonnes :
- `Ruund` : Phrase source en Ruund
- `French` : Phrase cible en Français

#### 1.3 Authentification Hugging Face
L'authentification via token HF_TOKEN permet l'accès à des modèles et datasets privés/protégés.

---

## Section 2 : Prétraitement du Texte

### Objectif
Standardiser et normaliser le texte brut pour améliorer la qualité des données d'entraînement.

### Code Principal
```python
import unicodedata
import re

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    
    # 1. Normalisation Unicode (NFC)
    text = unicodedata.normalize('NFC', text)
    
    # 2. Conversion en minuscules
    text = text.lower()
    
    # 3. Nettoyage de la ponctuation
    text = re.sub(r"[^\w\s.,!?']", "", text)
    
    # 4. Nettoyage des espaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
```

### Détails des Transformations

#### 2.1 Normalisation Unicode (NFC)

La normalisation Unicode est essentielle pour traiter les caractères accentués et spéciaux de manière cohérente.

**Exemple :**
```
Avant  : é (U+00E9, composé)
Après  : é (U+0065 + U+0301, décomposé normalisé)
```

Les formes de normalisation Unicode incluent :
- **NFD** (Décomposition) : Sépare les caractères composés
- **NFC** (Composition Canonique) : Combinaison de caractères (standard utilisé ici)
- **NFKD** : Décomposition compatible
- **NFKC** : Composition compatible

**NFC** est privilégiée car elle garantit une représentation cohérente tout en conservant une complexité minimale.

#### 2.2 Conversion en Minuscules
```python
text = text.lower()
```

**Objectif** : Réduire la variance lexicale. "Chat", "chat", et "CHAT" représentent le même concept.

**Impact** : 
- Réduit le vocabulaire d'environ 50-70%
- Améliore la généralisation du modèle
- Réduit le surapprentissage sur les variations de casse

#### 2.3 Nettoyage de la Ponctuation

```python
text = re.sub(r"[^\w\s.,!?']", "", text)
```

- **Conservé** : Lettres (`\w`), espaces (`\s`), ponctuation sémantique (`.`, `,`, `!`, `?`, `'`)
- **Supprimé** : Caractères spéciaux non informatifs (`@`, `#`, `$`, etc.)

**Justification** : La ponctuation sémantique (questions, exclamations) porte du sens ; les symboles spéciaux ajoutent du bruit.

#### 2.4 Nettoyage des Espaces

```python
text = re.sub(r'\s+', ' ', text).strip()
```

- `\s+` : Remplace une ou plusieurs espaces blancs par un seul espace
- `.strip()` : Supprime les espaces en début et fin de chaîne

**Exemple** :
```
Avant  : "Bonjour  ,   comment   ça   va ?"
Après  : "bonjour , comment ça va ?"
```

### Application aux Données

```python
df['Ruund'] = df['Ruund'].apply(preprocess_text)
df['French'] = df['French'].apply(preprocess_text)
```

Chaque phrase source (Ruund) et cible (Français) est prétraitée indépendamment.

---

## Section 3 : Filtrage et Nettoyage du Corpus

### Objectif
Améliorer la qualité du corpus en supprimant les données problématiques ou déséquilibrées.

### Code Principal
```python
initial_size = len(df)

# 1. Suppression doublons
df = df.drop_duplicates()

# 2. Calcul des longueurs
df['src_len'] = df['Ruund'].apply(lambda x: len(x.split()))
df['trg_len'] = df['French'].apply(lambda x: len(x.split()))

# 3. Suppression phrases vides
df = df[(df['src_len'] > 0) & (df['trg_len'] > 0)]

# 4. Filtrage par longueur
df = df[(df['src_len'] <= 80) & (df['trg_len'] <= 80)]

# 5. Filtrage par ratio
df = df[(df['src_len'] / df['trg_len'] <= 2.0) &
        (df['trg_len'] / df['src_len'] <= 2.0)]
```

### Détails des Filtres

#### 3.1 Suppression des Doublons
```python
df = df.drop_duplicates()
```

**Problème** : Les doublons causent :
- Surapprentissage (le modèle mémorise plutôt que généraliser)
- Biais d'évaluation (les métriques surestiment la qualité)
- Inefficacité (calcul dupliqué)

**Impact** : Généralement 1-5% de réduction selon la qualité des données source

#### 3.2 Calcul des Longueurs

```python
df['src_len'] = df['Ruund'].apply(lambda x: len(x.split()))
df['trg_len'] = df['French'].apply(lambda x: len(x.split()))
```

Chaque phrase est divisée en mots par `.split()` (séparation par espaces). La longueur est le nombre de mots (tokens au niveau du mot).

**Exemple** :
```
Phrase     : "bonjour comment ça va ?"
Longueur   : 5 mots
```

#### 3.3 Suppression des Phrases Vides

```python
df = df[(df['src_len'] > 0) & (df['trg_len'] > 0)]
```

Élimine les paires où au moins une phrase est vide après prétraitement. Cela indique souvent des données corrompues ou invalides.

#### 3.4 Filtrage par Longueur Absolue

```python
df = df[(df['src_len'] <= 80) & (df['trg_len'] <= 80)]
```

**Seuil** : 80 mots maximum

**Justifications** :
1. **Contrainte Computationnelle** : Les transformers utilisent l'attention quadratique ($O(n^2)$ en mémoire). Une séquence de 80 mots consomme ~6400 unités d'attention.
2. **Stabilité de l'Entraînement** : Les séquences très longues causent des instabilités d'apprentissage
3. **Pertinence Linguistique** : Les phrases très longues sont souvent complexes, mal alignées, ou contiennent des erreurs

**Formule de Mémoire Attention** :
$$\text{Mémoire Attention} = O(d \cdot n^2)$$

Où $d$ est la dimension de hidden state (~1024 pour mBART-large) et $n$ est la longueur de séquence.

#### 3.5 Filtrage par Ratio de Longueur

```python
df = df[(df['src_len'] / df['trg_len'] <= 2.0) &
        (df['trg_len'] / df['src_len'] <= 2.0)]
```

**Seuil** : Ratio entre 0.5 et 2.0

**Justification** : Pour une traduction valide, les longueurs source et cible doivent être proportionnelles.

**Formule du Ratio** :
$$r = \frac{L_{\text{source}}}{L_{\text{cible}}}$$

**Interprétation** :
- $r \approx 1.0$ : Traduction bien proportionnée
- $r > 2.0$ : Source très courte vs. cible longue (signal d'erreur d'alignement)
- $r < 0.5$ : Source très longue vs. cible courte (signal d'erreur d'alignement)

**Exemple de Paires Rejetées** :
```
❌ "bonjour" (1 mot) → "c'est une belle journée" (5 mots) [ratio = 0.2]
❌ "comment allez-vous et comment va votre famille" (8 mots) → "salut" (1 mot) [ratio = 8.0]
✅ "bonjour comment ça va" (4 mots) → "hello how are you" (4 mots) [ratio = 1.0]
```

### Résumé des Statistiques

```
Taille initiale       : N_0
Après doublons        : N_1
Après vides           : N_2
Après longueur        : N_3
Après ratio           : N_4 = N_final
```

Typiquement :
- Réduction doublons : 5-10%
- Réduction vides : 1-3%
- Réduction longueur : 15-30%
- Réduction ratio : 10-20%
- **Réduction totale** : 30-50%

---

## Section 4 : Configuration du Modèle

### Objectif
Initialiser le modèle mBART multilingue et l'adapter pour le Ruund.

### Code Principal
```python
from transformers import MBartForConditionalGeneration, AutoTokenizer

model_name = "facebook/mbart-large-50"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Ajout du token personnalisé pour Ruund
tokenizer.add_special_tokens({"additional_special_tokens": ["ruu_CM"]})
tokenizer.src_lang = "ruu_CM"
tokenizer.tgt_lang = "fr_XX"

# Chargement et adaptation du modèle
model = MBartForConditionalGeneration.from_pretrained(model_name)
model.config.tie_word_embeddings = False
model.resize_token_embeddings(len(tokenizer))

model.generation_config.forced_bos_token_id = tokenizer.lang_code_to_id["fr_XX"]
```

### Détails de Configuration

#### 4.1 mBART-large-50 : Architecture et Spécifications

**mBART** = **Multilingual BART** (Denoising Autoencoder Transformer)

**Spécifications du Modèle** :
- **Type** : Modèle de débruitage multilingue
- **Architecture** : Transformer séquence-à-séquence
- **Langues Supportées** : 50 langues
- **Taille** : Large
  - **Paramètres** : ~610 millions
  - **Dimension d'Embeddings** : 1024
  - **Nombre de Couches Encoder** : 12
  - **Nombre de Couches Decoder** : 12
  - **Têtes d'Attention** : 16

**Avantages de mBART** :
1. Pré-entraîné sur un corpus multilingue massif
2. Transfert de connaissances excellent vers des langues non vues
3. Architecture robuste pour la traduction
4. Fine-tuning efficace

#### 4.2 Ajout d'un Token de Langue Personnalisé

```python
tokenizer.add_special_tokens({"additional_special_tokens": ["ruu_CM"]})
```

**Code de Langue ISO 639-3** : 
- `ruu` = Ruund
- `_CM` = Cameroun (code de pays ISO 3166-1 alpha-2)

**Raison** : Le Ruund n'était pas dans les 50 langues pré-entraînées de mBART. Ajouter un token personnalisé permet au modèle d'identifier correctement la langue source.

#### 4.3 Configuration des Langues

```python
tokenizer.src_lang = "ruu_CM"  # Langue source
tokenizer.tgt_lang = "fr_XX"   # Langue cible (fr_XX est standard pour français)
```

Ces attributs informent le tokenizer et le modèle des langues de travail.

#### 4.4 Redimensionnement des Embeddings

```python
model.resize_token_embeddings(len(tokenizer))
```

**Problème** : Le nouveau token `ruu_CM` n'a pas de représentation d'embedding dans le modèle pré-entraîné.

**Solution** : Redimensionner les matrices d'embedding pour inclure le nouveau token.

**Mathématique** :
```
Avant  : E ∈ ℝ^(V_old × d_hidden)
Après  : E ∈ ℝ^(V_new × d_hidden)
         où V_new = V_old + 1
```

**Initialisation** : Les nouveaux embeddings sont initialisés aléatoirement (ou par moyenne des embeddings existants).

#### 4.5 Désactivation du Partage d'Embeddings

```python
model.config.tie_word_embeddings = False
```

**Par défaut** : mBART partage les matrices d'embedding entre l'encoder et le decoder.

**Raison de la désactivation** : Avec le nouveau token, il est plus sûr de maintenir des embeddings séparés pour plus de flexibilité.

#### 4.6 Forçage du Token de Début de Séquence

```python
model.generation_config.forced_bos_token_id = tokenizer.lang_code_to_id["fr_XX"]
```

**Concept** : 
- `BOS` = Beginning Of Sequence
- `forced_bos_token_id` = Forcer le modèle à commencer la génération avec ce token

**Effet** :
```
Avant forçage  : [aléatoire] comment ça va [...]
Après forçage  : [fr_XX] comment ça va [...]
```

**Raison** : Garantir que le modèle génère en français, même si ce n'est pas statistiquement probable.

---

## Section 5 : Tokenisation et Préparation des Données

### Objectif
Convertir le texte brut en représentations numériques (tokens) et préparer les données pour l'entraînement.

### Code Principal
```python
from datasets import Dataset
import numpy as np

dataset = Dataset.from_pandas(df[['Ruund', 'French']])

def preprocess_function(examples):
    # Tokenisation source (Ruund)
    model_inputs = tokenizer(
        examples["Ruund"],
        max_length=128,
        truncation=True,
        padding=False
    )
    
    # Tokenisation cible (Français)
    labels = tokenizer(
        text_target=examples["French"],
        max_length=128,
        truncation=True,
        padding=False
    )
    
    # Conversion en tenseurs
    model_inputs["labels"] = [
        np.array(l, dtype=np.int64) for l in labels["input_ids"]
    ]
    
    return model_inputs

tokenized_dataset = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=["Ruund", "French"]
)
```

### Détails de la Tokenisation

#### 5.1 Concept de Tokenisation

**Définition** : Conversion du texte continu en séquence d'identifiants numériques (tokens).

**Types de Tokenisation** :
1. **Tokenisation au Niveau du Mot** : Chaque mot = 1 token
   ```
   "Bonjour comment" → [token_1, token_2]
   Vocabulaire = ~50k mots
   ```

2. **Tokenisation Subword (BPE/WordPiece)** : Mots rares divisés en sous-mots
   ```
   "incompréhensible" → ["in", "compré", "hen", "sible"]
   Vocabulaire = ~50k tokens subword
   ```

3. **Tokenisation au Niveau du Caractère** : Chaque caractère = 1 token
   ```
   "Bonjour" → ['B', 'o', 'n', 'j', 'o', 'u', 'r']
   Vocabulaire = ~100 caractères
   ```

**mBART Utilise** : SentencePiece BPE avec vocabulaire de ~250k tokens

#### 5.2 Processus de Tokenisation

**Étape 1 : Normalisation Texte**
```
"Bonjour, COMMENT?" → "bonjour , comment ?"
```

**Étape 2 : Division en Tokens**
```
"bonjour , comment ?" → [token_123, token_456, token_789, token_345]
```

**Étape 3 : Ajout de Tokens Spéciaux**
```
[BOS, token_123, token_456, token_789, token_345, EOS]
```

#### 5.3 Paramètres de Tokenisation

| Paramètre | Valeur | Signification |
|---|---|---|
| `max_length` | 128 | Longueur maximale de séquence |
| `truncation` | True | Tronquer les séquences > 128 tokens |
| `padding` | False | Pas de padding ici (délégué au DataCollator) |

**Stratégie de Troncature** :
```
Avant   : [token_1, ..., token_150]
Après   : [token_1, ..., token_128]
```

Les tokens au-delà de 128 sont simplement ignorés (généralement la fin de phrase moins importante).

#### 5.4 Préparation des Labels

```python
model_inputs["labels"] = [np.array(l, dtype=np.int64) for l in labels["input_ids"]]
```

Les labels sont les tokens français tokenisés de la même manière. Ils sont utilisés pour calculer la perte d'entraînement.

**Structure Finale** :
```python
{
    "input_ids": [128 tokens source],
    "attention_mask": [128 masques (0 ou 1)],
    "labels": [128 tokens cible]
}
```

#### 5.5 Processing par Batch

```python
tokenized_dataset = dataset.map(
    preprocess_function,
    batched=True,  # Traiter par lots (plus efficace)
    remove_columns=["Ruund", "French"]  # Supprimer colonnes texte originales
)
```

**Avantage du Traitement par Batch** : 
- Plus rapide (vectorisation)
- Réduction mémoire après suppression des colonnes texte

---

## Section 6 : Division Train/Validation/Test

### Objectif
Créer trois ensembles distincts pour l'entraînement, le tuning et l'évaluation.

### Code Principal
```python
from datasets import DatasetDict

train_testvalid = tokenized_dataset.train_test_split(test_size=0.2, seed=42)
test_valid = train_testvalid["test"].train_test_split(test_size=0.5, seed=42)

final_datasets = DatasetDict({
    "train": train_testvalid["train"],
    "validation": test_valid["train"],
    "test": test_valid["test"]
})

train_dataset = final_datasets["train"]
eval_dataset = final_datasets["validation"]
test_dataset = final_datasets["test"]
```

### Détails de la Division

#### 6.1 Schéma de Division

```
Dataset Initial (100%)
    ├─ 80% → Train (60%)
    └─ 20% → Test+Valid
            ├─ 50% → Validation (10%)
            └─ 50% → Test (10%)

Résultat Final :
- Train      : 60%
- Validation : 20%
- Test       : 20%
```

**Formule** :
$$N_{\text{train}} = 0.80 \cdot N_{\text{total}}$$
$$N_{\text{val}} = 0.10 \cdot N_{\text{total}}$$
$$N_{\text{test}} = 0.10 \cdot N_{\text{total}}$$

#### 6.2 Rôles des Ensembles

| Ensemble | Rôle | Utilisation |
|---|---|---|
| **Train** | Apprendre les poids du modèle | Gradient descent |
| **Validation** | Ajuster hyperparamètres | Early stopping, meilleur checkpoint |
| **Test** | Évaluation finale | Rapport de performance |

#### 6.3 Importance de la Séparation

**Problème sans séparation** :
- Overfitting : Le modèle mémorise les données d'entraînement
- Évaluation biaisée : Les métriques surestiment la performance réelle

**Solution** :
- Train : 60% (optimisation)
- Val : 20% (monitoring)
- Test : 20% (rapport indépendant)

**Mathématique Formelle** :
$$\text{Erreur Généralisation} = \text{Erreur Test}$$

Le test set estime l'erreur réelle sur des données non vues.

#### 6.4 Seed Aléatoire

```python
seed=42
```

Utiliser une graine fixe garantit la reproductibilité. Les mêmes données split de la même manière à chaque exécution.

---

## Section 7 : Configuration de l'Entraînement

### Objectif
Définir tous les hyperparamètres et outils nécessaires pour l'entraînement du modèle.

### Code Principal
```python
from transformers import DataCollatorForSeq2Seq, Seq2SeqTrainer, Seq2SeqTrainingArguments
import evaluate
import numpy as np

# DataCollator
data_collator = DataCollatorForSeq2Seq(
    tokenizer,
    model=model,
    padding=True,
    label_pad_token_id=-100,
    pad_to_multiple_of=8,
    return_tensors="pt"
)

# Métrique
metric = evaluate.load("sacrebleu")

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    
    result = metric.compute(
        predictions=decoded_preds,
        references=[[ref] for ref in decoded_labels]
    )
    return {"bleu": round(result["score"], 2)}
```

### Détails de Configuration

#### 7.1 Data Collator

Le **DataCollator** est une fonction spécialisée qui :
1. Regroupe les exemples en batches
2. Applique le padding dynamique
3. Crée des masques d'attention

```python
DataCollatorForSeq2Seq(
    tokenizer,
    model=model,
    padding=True,
    label_pad_token_id=-100,
    pad_to_multiple_of=8,
    return_tensors="pt"
)
```

**Paramètres** :

| Paramètre | Valeur | Signification |
|---|---|---|
| `tokenizer` | - | Tokenizer pour padding token |
| `model` | - | Modèle pour inférer dimensions |
| `padding` | True | Appliquer padding |
| `label_pad_token_id` | -100 | ID spécial pour ignorer padding en perte |
| `pad_to_multiple_of` | 8 | Padding à multiple de 8 (optimisation GPU) |
| `return_tensors` | "pt" | Retourner tenseurs PyTorch |

**Effet du Padding** :

```
Batch non-padé :
  Exemple 1 : [token_1, token_2, token_3]
  Exemple 2 : [token_4, token_5, token_6, token_7, token_8]
  
Batch padé :
  Exemple 1 : [token_1, token_2, token_3, PAD, PAD]
  Exemple 2 : [token_4, token_5, token_6, token_7, token_8]
```

#### 7.2 Métrique BLEU

**BLEU** = **Bilingual Evaluation Understudy**

**Formule** :
$$\text{BLEU} = BP \cdot \exp\left(\sum_{n=1}^{N} w_n \log p_n\right)$$

Où :
- $BP$ = Brevity Penalty (pénalité pour traductions trop courtes)
- $p_n$ = Précision des n-grammes
- $w_n$ = Poids des n-grammes (généralement uniform, 1/4 pour n-grammes jusqu'à 4)
- $N$ = Longueur maximale des n-grammes (4)

**Interprétation** :
- $0 \leq \text{BLEU} \leq 100$
- BLEU = 100 : Traduction parfaite (identique à référence)
- BLEU > 40 : Traduction bonne
- BLEU 20-40 : Traduction acceptable
- BLEU < 20 : Traduction pauvre

**Exemple de Calcul** :
```
Référence    : "the cat sat on the mat"
Traduction   : "the cat sat on a mat"

Unigrammes : 6/7 correspondent (the, cat, sat, on, mat manquant)
Bigrammes  : 4/6 correspondent
Trigrammes : 2/5 correspondent
4-grammes  : 1/4 correspondent

BLEU ≈ 0.857 × 0.667 × 0.4 × 0.25 = 0.0572 ≈ 57.2
```

#### 7.3 Fonction de Calcul des Métriques

```python
def compute_metrics(eval_preds):
    preds, labels = eval_preds
    
    # Décoder les prédictions
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    
    # Remplacer les padding (-100) avant décodage
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    
    # Calculer BLEU
    result = metric.compute(
        predictions=decoded_preds,
        references=[[ref] for ref in decoded_labels]
    )
    return {"bleu": round(result["score"], 2)}
```

**Processus** :
1. **Décodage** : Convertir les IDs de tokens en texte
2. **Nettoyage Labels** : Remplacer les tokens padding (-100) avant décodage
3. **Calcul BLEU** : Comparer prédictions et labels
4. **Arrondi** : Arrondir à 2 décimales

---

## Section 8 : Entraînement du Modèle

### Objectif
Entraîner le modèle mBART à traduire du Ruund vers le Français.

### Code Principal
```python
training_args = Seq2SeqTrainingArguments(
    output_dir="./ruund-fr-mbart",
    num_train_epochs=10,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    gradient_accumulation_steps=1,
    gradient_checkpointing=False,
    warmup_steps=200,
    weight_decay=0.01,
    learning_rate=5e-5,
    predict_with_generate=True,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="bleu",
    bf16=True,
    fp16=False,
    optim="adafactor",
    logging_steps=50,
    report_to="none"
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    processing_class=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()
```

### Détails de l'Entraînement

#### 8.1 Hyperparamètres d'Entraînement

| Paramètre | Valeur | Signification |
|---|---|---|
| `output_dir` | "./ruund-fr-mbart" | Répertoire de sauvegarde |
| `num_train_epochs` | 10 | Nombre d'epochs (passages sur données) |
| `per_device_train_batch_size` | 16 | Batch size entraînement par GPU |
| `per_device_eval_batch_size` | 16 | Batch size évaluation par GPU |
| `gradient_accumulation_steps` | 1 | Accumulation de gradients (ici, aucune) |
| `warmup_steps` | 200 | Étapes de chauffage du learning rate |
| `weight_decay` | 0.01 | Régularisation L2 |
| `learning_rate` | 5e-5 | Taux d'apprentissage |
| `optim` | "adafactor" | Optimiseur (économe en mémoire) |

#### 8.2 Schéma d'Entraînement

**Epoch** = Passage complet sur l'ensemble d'entraînement

**Nombre total de mises à jour** :
$$\text{Updates} = \text{num_epochs} \times \frac{|\text{train_dataset}|}{batch\_size}$$

**Exemple** : 
- Dataset train : 5000 exemples
- Batch size : 16
- Epochs : 10

$$\text{Updates} = 10 \times \frac{5000}{16} = 10 \times 312.5 \approx 3125 \text{ mises à jour}$$

#### 8.3 Learning Rate Scheduling

**Warmup** : Augmentation progressive du learning rate

$$LR(t) = \text{base\_lr} \times \min\left(1, \frac{t}{\text{warmup\_steps}}\right)$$

**Graphique** :
```
LR
 |     /  ╲ (decay)
 |    /    ╲
 |   /      ╲___
 |  /          
 └────────────────── étapes
   0  200        fin
   warmup
```

**Raison** : 
- Les premiers gradients sont bruyants (données aléatoires)
- Augmenter progressivement stabilise l'entraînement
- Évite les divergences et les instabilités

#### 8.4 Optimiseur Adafactor

**Adafactor** = Optimizer adaptatif, efficient en mémoire

Comparé à Adam :
- **Mémoire** : 50-75% moins consommatrice
- **Performance** : Comparable ou meilleure
- **Formula** :

$$\theta_t = \theta_{t-1} - \alpha_t \frac{m_t}{\sqrt{v_t} + \epsilon}$$

Où $m_t$ et $v_t$ sont des estimations du gradient et de sa variance.

#### 8.5 Stratégies d'Évaluation et Sauvegarde

```python
eval_strategy="epoch"        # Évaluer à chaque fin d'epoch
save_strategy="epoch"        # Sauvegarder à chaque fin d'epoch
load_best_model_at_end=True  # Charger le meilleur modèle à la fin
metric_for_best_model="bleu" # Basé sur le score BLEU
```

**Early Stopping Implicite** : Le meilleur modèle (selon BLEU) est conservé et rechargé automatiquement.

#### 8.6 Précision Numérique

```python
bf16=True    # Bfloat16 (float16 robuste)
fp16=False   # Pas de float32 précis (trop mémoire)
```

**Bfloat16** : 16 bits mais avec plage float32 (plus stable que float16)

**Tradeoff** :
- **Vitesse** : 2x plus rapide (16 bits vs 32 bits)
- **Mémoire** : 2x moins consommatrice
- **Précision** : Mineure perte (acceptable pour NLP)

#### 8.7 Processus d'Entraînement

Pour chaque epoch :
1. **Forward Pass** : 
   $$\hat{y} = \text{model}(x)$$

2. **Calcul de la Perte (Loss)** :
   $$L = -\sum_i \log P(y_i | y_{<i}, x)$$
   
   (Cross-entropy loss pour chaque token)

3. **Backward Pass** : Calcul des gradients
   $$\frac{\partial L}{\partial \theta}$$

4. **Mise à Jour** : 
   $$\theta \leftarrow \theta - \alpha \nabla L$$

5. **Évaluation** : Calcul BLEU sur validation set
6. **Sauvegarde** : Si BLEU meilleur que précédent

---

## Section 9 : Évaluation et Inférence

### 9.1 Évaluation sur Test Set

```python
results = trainer.evaluate(test_dataset)
print(f"BLEU sur le test set : {results['eval_bleu']}")
```

**Objectif** : Évaluer la performance finale du modèle sur des données qu'il n'a jamais vues.

**Interprétation** :
- **BLEU > 50** : Excellent
- **BLEU 35-50** : Très bon
- **BLEU 20-35** : Acceptable
- **BLEU < 20** : À améliorer

### 9.2 Inférence (Traduction)

```python
def translate_sentence(sentence, model, tokenizer):
    # 1. Tokenisation
    inputs = tokenizer(
        sentence,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )
    
    # 2. Déplacer vers GPU si disponible
    if torch.cuda.is_available():
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    # 3. Génération
    with torch.no_grad():
        translated_tokens = model.generate(
            **inputs,
            max_length=128,
            num_beams=5,
            early_stopping=True
        )
    
    # 4. Décodage
    translated_sentence = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]
    
    return translated_sentence

# Exemple
ruund_sentence = "wajidikish mwan"
translated_french = translate_sentence(ruund_sentence, model, tokenizer)
print(f"Ruund: {ruund_sentence}")
print(f"Français: {translated_french}")
```

#### 9.2.1 Processus d'Inférence

**Étape 1 : Tokenisation**
```
"wajidikish mwan" → [token_123, token_456, token_789]
```

**Étape 2 : Encoding**
```
Encoder Process:
[token_123, token_456, token_789]
    ↓
Attention Layers ×12
    ↓
Représentations Contextuelles
```

**Étape 3 : Décoding**

Le decoder génère token par token, utilisant :
- La représentation encodée (contexte source)
- Les tokens précédemment générés

$$P(y_t | y_{<t}, x) = \text{softmax}(W \cdot h_t + b)$$

Où $h_t$ est la représentation cachée du decoder à l'étape $t$.

#### 9.2.2 Stratégies de Génération

**Beam Search** (`num_beams=5`) :
- Maintient les 5 hypothèses les plus probables
- À chaque étape, développe les meilleures hypothèses
- Sélectionne l'hypothèse avec la meilleure probabilité globale

**Vs Greedy** :
```
Greedy    : À chaque étape, choisir le token le plus probable
           Risque d'optima locaux faibles

Beam (=5) : Maintenir les 5 meilleures séquences
           Meilleure qualité, plus lent
```

**Early Stopping** (`early_stopping=True`) :
- Arrêter la recherche si le meilleur score ne peut pas s'améliorer
- Économie computationnelle

---

## Concepts Théoriques Clés

### Traduction Automatique Neuronale (NMT)

#### Modèle Probabiliste

$$P(\mathbf{y} | \mathbf{x}) = \prod_{t=1}^{T} P(y_t | y_{1:t-1}, \mathbf{x})$$

Pour chaque phrase cible $\mathbf{y}$ donnée source $\mathbf{x}$ :
- Probabilité = produit des probabilités conditionnelles
- Chaque token dépend des tokens précédents et du contexte source

#### Architecture Transformer

**Attention Mechanism** :
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Où :
- $Q$ = Query (ce que le modèle cherche)
- $K$ = Key (ce qui peut être trouvé)
- $V$ = Value (l'information)
- $d_k$ = Dimension de key (normalisation)

**Multi-Head Attention** :
$$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1,...,\text{head}_h)W^O$$

Où $h=16$ têtes (mBART-large)

#### Fine-tuning (Ajustement Fin)

**Concept** : Prendre un modèle pré-entraîné et l'adapter à une tâche spécifique.

**Avantage** :
- Utilise les connaissances apprises sur des données massives
- Nécessite moins de données spécifiques à la tâche
- Entraînement plus rapide

**Formule** :
$$\mathcal{L}_{\text{task}} = -\log P(y | x; \theta_{\text{pretrained}} + \Delta\theta)$$

Où $\Delta\theta$ est petit (learning rate faible)

---

## Conclusions

### Résumé du Pipeline

1. **Chargement des Données** : Corpus parallèle Ruund-Français
2. **Prétraitement** : Normalisation Unicode, minuscules, nettoyage
3. **Filtrage** : Suppression des doublons, phrases vides, déséquilibrées
4. **Tokenisation** : Conversion en tokens numériques (SentencePiece BPE)
5. **Modèle** : mBART-large-50 fine-tuné
6. **Entraînement** : 10 epochs avec optimiseur Adafactor
7. **Évaluation** : Métrique BLEU sur test set
8. **Inférence** : Traduction avec beam search

### Points Clés

| Aspect | Détail |
|---|---|
| **Modèle** | mBART-large-50 (~610M paramètres) |
| **Architecture** | Seq2Seq Transformer |
| **Tokenisation** | SentencePiece BPE (~250k tokens) |
| **Taille Séquence** | 128 tokens max |
| **Entraînement** | 10 epochs, batch size 16, lr=5e-5 |
| **Évaluation** | Métrique BLEU |
| **Génération** | Beam search avec 5 beams |

### Améliorations Possibles

1. **Augmentation de Données** : Back-translation, paraphrase
2. **Ensemble Models** : Combiner plusieurs modèles
3. **Fine-tuning Multi-Task** : Ajouter tâches auxiliaires
4. **Hyperparameter Search** : Optimiser lr, batch_size, warmup_steps
5. **Corpus Plus Grand** : Collecter plus de données parallèles Ruund-Français
6. **Corpus Plus Propre** : Meilleur filtrage et alignement
7. **Multilingual Transfer** : Utiliser des langues similaires

### Applicabilité

Ce système peut être utilisé pour :
- Traduction automatique Ruund ↔ Français
- Localisation de contenu
- Assistance à la traduction humaine (CAT)
- Recherche en NLP / linguistique computationnelle
- Préservation de langues minoritaires via technologie

---

## Références Mathématiques

### Formules Résumées

**Softmax** : 
$$\sigma(\mathbf{z})_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$$

**Cross-Entropy Loss** :
$$\mathcal{L} = -\sum_i y_i \log(\hat{y}_i)$$

**Attention** :
$$\text{Attn}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

**BLEU** :
$$\text{BLEU} = BP \cdot \exp\left(\sum_{n=1}^{4} \frac{1}{4}\log p_n\right)$$

---

**Document Généré** : Analyse Scientifique Complète du Notebook Traducteur Ruund-Français

**Auteur** : Analyse Automatique

**Date** : 2026

