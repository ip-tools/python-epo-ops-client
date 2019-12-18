import epo_ops
import epo_ops.models as model

client = epo_ops.Client(key='Ae4QJTuGuSW9BrbSZorvySGYBM5UwBjS',
                        secret='GqucKWA0jLV0xOGm')
research = client.classification_cpc_search('zerodur')
print(research.text)
# response = client.published_data(reference_type=client.publication,
#                                  input=model.Docdb('1000000', 'EP', 'A1'),
#                                  endpoint='biblio',
#                                  constituents=[])
# print(response.text)
