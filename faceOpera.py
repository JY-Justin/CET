from face_recognition import api as face_recognition
import numpy as np

def simcos(A, B):
    A = np.array(A)
    B = np.array(B)
    dist = np.linalg.norm(A - B)  # 二范数
    sim = 1.0 / (1.0 + dist)  #
    return sim

def compare_faces(x, y, Threshold,  top_k_num = 3):
    ressim = []
    match = [False] * len(x)
    for fet in x:
        sim = simcos(fet, y)
        ressim.append(sim)
    if max(ressim) > Threshold:  # 置信度阈值
        match[ressim.index(max(ressim))] = True
        ressim_np= np.array(ressim)
        ressim_sort = np.argsort(-np.array(ressim), axis = 0)
        top_k_idx = ressim_sort[0:top_k_num]
    return match, max(ressim), top_k_idx

# 对人脸进行识别(与库内人脸进行比较)
def identityRecognition(testimg, known_face_encodings, known_face_IDs, Threshold):
    #testimg：当前截图，待匹配人脸
    #known_face_encodings: 人脸编码集合
    #known_face_IDs： 人脸标号集合
    face_locations = face_recognition.face_locations(testimg)#检测出图像中所有面部
    #针对多人脸的操作， 核心思想是只取最大的
    max_face_id = 0
    face_locations_select = []
    if len(face_locations)>1:
        for face_idx in range(len(face_locations)):
            if (face_locations[face_idx][2]>face_locations[max_face_id][2]) and  (face_locations[face_idx][3]>face_locations[max_face_id][3]):
                max_face_id = face_idx
        face_locations_select.append(face_locations[face_idx])
    else:
        face_locations_select = face_locations
    face_encodings = face_recognition.face_encodings(testimg, face_locations_select) #获取图像中所有面部的编码
    retname, retscore = np.array(0), np.array(0)
    top_k_idx = []
    for face_encoding in face_encodings:
        matches, score, top_k_idx = compare_faces(known_face_encodings, face_encoding, Threshold, top_k_num = 3)
        retname, retscore = np.array(0), np.array(0)   #
        if True in matches:
            # first_match_index = matches.index(True)
            # name = known_face_IDs[first_match_index]
            known_face_IDs_np = np.array(known_face_IDs)
            name = known_face_IDs_np[top_k_idx]
            if score > retscore:
                retname = name
                retscore = score
    return retname, top_k_idx