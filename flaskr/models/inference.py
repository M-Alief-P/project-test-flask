import numpy as np
import pandas as pd
import tensorflow as tf

def get_food_recommendations(latitude, longitude, restaurants_data, model_path, k=5):
    """Mengembalikan rekomendasi makanan berdasarkan latitude dan longitude.

    Args:
        latitude (float): Latitude pengguna.
        longitude (float): Longitude pengguna.
        restaurants_data (DataFrame): DataFrame berisi data restoran, termasuk latitude dan longitude.
        model_path (str): Path menuju file TensorFlow Lite model (.tflite).
        k (int, optional): Jumlah tetangga terdekat yang akan dipertimbangkan. Defaultnya adalah 5.

    Returns:
        list: Daftar nama restoran yang direkomendasikan.
    """
    # Load model TensorFlow Lite
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Mengambil kolom latitude dan longitude dari data restoran
    locations = restaurants_data[['latitude', 'longitude']].values
    
    # Mendapatkan koordinat lokasi pengguna
    user_location = np.array([[latitude, longitude]], dtype=np.float32)
    
    # Memasukkan input latitude dan longitude ke dalam model
    interpreter.set_tensor(input_details[0]['index'], user_location)
    interpreter.invoke()
    
    # Mendapatkan output dari model
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Mendapatkan indeks restoran yang direkomendasikan
    recommended_restaurants_indices = np.argsort(output_data[0])[:k]
    
    # Mendapatkan nama restoran berdasarkan indeks yang direkomendasikan
    recommended_restaurants = restaurants_data.iloc[recommended_restaurants_indices]['restaurant_name'].tolist()
    
    return recommended_restaurants

# Contoh penggunaan fungsi untuk inferensi
latitude = -6.143376  # Contoh latitude pengguna
longitude = 106.149564  # Contoh longitude pengguna
restaurants_data = pd.read_csv('data/restaurant.csv')  # Contoh data restoran
model_path = 'models/model.tflite'  # Path menuju file TensorFlow Lite model
recommended_food = get_food_recommendations(latitude, longitude, restaurants_data, model_path)
print("Rekomendasi makanan untuk lokasi pengguna:", recommended_food)
