from getcountries import alert_country
import pandas as pd
import hashlib
import timeit
import sqlite3 as sql


@alert_country
def request_country():
    """
        Calls alert_country(decorator) to bring the countries from the web
    """
    return "Error in requesting country..."


def encode_sha1(str):
    """
        Uses the library hashlib to encrypt
    """
    return hashlib.sha1(str.encode()).hexdigest()


def get_info_country(json):
    """
        Gets information from the json obtained from the page
        restcountries.
        It returns the region, the name and the language.
    """
    name = json['name']['common']
    region = json['region']

    if('languages' not in json):
        language = "No language"
        return region, name, language

    languages = json['languages']

    for i in languages:
        language = languages[i]
        break
    return region, name, language


def time_values(df):
    """
        Prints the information of the column Time of
        the DataFrame of pandas.
    """
    total = df['Time(ms)'].sum()
    mean = df['Time(ms)'].mean()
    min = df['Time(ms)'].min()
    max = df['Time(ms)'].max()
    print('Total time: ' + str(total) + ' ms')
    print('Mean time: ' + str(mean) + ' ms')
    print('Min time: ' + str(min) + ' ms')
    print('Max time: ' + str(max) + ' ms')
    return total, mean, min, max


def sql_data_write(df):
    """
        Use only one time, it creates the database in SQLite.
        Use it too when the dataframe is modified.
    """
    conn = sql.connect('countries.db')
    df.to_sql('countries', con=conn)
    conn.close()


def sql_data_read(df):
    """
        Brings information from the database in SQLite
        and prints it in console.
    """
    conn = sql.connect('countries.db')
    countries = pd.read_sql('SELECT * FROM countries', conn)
    print(countries)
    conn.close()


def main():
    time = []
    stats = request_country()
    df = pd.DataFrame(columns=['Region', 'Country', 'Language'])

    for i in stats:
        start = timeit.default_timer()
        info = get_info_country(i)
        df.loc[len(df.index)] = info[0], info[1], encode_sha1(info[2])
        stop = timeit.default_timer()
        time.append(float("{:.2f}".format((stop - start)*1000)))
    df['Time(ms)'] = time  # Adding the column time with its values

    time_values(df)

    df.to_json(r'./data.json')  # Creates the .json in the actual directory

    sql_data_write(df)
    sql_data_read(df)


if __name__ == "__main__":
    main()
