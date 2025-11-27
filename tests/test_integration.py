# -*- coding: utf-8 -*-
"""
Tests d'intégration pour Pymodoro-CLI.
======================================

Ce module teste les scénarios d'utilisation complets de l'application,
simulant l'exécution du programme avec différentes configurations.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

# Import du module à tester
sys.path.insert(0, '..')
from pomodoro import main, creer_parseur_arguments


# =============================================================================
# TESTS D'INTÉGRATION - SCÉNARIOS COMPLETS
# =============================================================================

class TestScenarioComplet:
    """Tests de scénarios d'utilisation complets."""

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_execution_defaut(self, mock_config, mock_compte):
        """Test de l'exécution avec les paramètres par défaut."""
        with patch('sys.argv', ['pomodoro.py']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        # Le compte à rebours doit être appelé avec 25 minutes (défaut)
        mock_compte.assert_called()
        assert mock_compte.call_args[0][0] == 25

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_execution_travail_personnalise(self, mock_config, mock_compte):
        """Test avec une durée de travail personnalisée."""
        with patch('sys.argv', ['pomodoro.py', '--work', '45']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        # Vérifie que la durée personnalisée est utilisée
        assert mock_compte.call_args[0][0] == 45

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_execution_pause_only(self, mock_config, mock_compte):
        """Test du mode pause seule."""
        with patch('sys.argv', ['pomodoro.py', '--pause-only', '--break', '10']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        # Doit lancer une pause de 10 minutes
        mock_compte.assert_called_once_with(10, "PAUSE", False)


# =============================================================================
# TESTS D'INTÉGRATION - AFFICHAGE CONFIGURATION
# =============================================================================

class TestAffichageConfiguration:
    """Tests pour l'affichage de la configuration."""

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_affiche_configuration_travail(self, mock_config, mock_compte):
        """Vérifie que la durée de travail est affichée."""
        with patch('sys.argv', ['pomodoro.py', '--work', '30']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        output = captured.getvalue()
        assert "30 minutes" in output

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_affiche_configuration_pause(self, mock_config, mock_compte):
        """Vérifie que la durée de pause est affichée."""
        with patch('sys.argv', ['pomodoro.py', '--break', '7']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        output = captured.getvalue()
        assert "7 minutes" in output

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_affiche_configuration_cycles(self, mock_config, mock_compte):
        """Vérifie que le nombre de cycles est affiché."""
        with patch('sys.argv', ['pomodoro.py', '--cycles', '4']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                # Mock input pour les transitions entre cycles
                with patch('builtins.input', return_value=''):
                    main()

        output = captured.getvalue()
        assert "4" in output

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_affiche_mode_auto_oui(self, mock_config, mock_compte):
        """Vérifie l'affichage du mode auto activé."""
        with patch('sys.argv', ['pomodoro.py', '--auto']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        output = captured.getvalue()
        assert "Oui" in output

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_affiche_mode_auto_non(self, mock_config, mock_compte):
        """Vérifie l'affichage du mode auto désactivé."""
        with patch('sys.argv', ['pomodoro.py']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        output = captured.getvalue()
        assert "Non" in output


# =============================================================================
# TESTS D'INTÉGRATION - MULTI-CYCLES
# =============================================================================

class TestMultiCycles:
    """Tests pour l'exécution de plusieurs cycles."""

    @patch('pomodoro.executer_cycle_pomodoro')
    @patch('pomodoro.configurer_terminal')
    def test_execute_nombre_cycles_correct(self, mock_config, mock_cycle):
        """Vérifie que le bon nombre de cycles est exécuté."""
        nombre_cycles = 3
        with patch('sys.argv', ['pomodoro.py', '-c', str(nombre_cycles), '-a']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        # executer_cycle_pomodoro doit être appelé 3 fois
        assert mock_cycle.call_count == nombre_cycles

    @patch('pomodoro.executer_cycle_pomodoro')
    @patch('pomodoro.configurer_terminal')
    def test_cycles_numerotes_correctement(self, mock_config, mock_cycle):
        """Vérifie que les cycles sont numérotés correctement."""
        nombre_cycles = 4
        with patch('sys.argv', ['pomodoro.py', '-c', str(nombre_cycles), '-a']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        # Vérifie les numéros de cycle passés à la fonction
        for i, call in enumerate(mock_cycle.call_args_list, start=1):
            kwargs = call[1]
            assert kwargs['numero_cycle'] == i
            assert kwargs['total_cycles'] == nombre_cycles


# =============================================================================
# TESTS D'INTÉGRATION - MESSAGES FINAUX
# =============================================================================

class TestMessagesFinaux:
    """Tests pour les messages de fin de programme."""

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_message_remerciement_fin(self, mock_config, mock_compte):
        """Vérifie que le message de remerciement est affiché."""
        with patch('sys.argv', ['pomodoro.py']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        output = captured.getvalue()
        assert "Merci" in output or "Pymodoro" in output

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_banniere_affichee(self, mock_config, mock_compte):
        """Vérifie que la bannière est affichée au démarrage."""
        with patch('sys.argv', ['pomodoro.py']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        output = captured.getvalue()
        assert "PYMODORO-CLI" in output


# =============================================================================
# TESTS D'INTÉGRATION - GESTION DES ERREURS
# =============================================================================

class TestGestionErreurs:
    """Tests pour la gestion des erreurs et interruptions."""

    @patch('pomodoro.configurer_terminal')
    def test_argument_invalide_termine_programme(self, mock_config):
        """Vérifie que les arguments invalides terminent le programme."""
        with patch('sys.argv', ['pomodoro.py', '--work', 'invalid']):
            with pytest.raises(SystemExit):
                main()

    @patch('pomodoro.executer_cycle_pomodoro')
    @patch('pomodoro.configurer_terminal')
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_ctrl_c_entre_cycles(self, mock_input, mock_config, mock_cycle):
        """Vérifie que Ctrl+C entre les cycles termine proprement."""
        with patch('sys.argv', ['pomodoro.py', '-c', '2']):
            with patch.object(sys, 'stdout', MagicMock()):
                with pytest.raises(SystemExit) as exc_info:
                    main()

        assert exc_info.value.code == 0


# =============================================================================
# TESTS D'INTÉGRATION - SCÉNARIOS POMODORO RÉELS
# =============================================================================

class TestScenariosPomodoro:
    """Tests simulant des scénarios Pomodoro réels."""

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_scenario_pomodoro_classique(self, mock_config, mock_compte):
        """Test du scénario Pomodoro classique (25/5)."""
        with patch('sys.argv', ['pomodoro.py', '-w', '25', '-b', '5']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        # Session de travail de 25 minutes
        mock_compte.assert_called_with(25, "TRAVAIL", False)

    @patch('pomodoro.executer_cycle_pomodoro')
    @patch('pomodoro.configurer_terminal')
    def test_scenario_4_pomodoros_auto(self, mock_config, mock_cycle):
        """Test de 4 Pomodoros en mode automatique."""
        with patch('sys.argv', ['pomodoro.py', '-c', '4', '-a']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        # 4 cycles doivent être exécutés
        assert mock_cycle.call_count == 4

        # Tous en mode auto
        for call in mock_cycle.call_args_list:
            kwargs = call[1]
            assert kwargs['mode_auto'] is True

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_scenario_session_longue(self, mock_config, mock_compte):
        """Test d'une session de travail longue (45 min)."""
        with patch('sys.argv', ['pomodoro.py', '-w', '45', '-b', '15']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        mock_compte.assert_called_with(45, "TRAVAIL", False)

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.configurer_terminal')
    def test_scenario_pause_rapide(self, mock_config, mock_compte):
        """Test d'une pause rapide de 2 minutes."""
        with patch('sys.argv', ['pomodoro.py', '-p', '-b', '2']):
            captured = StringIO()
            with patch.object(sys, 'stdout', captured):
                main()

        mock_compte.assert_called_with(2, "PAUSE", False)
