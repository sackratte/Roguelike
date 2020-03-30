#Zum Ausführen des Compilings: 
#1. Falls Ordner "build" Besteht: Ordner Löschen
#2. Command line im Hauptordner öffnen und eingeben: "python setup.py build"
#pygame und cx_Freeze müssen installiert sein

import cx_Freeze

executables = [cx_Freeze.Executable("main_game.py")]

cx_Freeze.setup(
    name="main",
    options={"build_exe": {"packages":["pygame","tcod"], "include_files":[("data", "data")]}},
    executables = executables

    )
