# KUKULINER - CC

## How to Run Manually (this demo for Linux Ubuntu)

- Make sure you have installed Python (this project uses Python version 3.9).
- Make sure you have already installed venv.
- Create a venv in the root folder

```sh
python3 -m venv venv
```

- Activate the venv

```sh
source venv/bin/activate
```

- Install requirement.txt

```sh
pip install -r requirements. txt
```

- Run the project

```sh
flask --app flaskr run --debug
```

## Endpoint API

**Path :**

> /recommend_food

**Method :**

> `POST`

```json
[
  {
    "id_restaurant": 1,
    "id_reting": 1,
    "id_makanan": 1,
    "id_provinsi": 36,
    "id_kabupaten": 3673,
    "nama": "Sate Bandeng Ibu Amenah Serang",
    "alamat": "Jl. Sayabulu km 1, Lingk No.11, RT.2/RW.1, Dalung, Kec. Cipocok Jaya, Kota Serang, Banten 42127, Indonesia",
    "longitude": 106.149564,
    "latitude": -6.143376
  }
]
```

## Test in Postman

- Enter the following URL using the POST method: <http://localhost:5000/recommend_food>
- Press the 'Body' section and choose 'RAW', then select JSON as the format.
- For testing, enter the following data:

```sh
{
    "latitude": -6.143376,
    "longitude": 106.149564
}
```

- If success (status 200), you will receive something like this as a response:

```sh
{
    "kukuliner": [
        [
            "Sate Bandeng Ibu Amenah Serang",
            0.0
        ],
        [
            "Sate Bandeng - Bekakak Ayam Hj. Mariyam",
            3.294
        ],
        [
            "Rabeg Khas Serang H. Naswi (Magersari)",
            4.589
        ],
        [
            "Sate Bandeng Ibu Aliyah",
            5.778
        ],
        [
            "Warung Dahar Rabeg Khas Wong Banten",
            6.085
        ]
    ]
}
```
