# -*- coding: utf-8 -*-
"""
Tests unitaires pour le parseur d'arguments CLI de Pymodoro-CLI.
================================================================

Ce module teste la fonction creer_parseur_arguments() et tous les
arguments de ligne de commande supportés par l'application.
"""

import pytest
import sys
from unittest.mock import patch

# Import du module à tester
sys.path.insert(0, '..')
from pomodoro import (
    creer_parseur_arguments,
    DUREE_TRAVAIL_DEFAUT,
    DUREE_PAUSE_DEFAUT,
    DUREE_PAUSE_LONGUE_DEFAUT
)


# =============================================================================
# TESTS POUR creer_parseur_arguments()
# =============================================================================

class TestCreerParseurArguments:
    """Tests pour la création du parseur d'arguments."""

    def test_parseur_est_cree(self):
        """Vérifie que le parseur est créé sans erreur."""
        parser = creer_parseur_arguments()
        assert parser is not None

    def test_parseur_nom_programme(self):
        """Vérifie que le nom du programme est correct."""
        parser = creer_parseur_arguments()
        assert parser.prog == 'pomodoro'


# =============================================================================
# TESTS POUR LES VALEURS PAR DÉFAUT
# =============================================================================

class TestValeursParDefaut:
    """Tests pour les valeurs par défaut des arguments."""

    def test_work_defaut(self):
        """Vérifie la valeur par défaut de --work."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([])
        assert args.work == DUREE_TRAVAIL_DEFAUT

    def test_break_defaut(self):
        """Vérifie la valeur par défaut de --break."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([])
        assert args.pause == DUREE_PAUSE_DEFAUT

    def test_long_break_defaut(self):
        """Vérifie la valeur par défaut de --long-break."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([])
        assert args.pause_longue == DUREE_PAUSE_LONGUE_DEFAUT

    def test_cycles_defaut(self):
        """Vérifie la valeur par défaut de --cycles."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([])
        assert args.cycles == 1

    def test_auto_defaut_false(self):
        """Vérifie que --auto est False par défaut."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([])
        assert args.auto is False

    def test_pause_only_defaut_false(self):
        """Vérifie que --pause-only est False par défaut."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([])
        assert args.pause_only is False

    def test_silent_defaut_false(self):
        """Vérifie que --silent est False par défaut."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([])
        assert args.silent is False


# =============================================================================
# TESTS POUR L'ARGUMENT --work / -w
# =============================================================================

class TestArgumentWork:
    """Tests pour l'argument --work / -w."""

    def test_work_forme_longue(self):
        """Test de --work avec la forme longue."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--work', '50'])
        assert args.work == 50

    def test_work_forme_courte(self):
        """Test de -w avec la forme courte."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['-w', '30'])
        assert args.work == 30

    @pytest.mark.parametrize("valeur", [1, 10, 25, 45, 60, 90, 120])
    def test_work_valeurs_diverses(self, valeur):
        """Test paramétré avec diverses valeurs de travail."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--work', str(valeur)])
        assert args.work == valeur

    def test_work_zero(self):
        """Test avec une durée de travail de 0."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--work', '0'])
        assert args.work == 0

    def test_work_type_int(self):
        """Vérifie que work est bien un entier."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--work', '25'])
        assert isinstance(args.work, int)


# =============================================================================
# TESTS POUR L'ARGUMENT --break / -b
# =============================================================================

class TestArgumentBreak:
    """Tests pour l'argument --break / -b."""

    def test_break_forme_longue(self):
        """Test de --break avec la forme longue."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--break', '10'])
        assert args.pause == 10

    def test_break_forme_courte(self):
        """Test de -b avec la forme courte."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['-b', '15'])
        assert args.pause == 15

    @pytest.mark.parametrize("valeur", [1, 3, 5, 10, 15, 20])
    def test_break_valeurs_diverses(self, valeur):
        """Test paramétré avec diverses valeurs de pause."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--break', str(valeur)])
        assert args.pause == valeur


# =============================================================================
# TESTS POUR L'ARGUMENT --long-break / -l
# =============================================================================

class TestArgumentLongBreak:
    """Tests pour l'argument --long-break / -l."""

    def test_long_break_forme_longue(self):
        """Test de --long-break avec la forme longue."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--long-break', '20'])
        assert args.pause_longue == 20

    def test_long_break_forme_courte(self):
        """Test de -l avec la forme courte."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['-l', '30'])
        assert args.pause_longue == 30

    @pytest.mark.parametrize("valeur", [10, 15, 20, 30, 45])
    def test_long_break_valeurs_diverses(self, valeur):
        """Test paramétré avec diverses valeurs de pause longue."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--long-break', str(valeur)])
        assert args.pause_longue == valeur


# =============================================================================
# TESTS POUR L'ARGUMENT --cycles / -c
# =============================================================================

class TestArgumentCycles:
    """Tests pour l'argument --cycles / -c."""

    def test_cycles_forme_longue(self):
        """Test de --cycles avec la forme longue."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--cycles', '4'])
        assert args.cycles == 4

    def test_cycles_forme_courte(self):
        """Test de -c avec la forme courte."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['-c', '8'])
        assert args.cycles == 8

    @pytest.mark.parametrize("valeur", [1, 2, 4, 8, 10])
    def test_cycles_valeurs_diverses(self, valeur):
        """Test paramétré avec divers nombres de cycles."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--cycles', str(valeur)])
        assert args.cycles == valeur


# =============================================================================
# TESTS POUR L'ARGUMENT --auto / -a
# =============================================================================

class TestArgumentAuto:
    """Tests pour l'argument --auto / -a."""

    def test_auto_forme_longue(self):
        """Test de --auto avec la forme longue."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--auto'])
        assert args.auto is True

    def test_auto_forme_courte(self):
        """Test de -a avec la forme courte."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['-a'])
        assert args.auto is True

    def test_auto_absent(self):
        """Vérifie que auto est False si non spécifié."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([])
        assert args.auto is False


# =============================================================================
# TESTS POUR L'ARGUMENT --pause-only / -p
# =============================================================================

class TestArgumentPauseOnly:
    """Tests pour l'argument --pause-only / -p."""

    def test_pause_only_forme_longue(self):
        """Test de --pause-only avec la forme longue."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--pause-only'])
        assert args.pause_only is True

    def test_pause_only_forme_courte(self):
        """Test de -p avec la forme courte."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['-p'])
        assert args.pause_only is True

    def test_pause_only_absent(self):
        """Vérifie que pause_only est False si non spécifié."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([])
        assert args.pause_only is False


# =============================================================================
# TESTS POUR L'ARGUMENT --silent / -s
# =============================================================================

class TestArgumentSilent:
    """Tests pour l'argument --silent / -s."""

    def test_silent_forme_longue(self):
        """Test de --silent avec la forme longue."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--silent'])
        assert args.silent is True

    def test_silent_forme_courte(self):
        """Test de -s avec la forme courte."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['-s'])
        assert args.silent is True

    def test_silent_absent(self):
        """Vérifie que silent est False si non spécifié."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([])
        assert args.silent is False


# =============================================================================
# TESTS POUR LES COMBINAISONS D'ARGUMENTS
# =============================================================================

class TestCombinaisons:
    """Tests pour les combinaisons d'arguments."""

    def test_combinaison_work_break(self):
        """Test de la combinaison --work et --break."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['--work', '50', '--break', '10'])
        assert args.work == 50
        assert args.pause == 10

    def test_combinaison_complete(self):
        """Test avec tous les arguments spécifiés."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([
            '-w', '45',
            '-b', '10',
            '-l', '20',
            '-c', '4',
            '-a',
            '-s'
        ])
        assert args.work == 45
        assert args.pause == 10
        assert args.pause_longue == 20
        assert args.cycles == 4
        assert args.auto is True
        assert args.silent is True

    def test_combinaison_formes_mixtes(self):
        """Test avec mélange de formes courtes et longues."""
        parser = creer_parseur_arguments()
        args = parser.parse_args([
            '--work', '30',
            '-b', '7',
            '--cycles', '3',
            '-a'
        ])
        assert args.work == 30
        assert args.pause == 7
        assert args.cycles == 3
        assert args.auto is True

    def test_scenario_pomodoro_classique(self):
        """Test du scénario Pomodoro classique (4 cycles de 25/5 min)."""
        parser = creer_parseur_arguments()
        args = parser.parse_args(['-w', '25', '-b', '5', '-c', '4', '-a'])
        assert args.work == 25
        assert args.pause == 5
        assert args.cycles == 4
        assert args.auto is True


# =============================================================================
# TESTS POUR LES ERREURS D'ARGUMENTS
# =============================================================================

class TestErreursArguments:
    """Tests pour les erreurs de parsing d'arguments."""

    def test_work_non_entier_echoue(self):
        """Test qu'une valeur non entière pour --work échoue."""
        parser = creer_parseur_arguments()
        with pytest.raises(SystemExit):
            parser.parse_args(['--work', 'abc'])

    def test_break_non_entier_echoue(self):
        """Test qu'une valeur non entière pour --break échoue."""
        parser = creer_parseur_arguments()
        with pytest.raises(SystemExit):
            parser.parse_args(['--break', 'xyz'])

    def test_cycles_non_entier_echoue(self):
        """Test qu'une valeur non entière pour --cycles échoue."""
        parser = creer_parseur_arguments()
        with pytest.raises(SystemExit):
            parser.parse_args(['--cycles', '3.5'])

    def test_argument_inconnu_echoue(self):
        """Test qu'un argument inconnu fait échouer le parsing."""
        parser = creer_parseur_arguments()
        with pytest.raises(SystemExit):
            parser.parse_args(['--inconnu'])

    def test_work_sans_valeur_echoue(self):
        """Test que --work sans valeur échoue."""
        parser = creer_parseur_arguments()
        with pytest.raises(SystemExit):
            parser.parse_args(['--work'])


# =============================================================================
# TESTS POUR L'AIDE
# =============================================================================

class TestAide:
    """Tests pour l'affichage de l'aide."""

    def test_help_disponible(self):
        """Vérifie que --help est disponible."""
        parser = creer_parseur_arguments()
        # --help fait un sys.exit(0)
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(['--help'])
        assert exc_info.value.code == 0

    def test_help_forme_courte(self):
        """Vérifie que -h est disponible."""
        parser = creer_parseur_arguments()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(['-h'])
        assert exc_info.value.code == 0
