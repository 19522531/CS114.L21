# Import libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
import glob
import time

def get_output_layers(net):                     #Hàm đọc tên các nhãn.
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers
def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h): #Hàm vẽ bounding box lên các ảnh
    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

    cv2.putText(img, label + str(confidence) , (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def drawBox(image, points):                     #Hàm vẽ các bounding box.
    height, width = image.shape[:2]
    for (label, xi,yi, wi, hi) in points:
        center_x = int(xi * width)
        center_y = int(yi * height)
        w = int(wi * width)
        h = int(hi * height)
        # Rectangle coordinates
        x = int(center_x - w / 2)
        y = int(center_y - h / 2)
        cv2.rectangle(image, (x, y), (x + w, y + h), black, 1)
    return
def savePredict(pathSave, name, text):          #Hàm lưu các file txt có format: label 0.xxxx 0.yyyy 0.wwww 0.hhhhh
    textName = pathSave + '/' + name + '.txt'
    with open(textName, 'w+') as groundTruth:
        groundTruth.write(text)
        groundTruth.close()

pathImg= r"images-optional"
#Đia chỉ để các file ảnh để model dự đoán đối tượng
pathDirection = r"detection-results"
#Địa chỉ để xuất output dự đoán của model
print("start")
for img in glob.glob(pathImg + '/*.jpg'): # load lần lượt các ảnh trong folder để detect
    name = img.split('images-optional')[-1].split('.')[0]
    image = cv2.imread(img)
    #Đọc ảnh
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392
    #Đoc chiều dài và rộng của ảnh

    classes = None
    with open("/dia_chi_file/yolo.names", 'r') as f: # Thay đổi địa chỉ của fiell yolo.names tại đây
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    #Random màu để vẽ bounding box
    net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg") #Thay đổi tên và địa chỉ file weight và file cfg tại đây
    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
    #cvt ảnh sang dạng blob
    net.setInput(blob)

    outs = net.forward(get_output_layers(net))
    #print(outs)
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5 # Ngưỡng detect. Nếu xác suất đối tượng >0.5 thì nó mới được xem là một đối tượng đúng
    # Giảm nếu model không cần độ chính xác cao, tăng nếu model cần độ chính xác cao
    nms_threshold = 0.4
    
    #start = time.time()
    for out in outs: #Xuất các đối tượng được predict
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                #print(confidence)
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                #print(w,h,x,y)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    #lưu file txt
    Result = ""
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        textpredict = "{} {} {} {} {} {}\n".format(str(class_ids[i]), confidences[i], x, y, x+w, y+h)
        Result += textpredict
    savePredict(pathDirection, name, Result)
    
