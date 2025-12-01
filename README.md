# 🍅 Pymodoro-CLI

Un chronomètre Pomodoro en ligne de commande, simple et efficace.

## Description

Pymodoro-CLI est un outil CLI Python qui implémente la technique Pomodoro pour améliorer votre productivité. Il offre un compte à rebours dynamique avec barre de progression, des notifications sonores, et une gestion complète des cycles travail/pause.

## Fonctionnalités

- ⏱️ **Compte à rebours dynamique** - Affichage en temps réel sur une seule ligne
- 📊 **Barre de progression visuelle** - Suivez votre avancement
- 🔔 **Notifications sonores** - Alertes à la fin de chaque session
- 🔄 **Gestion des cycles** - Enchaînement automatique travail/pause
- ⚙️ **Personnalisable** - Durées configurables via arguments CLI
- 🖥️ **Multi-plateforme** - Windows, macOS, Linux

## Installation

### Via PyPI (recommandé)

```bash
pip install pymodoro-timer
```

C'est tout ! Les commandes `pymodoro` et `pomodoro` sont accessibles depuis n'importe où dans votre terminal.

### Depuis les sources

```bash
git clone https://github.com/LuKrlier/Pymodoro-CLI.git
cd Pymodoro-CLI
pip install .
```

### Installation développeur

```bash
git clone https://github.com/LuKrlier/Pymodoro-CLI.git
cd Pymodoro-CLI
pip install -e ".[dev]"
```

## Utilisation

### Commandes de base

```bash
# Session de travail par défaut (25 minutes)
pymodoro

# Personnaliser la durée de travail
pymodoro --work 50

# Personnaliser la durée de pause
pymodoro --break 10

# Lancer plusieurs cycles
pymodoro --cycles 4

# Mode automatique (enchaîne sans intervention)
pymodoro --auto --cycles 4

# Lancer une pause uniquement
pymodoro --pause-only
```

### Options disponibles

| Option | Court | Description | Défaut |
|--------|-------|-------------|--------|
| `--work` | `-w` | Durée du travail (minutes) | 25 |
| `--break` | `-b` | Durée de la pause (minutes) | 5 |
| `--long-break` | `-l` | Durée pause longue (minutes) | 15 |
| `--cycles` | `-c` | Nombre de cycles | 1 |
| `--auto` | `-a` | Mode automatique | Non |
| `--pause-only` | `-p` | Pause seule | Non |
| `--silent` | `-s` | Mode silencieux | Non |

### Exemples

```bash
# Session Pomodoro classique : 4 cycles de 25/5 min
pymodoro -w 25 -b 5 -c 4 -a

# Session longue avec pauses étendues
pymodoro -w 45 -b 15 -l 30 -c 2

# Pause rapide de 10 minutes
pymodoro -p -b 10
```

## Technique Pomodoro

La technique Pomodoro est une méthode de gestion du temps :

1. 🍅 **Travail** : 25 minutes de concentration intense
2. ☕ **Pause courte** : 5 minutes de repos
3. 🔄 **Répéter** : 4 cycles
4. 🌟 **Pause longue** : 15-30 minutes après 4 cycles

## Tests

```bash
# Installer pytest
pip install pytest pytest-cov

# Lancer les tests
python -m pytest tests/ -v

# Avec couverture de code
python -m pytest tests/ --cov=pomodoro --cov-report=term-missing
```

## Structure du projet

```
Pymodoro-CLI/
├── pomodoro.py          # Script principal
├── pyproject.toml       # Configuration du package
├── requirements-dev.txt # Dépendances de développement
├── tests/               # Tests unitaires
│   ├── conftest.py
│   ├── test_utilitaires.py
│   ├── test_argparse.py
│   ├── test_compte_a_rebours.py
│   ├── test_son.py
│   ├── test_terminal.py
│   └── test_integration.py
├── LICENSE
└── README.md
```

## Licence

MIT License - Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteur

Lukrlier (Lurlier Inc)

---

⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile !
