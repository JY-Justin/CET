import cv2
import numpy as np
from TCPServer import *

# 识别出人脸后要画的边框的颜色，RGB格式
color = [[0, 0, 255], [0, 255, 0], [255, 0, 0],
         [255, 255, 0], [255, 0, 255], [0, 255, 25],
         [255, 128, 0], [0, 128, 255], [128, 255, 0]]

classfier = cv2.CascadeClassifier(
    "./haarcascade_frontalface_alt2.xml")

known_face_encodings, known_face_IDs,known_face_name = [], [],[]
libpath = "../facialData\\"

def load_faceEncode():
    cursor = mydb.cursor()
    cursor.execute('select * from facecode')
    s = cursor.fetchall()
    for encode in s:
        str_id = encode[0]
        encode_str = encode[1]
        face_encoding = []
        encode_info = encode_str.split(' ')
        length = len(encode_info)
        if length != 129:
            print("encode <128L: {}".format(str_id))
            continue
        for info_idx in range(len(encode_info) - 1):
            face_encoding.append(float(encode_info[info_idx]))
        face_encoding = np.array(face_encoding)
        known_face_encodings.append(face_encoding)
        known_face_IDs.append(str(str_id))  # 以图片的名称来作为图片的标识
    cursor.close()
    # mydb.close()

def load_Face(id):
    file_name = '"{}"'.format(id)
    cursor = mydb.cursor()
    sql_str = "select * from images where names = {}".format(file_name)
    cursor.execute(sql_str)
    s = cursor.fetchall()
    fp = open('buffImage.jpg', 'wb')
    fp.write(s[0][1])
    fp.close()
    cursor.close()

def update_faceEncode():
    cursor = mydb.cursor()
    cursor.execute("select * from facecode where flag = 1")
    s = cursor.fetchall()
    if len(s) == 0:
        return
    for update_info in s:
        known_face_ID = np.array(known_face_IDs)
        str_id = str(update_info[0])
        encode_str = update_info[1]
        face_encoding = []
        encode_info = encode_str.split(' ')
        length = len(encode_info)
        if length != 129:
            print("encode <128L: {}".format(str_id))
            continue
        for info_idx in range(len(encode_info) - 1):
            face_encoding.append(float(encode_info[info_idx]))
        face_encoding = np.array(face_encoding)

        idx = np.where(known_face_ID[:] == str_id)[0]

        if len(idx) == 0:
            known_face_encodings.append(face_encoding)
            known_face_IDs.append(str(str_id))  # 以图片的名称来作为图片的标识
        else:
            known_face_encodings[idx[0]] = face_encoding
        try:
            cursor.execute("UPDATE facecode SET flag = %s WHERE id=%s", (0, str(str_id)))
            mydb.commit()
        except Exception as e:
            print("Excrption:{}".format(e))
            continue
    cursor.close()