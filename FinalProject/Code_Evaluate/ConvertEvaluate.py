import cv2 
import os 
import glob
import numpy as np

path_input = "C:/Users/Admin/Desktop/mAP/data_convert"
# Địa chỉ chứa cả file ảnh và file .txt gán nhãn.( nhớ là file ảnh và txt phải trùng nhau)
path_output = "C:/Users/Admin/Desktop/mAP/input/ground-truth"
# Địa chỉ xuất file txt chứa các giá trị pixel để tính mAP

def check(path_txt):                                                    #Kiểm tra xem file txt và file ảnh có trùng nhau không
        name = path_txt.split(".")[0]                                   #Nếu trùng thì mới xử lý tiếp
        if os.path.isfile(name + '.png'):
                return True
        return False
for path_txt in glob.glob(path_input + "/*.txt"):
        no=[0,0,0,0,0]
        #print(path_txt)
        if check(path_txt):
                image = cv2.imread(path_txt.split(".")[0] + ".png")     #Các bạn đổi đuôi định dạng ảnh ở đây
                h,w = image.shape[:2]                                   #Đọc giá trị chiều rộng và dài của ảnh
                output=""
                with open(path_txt, "r") as stream:                     #Mở lần lượt các file txt
                        for line in stream.readlines():                 #Đọc từng dòng trong mỗi file txt
                                line = line.strip()
                                coord = line.split(" ")
                                a = coord[0]                            #gán a bằng giá trị của nhãn
                                num = int(line.split(' ',1)[0])
                                no[num]+=1
                                coord = [float(i) for i in coord[1:]]   #Đọc các giá trị tọa độ dạng 0.xxxx
                                box = np.array(coord) * np.array([w,h,w,h]) # Chuyển các array thành định dạng box
                                (centerX, centerY, width, height) = box.astype('int') #Convert tọa độ
                                left = centerX - int(width/2)
                                top = centerY - int(height/2)
                                right = centerX + int(width/2)
                                bottom = centerY + int(height/2)
                                #out2 = "{} {} {} {} {} difficult\n".format(a, left, top, right, bottom)
                                out1 = "{} {} {} {} {}\n".format(a, left, top, right, bottom) #Ghi lại theo định dạng pixel theo từng dòng
                                #if (no[num] ==1):
                                #         output +=out1
                                #elif (no[num] != 1):
                                output +=out1 #ghi lại theo từng file
                name_output = path_txt.split('/')[-1] # cắt tên của file txt dạng 0.xxx để đặt tên cho file txt dạng pixel
                print(name_output[13:])
                with open(path_output + "/" + name_output[13:], 'w') as stream_out:
                        stream_out.write(output)                        #Lưu file vào thư mục path_output
                stream.close()
                stream_out.close()
                
              


print("done")     
