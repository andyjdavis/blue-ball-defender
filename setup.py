from cx_Freeze import setup,Executable

includefiles = [
'resources/DeathFlash.ogg',
'resources/sfx_fly.ogg',
'resources/terre.png',
'resources/music/DST-2ndBallad.mp3',
'resources/music/DST-AngryRobotIII.mp3',
'resources/music/DST-GangsterCredit.mp3',
]

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], 'include_files':includefiles}

setup(
    name = 'Blue Ball Defender',
    version = '1.0',
    description = 'Defend our fragile blue world',
    author = 'Andrew Davis',
    options = {"build_exe": build_exe_options}, 
	executables = [Executable(script="main.py", base="Win32GUI", targetName="BlueBallDefender.exe")]
)
