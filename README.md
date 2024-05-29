# DTEK selenium parser


Quick-written program to to gather the data from https://www.dtek-kem.com.ua/ua/shutdowns.

Forked from https://github.com/jjisolo/dtek-selelium-parser

Install google-chrome:
``` bash
### Debian
sudo apt update && sudo apt install -y apt-transport-https ca-certificates curl  gnupg
curl -sSL -O https://dl.google.com/linux/linux_signing_key.pub
KEYRINGS_PATH=/usr/share/keyrings
sudo cp linux_signing_key.pub ${KEYRINGS_PATH}
echo "deb [arch=amd64 signed-by=${KEYRINGS_PATH}/linux_signing_key.pub] https://dl.google.com/linux/chrome/deb/ stable main" \
 | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update && sudo apt install -y google-chrome-stable
```

Usage:
``` bash
python3 ./dtek.py -f test.json --street "вул. Балаклієвська" --house "12"
python3 ./dtek.py --noheadless --json-stderr test.json --street "вул. Балаклієвська" --house "12"
```
