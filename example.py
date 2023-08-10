from __future__ import annotations
from typing import Any

from luxor import GraphQlClient, get_subaccount_mining_summary, get_subaccounts
from resolvers import RESOLVERS

client: GraphQlClient = GraphQlClient(
    host="https://api.beta.luxor.tech/graphql",
    method="POST",
    key="lxk.b991087e6f4ea874a9eb32bd5c3bfe65",
)

resolver: RESOLVERS = RESOLVERS(df=True)

# resp: dict[str, Any] = get_subaccount_mining_summary('gp', 'BTC', '_15_MINUTE')
# print(resp)
# resolved = resolver.resolve_get_subaccount_mining_summary(resp)

# print(resolved)

resp: dict[str, Any] = get_subaccounts(10)
print(resp)
resolved = resolver.resolve_get_subaccounts(resp)

print(resolved)