import cx_Freeze

executables = [cx_Freeze.Executable('main.py')]

cx_Freeze.setup(
    name="sunmoon game",
    options={'build_exe': {'packages': ['pygame', 'controles'],
                           'include_files': ['Capturaveis', 'Cenário', 'Icon', 'Menu', 'Personagens', 'Sons', 'Vencedor']}},

    executables=executables

)