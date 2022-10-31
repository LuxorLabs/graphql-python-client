from __future__ import annotations

import json
import logging
from typing import Any

import requests
from rich import print
from rich import print_json
from rich.console import Console
from rich.table import Table


class GraphQlClient:
    def __init__(
        self,
        host: str,
        key: str,
        method: str,
        verbose: bool = False,
    ):
        """
        Parameters
        ----------

        host : str
            Base endpoint for all API requests. Default is: https://api.cairo.luxorlabs.dev/graphql

        key : str
            Random generated API Key. Default is an empty string.

        method : str
            API request METHOD. Default is `POST`.

        verbose : boolean
            Boolean flag that controls if API querys are logged.
        """

        self.host = host
        self.key = key
        self.method = method
        self.verbose = verbose

    def print_graphql_result(self, json_result: dict[str, Any]) -> None:
        try:
            data: dict[str, Any] = json_result["data"]
            # Obtain the first key, usually the graphql operation
            graphql_operation: str = list(data.keys())[0]
            result: dict[str, Any] = data[graphql_operation]
            edges: list[dict[str, Any]] | None = result.get("edges")

            if edges is None or len(edges) == 0:
                print_json(data=result)
                return

            table = Table(
                show_header=True,
                header_style="yellow",
                show_lines=True,
                title=f"Result: {graphql_operation}",
                title_style="bold yellow",
            )

            # Get the columns for the result based on a sample of the result
            sample = edges[0]["node"]
            columns = list(sample.keys())

            for column_name in columns:
                table.add_column(column_name)

            for row in edges:
                values = [row["node"][column] for column in columns]
                table.add_row(*values)

            console = Console()
            console.print(table)

        except Exception:
            print(json_result)

    def request(
        self,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Base function to execute operations against Luxor's GraphQL API

        query (str): GraphQL compliant query string.
        params (dictionary): dictionary containing the query parameters, values depend on query.
        """

        headers = {
            "Content-Type": "application/json",
            "x-lux-api-key": f"{self.key}",
        }

        s = requests.Session()
        s.headers = headers  # type: ignore

        if self.verbose:
            logging.info(query)

        response = s.request(
            self.method,
            self.host,
            data=json.dumps({"query": query, "variables": params}).encode("utf-8"),
        )

        if response.status_code == 200:
            json_response = response.json()
            self.print_graphql_result(json_response)
            return json_response
        elif response.content:
            raise Exception(
                str(response.status_code)
                + ": "
                + str(response.reason)
                + ": "
                + str(response.content.decode()),
            )
        else:
            raise Exception(str(response.status_code) + ": " + str(response.reason))
