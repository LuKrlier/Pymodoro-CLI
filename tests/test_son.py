# -*- coding: utf-8 -*-
"""
Tests unitaires pour les notifications sonores de Pymodoro-CLI.
===============================================================

Ce module teste la fonction emettre_son() et son comportement
sur différents systèmes d'exploitation.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

# Import du module à tester
sys.path.insert(0, '..')
from pomodoro import emettre_son


# =============================================================================
# TESTS POUR emettre_son() - WINDOWS
# =============================================================================

class TestEmettreSonWindows:
    """Tests pour emettre_son() sur Windows."""

    @patch('platform.system', return_value='Windows')
    def test_windows_utilise_winsound(self, mock_platform):
        """Vérifie que Windows utilise winsound.Beep."""
        mock_winsound = MagicMock()
        with patch.dict('sys.modules', {'winsound': mock_winsound}):
            with patch('pomodoro.time.sleep'):
                emettre_son()

        # winsound.Beep doit être appelé
        mock_winsound.Beep.assert_called()

    @patch('platform.system', return_value='Windows')
    def test_windows_beep_frequence_1000hz(self, mock_platform):
        """Vérifie que le beep est à 1000 Hz."""
        mock_winsound = MagicMock()
        with patch.dict('sys.modules', {'winsound': mock_winsound}):
            with patch('pomodoro.time.sleep'):
                emettre_son()

        # Vérifie les paramètres du premier appel
        first_call = mock_winsound.Beep.call_args_list[0]
        frequence = first_call[0][0]
        assert frequence == 1000

    @patch('platform.system', return_value='Windows')
    def test_windows_beep_duree_500ms(self, mock_platform):
        """Vérifie que le beep dure 500 ms."""
        mock_winsound = MagicMock()
        with patch.dict('sys.modules', {'winsound': mock_winsound}):
            with patch('pomodoro.time.sleep'):
                emettre_son()

        first_call = mock_winsound.Beep.call_args_list[0]
        duree = first_call[0][1]
        assert duree == 500

    @patch('platform.system', return_value='Windows')
    def test_windows_double_beep(self, mock_platform):
        """Vérifie qu'il y a deux beeps."""
        mock_winsound = MagicMock()
        with patch.dict('sys.modules', {'winsound': mock_winsound}):
            with patch('pomodoro.time.sleep'):
                emettre_son()

        # Beep doit être appelé 2 fois
        assert mock_winsound.Beep.call_count == 2


# =============================================================================
# TESTS POUR emettre_son() - MACOS
# =============================================================================

class TestEmettreSonMacOS:
    """Tests pour emettre_son() sur macOS."""

    @patch('platform.system', return_value='Darwin')
    @patch('os.system')
    def test_macos_utilise_afplay(self, mock_os_system, mock_platform):
        """Vérifie que macOS utilise afplay."""
        emettre_son()

        mock_os_system.assert_called_once()
        call_arg = mock_os_system.call_args[0][0]
        assert 'afplay' in call_arg

    @patch('platform.system', return_value='Darwin')
    @patch('os.system')
    def test_macos_joue_glass_aiff(self, mock_os_system, mock_platform):
        """Vérifie que macOS joue le son Glass.aiff."""
        emettre_son()

        call_arg = mock_os_system.call_args[0][0]
        assert 'Glass.aiff' in call_arg


# =============================================================================
# TESTS POUR emettre_son() - LINUX
# =============================================================================

class TestEmettreSonLinux:
    """Tests pour emettre_son() sur Linux."""

    @patch('platform.system', return_value='Linux')
    @patch('pomodoro.time.sleep')
    def test_linux_utilise_bel(self, mock_sleep, mock_platform):
        """Vérifie que Linux utilise le caractère BEL."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            with patch('builtins.print') as mock_print:
                emettre_son()

        # print avec '\a' doit être appelé
        mock_print.assert_called()

    @patch('platform.system', return_value='Linux')
    @patch('pomodoro.time.sleep')
    def test_linux_double_bel(self, mock_sleep, mock_platform):
        """Vérifie qu'il y a deux BEL sur Linux."""
        with patch('builtins.print') as mock_print:
            emettre_son()

        # print doit être appelé 2 fois
        assert mock_print.call_count == 2


# =============================================================================
# TESTS POUR emettre_son() - GESTION DES ERREURS
# =============================================================================

class TestEmettreSonErreurs:
    """Tests pour la gestion des erreurs dans emettre_son()."""

    @patch('platform.system', return_value='Windows')
    def test_erreur_winsound_fallback(self, mock_platform):
        """Vérifie le fallback si winsound échoue."""
        mock_winsound = MagicMock()
        mock_winsound.Beep.side_effect = Exception("Erreur audio")

        captured = StringIO()
        with patch.dict('sys.modules', {'winsound': mock_winsound}):
            with patch.object(sys, 'stdout', captured):
                emettre_son()

        # Doit afficher le message de fallback
        output = captured.getvalue()
        assert "BEEP" in output

    @patch('platform.system', return_value='Darwin')
    @patch('os.system', side_effect=Exception("Erreur système"))
    def test_erreur_macos_fallback(self, mock_os, mock_platform):
        """Vérifie le fallback si afplay échoue sur macOS."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            emettre_son()

        output = captured.getvalue()
        assert "BEEP" in output

    @patch('platform.system', return_value='UnknownOS')
    @patch('builtins.print', side_effect=[Exception("Erreur print"), None])
    def test_erreur_generique_fallback(self, mock_print, mock_platform):
        """Vérifie le fallback pour un OS inconnu avec erreur."""
        with patch('pomodoro.time.sleep'):
            # Ne doit pas lever d'exception
            emettre_son()


# =============================================================================
# TESTS POUR emettre_son() - SYSTÈMES INCONNUS
# =============================================================================

class TestEmettreSonAutreOS:
    """Tests pour emettre_son() sur des OS non reconnus."""

    @patch('platform.system', return_value='FreeBSD')
    @patch('pomodoro.time.sleep')
    def test_freebsd_utilise_bel(self, mock_sleep, mock_platform):
        """Vérifie que FreeBSD utilise le caractère BEL (fallback Linux)."""
        with patch('builtins.print') as mock_print:
            emettre_son()

        # Doit utiliser le fallback Linux (print avec '\a')
        mock_print.assert_called()

    @patch('platform.system', return_value='SunOS')
    @patch('pomodoro.time.sleep')
    def test_sunos_utilise_bel(self, mock_sleep, mock_platform):
        """Vérifie que SunOS utilise le caractère BEL (fallback Linux)."""
        with patch('builtins.print') as mock_print:
            emettre_son()

        mock_print.assert_called()
