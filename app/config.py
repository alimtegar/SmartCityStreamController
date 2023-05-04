VEHICLE_DETECTION_MODEL_PATH = 'yolov8n.pt'
PLATE_DETECTION_MODEL_PATH = './model_weights/plate_detection_model_nano.pt'
TEXT_RECOGNITION_MODEL_PATH = './model_weights/text_recognition_model.pt'
# VIDEO_PATH = 'vehicle-traffic-2.webm'

# Class IDs of Interest
WANTED_CLASS_ID_LIST = [
    1, # bicycle
    2, # car
    3, # motorcycle
    5, # bus
    7, # truck
]

CLASS_NAME_MAP = {
    1: 'bicycle',
    2: 'car',
    3: 'motorcycle',
    5: 'bus',
    7: 'truck',
}

CLASS_NAMES = list(CLASS_NAME_MAP.values())

PLATE_CITY_MAP = {
    'AA': 'Purworejo, Temanggung, Magelang, Wonosobo, kebumen, Kedu',
    'AD': 'Surakarta, Boyolali, Wonogiri, Sukoharjo, Karanganyar, Sragen, Klaten',
    'K': 'Pati, Kudus, Cepu, Jepara, Grobogan, Rembang, Blora',
    'AA': 'Purworejo, Temanggung, Magelang, Wonosobo, kebumen, Kedu',
    'AD': 'Surakarta, Boyolali, Wonogiri, Sukoharjo, Karanganyar, Sragen, Klaten',
    'K': 'Pati, Kudus, Cepu, Jepara, Grobogan, Rembang, Blora',
    'R': 'Banjarnegara, Banyumas, Cilacap, Purbalingga',
    'G': 'Brebes, Pemalang, Batang, Tegal, Pekalongan',
    'H': 'Semarang, Salatiga, Kendal, Demak','AB': 'Yogyakarta',
    'D': 'Bandung, Cimahi',
    'F': 'Bogor, Sukabumi, Cianjur',
    'E': 'Kuningan, Cirebon, Majalengka, Indramayu',
    'Z': 'Banjar, Garut, Ciamis, Tasikmalaya, Sumedang',
    'T': 'Subang, Purwakarta, Karawang',
    'A': 'Banten, Tangerang, Cilegon, Lebak, Serang, Pandeglang',
    'B': 'DKI Jakarta, Bekasi, Depok',
    'AG': 'Tulungagung, Kediri, Blitar, Trenggalek, Nganjuk',
    'AE': 'Ngawi, Madiun, Pacitan, Ponorogo, Magetan',
    'L': 'Jawa timur, Surabaya',
    'M': 'Madura, Bangkalan, Sampang, Sumenep, Pamekasan',
    'N': 'Malang, Pasuruan, Probolinggo, Batu, Lumajang',
    'S': 'Jombang, Bojonegoro, Lamongan, Mojokerto',
    'W': 'Gresik, Sidoarjo',
    'P': 'Banyuwangi, Besuki, Bondowoso, Jember, situbondo',
    'DK': 'Bali',
    'ED': 'Sumba Timur',
    'EA': 'Sumbawa, Bima, Dompu',
    'EB': 'Nusa Tenggara, Flores',
    'DH': 'Kupang, Rote Ndao, Timor',
    'DR': 'Lombok, Mataram',
    'KU': 'Kalimantan Utara',
    'KT': 'Kalimantan Timur',
    'DA': 'Kalimantan Selatan',
    'KB': 'Kalimantan Barat',
    'KH': 'Kalimantan Tengah',
    'DC': 'Sulawesi Barat',
    'DD': 'Sulawesi selatan',
    'DN': 'Sulawesi Tengah',
    'DT': 'Sulawesi Tenggara',
    'DL': 'Sitaro, Talaud, Sangihe',
    'DM': 'Gorontalo',
    'DB': 'Manado, Minahasa, Tomohon, Bolaang Mongondow',
    'BA': 'Sumatera Barat',
    'BB': 'Sumatera Utara bagian barat',
    'BD': 'Bengkulu',
    'BE': 'Lampung',
    'BG': 'Sumatera Selatan bagian timur',
    'BH': 'Jambi',
    'BK': 'Sumatera Utara',
    'BL': 'Aceh',
    'BM': 'Riau',
    'BN': 'Bangka Belitung',
    'BP': 'Kepulauan Riau',
    'DE': 'Maluku',
    'DG': 'Mauku Utara',
    'PA': 'Papua',
    'PB': 'Papua Barat',
}

# LINE_START = (540, 2110)
# LINE_END = (3834, 1370)
COUNTER_AREA_H = 20

# Text Recognition Config
VOCABULARY = [
    '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z'
]
IDX2CHAR = {k: v for k, v in enumerate(VOCABULARY, start=0)}
CHAR2IDX = {v: k for k, v in IDX2CHAR.items()}

# Database Config
DB_DIALECT = 'mysql'
DB_DRIVER = 'mysqlconnector'
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'smart_city'
DB_SOCKET='/Applications/MAMP/tmp/mysql/mysql.sock'