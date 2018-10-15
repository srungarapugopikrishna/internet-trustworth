
from fakelinkshub.dumps.opensources_dump import opensources_dump_data as data
import itertools
import pprint

pp = pprint.PrettyPrinter(indent=4)

types = []
for i in data:
    if data[i]['type'] and data[i]['type'].strip().lower() not in types:
        types.append(data[i]['type'].strip().lower())
    if data[i]['2nd type'] and data[i]['2nd type'].strip().lower() not in types:
        types.append(data[i]['2nd type'].strip().lower())
    if data[i]['3rd type'] and data[i]['3rd type'].strip().lower() not in types:
        types.append(data[i]['3rd type'].strip().lower())

result = dict((type, []) for type in types)

for i in data:
    if data[i]['type']:
        result[data[i]['type'].strip().lower()].append(i)
    if data[i]['2nd type']:
        result[data[i]['2nd type'].strip().lower()].append(i)
    if data[i]['3rd type']:
        result[data[i]['3rd type'].strip().lower()].append(i)

urls = []
for i in result.keys():
    urls.append(result[i])

urls = list(itertools.chain.from_iterable(urls))

print(set(urls))
