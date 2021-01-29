import csv
import country


def read_stats(main=False):
    with open("World_priv.csv") as file:
        values = []
        reader = csv.reader(file)
        for line in reader:
            values.append(line)
    heads = values[0]
    heads = list(map(str.lower, heads))
    values.pop(0)
    prop_values = {}
    for value in values:
        value = list(map(str.lower, value))
        prop_value = dict(zip(heads[1:], value[1:]))
        prop_values[value[0].lower()] = prop_value
    #print(prop_values["altafia"])
    return init_countries(prop_values, main)


def init_countries(all, main):
    countries = {}
    for name in all:
        if main == True:
            countries[name.lower()] = country.country_init(name, all[name], test=True)
            return None
        countries[name.lower()] = country.country_init(name, all[name])
    return countries


if __name__ == "__main__":
    print(read_stats(main=True))
