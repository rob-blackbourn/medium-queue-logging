# Code for "How to use Python logging QueueHandler with dictConfig"

The following script was tested on Ubuntu 18.04 with Python 3.7

```bash
# Clone the repo
git clone https://github.com/rob-blackbourn/medium-queue-logging.git

# Set up the project
cd medium-queue-logging
python3.7 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

# Run the example
export PYTHONPATH=.:$PYTHONPATH
python examples/main.py
```
