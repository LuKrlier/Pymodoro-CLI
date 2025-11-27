# -*- coding: utf-8 -*-
"""
Tests unitaires pour le compte à rebours de Pymodoro-CLI.
=========================================================

Ce module teste les fonctionnalités de compte à rebours:
- compte_a_rebours()
- executer_cycle_pomodoro()
- Gestion des interruptions (Ctrl+C)
"""

import pytest
import sys
from unittest.mock import patch, MagicMock, call
from io import StringIO

# Import du module à tester
sys.path.insert(0, '..')
from pomodoro import (
    compte_a_rebours,
    executer_cycle_pomodoro,
    formater_temps
)


# =============================================================================
# TESTS POUR compte_a_rebours() - COMPORTEMENT GÉNÉRAL
# =============================================================================

class TestCompteAReboursGeneral:
    """Tests généraux pour la fonction compte_a_rebours()."""

    @patch('pomodoro.time.sleep')
    @patch('pomodoro.emettre_son')
    @patch('pomodoro.effacer_ligne')
    @patch('pomodoro.afficher_fin_session')
    def test_compte_a_rebours_session_travail(
        self, mock_fin, mock_effacer, mock_son, mock_sleep
    ):
        """Test d'une session de travail complète."""
        # Utilise une durée très courte pour le test (1 minute = 60 secondes)
        # On mock sleep pour qu'il ne bloque pas
        duree = 1

        # Capture stdout
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            compte_a_rebours(duree, "TRAVAIL")

        # Vérifie que sleep a été appelé (60 fois pour 1 minute)
        assert mock_sleep.call_count == duree * 60
        # Vérifie que le son a été émis
        mock_son.assert_called_once()
        # Vérifie que la ligne a été effacée
        mock_effacer.assert_called_once()
        # Vérifie que le message de fin a été affiché
        mock_fin.assert_called_once_with("TRAVAIL", "🎉")

    @patch('pomodoro.time.sleep')
    @patch('pomodoro.emettre_son')
    @patch('pomodoro.effacer_ligne')
    @patch('pomodoro.afficher_fin_session')
    def test_compte_a_rebours_session_pause(
        self, mock_fin, mock_effacer, mock_son, mock_sleep
    ):
        """Test d'une session de pause complète."""
        duree = 1

        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            compte_a_rebours(duree, "PAUSE")

        # Vérifie que le message de fin est pour une pause
        mock_fin.assert_called_once_with("PAUSE", "✨")

    @patch('pomodoro.time.sleep')
    @patch('pomodoro.emettre_son')
    def test_compte_a_rebours_affiche_message_demarrage(
        self, mock_son, mock_sleep
    ):
        """Vérifie que le message de démarrage est affiché."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            with patch('pomodoro.effacer_ligne'):
                with patch('pomodoro.afficher_fin_session'):
                    compte_a_rebours(1, "TRAVAIL")

        output = captured.getvalue()
        assert "Session de TRAVAIL démarrée" in output
        assert "1 minutes" in output

    @patch('pomodoro.time.sleep')
    @patch('pomodoro.emettre_son')
    def test_compte_a_rebours_affiche_ctrl_c_instruction(
        self, mock_son, mock_sleep
    ):
        """Vérifie que l'instruction Ctrl+C est affichée."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            with patch('pomodoro.effacer_ligne'):
                with patch('pomodoro.afficher_fin_session'):
                    compte_a_rebours(1, "TRAVAIL")

        output = captured.getvalue()
        assert "Ctrl+C" in output


# =============================================================================
# TESTS POUR compte_a_rebours() - EMOJI ET COULEURS
# =============================================================================

class TestCompteAReboursAffichage:
    """Tests pour l'affichage visuel du compte à rebours."""

    @patch('pomodoro.time.sleep')
    @patch('pomodoro.emettre_son')
    def test_emoji_tomate_pour_travail(self, mock_son, mock_sleep):
        """Vérifie que l'emoji tomate est utilisé pour le travail."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            with patch('pomodoro.effacer_ligne'):
                with patch('pomodoro.afficher_fin_session'):
                    compte_a_rebours(1, "TRAVAIL")

        output = captured.getvalue()
        assert "🍅" in output

    @patch('pomodoro.time.sleep')
    @patch('pomodoro.emettre_son')
    def test_emoji_cafe_pour_pause(self, mock_son, mock_sleep):
        """Vérifie que l'emoji café est utilisé pour la pause."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            with patch('pomodoro.effacer_ligne'):
                with patch('pomodoro.afficher_fin_session'):
                    compte_a_rebours(1, "PAUSE")

        output = captured.getvalue()
        assert "☕" in output

    @patch('pomodoro.time.sleep')
    @patch('pomodoro.emettre_son')
    def test_barre_progression_presente(self, mock_son, mock_sleep):
        """Vérifie que la barre de progression est affichée."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            with patch('pomodoro.effacer_ligne'):
                with patch('pomodoro.afficher_fin_session'):
                    compte_a_rebours(1, "TRAVAIL")

        output = captured.getvalue()
        # Vérifie la présence des caractères de barre de progression
        assert "█" in output or "░" in output


# =============================================================================
# TESTS POUR compte_a_rebours() - GESTION DU TEMPS
# =============================================================================

class TestCompteAReboursTemps:
    """Tests pour la gestion du temps dans le compte à rebours."""

    @patch('pomodoro.time.sleep')
    @patch('pomodoro.emettre_son')
    def test_sleep_appele_correctement(self, mock_son, mock_sleep):
        """Vérifie que time.sleep est appelé avec 1 seconde."""
        with patch.object(sys, 'stdout', MagicMock()):
            with patch('pomodoro.effacer_ligne'):
                with patch('pomodoro.afficher_fin_session'):
                    compte_a_rebours(1, "TRAVAIL")

        # Vérifie que sleep(1) est appelé pour chaque seconde
        mock_sleep.assert_called_with(1)

    @patch('pomodoro.time.sleep')
    @patch('pomodoro.emettre_son')
    def test_nombre_iterations_correct(self, mock_son, mock_sleep):
        """Vérifie que le nombre d'itérations est correct."""
        duree_minutes = 2
        with patch.object(sys, 'stdout', MagicMock()):
            with patch('pomodoro.effacer_ligne'):
                with patch('pomodoro.afficher_fin_session'):
                    compte_a_rebours(duree_minutes, "TRAVAIL")

        # 2 minutes = 120 secondes, sleep appelé 120 fois
        assert mock_sleep.call_count == duree_minutes * 60


# =============================================================================
# TESTS POUR compte_a_rebours() - INTERRUPTIONS
# =============================================================================

class TestCompteAReboursInterruptions:
    """Tests pour la gestion des interruptions (Ctrl+C)."""

    @patch('pomodoro.time.sleep')
    def test_keyboard_interrupt_gere(self, mock_sleep):
        """Vérifie que KeyboardInterrupt est géré proprement."""
        # Simule une interruption après quelques itérations
        mock_sleep.side_effect = [None, None, KeyboardInterrupt()]

        with patch.object(sys, 'stdout', MagicMock()):
            with patch('pomodoro.effacer_ligne'):
                with pytest.raises(SystemExit) as exc_info:
                    compte_a_rebours(1, "TRAVAIL")

        # Vérifie que le programme se termine avec code 0
        assert exc_info.value.code == 0

    @patch('pomodoro.time.sleep')
    def test_message_annulation_affiche(self, mock_sleep):
        """Vérifie que le message d'annulation est affiché."""
        mock_sleep.side_effect = KeyboardInterrupt()

        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            with patch('pomodoro.effacer_ligne'):
                with pytest.raises(SystemExit):
                    compte_a_rebours(1, "TRAVAIL")

        output = captured.getvalue()
        assert "annulée" in output


# =============================================================================
# TESTS POUR executer_cycle_pomodoro()
# =============================================================================

class TestExecuterCyclePomodoro:
    """Tests pour la fonction executer_cycle_pomodoro()."""

    @patch('pomodoro.compte_a_rebours')
    def test_affiche_numero_cycle(self, mock_compte):
        """Vérifie que le numéro de cycle est affiché."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            executer_cycle_pomodoro(
                duree_travail=25,
                duree_pause=5,
                duree_pause_longue=15,
                numero_cycle=2,
                total_cycles=4,
                mode_auto=True
            )

        output = captured.getvalue()
        assert "Cycle 2/4" in output

    @patch('pomodoro.compte_a_rebours')
    def test_dernier_cycle_pas_de_pause(self, mock_compte):
        """Vérifie que le dernier cycle n'a pas de pause après."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            executer_cycle_pomodoro(
                duree_travail=25,
                duree_pause=5,
                duree_pause_longue=15,
                numero_cycle=4,
                total_cycles=4,
                mode_auto=True
            )

        # compte_a_rebours ne doit être appelé qu'une fois (travail seulement)
        assert mock_compte.call_count == 1
        mock_compte.assert_called_with(25, "TRAVAIL", False)

    @patch('pomodoro.compte_a_rebours')
    @patch('pomodoro.time.sleep')
    def test_mode_auto_enchaine_pause(self, mock_sleep, mock_compte):
        """Vérifie que le mode auto enchaîne automatiquement la pause."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            executer_cycle_pomodoro(
                duree_travail=25,
                duree_pause=5,
                duree_pause_longue=15,
                numero_cycle=1,
                total_cycles=4,
                mode_auto=True
            )

        # compte_a_rebours doit être appelé 2 fois (travail + pause)
        assert mock_compte.call_count == 2

    @patch('pomodoro.compte_a_rebours')
    @patch('builtins.input', return_value='')
    def test_mode_manuel_attend_input(self, mock_input, mock_compte):
        """Vérifie que le mode manuel attend une entrée utilisateur."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            executer_cycle_pomodoro(
                duree_travail=25,
                duree_pause=5,
                duree_pause_longue=15,
                numero_cycle=1,
                total_cycles=4,
                mode_auto=False
            )

        # input() doit être appelé
        mock_input.assert_called_once()

    @patch('pomodoro.compte_a_rebours')
    def test_pause_longue_apres_4_cycles(self, mock_compte):
        """Vérifie qu'une pause longue est utilisée après 4 cycles."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            with patch('pomodoro.time.sleep'):
                executer_cycle_pomodoro(
                    duree_travail=25,
                    duree_pause=5,
                    duree_pause_longue=15,
                    numero_cycle=4,
                    total_cycles=8,
                    mode_auto=True
                )

        # Vérifie que la pause longue est appelée
        calls = mock_compte.call_args_list
        # Le deuxième appel doit être la pause longue (15 min)
        assert calls[1] == call(15, "PAUSE LONGUE", False)

    @patch('pomodoro.compte_a_rebours')
    def test_pause_courte_cycles_normaux(self, mock_compte):
        """Vérifie qu'une pause courte est utilisée pour les cycles normaux."""
        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            with patch('pomodoro.time.sleep'):
                executer_cycle_pomodoro(
                    duree_travail=25,
                    duree_pause=5,
                    duree_pause_longue=15,
                    numero_cycle=1,
                    total_cycles=4,
                    mode_auto=True
                )

        calls = mock_compte.call_args_list
        # Le deuxième appel doit être la pause courte (5 min)
        assert calls[1] == call(5, "PAUSE", False)


# =============================================================================
# TESTS POUR executer_cycle_pomodoro() - INTERRUPTIONS
# =============================================================================

class TestExecuterCycleInterruptions:
    """Tests pour les interruptions dans executer_cycle_pomodoro()."""

    @patch('pomodoro.compte_a_rebours')
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt_pendant_input(self, mock_input, mock_compte):
        """Vérifie que Ctrl+C pendant input() termine proprement."""
        with patch.object(sys, 'stdout', MagicMock()):
            with pytest.raises(SystemExit) as exc_info:
                executer_cycle_pomodoro(
                    duree_travail=25,
                    duree_pause=5,
                    duree_pause_longue=15,
                    numero_cycle=1,
                    total_cycles=4,
                    mode_auto=False
                )

        assert exc_info.value.code == 0


# =============================================================================
# TESTS POUR LA LOGIQUE DE PAUSE LONGUE
# =============================================================================

class TestLogiquePauseLongue:
    """Tests pour la logique de pause longue (tous les 4 cycles)."""

    @pytest.mark.parametrize("cycle,attendu_longue", [
        (1, False),
        (2, False),
        (3, False),
        (4, True),
        (5, False),
        (6, False),
        (7, False),
        (8, True),
    ])
    @patch('pomodoro.compte_a_rebours')
    def test_cycle_pause_longue_modulo_4(
        self, mock_compte, cycle, attendu_longue
    ):
        """Vérifie que la pause longue est utilisée tous les 4 cycles."""
        # Pas le dernier cycle pour avoir une pause
        total_cycles = cycle + 1

        captured = StringIO()
        with patch.object(sys, 'stdout', captured):
            with patch('pomodoro.time.sleep'):
                executer_cycle_pomodoro(
                    duree_travail=25,
                    duree_pause=5,
                    duree_pause_longue=15,
                    numero_cycle=cycle,
                    total_cycles=total_cycles,
                    mode_auto=True
                )

        calls = mock_compte.call_args_list
        if len(calls) > 1:
            type_pause_appele = calls[1][0][1]
            if attendu_longue:
                assert type_pause_appele == "PAUSE LONGUE"
            else:
                assert type_pause_appele == "PAUSE"
