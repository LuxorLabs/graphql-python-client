from __future__ import annotations

import json
import logging
import os
from typing import Any

import typer
from dotenv import load_dotenv
from rich import print

from client import GraphQlClient

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("requests.log")],
)


app = typer.Typer()

HOST = os.getenv("HOST")
API_KEY = os.getenv("API_KEY")
METHOD = os.getenv("METHOD")

env_settings: list[str | None] = [HOST, API_KEY, METHOD]

if None in env_settings:
    print("[bold red]Alert![/bold red] It seems you have not setup your .env file.")
    print(
        "Please copy the [bold].env.example[/bold] with the name of [bold green].env[/bold green] and write your own values",
    )
    exit(1)


CLIENT = GraphQlClient(host=HOST, key=API_KEY, method=METHOD)  # type: ignore


@app.command()
def get_all_transaction_history(
    mpn: str,
    subaccount: str,
    first: int,
) -> dict[str, Any]:
    """
    Get all the transaction history of the user associated to the token provided.

    mpn (str): mining profile name, refers to the coin ticker
    subaccount (str): subaccount username
    first (int): limits the number of data points returned.
    """

    query = """query getAllTransactionHistory($cid: CurrencyProfileName!, $uname: String!, $first: Int) {
        getAllTransactionHistory(cid: $cid, uname: $uname, first: $first, orderBy: CREATED_AT_DESC) {
            edges {
                node {
                    transactionId
                    amount
                    status
                    payoutAddress
                    currency
                    createdAt
                }
            }
        }
    }
    """

    params = {"cid": mpn, "uname": f"{subaccount}", "first": first}

    return CLIENT.request(query, params)


@app.command()
def get_subaccounts(first: int, offset: int = 0) -> dict[str, Any]:
    """
    Returns all subaccounts that belong to the Profile owner of the API Key.

    first (int): limits the number of data points returned.
    offset (int): skips elements of data points returned.
    """

    query = """query getSubaccounts($first: Int, $offset: Int) {users(first: $first, offset: $offset) {edges {node {username}}}}"""
    params = {"first": first, "offset": offset}

    return CLIENT.request(query, params)


@app.command()
def get_subaccount_mining_summary(
    subaccount: str,
    mpn: str,
    input_interval: str,
) -> dict[str, Any]:
    """
    Returns an object of a subaccount mining summary.

    subaccount (str): subaccount username
    mpn (str): mining profile name, refers to the coin ticker
    inputInterval (str): intervals to generate the mining summary lookback, options are: `_15_MINUTE`, `_1_HOUR`, `_1_HOUR` and `_1_DAY`
    """

    query = """query getMiningSummary($mpn: MiningProfileName!, $userName: String!, $inputDuration: HashrateIntervals!) {
                    getMiningSummary(mpn: $mpn, userName: $userName, inputDuration: $inputDuration) {
                        hashrate
                        validShares
                        invalidShares
                        staleShares
                        badShares
                        lowDiffShares
                        revenue
                }
            }
    """

    params = {
        "userName": f"{subaccount}",
        "mpn": mpn,
        "inputDuration": input_interval,
    }

    return CLIENT.request(query, params)


@app.command()
def get_subaccount_hashrate_history(
    subaccount: str,
    mpn: str,
    input_interval: str,
    first: int,
) -> dict[str, Any]:
    """
    Returns an object of a subaccount hashrate timeseries.

    subaccount (str): subaccount username
    mpn (str): mining profile name, refers to the coin ticker
    input_interval (str): intervals to generate the timeseries, options are: `_15_MINUTE`, `_1_HOUR`, `_6_HOUR` and `_1_DAY`
    first (int): limits the number of data points returned
    """

    query = """query getHashrateHistory($inputUsername: String, $mpn: MiningProfileName, $inputInterval: HashrateIntervals, $first: Int) {
        getHashrateHistory(inputUsername: $inputUsername, mpn: $mpn, inputInterval: $inputInterval, first: $first) {
            edges {
                node {
                    time
                    hashrate
                }
            }
        }
    }"""
    params = {
        "inputUsername": f"{subaccount}",
        "mpn": mpn,
        "inputInterval": input_interval,
        "first": first,
    }

    return CLIENT.request(query, params)


@app.command()
def get_worker_details(
    subaccount: str,
    mpn: str,
    minutes: int,
    first: int,
) -> dict[str, Any]:
    """
    Returns object of all workers pointed to a subaccount hashrate and efficiency details with a user-defined interval.

    subaccount (str): subaccount username
    mpn (str): mining profile name, refers to the coin ticker
    minutes (int): minutes lookback to generate metrics
    first (int): limits the number of data points returned
    """

    query = """query getWorkerDetails($duration: IntervalInput!, $mpn: MiningProfileName!, $uname: String!, $first: Int) {
                    getWorkerDetails(
                        duration: $duration
                        mpn: $mpn
                        uname: $uname
                        first: $first
                    ) {
                        edges {
                        node {
                            workerName
                            hashrate
                            validShares
                            staleShares
                            badShares
                            duplicateShares
                            invalidShares
                            lowDiffShares
                            efficiency
                            revenue
                            status
                            updatedAt
                        }
                        }
                    }
                }"""

    duration = {"minutes": minutes}
    params = {
        "duration": duration,
        "mpn": mpn,
        "uname": f"{subaccount}",
        "first": first,
    }

    return CLIENT.request(query, params)


@app.command()
def get_worker_details_1H(
    subaccount: str,
    mpn: str,
    first: int,
) -> dict[str, Any]:
    """
    Returns object of all workers pointed to a subaccount hashrate and efficiency details in the last hour.

    subaccount (str): subaccount username
    mpn (str): mining profile name, refers to the coin ticker
    first (int): limits the number of data points returned
    """

    query = """query getWorkersOverview($mpn: MiningProfileName, $username: String, $first: Int) {
                miners(filter: {
                        miningProfileName: { equalTo: $mpn }
                        user: { username: { equalTo: $username } }
                }, first: $first) {
                    edges {
                    node {
                        workerName
                        details1H {
                            hashrate
                            status
                            efficiency
                            validShares
                            staleShares
                            badShares
                            duplicateShares
                            invalidShares
                            lowDiffShares
                        }
                    }
                }
            }
        }"""
    params = {"username": f"{subaccount}", "mpn": mpn, "first": first}

    return CLIENT.request(query, params)


@app.command()
def get_worker_details_24H(
    subaccount: str,
    mpn: str,
    first: int,
) -> dict[str, Any]:
    """
    Returns object of all workers pointed to a subaccount hashrate and efficiency details in the last 24 hours.

    subaccount (str): subaccount username
    mpn (str): mining profile name, refers to the coin ticker
    first (int): limits the number of data points returned
    """

    query = """query getWorkersOverview($mpn: MiningProfileName, $username: String, $first: Int) {
                miners(filter: {
                        miningProfileName: { equalTo: $mpn }
                        user: { username: { equalTo: $username } }
                }, first: $first) {
                    edges {
                    node {
                        workerName
                        details24H {
                            hashrate
                            status
                            efficiency
                            validShares
                            staleShares
                            badShares
                            duplicateShares
                            invalidShares
                            lowDiffShares
                        }
                    }
                }
            }
        }"""
    params = {"username": f"{subaccount}", "mpn": mpn, "first": first}

    return CLIENT.request(query, params)


@app.command()
def get_worker_hashrate_history(
    subaccount: str,
    workername: str,
    mpn: str,
    input_bucket: str,
    input_duration: str,
    first: int,
) -> dict[str, Any]:
    """
    Returns an object of a miner hashrate timeseries.

    subaccount (str): subaccount username
    workername (str): rig identifier
    mpn (str): mining profile name, refers to the coin ticker
    input_bucket (str): intervals to generate the timeseries, options are: `_15_MINUTE`, `_1_HOUR`, `_6_HOUR` and `_1_DAY`
    input_duration (str): intervals to generate the timeseries, options are: `_15_MINUTE`, `_1_HOUR`, `_6_HOUR` and `_1_DAY`
    first (int): limits the number of data points returned
    """

    query = """query getWorkerHashrateHistory($inputUsername: String!, $workerName: String!, $mpn: MiningProfileName!, $inputBucket: HashrateIntervals!, $inputDuration: HashrateIntervals!, $first: Int) {
                getWorkerHashrateHistory(username: $inputUsername, workerName: $workerName, mpn: $mpn, inputBucket: $inputBucket, inputDuration: $inputDuration, first: $first) {
                    edges {
                        node {
                            time
                            hashrate
                        }
                    }
                }
            }"""

    params = {
        "inputUsername": f"{subaccount}",
        "workerName": workername,
        "mpn": mpn,
        "inputBucket": input_bucket,
        "inputDuration": input_duration,
        "first": first,
    }

    return CLIENT.request(query, params)


@app.command()
def get_subaccount_workers_status(
    mpn: str,
    subaccount: str,
) -> dict[str, Any]:
    """
    Returns an integer count of distinct Profile active workers.

    mpn (str): mining profile name, refers to the coin ticker
    subaccount (str): subaccount name
    """

    query = """query getUserMinersStatusCount($usrname: String!, $mpn: MiningProfileName!) {
                getUserMinersStatusCount(usrname: $usrname, mpn: $mpn) {
                    dead
                    warning
                    active
                }
            }
    """

    params = {"mpn": mpn, "usrname": f"{subaccount}"}

    return CLIENT.request(query, params)


@app.command()
def get_pool_hashrate(mpn: str, org_slug: str) -> dict[str, Any]:
    """
    Returns an integer count of distinct Profile active workers.

    mpn (str): mining profile name, refers to the coin ticker
    org_slug (str): organization name
    """
    query = """query getPoolHashrate {
                getPoolHashrate(mpn: BTC, orgSlug: "luxor")
            }
        """
    params = {"mpn": mpn, "orgSlug": org_slug}
    return CLIENT.request(query, params)


@app.command()
def get_revenue(
    subaccount: str,
    mpn: str,
    start_interval: str,
    end_interval: str,
) -> dict[str, Any]:
    """
    Returns on-chain transactions for a subaccount and currency combo.

    subaccount (str): subaccount username
    mpn (str): mining profile name, refers to the coin ticker
    cid (str): currency identifier, refers to the coin ticker
    start_interval (str): string JSON representation of an interval of time that has passed
    end_interval (str): string JSON representation of an interval of time that has passed
    """

    query = """query getRevenue($uname: String!, $cid: CurrencyProfileName!, $startInterval: IntervalInput!, $endInterval: IntervalInput!) {
                getRevenue(uname: $uname, cid: $cid, startInterval: $startInterval, endInterval: $endInterval)
            }"""
    params = {
        "uname": f"{subaccount}",
        "cid": mpn,
        "startInterval": json.loads(start_interval),
        "endInterval": json.loads(end_interval),
    }

    return CLIENT.request(query, params)


@app.command()
def get_profile_active_worker_count(mpn: str) -> dict[str, Any]:
    """
    Returns an integer count of distinct Profile active workers.
    Workers are classified as active if we recorded a share in the last 15 minutes.

    mpn (str): mining profile name, refers to the coin ticker
    """

    query = """query getUserMinersStatusCount {
                getUserMinersStatusCount(mpn: BTC)
            }
        """
    params = {"mpn": mpn}

    return CLIENT.request(query, params)


@app.command()
def get_profile_inactive_worker_count(mpn: str) -> dict[str, Any]:
    """
    Returns an integer count of distinct Profile inactive workers.
    Workers are classified as inactive if we have not recorded a share in the last 15 minutes.

    mpn (str): Mining profile name, refers to the coin ticker
    """

    query = """query getInactiveWorkers {
                getProfileInactiveWorkers(mpn: BTC)
            }
        """
    params = {"mpn": mpn}

    return CLIENT.request(query, params)


@app.command()
def get_transaction_history(
    subaccount: str,
    cid: str,
    first: int,
) -> dict[str, Any]:
    """
    Returns on-chain transactions for a subaccount and currency combo.

    subaccount (str): Subaccount username
    cid (str): Currency identifier, refers to the coin ticker
    first (int): Limits the number of data points returned
    """

    query = """query getTransactionHistory($uname: String!, $cid: CurrencyProfileName!, $first: Int) {
                getTransactionHistory(uname: $uname, cid: $cid, first: $first, orderBy: CREATED_AT_DESC) {
                    edges {
                    node {
                        createdAt
                        amount
                        status
                        transactionId
                    }
                    }
                }
            }"""
    params = {"uname": f"{subaccount}", "cid": cid, "first": first}

    return CLIENT.request(query, params)


@app.command()
def get_hashrate_score_history(
    subaccount: str,
    mpn: str,
    first: int,
) -> dict[str, Any]:
    """

    Returns a subaccount earnings, scoring hashrate and efficiency per day.

    Args:
        subaccount (str): Subaccount username
        mpn (str): Mining profile name, refers to the coin ticker
        first (int): Limits the number of data points returned

    Returns:
        dict[str, Any]: JSON response of the graphql query
    """

    query = """ query getHashrateScoreHistory($mpn: MiningProfileName!, $uname: String!, $first : Int) {
                getHashrateScoreHistory(mpn: $mpn, uname: $uname, first: $first, orderBy: DATE_DESC) {
                    nodes {
                        date
                        hashrate
                        efficiency
                        revenue
                        }
                    }
                }"""

    params = {"uname": f"{subaccount}", "mpn": mpn, "first": first}

    return CLIENT.request(query, params)


@app.command()
def get_revenue_ph(mpn: str) -> dict[str, Any]:
    """

    Returns average Hashprice per PH over the last 24H.

    Args:
        mpn (str): Mining profile name, refers to the coin ticker

    Returns:
        dict[str, Any]: JSON response of the graphql query
    """

    query = """query getRevenuePh($mpn: MiningProfileName!) {
                getRevenuePh(mpn: $mpn)
            }
    """

    params = {"mpn": mpn}

    return CLIENT.request(query, params)


@app.command()
def create_custom_request(query: str, params: str) -> dict[str, Any]:
    """

    Returns the result of the custom graphql query sent to the endpoint

    Args:
        query (str): The GraphQl query to execute
        params (str): The string representation of the params e.g. '{"argument": "value"}'

    Returns:
        dict[str, Any]: JSON response of the graphql query.
    """

    return CLIENT.request(query, json.loads(params))


if __name__ == "__main__":
    app()
