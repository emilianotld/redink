#!/usr/bin/env python3
# Copyright 2026 Alejandro Emiliano Toledo
# Licensed under the Apache License, Version 2.0

"""
Risk evaluation engine responsible for classifying findings
and estimating potential business impact.
"""
import random
from redink import __version__
def print_banner():
    RED = "\033[91m"
    RESET = "\033[0m"
    banner_main = r"""

  $$$$$$$\  $$$$$$$$\ $$$$$$$\  $$$$$$\ $$\   $$\ $$\   $$\ 
  $$  __$$\ $$  _____|$$  __$$\ \_$$  _|$$$\  $$ |$$ | $$  |
  $$ |  $$ |$$ |      $$ |  $$ |  $$ |  $$$$\ $$ |$$ |$$  / 
  $$$$$$$  |$$$$$\    $$ |  $$ |  $$ |  $$ $$\$$ |$$$$$  /  
  $$  __$$< $$  __|   $$ |  $$ |  $$ |  $$ \$$$$ |$$  $$<   
  $$ |  $$ |$$ |      $$ |  $$ |  $$ |  $$ |\$$$ |$$ |\$$\  
  $$ |  $$ |$$$$$$$$\ $$$$$$$  |$$$$$$\ $$ | \$$ |$$ | \$$\ 
  \__|  \__|\________|\_______/ \______|\__|  \__|\__|  \__|

                                                          
   """                                                                                                           
    banner_lava = r"""
                _ _       _    
    _ __ ___  _| (_)_ __ | | __
  | '__/ _ \/ _` | | '_ \| |/ /
  | | |  __/ (_| | | | | |   < 
  |_|  \___|\__,_|_|_| |_|_|\_\
 
    , . ' ,  .  , '  . , '
  v ` . v ' $ . v  $ .  ' v
 ~^~`~^~`~$~^~`~$~^~`~^~$~^~
  The floor is expensive lava.
    """

    banner_pluma = r"""
      / \
     /   \  (The Nib)
    |  |  |
     \ | /
      \|/
       v
       |
       | R E D I N K
       |
     ' v ,
   ( $$$$$ ) -> Estimated Loss Pool
    """
    banner_giant = r"""

    ██▀███  ▓█████ ▓█████▄  ██▓ ███▄    █  ██ ▄█▀     
    ▓██ ▒ ██▒▓█   ▀ ▒██▀ ██▌▓██▒ ██ ▀█   █  ██▄█▒ 
    ▓██ ░▄█ ▒▒███   ░██   █▌▒██▒▓██  ▀█ ██▒▓███▄░ 
    ▒██▀▀█▄  ▒▓█  ▄ ░▓█▄   ▌░██░▓██▒  ▐▌██▒▓██ █▄ 
    ░██▓ ▒██▒░▒████▒░▒████▓ ░██░▒██░   ▓██░▒██▒ █▄
    ░ ▒▓ ░▒▓░░░ ▒░ ░ ▒▒▓  ▒ ░▓  ░ ▒░   ▒ ▒ ▒ ▒▒ ▓▒
      ░▒ ░ ▒░ ░ ░  ░ ░ ▒  ▒  ▒ ░░ ░░   ░ ▒░░ ░▒ ▒░
      ░░   ░    ░    ░ ░  ░  ▒ ░   ░   ░ ░ ░ ░░ ░ 
      ░        ░  ░   ░     ░           ░ ░  ░   
                    ░                            
    
    Each attack takes its toll - document the risks!
    """
    selected_banner = random.choice([banner_main, banner_lava, banner_pluma, banner_giant])
    print(RED + selected_banner + RESET)
    print ("Welcome to REDINK - Risk Evaluation and Documentation INK")
    print ("Assessing risks, one ink drop at a time!\n")
    print("Version:", __version__, "\n")
    print("by Max Mars\n")
    print("Disclaimer:\n[!] Authorized use only. Assess systems you own or have explicit permission to test.\n[!] Risk and loss estimates are indicative, not guarantees.\n")
   
    