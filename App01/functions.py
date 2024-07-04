import pandas as pd
from .models import BusanDistrict

def load_busan_dataset(csv_file):
    try:
        busan_dataset = pd.read_csv(csv_file)
        return busan_dataset
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find the CSV file at {csv_file}")

def analyze_feature(busan_dataset, input_user, feature_name, result_gu):
    min_diff = float('inf')
    closest_gu = None

    for index, value in enumerate(busan_dataset[feature_name]):
        diff = abs(value - input_user)
        if diff < min_diff:
            min_diff = diff
            closest_gu = busan_dataset['gu'][index]

    if closest_gu in result_gu:
        result_gu[closest_gu] += 1
    else:
        print(f"Warning: '{closest_gu}' not found in result_gu keys.")

    return result_gu

def recommend_district(input_user):
    csv_file = r'C:\Users\it\TeamProject\App01\data\busan_dataset.csv'
    busan_dataset = load_busan_dataset(csv_file)

    result_gu = {
        "gangseo": 0, "geumjeong": 0, "gijang": 0, "nam": 0, "dong": 0,
        "dongrae": 0, "busanjin": 0, "buk": 0, "sasang": 0, "saha": 0,
        "suyeong": 0, "yeonje": 0, "yeongdo": 0, "jung": 0, "haeundae": 0
    }

    features = {
        'price': input_user[0],
        'hospital': input_user[1],
        'bus': input_user[2],
        'convenience': input_user[3],
        'subway': input_user[4],
        'department': input_user[5],
        'office': input_user[6],
        'mart': input_user[7],
        'kindergarten': input_user[8],
        'library': input_user[9],
        'park': input_user[10],
        'school': input_user[11],
        'bank': input_user[12],
        'senior': input_user[13]
    }

    for feature_name, user_input in features.items():
        result_gu = analyze_feature(busan_dataset, user_input, feature_name, result_gu)

    gu_korean = {
        "gangseo": "강서구", "geumjeong": "금정구", "gijang": "기장군", "nam": "남구", "dong": "동구",
        "dongrae": "동래구", "busanjin": "부산진구", "buk": "북구", "sasang": "사상구", "saha": "사하구",
        "suyeong": "수영구", "yeonje": "연제구", "yeongdo": "영도구", "jung": "중구", "haeundae": "해운대구"
    }

    recommend_gu = gu_korean.get(max(result_gu, key=result_gu.get), "Unknown")

    # result_gu 사전 초기화
    for key in result_gu:
        result_gu[key] = 0

    return recommend_gu
