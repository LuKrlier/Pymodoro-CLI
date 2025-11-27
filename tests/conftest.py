# -*- coding: utf-8 -*-
"""
Configuration et fixtures partagées pour les tests Pymodoro-CLI.
===============================================================

Ce fichier contient les fixtures pytest réutilisables dans tous les tests.
"""

import pytest
import sys
import os
from io import StringIO
from unittest.mock import MagicMock, patch

# Ajouter le répertoire parent au path pour importer pomodoro
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# =============================================================================
# FIXTURES POUR LA CAPTURE DE SORTIE
# =============================================================================

@pytest.fixture
def capture_stdout():
    """
    Fixture pour capturer la sortie standard (stdout).

    Yields:
        StringIO: Un objet StringIO qui capture stdout.

    Exemple:
        def test_output(capture_stdout):
            print("Hello")
            assert "Hello" in capture_stdout.getvalue()
    """
    captured = StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    yield captured
    sys.stdout = old_stdout


@pytest.fixture
def mock_stdout():
    """
    Fixture pour mocker sys.stdout.write et sys.stdout.flush.

    Utile pour tester les fonctions qui écrivent directement sur stdout
    sans passer par print().

    Yields:
        MagicMock: Le mock de stdout.
    """
    mock = MagicMock()
    with patch.object(sys, 'stdout', mock):
        yield mock


# =============================================================================
# FIXTURES POUR LES ARGUMENTS CLI
# =============================================================================

@pytest.fixture
def args_defaut():
    """
    Fixture retournant les arguments par défaut simulés.

    Returns:
        argparse.Namespace: Arguments par défaut du programme.
    """
    import argparse
    return argparse.Namespace(
        work=25,
        pause=5,
        pause_longue=15,
        cycles=1,
        auto=False,
        pause_only=False,
        silent=False
    )


@pytest.fixture
def args_personnalises():
    """
    Fixture retournant des arguments personnalisés.

    Returns:
        argparse.Namespace: Arguments personnalisés pour les tests.
    """
    import argparse
    return argparse.Namespace(
        work=50,
        pause=10,
        pause_longue=20,
        cycles=4,
        auto=True,
        pause_only=False,
        silent=True
    )


# =============================================================================
# FIXTURES POUR LE TEMPS
# =============================================================================

@pytest.fixture
def mock_time_sleep():
    """
    Fixture pour mocker time.sleep afin d'accélérer les tests.

    Yields:
        MagicMock: Le mock de time.sleep.
    """
    with patch('time.sleep') as mock_sleep:
        yield mock_sleep


@pytest.fixture
def mock_time():
    """
    Fixture pour mocker le module time complet.

    Yields:
        MagicMock: Le mock du module time.
    """
    with patch('pomodoro.time') as mock_t:
        yield mock_t


# =============================================================================
# FIXTURES POUR LE SON
# =============================================================================

@pytest.fixture
def mock_winsound():
    """
    Fixture pour mocker winsound sur Windows.

    Yields:
        MagicMock: Le mock de winsound.Beep.
    """
    mock = MagicMock()
    with patch.dict('sys.modules', {'winsound': mock}):
        yield mock


@pytest.fixture
def mock_platform_windows():
    """
    Fixture pour simuler un environnement Windows.

    Yields:
        MagicMock: Le mock de platform.system retournant "Windows".
    """
    with patch('platform.system', return_value="Windows"):
        yield


@pytest.fixture
def mock_platform_linux():
    """
    Fixture pour simuler un environnement Linux.

    Yields:
        MagicMock: Le mock de platform.system retournant "Linux".
    """
    with patch('platform.system', return_value="Linux"):
        yield


@pytest.fixture
def mock_platform_macos():
    """
    Fixture pour simuler un environnement macOS.

    Yields:
        MagicMock: Le mock de platform.system retournant "Darwin".
    """
    with patch('platform.system', return_value="Darwin"):
        yield


# =============================================================================
# FIXTURES POUR LES ENTRÉES UTILISATEUR
# =============================================================================

@pytest.fixture
def mock_input():
    """
    Fixture pour mocker la fonction input().

    Yields:
        MagicMock: Le mock de builtins.input.
    """
    with patch('builtins.input', return_value='') as mock_inp:
        yield mock_inp


@pytest.fixture
def mock_input_keyboard_interrupt():
    """
    Fixture pour simuler un Ctrl+C lors d'un input().

    Yields:
        MagicMock: Le mock de builtins.input levant KeyboardInterrupt.
    """
    with patch('builtins.input', side_effect=KeyboardInterrupt):
        yield
