import cv2
import numpy as np
import os
from PIL import Image



pasta='./faces'

largura_final = 800  # Tamanho da janela
altura_final = 800 

imagem_final = np.zeros((altura_final, largura_final, 3), dtype=np.uint8)

     

imagens = []


for arquivo in os.listdir(pasta):
    caminho = os.path.join(pasta, arquivo)
    
    # Verifica se o arquivo é uma imagem
    if os.path.isfile(caminho) and arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
        # Abra a imagem com o OpenCV
        imagem = cv2.imread(caminho)
        imagens.append(imagem)
        
    
    for i , imagem in enumerate(imagens):
        imagem_redimensionada = cv2.resize(imagem, (400, 200))       
        
        #cv2.imshow('DataBase',imagem_redimensionada)
        #cv2.waitKey(0)
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







