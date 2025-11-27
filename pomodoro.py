#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pymodoro-CLI - Chronomètre Pomodoro en ligne de commande
=========================================================

Un outil CLI simple et efficace pour gérer vos sessions de travail
en utilisant la technique Pomodoro.

Auteur: Lukrlier (Lurlier Inc)
Licence: MIT
"""

import argparse
import sys
import time
import platform
import os


# =============================================================================
# CONFIGURATION DE L'ENCODAGE POUR WINDOWS
# =============================================================================

def configurer_terminal():
    """
    Configure le terminal pour supporter les caractères Unicode sur Windows.

    Sur Windows, le terminal utilise par défaut l'encodage cp1252 qui ne supporte
    pas tous les caractères Unicode (comme les emojis). Cette fonction configure
    le terminal pour utiliser UTF-8.
    """
    if platform.system() == "Windows":
        # Active le mode UTF-8 pour la console Windows
        os.system('chcp 65001 >nul 2>&1')
        # Reconfigure stdout pour utiliser UTF-8
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')


# =============================================================================
# CONFIGURATION PAR DÉFAUT
# =============================================================================

# Durée par défaut d'une session de travail (en minutes)
DUREE_TRAVAIL_DEFAUT = 25

# Durée par défaut d'une pause courte (en minutes)
DUREE_PAUSE_DEFAUT = 5

# Durée par défaut d'une pause longue (en minutes)
DUREE_PAUSE_LONGUE_DEFAUT = 15


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def effacer_ligne():
    """
    Efface la ligne courante du terminal et repositionne le curseur au début.
    Utilise le caractère de retour chariot (\r) pour revenir au début de la ligne.
    """
    # \r ramène le curseur au début de la ligne
    # Les espaces effacent le contenu précédent
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()


def formater_temps(secondes):
    """
    Convertit un nombre de secondes en format MM:SS lisible.

    Args:
        secondes (int): Le nombre total de secondes à convertir.

    Returns:
        str: Le temps formaté sous la forme "MM:SS".

    Exemple:
        >>> formater_temps(125)
        '02:05'
    """
    minutes = secondes // 60
    secs = secondes % 60
    return f"{minutes:02d}:{secs:02d}"


def emettre_son():
    """
    Émet un son de notification selon le système d'exploitation.

    - Windows: Utilise le beep système via winsound
    - macOS: Utilise la commande 'afplay' avec un son système
    - Linux: Utilise le caractère BEL (\\a) pour le terminal

    En cas d'échec, affiche simplement "BEEP!" dans le terminal.
    """
    systeme = platform.system()

    try:
        if systeme == "Windows":
            # Sous Windows, on utilise le module winsound
            import winsound
            # Fréquence: 1000 Hz, Durée: 500 ms
            winsound.Beep(1000, 500)
            time.sleep(0.1)
            winsound.Beep(1000, 500)
        elif systeme == "Darwin":  # macOS
            # Sous macOS, on utilise le son système "Glass"
            import os
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        else:  # Linux et autres systèmes Unix
            # Utilise le caractère BEL pour émettre un bip terminal
            print('\a', end='', flush=True)
            time.sleep(0.3)
            print('\a', end='', flush=True)
    except Exception:
        # Si tout échoue, on affiche un message textuel
        print("\n🔔 BEEP! BEEP!")


def afficher_banniere():
    """
    Affiche la bannière ASCII du programme au démarrage.
    Donne une identité visuelle au chronomètre Pomodoro.
    """
    banniere = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🍅  PYMODORO-CLI - Chronomètre Pomodoro  🍅             ║
    ║                                                           ║
    ║   Technique Pomodoro : Travaillez efficacement !          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banniere)


def afficher_fin_session(type_session, message_emoji):
    """
    Affiche un message visuel clair à la fin d'une session.

    Args:
        type_session (str): Le type de session terminée ("TRAVAIL" ou "PAUSE").
        message_emoji (str): L'emoji à afficher avec le message.
    """
    print("\n")
    print("    " + "═" * 55)
    print(f"    ║  {message_emoji}  SESSION DE {type_session} TERMINÉE !  {message_emoji}  ")
    print("    " + "═" * 55)
    print("\n")


# =============================================================================
# FONCTION PRINCIPALE DU COMPTE À REBOURS
# =============================================================================

def compte_a_rebours(duree_minutes, type_session="TRAVAIL"):
    """
    Lance un compte à rebours dynamique dans le terminal.

    Cette fonction affiche un compte à rebours qui s'actualise sur la même ligne,
    sans spammer la console. Elle utilise le retour chariot (\r) pour écraser
    l'affichage précédent.

    Args:
        duree_minutes (int): La durée du compte à rebours en minutes.
        type_session (str): Le type de session ("TRAVAIL" ou "PAUSE").
                           Utilisé pour personnaliser l'affichage.

    Raises:
        KeyboardInterrupt: Si l'utilisateur appuie sur Ctrl+C pour annuler.
    """
    # Conversion de la durée en secondes
    duree_totale_secondes = duree_minutes * 60
    secondes_restantes = duree_totale_secondes

    # Définition des couleurs et emojis selon le type de session
    if type_session == "TRAVAIL":
        emoji = "🍅"
        couleur_debut = "\033[91m"  # Rouge pour le travail
    else:
        emoji = "☕"
        couleur_debut = "\033[92m"  # Vert pour la pause

    couleur_fin = "\033[0m"  # Réinitialisation de la couleur

    # Message de démarrage
    print(f"\n    {emoji} Session de {type_session} démarrée ({duree_minutes} minutes)")
    print("    " + "─" * 45)
    print("    Appuyez sur Ctrl+C pour annuler.\n")

    try:
        # Boucle principale du compte à rebours
        while secondes_restantes >= 0:
            # Calcul de la progression (barre de progression visuelle)
            progression = 1 - (secondes_restantes / duree_totale_secondes)
            largeur_barre = 30
            rempli = int(largeur_barre * progression)
            vide = largeur_barre - rempli

            # Construction de la barre de progression
            barre = "█" * rempli + "░" * vide

            # Formatage du temps restant
            temps_formate = formater_temps(secondes_restantes)

            # Affichage dynamique sur la même ligne
            # \r ramène le curseur au début de la ligne
            message = f"    {emoji} [{barre}] {couleur_debut}{temps_formate}{couleur_fin} restant"
            sys.stdout.write('\r' + message)
            sys.stdout.flush()

            # Attente d'une seconde avant la prochaine mise à jour
            if secondes_restantes > 0:
                time.sleep(1)

            secondes_restantes -= 1

        # Fin du compte à rebours
        effacer_ligne()

        # Notification sonore
        emettre_son()

        # Message visuel de fin
        if type_session == "TRAVAIL":
            afficher_fin_session("TRAVAIL", "🎉")
            print("    💡 Conseil : Prenez une pause bien méritée !\n")
        else:
            afficher_fin_session("PAUSE", "✨")
            print("    💪 Conseil : Prêt pour une nouvelle session de travail !\n")

    except KeyboardInterrupt:
        # Gestion de l'annulation par l'utilisateur (Ctrl+C)
        effacer_ligne()
        print(f"\n\n    ⚠️  Session de {type_session} annulée par l'utilisateur.\n")
        sys.exit(0)


# =============================================================================
# GESTION DES ARGUMENTS EN LIGNE DE COMMANDE
# =============================================================================

def creer_parseur_arguments():
    """
    Crée et configure le parseur d'arguments de ligne de commande.

    Utilise argparse pour permettre à l'utilisateur de personnaliser
    les durées des sessions via des arguments.

    Returns:
        argparse.ArgumentParser: Le parseur configuré avec tous les arguments.

    Arguments disponibles:
        --work, -w    : Durée de la session de travail en minutes
        --break, -b   : Durée de la pause courte en minutes
        --long-break  : Durée de la pause longue en minutes
        --cycles, -c  : Nombre de cycles Pomodoro à effectuer
        --auto        : Mode automatique (enchaîne travail et pauses)
    """
    parser = argparse.ArgumentParser(
        prog='pomodoro',
        description='''
        🍅 Pymodoro-CLI - Chronomètre Pomodoro en ligne de commande

        La technique Pomodoro consiste à travailler en sessions concentrées
        de 25 minutes, suivies de courtes pauses de 5 minutes.
        Après 4 sessions, prenez une pause longue de 15-30 minutes.
        ''',
        epilog='''
        Exemples d'utilisation:
          python pomodoro.py                    # Session de travail par défaut (25 min)
          python pomodoro.py --work 50          # Session de travail de 50 minutes
          python pomodoro.py --break 10         # Pause de 10 minutes
          python pomodoro.py -w 25 -b 5 -c 4    # 4 cycles complets
          python pomodoro.py --auto -c 4        # Mode automatique avec 4 cycles
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Argument pour la durée de travail
    parser.add_argument(
        '-w', '--work',
        type=int,
        default=DUREE_TRAVAIL_DEFAUT,
        metavar='MINUTES',
        help=f'Durée de la session de travail en minutes (défaut: {DUREE_TRAVAIL_DEFAUT})'
    )

    # Argument pour la durée de pause courte
    parser.add_argument(
        '-b', '--break',
        type=int,
        default=DUREE_PAUSE_DEFAUT,
        dest='pause',  # Renommé car 'break' est un mot réservé Python
        metavar='MINUTES',
        help=f'Durée de la pause courte en minutes (défaut: {DUREE_PAUSE_DEFAUT})'
    )

    # Argument pour la pause longue
    parser.add_argument(
        '-l', '--long-break',
        type=int,
        default=DUREE_PAUSE_LONGUE_DEFAUT,
        dest='pause_longue',
        metavar='MINUTES',
        help=f'Durée de la pause longue en minutes (défaut: {DUREE_PAUSE_LONGUE_DEFAUT})'
    )

    # Argument pour le nombre de cycles
    parser.add_argument(
        '-c', '--cycles',
        type=int,
        default=1,
        metavar='N',
        help='Nombre de cycles Pomodoro à effectuer (défaut: 1)'
    )

    # Mode automatique
    parser.add_argument(
        '-a', '--auto',
        action='store_true',
        help='Mode automatique : enchaîne travail et pauses sans intervention'
    )

    # Mode pause seule
    parser.add_argument(
        '-p', '--pause-only',
        action='store_true',
        help='Lance uniquement une session de pause'
    )

    # Mode silencieux (pas de son)
    parser.add_argument(
        '-s', '--silent',
        action='store_true',
        help='Mode silencieux : désactive les notifications sonores'
    )

    return parser


# =============================================================================
# FONCTIONS DE GESTION DES CYCLES
# =============================================================================

def executer_cycle_pomodoro(duree_travail, duree_pause, duree_pause_longue,
                            numero_cycle, total_cycles, mode_auto):
    """
    Exécute un cycle Pomodoro complet (travail + pause).

    Args:
        duree_travail (int): Durée de la session de travail en minutes.
        duree_pause (int): Durée de la pause courte en minutes.
        duree_pause_longue (int): Durée de la pause longue en minutes.
        numero_cycle (int): Numéro du cycle actuel (commence à 1).
        total_cycles (int): Nombre total de cycles à effectuer.
        mode_auto (bool): Si True, enchaîne automatiquement les sessions.
    """
    print(f"\n    📊 Cycle {numero_cycle}/{total_cycles}")
    print("    " + "═" * 45)

    # Session de travail
    compte_a_rebours(duree_travail, "TRAVAIL")

    # Vérification si c'est le dernier cycle
    if numero_cycle == total_cycles:
        print("    🏆 Félicitations ! Tous les cycles sont terminés !")
        print("    " + "═" * 45 + "\n")
        return

    # Détermination du type de pause (longue après 4 cycles)
    if numero_cycle % 4 == 0:
        duree_pause_actuelle = duree_pause_longue
        type_pause = "PAUSE LONGUE"
    else:
        duree_pause_actuelle = duree_pause
        type_pause = "PAUSE"

    # En mode automatique, on enchaîne directement
    if mode_auto:
        print(f"    ⏭️  Enchaînement automatique vers la {type_pause}...")
        time.sleep(2)
        compte_a_rebours(duree_pause_actuelle, type_pause)
    else:
        # Sinon, on demande confirmation à l'utilisateur
        print(f"    ❓ Appuyez sur Entrée pour démarrer la {type_pause} ({duree_pause_actuelle} min)...")
        print("       (ou Ctrl+C pour quitter)")
        try:
            input()
            compte_a_rebours(duree_pause_actuelle, type_pause)
        except KeyboardInterrupt:
            print("\n\n    👋 À bientôt !\n")
            sys.exit(0)


# =============================================================================
# POINT D'ENTRÉE DU PROGRAMME
# =============================================================================

def main():
    """
    Fonction principale du programme.

    Cette fonction orchestre l'exécution du chronomètre Pomodoro:
    1. Configure le terminal pour l'UTF-8 (Windows)
    2. Affiche la bannière de bienvenue
    3. Parse les arguments de ligne de commande
    4. Exécute les cycles Pomodoro selon les paramètres
    """
    # Configuration du terminal pour supporter les emojis sur Windows
    configurer_terminal()

    # Affichage de la bannière
    afficher_banniere()

    # Création et parsing des arguments
    parser = creer_parseur_arguments()
    args = parser.parse_args()

    # Récupération des paramètres
    duree_travail = args.work
    duree_pause = args.pause
    duree_pause_longue = args.pause_longue
    nombre_cycles = args.cycles
    mode_auto = args.auto
    pause_seule = args.pause_only

    # Affichage de la configuration actuelle
    print("    ⚙️  Configuration:")
    print(f"       • Travail    : {duree_travail} minutes")
    print(f"       • Pause      : {duree_pause} minutes")
    print(f"       • Pause longue: {duree_pause_longue} minutes")
    print(f"       • Cycles     : {nombre_cycles}")
    print(f"       • Mode auto  : {'Oui' if mode_auto else 'Non'}")

    # Mode pause seule
    if pause_seule:
        compte_a_rebours(duree_pause, "PAUSE")
        return

    # Exécution des cycles
    for cycle in range(1, nombre_cycles + 1):
        executer_cycle_pomodoro(
            duree_travail=duree_travail,
            duree_pause=duree_pause,
            duree_pause_longue=duree_pause_longue,
            numero_cycle=cycle,
            total_cycles=nombre_cycles,
            mode_auto=mode_auto
        )

        # Pause entre les cycles (sauf mode auto)
        if cycle < nombre_cycles and not mode_auto:
            print(f"\n    ⏭️  Appuyez sur Entrée pour démarrer le cycle {cycle + 1}...")
            try:
                input()
            except KeyboardInterrupt:
                print("\n\n    👋 À bientôt !\n")
                sys.exit(0)

    # Message final
    print("\n    🍅 Merci d'avoir utilisé Pymodoro-CLI !")
    print("    📈 Continuez à travailler efficacement !\n")


# =============================================================================
# EXÉCUTION DU SCRIPT
# =============================================================================

if __name__ == "__main__":
    main()
