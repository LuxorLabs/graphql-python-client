# Luxor Python Library and Command Line GraphQL API Client

## API Documentation
This Library / Client implements a subset of available endpoints. API Docs can be found here: https://docs.luxor.tech/.

## Get Started

To get started, you will need the following basic information:
- Endpoint: `https://api.beta.luxor.tech/graphql`
- Organization Slug: `luxor`
- API Key: Generated through Luxor UI

## Library Usage
Luxor is divided in two parts, the first one containing the GraphQL API requests and the second adds resolvers for the API output.

**Code Snippet**
```
from luxor import API
from resolvers import RESOLVERS

API = API(host = 'https://api.beta.luxor.tech/graphql', method = 'POST', org = 'luxor', key = 'lxk514e9be027b9a132b1aa39bab818a12e')
RESOLVERS = RESOLVERS(df = False)

resp = API.method(parameters)
resolved = RESOLVERS.method(resp)
```

## Command Line Usage
To get started and get params help run: 
```
python luxor.py -h
```

Result:
```
Options:
  -h, --help            
                        show this help message and exit
  -e HOST, --endpoint=HOST
                        API ENDPOINT
  -o ORG, --organization=ORG 
                        Organization Slug
  -k KEY, --key=KEY     
                        Profile API Key
  -m METHOD, --method=METHOD
                        API Request method
  -f FUNCTION, --function=FUNCTION
                        API Class method
  -q QUERY, --method=QUERY
                        API Request query
  -p PARAMS, --params=PARAMS
                        API Request params
  -d DF, --df=DF        
                        Pandas DataFrame
```

Example usage:
```
python3 luxor.py -k KEY -f get_transaction_history -p username,BTC,10
```

Happy Hashing!