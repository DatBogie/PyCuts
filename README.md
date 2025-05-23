<h1 align="center"><img src="./icons/PyCutsLogoFull.png" height="45px"></h1>
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

<details>
<summary><h3>Windows</h3></summary>
<ol>
	<li>Download and extract <code>PyCuts-win.zip</code> from the <a href="https://github.com/DatBogie/PyCuts/releases/latest">latest release</a>.</li>
	<li>Run <code>install-win.bat</code> to create Start Menu shortcuts and install the <code>.exe</code>s to <code>%LOCALAPPDATA%\PyCuts</code>.</li>
	<li>Open <code>PyCuts</code> to start the PyCuts listener service.</li>
	<li>Right click on the tray icon and select <code>Open GUI</code> to open the GUI manager, or simply open <code>PyCuts Config</code>.</li>
</ol>
</details>

<details>
<summary><h3>Linux</h3></summary>
<ol>
	<li>Download and extract <code>PyCuts-lin.zip</code> from the <a href="https://github.com/DatBogie/PyCuts/releases/latest">latest release</a>.</li>
	<li>Run <code>install-lin.sh</code> to create <code>~/.local/share/applications</code> <code>.desktop</code> files and install the binaries to <code>~/.local/share/PyCuts</code>.</li>
	<li>Open <code>PyCuts</code> to start the PyCuts listener service.</li>
	<li>Right click on the tray icon and select <code>Open GUI</code> to open the GUI manager, or simply open <code>PyCuts Config</code>.</li>
</ol>
</details>

<details>
<summary><h3>macOS</h3></summary>
<ol>
<li>Download and extract <code>PyCuts-mac.zip</code> from the <a href="https://github.com/DatBogie/PyCuts/releases/latest">latest release</a>.</li>
<li>Run <code>install-mac.sh</code> to install <code>PyCuts Config.app</code> to <code>~/Applications</code>, and <code>PyCuts</code> to <code>/usr/local/bin</code>.</li>
<li>Open Terminal (or any other terminal emulator) and run <code>pycuts</code>. It may ask for or complain about not having certain permissions. Once it does, or you start seeing output, close the terminal window.</li>
<li>Open System Settings, go to <code>Privacy & Security > Accessibility</code>, and turn on the switch next to Terminal (or your terminal emulator app).</li>
<li>In System Settings, go to <code>Privacy & Security > Input Monitoring</code>, and turn on the switch next to Terminal (or your terminal emulator app).</li>
<li>Open Terminal (or any other terminal emulator) and run <code>pycuts</code> to start the PyCuts listener service.</li>
<li>Right click on the tray icon and select <code>Open GUI</code> to open the GUI manager, or simply open <code>PyCuts Config</code> from Launchpad or Spotlight Search.</li>
</ol>
</details>

---

# Building from Source
> [!Important]
> Python (`>=3.9`) must be installed, and it must be in PATH; running `python` (Windows) or `python3` must bring you into a Python shell.

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
