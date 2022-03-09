from getcountries import alert_country
import pandas as pd
import hashlib
import timeit
import sqlite3 as sql


@alert_country
def request_country():
    print("Ocurrio un error")
    return None


def encode_sha1(str):
    return hashlib.sha1(str.encode()).hexdigest()


def get_info_country(json):
    name = json['name']['common']
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
    print('Total time: ' + str(df['Time(ms)'].sum()) + ' ms')
    print('Mean time: ' + str(df['Time(ms)'].mean()) + ' ms')
    print('Min time: ' + str(df['Time(ms)'].min()) + ' ms')
    print('Max time: ' + str(df['Time(ms)'].max()) + ' ms')


def sql_data_movement(df):
    conn = sql.connect('countries.db')
    df.to_sql('countries', con=conn)


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
    df['Time(ms)'] = time  # Adding the column time with its values

    print(df.head())

    time_values(df)

    df.to_json(r'./data.json')


if __name__ == "__main__":
    main()
