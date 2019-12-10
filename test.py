# 导入人脸识别库
import face_recognition
import globVar
with open(globVar.libpath + 'faceList.txt', 'r') as f:
    lines = f.readlines()
    # result_file = open('G:/研二/监考分配/facialCarding/facialCarding/facialData/face_ecnode.txt', 'w')
encode_file = open('facialData/face_ecnode.txt')

for line in lines:
    img_lable_name = line.split()
    # image = face_recognition.load_image_file(globVar.libpath + str(img_lable_name[0]))
    #
    # face_locations = face_recognition.face_locations(image)
    # face_encoding = face_recognition.face_encodings(image, face_locations)[0]
    #
    # face_encoding_list = face_encoding.tolist()
    # str_face_encoding = ''
    # for list_idx in range(len(face_encoding_list)):
    #     str_face_encoding += '{}'.format(face_encoding_list[list_idx]) + ' '
    # result_file.write(str_face_encoding + '\n')
    face_encoding = []
    str_encode = encode_file.readline()[:-1]
    encode_info = str_encode.split(' ')
    for info_idx in range(len(encode_info) - 1):
        face_encoding.append(float(encode_info[info_idx]))
    globVar.known_face_encodings.append(face_encoding)
    globVar.known_face_IDs.append(str(img_lable_name[1]))
# result_file.close()
encode_file.close()