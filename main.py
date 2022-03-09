from decorator import alert_country
import pandas as pd


@alert_country
def request_country(pais):
    print("Pais no existente en la base de datos")
    return None

def get_info_country(json):
    print(json['name']['common'])

def main():
    stats = request_country('peru')
    get_info_country(stats)
    
    



if __name__ == "__main__":
    main()
