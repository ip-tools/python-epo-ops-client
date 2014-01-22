python-epo-ops-client
=====================

python-epo-ops-client is an Apache2 Licensed client library for accessing the
[European Patent Office][EPO]'s ("EPO") [Open Patent Services][OPS] ("OPS")
v.3.1.

```
import epo_ops

anonymous_client = epo_ops.Client()
input_number = epo_ops.Docdb(xx)
anonymous_client.published_data(
  reference_type = 'publication',  # publication, application, priority
  input = epo_ops.Docdb(xx),  # original, docdb, epodoc
  endpoint = 'biblio', # optional, defaults to biblio in case of published_data
  constituents = [] # array of optional constituents
)


client = epo_ops.RegisteredClient(key='abc', secret='xyz')
client.encoded_credentials
client.access_token
```

## Features

[EPO]: http://epo.org
[OPS]: http://www.epo.org/searching/free/ops.html
