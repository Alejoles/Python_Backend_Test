from re import T
from tracemalloc import start
from getcountries import alert_country
import pandas as pd
import hashlib
import timeit


@alert_country
def request_country():
    print("Ocurrio un error")
    return None


def encode_sha1(str):
    return hashlib.sha1(str.encode()).hexdigest()


def get_info_country(json):
    name = json['translations']['spa']['common']
    region = json['region']

    if('languages' not in json):
        language = "No language"
        return region, name, encode_sha1(language)

    languages = json['languages']

    for i in languages:
        language = languages[i]
        break
    return region, name, encode_sha1(language)


def time_values(df):
    print(df['Time'].sum())
    print(df['Time'].mean())
    print(df['Time'].min())
    print(df['Time'].max())


def main():
    stats = request_country()
    time = []
    df = pd.DataFrame(columns=['Region', 'Country', 'Language'])
    for i in stats:
        start = timeit.default_timer()
        info = get_info_country(i)
        df.loc[len(df.index)] = info
        stop = timeit.default_timer()
        time.append(float("{:.2f}".format((stop - start)*1000)))
    df['Time'] = time
    print(df.head())


if __name__ == "__main__":
    main()
