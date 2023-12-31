#!/usr/bin/env python3
import face_recognition
import os, sys
import cv2
import numpy as np
import copy
import random
import time
from speech import Speech
import threading

    
def savephoto(frame, video_capture):
    
    while True:
        name = input("Insert name ('cancel' to cancel): ")

        if name.lower() == 'cancel':
            break

        if name:
            directory = "faces"
            
            filename = os.path.join(directory, f"{name}_.jpg")

            if os.path.exists(filename):
                i = 1
                while True:
                    new_filename = os.path.join(directory, f"{name}_{i}.jpg")
                    if not os.path.exists(new_filename):
                        filename = new_filename
                        break
                    i += 1

            cv2.imwrite(filename, frame)
            print(f"Photo saved as {filename}")
            video_capture.release()
            cv2.destroyAllWindows()
            python_script = "main.py"
            os.system(f"python3 {python_script}")

def sp(tracks):
    s=Speech(tracks)
    s.run()

def database():
    pasta='./faces'

    largura_final = 800  # Tamanho da janela
    altura_final = 800 

    imagem_final = np.zeros((altura_final, largura_final, 3), dtype=np.uint8)

        

    imagens = []


    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        
        
        if os.path.isfile(caminho) and arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
          
            imagem = cv2.imread(caminho)
            imagens.append(imagem)
            
        
        for i , imagem in enumerate(imagens):
            imagem_redimensionada = cv2.resize(imagem, (400, 200))       
            
            
            print(i)
            if i==0:
                roi=imagem_final[ 0:200, 0:400]
                cv2.addWeighted(roi, 0, imagem_redimensionada, 1, 0, roi)
            elif i==1:
                roi=imagem_final[ 0:200, 400:800]
                cv2.addWeighted(roi, 0, imagem_redimensionada, 1, 0, roi)
            elif i==2:
                roi=imagem_final[200:400,0:400]
                cv2.addWeighted(roi, 0, imagem_redimensionada, 1, 0, roi)
            elif i==3:
                roi=imagem_final[200:400,400:800]
                cv2.addWeighted(roi, 0, imagem_redimensionada, 1, 0, roi)
            elif i==4:
                roi=imagem_final[400:600 , 0:400]
                cv2.addWeighted(roi, 0, imagem_redimensionada, 1, 0, roi)
            elif i==5:
                roi=imagem_final[400:600, 400:800]
                cv2.addWeighted(roi, 0, imagem_redimensionada, 1, 0, roi)
            elif i==6:
                roi=imagem_final[ 600:800, 0:400]
                cv2.addWeighted(roi, 0, imagem_redimensionada, 1, 0, roi)
            elif i==7:
                roi=imagem_final[600:800, 400:800]
                cv2.addWeighted(roi, 0, imagem_redimensionada, 1, 0, roi)

        


    cv2.imshow('DataBase',imagem_final)

    cv2.waitKey(0)
    
class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True
    people = []
    tracks = {}
    color = {}
    
    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f'faces/{image}')
            face_encodings = face_recognition.face_encodings(face_image)

            if face_encodings:
                
                face_encoding = face_encodings[0]

                self.known_face_encodings.append(face_encoding)
                name_without_extension = os.path.splitext(image)[0]
                name = name_without_extension.split('_')[0]

                self.known_face_names.append(name)
            else:
                print(f"No faces detected in the image: {image}")
            
        self.people = set(self.known_face_names)
        print(self.people)
        print('Press S to save last frame')

    

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)
        start_time = 0
        end_time= time.time()
        f_start = time.time()
        fps = 0
        if not video_capture.isOpened():
            sys.exit('Video source not found...')
   
        dif_max_loc_0 = 0
        dif_max_loc_1 = 0
        while True:
            ret, frame = video_capture.read()

            img = copy.deepcopy(frame)
            frame_cut = copy.deepcopy(frame)
            if self.process_current_frame:
                for name in self.tracks:
                    if True in self.tracks[name]:
                        frame_cut[self.tracks[name][0]:self.tracks[name][2],self.tracks[name][3]:self.tracks[name][1]] = 0
                    
               
                small_frame = cv2.resize(frame_cut, (0,0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:,:,::+1]
                

                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
                 
                self.face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = 'Unknown'

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        

                    self.face_names.append(f'{name}')
            
                
            for name in self.tracks:
                if not name in self.face_names and True in self.tracks[name]:
                        last_gray_frame = cv2.cvtColor(last_frame, cv2.COLOR_BGR2GRAY)
                        mask = last_gray_frame[self.tracks[name][0]:self.tracks[name][2],self.tracks[name][3]:self.tracks[name][1]]
                        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        result = cv2.matchTemplate(gray_frame,mask, cv2.TM_CCOEFF_NORMED)

                        _, _, _, max_loc = cv2.minMaxLoc(result)
                        h,w= mask.shape
                        
                        if self.tracks[name][7] == None:
                            self.tracks[name][5] = time.time() #start
                            self.tracks[name][7] = max_loc #last loc
                            
                            
                        self.tracks[name][6] = time.time() #end

                        dif_time = self.tracks[name][6] - self.tracks[name][5]

                        if dif_time > 0: 
                            dif_max_loc_0 = abs(max_loc[0] - self.tracks[name][7][0]) / dif_time
                            dif_max_loc_1 = abs(max_loc[1] - self.tracks[name][7][1]) / dif_time


                        if (dif_max_loc_0 > 1000 or dif_max_loc_1 > 1000):
                            self.tracks[name][4] = False
                            self.tracks[name][7] = None
                        
                            continue
                        self.tracks[name][5]= time.time()
                        self.tracks[name][7] = max_loc
                        f_end = time.time()
                        fps = 1/(f_end -f_start)
                        f_start = time.time()
                        cv2.rectangle(frame, (max_loc[0],max_loc[1]),(max_loc[0]+w, max_loc[1]+h),self.color[name],2)
                        cv2.rectangle(frame, (max_loc[0],max_loc[1]+h-25),(max_loc[0]+w, max_loc[1]+h),self.color[name],-1)
                        cv2.putText(frame, f'{name}', (max_loc[0] + 6, max_loc[1] + h - 6),cv2.FONT_HERSHEY_DUPLEX,0.8,(255,255,255),1)
                        cv2.putText(frame,f'{str(int(fps))} fps',(10,20),cv2.FONT_HERSHEY_DUPLEX,0.8,(0,255,0),1)
                   
                       

            for(top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *=4
                bottom *=4
                left *= 4

                if not name in self.color:
                    self.color[name] =(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
                cv2.rectangle(frame,(left,top),(right,bottom),self.color[name],2)
                cv2.rectangle(frame, (left, bottom - 25), (right,bottom),self.color[name], -1)
                cv2.putText(frame, name, (left + 6, bottom - 6),cv2.FONT_HERSHEY_DUPLEX,0.8,(255,255,255),1)
                cv2.putText(frame,f'{str(int(fps))} fps',(10,20),cv2.FONT_HERSHEY_DUPLEX,0.8,(0,255,0),1)

                self.tracks[name] = [top, right, bottom, left, True, None, None, None]

                last_frame = img

                print(self.tracks)

            f_end = time.time()
            fps = 1/(f_end -f_start)
            f_start = time.time()

            
            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) == ord('q'):
                break
            if cv2.waitKey(1) == ord('d'):
                database()
            if cv2.waitKey(1) == ord('s'):
                savephoto(img, video_capture)    
            end_time = time.time()
            dif_time = end_time - start_time
            if dif_time > 2:
                sp_thread = threading.Thread(target=sp, args=(self.tracks,))
                sp_thread.start()
                start_time = time.time()
            
            
            
            
        video_capture.release()
        cv2.destroyAllWindows()
    
    