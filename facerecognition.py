#!/usr/bin/env python3
import face_recognition
import os, sys
import cv2
import numpy as np
import math
import copy
import random

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2))+'%'
    else:
        value = (linear_val +((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value,2)) + '%'
    
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
            fr = FaceRecognition()
            fr.run_recognition()
    
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
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            name_without_extension = os.path.splitext(image)[0]
            name = name_without_extension.split('_')[0]

            self.known_face_names.append(name)
            
            
        self.people = set(self.known_face_names)
        print(self.people)
        print('Press S to save last frame')

    

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        while True:
            ret, frame = video_capture.read()

            img = copy.deepcopy(frame)
            if self.process_current_frame:
                small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
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

                self.tracks[name] = top, right, bottom, left, 1

                print(self.tracks)
            cv2.imshow('Face Recognition', frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
            if cv2.waitKey(1) == ord('s'):
                savephoto(img, video_capture)     
        video_capture.release()
        cv2.destroyAllWindows()
    
    