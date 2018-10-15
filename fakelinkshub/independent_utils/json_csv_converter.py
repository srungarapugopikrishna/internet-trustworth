import csv
import json
import sys
import pprint

def _data_driver(data, key_prefix=None, columns=[], values=[]):
    for key in sorted(data.keys()):
        if type(data[key]) is dict:
            if key_prefix is None:
                _data_driver(data[key], key, columns, values)
            else:
                _data_driver(data[key], key_prefix+'_'+key, columns, values)
        else:
            if key_prefix is None:
                columns.append(key)
                values.append(data[key])
            else:
                columns.append(key_prefix+'_'+key)
                values.append(data[key])
    return columns, values


def json_to_csv(json_data, file_name):
    """
    converts json data to csv file
    :param json_data: data in json format
    :param file_name: path and name of the file
    :return: True, file_name
    """
    try:
        data = json.loads(json_data)
        with open(file_name, 'wb') as csvfile:
            csv_writer_object = csv.writer(csvfile, delimiter=',')
            for idx, rec in enumerate(data):
                cols, vals = _data_driver(rec, None, [], [])
                if idx == 0:
                    csv_writer_object.writerow(cols)
                csv_writer_object.writerow(vals)
        return True, file_name
    except Exception as e:
        return False, e


def csv_to_json(file_path, delimiter='_'):
    """
    converts csv file to json data
    :param file_path: path of the file
    :param delimiter: delimiter to divide column names
    :return: json data
    """
    with open(file_path, encoding="utf8") as csvinput:
        output = []
        maxInt = sys.maxsize
        decrement = True
        while decrement:
            # decrease the maxInt value by factor 10
            # as long as the OverflowError occurs.

            decrement = False
            try:
                csv.field_size_limit(maxInt)
            except OverflowError:
                maxInt = int(maxInt / 10)
                decrement = True
        reader = csv.reader(csvinput)
        header = next(reader)
        for row in reader:
            result = {}
            for rec in header:
                if delimiter in rec:
                    t_dict = result
                    temp = rec.split(delimiter)
                    for idx, val in enumerate(temp):
                        if idx == len(temp) - 1:
                            t_dict[val] = row.pop(0)
                        else:
                            try:
                                if t_dict[val]:
                                    t_dict = t_dict[val]
                            except KeyError:
                                t_dict[val] = {}
                                t_dict = t_dict[val]
                else:
                    result[rec] = row.pop(0)
            output.append(result)
    return output


kaggle_dumps = csv_to_json('C:\\Users\\gsrungarapu\\Desktop\\internet-trustworth-master\\fakelinkshub\\resources\\kaggle_dataset.csv')

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(kaggle_dumps)
urls = []
for i in kaggle_dumps:
    urls.append(i['site']['url'])

urls = list(set(urls))
print(len(urls))


# json = json.dumps(kaggle_dumps)
# f = open("C:\\Users\\gsrungarapu\\Desktop\\internet-trustworth-master\\fakelinkshub\\resources\\kaggle_dataset.json", "w")
# f.write(json)
# f.close()
