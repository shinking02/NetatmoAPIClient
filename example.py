from netatmo_api_client import NetatmoAPIClient
from datetime import datetime

# NetatmoClientクラスのインスタンス化
client = NetatmoAPIClient()

# ステーションデータを取得
stations_data = client.get_stations_data()
print("Stations Data:", stations_data)

# 気温、湿度、CO2、いつのデータかを表示
for device in stations_data['body']['devices']:
    module_name = device['module_name']
    dashboard_data = device['dashboard_data']
    temperature = dashboard_data.get('Temperature')
    humidity = dashboard_data.get('Humidity')
    co2 = dashboard_data.get('CO2')
    timestamp = dashboard_data.get('time_utc')

    # タイムスタンプを整形
    dt = datetime.fromtimestamp(timestamp)

    print(f"Module: {module_name}")
    print(f"Temperature: {temperature} °C")
    print(f"Humidity: {humidity} %")
    print(f"CO2: {co2} ppm")
    print(f"Time: {dt}")