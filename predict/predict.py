import numpy as np
from keras.utils import load_img, img_to_array
from keras.applications.efficientnet_v2 import EfficientNetV2B0, preprocess_input
from ultralytics import YOLO
from collections import Counter
from utils import format, get_by_name
from pyodbc import Cursor


def YoloPredict(file, sql: Cursor) -> list:
    try:
        model = YOLO("../models/best.pt")
        results = model.predict(source=file, conf=0.5)

        class_result = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.data[0][-1])
                class_result.append(model.names[class_id])

        counter = Counter(class_result)
        most_common = counter.most_common(1)
        name = most_common[0][0]

        plant = get_by_name(name, sql)
        acc_result = f"{format(class_result)}%"

        return {"accuracy": acc_result, "plant": plant}
    except Exception as e:
        print("An error occurred in YoloPredict:", str(e))
        return None


def EfficientNetV2Predict(file):
    model = EfficientNetV2B0(weights="imagenet", include_top=False)
    try:
        pic_size = 244
        image = load_img(file, target_size=(pic_size, pic_size))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(file)

        features = model.predict(image)
        return features
    except Exception as e:
        print("An error occurred in EfficientNetV2Predict:", str(e))
        return None
