# <img src="./icons/PyCutsTrayIcon.png" height="20px"> PyCuts
Global shortcuts service with GUI manager, written in Python.

---

# Installation/Use
Every supported OS (Windows, Linux, macOS) will have a `.zip` file in each release. Each archive contains two items:

1. `PyCuts`
<br>`.exe` on Windows; no extension on Linux/macOS.
<br>The listener service (backend) that actually detects keypresses and runs shortcut commands.
2. `PyCuts Config`
<br>`.exe` on Windows; no extension on Linux; `.app` on macOS.
<br>The GUI configurator that allows easily managing global shortcuts.

## Windows
1. Download and extract `PyCuts-win.zip` from the [latest release](https://github.com/DatBogie/PyCuts/releases/latest).
2. Run `install-win.bat` to create Start Menu shortcuts and install the `.exe`s to `%LOCALAPPDATA%\PyCuts`.
3. Open `PyCuts` to start the PyCuts listener service.
4. Right click on the tray icon and select `Open GUI` to open the GUI manager, or simply open `PyCuts Config`.

## Linux
1. Download and extract `PyCuts-lin.zip` from the [latest release](https://github.com/DatBogie/PyCuts/releases/latest).
2. Run `install-lin.sh` to create `~/.local/share/applications` `.desktop` files and install the binaries to `~/.local/share/PyCuts`.
3. Open `PyCuts` to start the PyCuts listener service.
4. Right click on the tray icon and select `Open GUI` to open the GUI manager, or simply open `PyCuts Config`.

## macOS
1. Download and extract `PyCuts-mac.zip` from the [latest release](https://github.com/DatBogie/PyCuts/releases/latest).
2. Run `install-mac.sh` to install `PyCuts Config.app` to `~/Applications`, and `PyCuts` to `/usr/local/bin`.
3. Open Terminal (or any other terminal emulator) and run `pycuts`. It may ask for or complain about not having certain permissions. Once it does, or you start seeing output, close the terminal window.
3. Open System Settings, go to `Privacy & Security > Accessibility`, and turn on the switch next to Terminal (or your terminal emulator app).
4. In System Settings, go to `Privacy & Security > Input Monitoring`, and turn on the switch next to Terminal (or your terminal emulator app).
5. Open Terminal (or any other terminal emulator) and run `pycuts` to start the PyCuts listener service.
6. Right click on the tray icon and select `Open GUI` to open the GUI manager, or simply open `PyCuts Config` from Launchpad or Spotlight Search.

---

# Building from Source
> [!Important]
> Python (`>=3.9`) must be installed, and it must be in PATH—running `python` (Windows) or `python3` must bring you into a Python shell.

1. Clone this repository by either:
	<br>a) Cloning it with `git` in a terminal:

	```
	git clone https://github.com/DatBogie/PyCuts.git
	```
	b) Downloading it as a `.zip`:
		1. Scroll up and click the blue `<> Code` button.
		2. Click `Download ZIP`.
		3. Extract `PyCuts-main.zip`.
2. Open a terminal emulator and `cd` into the repository.
3. Run `build.py`:
	##### Windows:

	```
	python build.py
	```
	##### Linux/macOS:

	```
	python3 build.py
	```
---