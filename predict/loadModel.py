import joblib
import os


def LoadModel(input):
    path = os.path.join(os.getcwd(), "../models/EfficientNet.keras")
    loaded_model = joblib.load(path)
    prediction = loaded_model.predict(input)

    return Result(prediction[0])

def Result(prediction):
    arr = ["bạc hà", "bách bộ", "bạch đồng nữ", "bạch hoa xà thiệt thảo", "bán hạ nam", "bố chính sâm", "bồ công anh", "cà gai leo", "cam thảo đất", "cỏ mần trầu", "cỏ nhọ nồi", "cỏ sữa lá nhỏ", "cỏ tranh", "cỏ xước", "cối xay", "cốt khí", "cúc hoa", "cúc tần", "dành dành", "dâu", "địa hoàng", "địa liền", "diệp hạ châu", "đinh lăng", "đơn lá đỏ", "dừa cạn", "gai", "gừng", "hạ khô thảo nam", "hoắc hương", "húng chanh", "hương nhu", "huyết dụ", "hy thiêm", "ích mẫu", "ké đầu ngựa", "khổ sâm cho lá", "kim ngân", "kim tiền thảo", "kinh giới", "lá lốt", "mã đề", "mạch môn", "mần tưới", "mỏ quạ", "mơ tam thể", "náng", "ngải cứu", "nghệ", "ngủ gia bì chân kim", "nhân trần", "nhót", "ổi", "phèn đen", "quýt", "rau má", "rầu mèo", "rau sam", "sả", "sài đất", "sắn dây", "sim", "thiên môn", "tía tô", "trắc bá diệp", "trinh nữ hoàng cung", "xạ can", "xích đồng nam", "xuyên tâm liên", "ý dĩ"]
    
    return arr[prediction]