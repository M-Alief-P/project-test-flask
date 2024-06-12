from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import tensorflow as tf
import googlemaps

app = Flask(__name__)

def get_distance_with_google_maps(latitude1, longitude1, latitude2, longitude2):
    """Menggunakan Google Maps Distance Matrix API untuk menghitung jarak antara dua titik.

    Args:
        latitude1 (float): Latitude titik awal.
        longitude1 (float): Longitude titik awal.
        latitude2 (float): Latitude titik tujuan.
        longitude2 (float): Longitude titik tujuan.

    Returns:
        float: Jarak antara dua titik dalam kilometer.
    """
    gmaps = googlemaps.Client(key='AIzaSyBGneXInfhvRvjz-s0sCQYNTODmEPo0dIY')

    # Menentukan lokasi awal dan tujuan
    origin = f"{latitude1},{longitude1}"
    destination = f"{latitude2},{longitude2}"

    # Meminta informasi jarak melalui Google Maps Distance Matrix API
    distance_matrix = gmaps.distance_matrix(origin, destination)

    # Mengambil jarak dalam kilometer
    distance = distance_matrix['rows'][0]['elements'][0]['distance']['value'] / 1000

    return distance

def get_food_recommendations(latitude, longitude, restaurants_data, model_path, k=10, max_distance=20):
    """Mengembalikan rekomendasi makanan beserta jaraknya dari latitude dan longitude.

    Args:
        latitude (float): Latitude pengguna.
        longitude (float): Longitude pengguna.
        restaurants_data (DataFrame): DataFrame berisi data restoran, termasuk latitude dan longitude.
        model_path (str): Path menuju file TensorFlow Lite model (.tflite).
        k (int, optional): Jumlah rekomendasi terdekat yang akan dipertimbangkan. Defaultnya adalah 10.
        max_distance (float, optional): Jarak maksimum (dalam kilometer) dari lokasi pengguna ke restoran yang akan direkomendasikan. Defaultnya adalah 20.

    Returns:
        list: Daftar tuple berisi nama restoran dan jaraknya dari lokasi pengguna.
    """
    # Load model TensorFlow Lite
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Mendapatkan koordinat lokasi pengguna
    user_location = np.array([[latitude, longitude]], dtype=np.float32)
    
    # Memasukkan input latitude dan longitude ke dalam model
    interpreter.set_tensor(input_details[0]['index'], user_location)
    interpreter.invoke()
    
    # Mendapatkan output dari model
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Mendapatkan indeks restoran yang direkomendasikan
    recommended_restaurants_indices = np.argsort(output_data[0])[:k]
    
    # Membuat DataFrame sementara untuk menyimpan hasil rekomendasi restoran
    recommended_restaurants_df = pd.DataFrame(columns=['nama', 'latitude', 'longitude', 'distance'])
    
    # Mendapatkan nama restoran berdasarkan indeks yang direkomendasikan beserta jaraknya
    recommended_restaurants = []
    for idx in recommended_restaurants_indices:
        restaurant_name = restaurants_data.iloc[idx]['nama']
        restaurant_lat = restaurants_data.iloc[idx]['latitude']
        restaurant_lon = restaurants_data.iloc[idx]['longitude']
        distance = get_distance_with_google_maps(latitude, longitude, restaurant_lat, restaurant_lon)
        
        # Filter restoran berdasarkan jarak maksimum
        if distance <= max_distance:
            recommended_restaurants_df.loc[len(recommended_restaurants_df)] = {'nama': restaurant_name, 
                                                                               'latitude': restaurant_lat,
                                                                               'longitude': restaurant_lon,
                                                                               'distance': distance}
    
    # Mengurutkan restoran berdasarkan jarak
    recommended_restaurants_df = recommended_restaurants_df.sort_values(by='distance')

    # Mengambil 10 restoran terdekat
    recommended_restaurants = recommended_restaurants_df.head(10)[['nama', 'distance']].values.tolist()
    
    return recommended_restaurants


@app.route('/recommend_food', methods=['POST'])
def recommend_food():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    
    # Data restoran dari file JSON
    restaurants_data = pd.read_json('YOUR JSON PATH')
    
    # Path menuju file TensorFlow Lite model
    model_path = 'YOUR TENSORFLOW LITE PATH'
    
    recommended_food = get_food_recommendations(latitude, longitude, restaurants_data, model_path)
    
    return jsonify({'kukuliner': recommended_food})

if __name__ == '__main__':
    app.run(debug=True)
