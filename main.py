from getcountries import alert_country
import pandas as pd
import hashlib
import timeit
import sqlite3 as sql


@alert_country
def request_country():
    """
        Calls alert_country to bring the countries from the web
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
        restcountries and aditional encrypts the language.
        It returns the region, the name and the encrypted language.
        Encrypts using encode_sha1(str)
    """
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
    """
        Prints the information of the column Time of
        the DataFrame of pandas.
    """
    print('Total time: ' + str(df['Time(ms)'].sum()) + ' ms')
    print('Mean time: ' + str(df['Time(ms)'].mean()) + ' ms')
    print('Min time: ' + str(df['Time(ms)'].min()) + ' ms')
    print('Max time: ' + str(df['Time(ms)'].max()) + ' ms')


def sql_data_write(df):
    """
        Use only one time, it creates the database in SQLite.
        Use it too when the dataframe is modified.
    """
    conn = sql.connect('countries.db')
    df.to_sql('countries', con=conn)


def sql_data_read(df):
    """
        Brings information from the database in SQLite
        and prints it in console.
    """
    conn = sql.connect('countries.db')
    countries = pd.read_sql('SELECT * FROM countries', conn)
    print(countries)


def main():
    time = []
    stats = request_country()
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

    df.to_json(r'./data.json')  # Creates the .json in the actual directory

    sql_data_write(df)
    sql_data_read(df)


if __name__ == "__main__":
    main()
