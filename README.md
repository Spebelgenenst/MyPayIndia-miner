# MyPayIndia-miner
A better free lightweight autoclicker for MyPayIndia. Mine MPI inr for free and make money $$$$ (~2500inr per month)

> [!important]
> multiple accounts per person is against the ToS

![MyPayIndia Miner Logo](https://github.com/Spebelgenenst/MyPayIndia-miner/blob/main/assets/mpi-miner.png?raw=true)

## Setup
> [!note]
> I recommend using multiple ips for 10+ accounts and you should select a leader.
### Quickstart
1. go to [the latest release](https://github.com/Spebelgenenst/MyPayIndia-miner/releases/latest) and download the correct file for your os
2. run it in the terminal
```
miner --help
```
```
miner.exe --help
```

### Build it from source
1. install pyinstaller
```
pip install pyinstaller
```
2. go to [the latest release](https://github.com/Spebelgenenst/MyPayIndia-miner/releases/latest) and download miner.py
3. (recommended) put miner.py in a new directory (not downloads)
4. build
```
pyinstaller miner.py --onefile
```

### without pyinstaller
1. go to [the latest release](https://github.com/Spebelgenenst/MyPayIndia-miner/releases/latest) and download miner.py
2. install requests
```
pip install requests
```
3. run it
```
python miner.py --help
```

## How do the programm works

1. create a session
2. set PHPSESSID to your session id
3. get the X-CSRF-TOKEN **from** the javascript **for** the header
4. post request to https://mypayindia.com/iotm/button/click for mining

(the XSRF-TOKEN in the cookies is not important)

## License
This project is licensed under the GNU General Public License ver3 or later. See the [LICENSE](LICENSE) file for details.
