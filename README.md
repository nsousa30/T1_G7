# T1_G7


## Sobre o Projeto

Este projeto foi desenvolvido para o primeiro trabalho da disciplina Sistemas Avançados de Visão Industrial. Tem como objetivo detetar diferentes caras e através de uma base de dados dizer se é uma cara conhecida ou desconhecida.

## Colaboradores
- José Duarte (josemduarte@ua.pt)
- Nuno Sousa (nsousa@ua.pt)
- Sérgio Santos (sergioxsantos@ua.pt)

## Para começar

Este projeto usa [OpenCV](https://opencv.org/) para deteção das caras.

## Instalação
Para instalar o projeto, é primeiro necessário clonar o repositório através da seguinte linha de código:
```
git clone https://github.com/nsousa30/T1_G7.git

```

Para instalar todas as dependencias, é só correr no terminal:
```
pip install -r requirements.txt
```


## Uso

1. Coloque as imagens das pessoas que deseja reconhecer no diretório "faces". Os nomes dos arquivos de imagem devem conter o nome da pessoa mais "_" (por exemplo, "Joao_.jpg").
2. Execute o script main.py:
3. O script capturará a transmissão de vídeo da sua webcam e a exibirá. Se um rosto reconhecido for detectado, ele mostrará o nome da pessoa na tela. Se for um rosto desconhecido, será rotulado como "Unknown".
4. Pressione 'S' para guardar o frame atual com rostos reconhecidos. Será solicitado a inserir o nome da pessoa no frame.
5. Pressione 'D' para visualizar as fotos guardadas.
6. O projeto também inclui um recurso de texto para fala. Ele cumprimentará as pessoas reconhecidas pelo nome e os rostos desconhecidos como "Hello Stranger".

