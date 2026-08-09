# MyPayIndia-miner
A better free lightweight autoclicker for MyPayIndia. Mine MPI inr for free and make money $$$$ (~2500inr per month)

![MyPayIndia Miner Logo](https://github.com/Spebelgenenst/MyPayIndia-miner/blob/main/assets/mpi-miner.png?raw=true)

## Setup (linux/macos)
download the latest release
```
curl -o miner.py https://github.com/Spebelgenenst/MyPayIndia-miner/releases/latest/download/miner.py
```
create a virtual environment
```
python -m venv .venv
```
activate the virtual environment **this needs to be done everytime to execute the programm**
```
source .venv/bin/activate
```
install requirements:
```
pip install requests
```
run the program (calibration may take a while)
```
python miner.py
```
note: Any information provided by the program regarding the CPS must be multiplied by 10 to be comparable to MyPayinda

## How do the programm works (concept)

1. create a session
2. set PHPSESSID to your session id
3. get the X-CSRF-TOKEN **from** the javascript **for** the header
4. post request to https://mypayindia.com/iotm/button/click for mining

(the XSRF-TOKEN in the cookies is not important)

## License
This project is licensed under the GNU General Public License ver3 or later. See the [LICENSE](LICENSE) file for details.
