# import packages
import pandas as pd
from typing import Dict, Any, Union

class RESOLVERS:
    """
    A class used to resolve (format) GraphQL API responses into a Python list 
    or Pandas DataFrame from Luxor's API.

    Methods
    -------
    resolve_get_subaccounts(json)
        Returns a formatted object of all subaccounts that belong to the Profile owner of the API Key.
    
    resolve_get_subaccount_hashrate_history(json)
        Returns a formatted object of a subaccount hashrate timeseries. 

    resolve_get_worker_details(json)
        Returns a formatted object of all workers pointed to a subaccount hashrate and efficiency details.
        Can be used for 1H and 24H API calls.

    resolve_get_worker_hashrate_history(json)
        Returns a formatted object of a miner hashrate timeseries.

    resolve_get_profile_active_worker_count(json)
        Returns a formatted object of a Profile active workers.
        Workers are classified as active if we recorded a share in the last 15 minutes.

    resolve_get_profile_inactive_worker_count(json)
        Returns a formatted object a Profile inactive workers.
        Workers are classified as inactive if we have not recorded a share in the last 15 minutes.

    resolve_get_transaction_history(json)
        Returns a formatted object of on-chain transactions for a subaccount and currency combo.
    """
    def __init__(self, df: bool = False):
        """
        Parameters
        ----------
        df : boolean
            A boolean flag that determines the output of each method. Default = True.
        """

        self.df = df

    def resolve_get_subaccounts(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        """
        Returns a formatted object of all subaccounts that belong to the Profile owner of the API Key.
        """

        data = [
            list(i['node'].values())[0] for i in json['data']['users']['edges']
        ]

        if self.df:
            return pd.DataFrame(data, columns=['subaccounts'])
        else:
            return data

    def resolve_get_subaccount_hashrate_history(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        """
        Returns a formatted object of a subaccount hashrate timeseries. 
        """

        data = [
            list(i['node'].values())
            for i in json['data']['getHashrateHistory']['edges']
        ]

        if self.df:
            return pd.DataFrame(data, columns=['timestamp', 'hashrate'])
        else:
            return data

    def resolve_get_worker_details(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        """
        Returns a formatted object of all workers pointed to a subaccount hashrate and efficiency details.
        Can be used for 1H and 24H API calls.
        """

        data = [
            list(i['node'].values()) for i in json['data']['miners']['edges']
        ]

        if self.df:
            return pd.concat([
                pd.DataFrame([i[0] for i in data], columns=['workerNames']),
                pd.DataFrame.from_dict([i[1] for i in data])
            ],
                             axis=1)
        else:
            return data

    def resolve_get_worker_hashrate_history(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        """
        Returns a formatted object of a miner hashrate timeseries.
        """

        data = [
            list(i['node'].values())
            for i in json['data']['getWorkerHashrateHistory']['edges']
        ]

        if self.df:
            return pd.DataFrame(data, columns=['timestamp', 'hashrate'])
        else:
            return data

    def resolve_get_profile_active_worker_count(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        """
        Returns a formatted object of a Profile active workers.
        Workers are classified as active if we recorded a share in the last 15 minutes.
        """

        if self.df:
            return pd.DataFrame([json['data']['getProfileActiveWorkers']],
                                columns=['activeWorkers'])
        else:
            return json['data']['getProfileActiveWorkers']

    def resolve_get_profile_inactive_worker_count(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        """
        Returns a formatted object a Profile inactive workers.
        Workers are classified as inactive if we have not recorded a share in the last 15 minutes.
        """

        if self.df:
            return pd.DataFrame([json['data']['getProfileInactiveWorkers']],
                                columns=['inactiveWorkers'])
        else:
            return json['data']['getProfileInactiveWorkers']

    def resolve_get_transaction_history(self, json: Dict[str, Any]) -> Union[list, pd.DataFrame]:
        """
        Returns a formatted object of on-chain transactions for a subaccount and currency combo.
        """

        data = [
            list(i['node'].values())
            for i in json['data']['getTransactionHistory']['edges']
        ]

        if self.df:
            return pd.DataFrame(
                data,
                columns=['createdAt', 'amount', 'status', 'Transaction ID'])
        else:
            return data