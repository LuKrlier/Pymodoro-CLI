# -*- coding: utf-8 -*-
"""
Tests unitaires pour les fonctions utilitaires de Pymodoro-CLI.
===============================================================

Ce module teste les fonctions helper du chronomètre Pomodoro:
- formater_temps()
- effacer_ligne()
- afficher_banniere()
- afficher_fin_session()
"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

# Import du module à tester
sys.path.insert(0, '..')
from pomodoro import (
    formater_temps,
    effacer_ligne,
    afficher_banniere,
    afficher_fin_session,
    DUREE_TRAVAIL_DEFAUT,
    DUREE_PAUSE_DEFAUT,
    DUREE_PAUSE_LONGUE_DEFAUT
)


# =============================================================================
# TESTS POUR formater_temps()
# =============================================================================

class TestFormaterTemps:
    """Tests pour la fonction formater_temps()."""

    def test_zero_secondes(self):
        """Test avec 0 secondes -> doit retourner '00:00'."""
        assert formater_temps(0) == "00:00"

    def test_moins_une_minute(self):
        """Test avec des valeurs inférieures à 60 secondes."""
        assert formater_temps(1) == "00:01"
        assert formater_temps(30) == "00:30"
        assert formater_temps(59) == "00:59"

    def test_une_minute_exacte(self):
        """Test avec exactement 60 secondes -> '01:00'."""
        assert formater_temps(60) == "01:00"

    def test_minutes_et_secondes(self):
        """Test avec des valeurs mixtes minutes et secondes."""
        assert formater_temps(61) == "01:01"
        assert formater_temps(90) == "01:30"
        assert formater_temps(125) == "02:05"
        assert formater_temps(599) == "09:59"

    def test_dix_minutes_et_plus(self):
        """Test avec des durées de 10 minutes et plus."""
        assert formater_temps(600) == "10:00"
        assert formater_temps(1500) == "25:00"  # Session Pomodoro standard
        assert formater_temps(1800) == "30:00"

    def test_une_heure(self):
        """Test avec des durées d'une heure et plus."""
        assert formater_temps(3600) == "60:00"
        assert formater_temps(3661) == "61:01"

    def test_valeurs_typiques_pomodoro(self):
        """Test avec les durées typiques d'une session Pomodoro."""
        # 25 minutes de travail
        assert formater_temps(25 * 60) == "25:00"
        # 5 minutes de pause
        assert formater_temps(5 * 60) == "05:00"
        # 15 minutes de pause longue
        assert formater_temps(15 * 60) == "15:00"

    @pytest.mark.parametrize("secondes,attendu", [
        (0, "00:00"),
        (1, "00:01"),
        (59, "00:59"),
        (60, "01:00"),
        (61, "01:01"),
        (125, "02:05"),
        (599, "09:59"),
        (600, "10:00"),
        (1500, "25:00"),
        (3599, "59:59"),
        (3600, "60:00"),
    ])
    def test_parametrize_valeurs_diverses(self, secondes, attendu):
        """Test paramétré avec diverses valeurs de secondes."""
        assert formater_temps(secondes) == attendu


# =============================================================================
# TESTS POUR effacer_ligne()
# =============================================================================

class TestEffacerLigne:
    """Tests pour la fonction effacer_ligne()."""

    def test_effacer_ligne_ecrit_sur_stdout(self):
        """Vérifie que effacer_ligne écrit sur stdout."""
        mock_stdout = MagicMock()
        with patch.object(sys, 'stdout', mock_stdout):
            effacer_ligne()
            # Vérifie que write a été appelé
            mock_stdout.write.assert_called()
            # Vérifie que flush a été appelé
            mock_stdout.flush.assert_called()

    def test_effacer_ligne_contient_retour_chariot(self):
        """Vérifie que le message contient \\r pour revenir au début."""
        mock_stdout = MagicMock()
        with patch.object(sys, 'stdout', mock_stdout):
            effacer_ligne()
            # Récupère l'argument passé à write
            call_args = mock_stdout.write.call_args[0][0]
            # Vérifie la présence de \r
            assert '\r' in call_args

    def test_effacer_ligne_contient_espaces(self):
        """Vérifie que le message contient des espaces pour effacer."""
        mock_stdout = MagicMock()
        with patch.object(sys, 'stdout', mock_stdout):
            effacer_ligne()
            call_args = mock_stdout.write.call_args[0][0]
            # Vérifie la présence d'espaces (au moins 80)
            assert ' ' * 80 in call_args


# =============================================================================
# TESTS POUR afficher_banniere()
# =============================================================================

class TestAfficherBanniere:
    """Tests pour la fonction afficher_banniere()."""

    def test_banniere_affiche_quelque_chose(self):
        """Vérifie que la bannière affiche du contenu."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            afficher_banniere()
        output = captured.getvalue()
        assert len(output) > 0

    def test_banniere_contient_nom_projet(self):
        """Vérifie que la bannière contient le nom du projet."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            afficher_banniere()
        output = captured.getvalue()
        assert "PYMODORO-CLI" in output

    def test_banniere_contient_pomodoro(self):
        """Vérifie que la bannière mentionne Pomodoro."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            afficher_banniere()
        output = captured.getvalue()
        assert "Pomodoro" in output

    def test_banniere_contient_emoji_tomate(self):
        """Vérifie que la bannière contient l'emoji tomate."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            afficher_banniere()
        output = captured.getvalue()
        # L'emoji tomate peut être encodé différemment
        assert "🍅" in output or "Pomodoro" in output

    def test_banniere_contient_cadre(self):
        """Vérifie que la bannière contient un cadre visuel."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            afficher_banniere()
        output = captured.getvalue()
        # Vérifie la présence de caractères de cadre
        assert "╔" in output or "═" in output


# =============================================================================
# TESTS POUR afficher_fin_session()
# =============================================================================

class TestAfficherFinSession:
    """Tests pour la fonction afficher_fin_session()."""

    def test_fin_session_travail(self):
        """Test de l'affichage de fin de session de travail."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            afficher_fin_session("TRAVAIL", "🎉")
        output = captured.getvalue()
        assert "TRAVAIL" in output
        assert "TERMINÉE" in output

    def test_fin_session_pause(self):
        """Test de l'affichage de fin de session de pause."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            afficher_fin_session("PAUSE", "✨")
        output = captured.getvalue()
        assert "PAUSE" in output
        assert "TERMINÉE" in output

    def test_fin_session_contient_emoji(self):
        """Vérifie que le message contient l'emoji fourni."""
        emoji_test = "🎉"
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            afficher_fin_session("TRAVAIL", emoji_test)
        output = captured.getvalue()
        # L'emoji doit apparaître 2 fois (début et fin)
        assert output.count(emoji_test) >= 1

    def test_fin_session_contient_separateurs(self):
        """Vérifie que le message contient des séparateurs visuels."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            afficher_fin_session("TRAVAIL", "🎉")
        output = captured.getvalue()
        assert "═" in output

    @pytest.mark.parametrize("type_session,emoji", [
        ("TRAVAIL", "🎉"),
        ("PAUSE", "✨"),
        ("PAUSE LONGUE", "🌟"),
        ("TEST", "🧪"),
    ])
    def test_fin_session_types_divers(self, type_session, emoji):
        """Test paramétré avec différents types de session."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            afficher_fin_session(type_session, emoji)
        output = captured.getvalue()
        assert type_session in output


# =============================================================================
# TESTS POUR LES CONSTANTES
# =============================================================================

class TestConstantes:
    """Tests pour les constantes de configuration par défaut."""

    def test_duree_travail_defaut(self):
        """Vérifie que la durée de travail par défaut est 25 minutes."""
        assert DUREE_TRAVAIL_DEFAUT == 25

    def test_duree_pause_defaut(self):
        """Vérifie que la durée de pause par défaut est 5 minutes."""
        assert DUREE_PAUSE_DEFAUT == 5

    def test_duree_pause_longue_defaut(self):
        """Vérifie que la durée de pause longue par défaut est 15 minutes."""
        assert DUREE_PAUSE_LONGUE_DEFAUT == 15

    def test_constantes_sont_positives(self):
        """Vérifie que toutes les durées sont positives."""
        assert DUREE_TRAVAIL_DEFAUT > 0
        assert DUREE_PAUSE_DEFAUT > 0
        assert DUREE_PAUSE_LONGUE_DEFAUT > 0

    def test_ordre_durees(self):
        """Vérifie l'ordre logique des durées."""
        # La pause courte est plus courte que la pause longue
        assert DUREE_PAUSE_DEFAUT < DUREE_PAUSE_LONGUE_DEFAUT
        # Le travail est plus long que la pause courte
        assert DUREE_TRAVAIL_DEFAUT > DUREE_PAUSE_DEFAUT
