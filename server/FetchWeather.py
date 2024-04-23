import requests

def fetch_weather_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return filter_data(data)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def filter_data(weatherRawData):
    result = ""
    if weatherRawData:
        records = weatherRawData['records']
        for record in records['location']:
            result += f"Location: {record['locationName']}\n"
            for weather_element in record['weatherElement']:
                for time in weather_element['time']:  # Iterate through each time slot
                    start_time = time['startTime'][:13]+"點"
                    end_time = time['endTime'][:13]+"點"
                    element_value = time['parameter']['parameterName']
                    result += f"{start_time} 到 {end_time} - {weather_element['elementName']}: {element_value}\n"
            result += "---\n"
    return result

def main():
    token = "CWA-547A664B-85B9-4716-9B09-2C2BD7297F8E"
    # 36-hour forecast URL
    short_term_url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={token}"

    print("Fetching 36-hour forecast:")
    short_term_data = fetch_weather_data(short_term_url)
    print(short_term_data)



if __name__ == "__main__":
    main()
