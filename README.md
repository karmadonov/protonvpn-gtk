# ProtonVPN-GTK</h1>
  
![Screenshot](https://raw.githubusercontent.com/karmadonov/protonvpn-gtk/screenshots/protonvpn.png)


<b style="color:red">❗️ In development ❗️ See [status](#status).</b>

An unofficial GTK 3 client for ProtonVPN. It's just GTK+ frontend for [ProtonVPN/protonvpn-cli-ng](https://github.com/ProtonVPN/protonvpn-cli-ng/).

## Installation
### Requirements
* Python 3.6+
* protonvpn-cli-ng

### Installing
* install [protonvpn-cli-ng](https://github.com/ProtonVPN/protonvpn-cli-ng/) with all dependencies.
* install [PyGObjects](https://python-gtk-3-tutorial.readthedocs.io/en/latest/install.html).
* install [ProtonVPN-GTK](https://github.com/karmadonov/protonvpn-gtk): `sudo python3 setup.py install`

### Usage
Run `sudo protonvpn-gtk`.

### Status

Implementation ToDO:

- [X] Show connection status.
- [ ] Connect to server.
- [X] Disconnect the current session.
- [X] Change icon color on status change.
- [ ] Edit configuration.
- [ ] Add tests.
- [ ] Add logging.
