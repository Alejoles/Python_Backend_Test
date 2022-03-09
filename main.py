from tracemalloc import start
from decorator import alert_country
import pandas as pd
import hashlib
import timeit


@alert_country
def request_country():
    print("Ocurrio un error")
    return None

def get_info_country(json):
    sha1 = hashlib.sha1()
    name = json['translations']['spa']['common']
    region = json['region']
    if(name == 'Antártida'):
        language = "No language"
        sha1.update(language.encode())
        return region, name, sha1.hexdigest()
    languages = json['languages']
    for i in languages:
        language = languages[i]
        sha1.update(language.encode())
        break
    return region, name, sha1.hexdigest()
    

def main():
    stats = request_country()
    time = []
    df = pd.DataFrame(columns=['Region', 'Country', 'Language'])
    for i in stats:
        info = get_info_country(i)
        start = timeit.default_timer()
        df.loc[len(df.index)] = info
        stop = timeit.default_timer()
        time.append("{:.2f}".format((stop - start)*1000) + ' ms')
    df['Time'] = time
    print(df.head)
    



if __name__ == "__main__":
    main()
