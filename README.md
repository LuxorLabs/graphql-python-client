# Luxor Python Library and Command Line GraphQL API Client

## API Documentation
This Library / Client implements a subset of available endpoints. API Docs can be found [here](https://docs.luxor.tech/).

## Get Started

To get started, you will need the following basic information:
- Endpoint: `https://api.beta.luxor.tech/graphql`
- Organization Slug: `luxor`
- API Key: Generated through Luxor UI

Additionally, remember to install the needed dependencies for the script with:

```bash
# We suggest using a python 3.10 and a virtual environment
pip install -r requirements3.txt
```

## Library Usage
Luxor is divided in two parts, the first one containing the GraphQL API requests and the second adds resolvers for the API output.

**Code Snippet**
```python
from luxor import API
from resolvers import RESOLVERS

API = API(host = 'https://api.beta.luxor.tech/graphql', method = 'POST', org = 'luxor', key = 'lxk514e9be027b9a132b1aa39bab818a12e')
RESOLVERS = RESOLVERS(df = False)

resp = API.method(parameters)
resolved = RESOLVERS.method(resp)
```

## Command Line Usage
To get started and get params help run:
```bash
python luxor.py -h
```

Result:
```console
$ python3 luxor.py --help

 Usage: luxor.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                   │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                            │
│ --help                        Show this message and exit.                                                                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ get-all-transaction-history        Get all the transaction history of the user associated to the token provided.                                                          │
│ get-hashrate-score-history         Returns a subaccount earnings, scoring hashrate and efficiency per day.                                                                │
│ get-pool-hashrate                  Returns an integer count of distinct Profile active workers.                                                                           │
│ get-profile-active-worker-count    Returns an integer count of distinct Profile active workers. Workers are classified as active if we recorded a share in the last 15    │
│                                    minutes.                                                                                                                               │
│ get-profile-inactive-worker-count  Returns an integer count of distinct Profile inactive workers. Workers are classified as inactive if we have not recorded a share in   │
│                                    the last 15 minutes.                                                                                                                   │
│ get-revenue                        Returns on-chain transactions for a subaccount and currency combo.                                                                     │
│ get-revenue-ph                     Returns average Hashprice per PH over the last 24H.                                                                                    │
│ get-subaccount-hashrate-history    Returns an object of a subaccount hashrate timeseries.                                                                                 │
│ get-subaccount-mining-summary      Returns an object of a subaccount mining summary.                                                                                      │
│ get-subaccount-workers-status      Returns an integer count of distinct Profile active workers.                                                                           │
│ get-subaccounts                    Returns all subaccounts that belong to the Profile owner of the API Key.                                                               │
│ get-transaction-history            Returns on-chain transactions for a subaccount and currency combo.                                                                     │
│ get-worker-details                 Returns object of all workers pointed to a subaccount hashrate and efficiency details with a user-defined interval.                    │
│ get-worker-details-1h              Returns object of all workers pointed to a subaccount hashrate and efficiency details in the last hour.                                │
│ get-worker-details-24h             Returns object of all workers pointed to a subaccount hashrate and efficiency details in the last 24 hours.                            │
│ get-worker-hashrate-history        Returns an object of a miner hashrate timeseries.                                                                                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Example usage:
```bash
python3 luxor.py -k KEY -f get_transaction_history -p username,BTC,10
```

## Developing

We use [pre-commit](https://pre-commit.com/#install) to maintain the same code standards. To use it just run:

```bash
pre-commit install
```

Now it will run the needed validations with each commit.

## Happy Hashing!
