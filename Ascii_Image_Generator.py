##Libraries :  Pillow - Image processing 
##             NumPy - numerical computing

import sys,random,argparse
import numpy as np
from pathlib import Path
import os
import math

from PIL import Image

#Escala 
#Source: http://paulbourke.net/dataformats/asciiart/

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`'. "
gscale2 = "@%#*+=-:. "


def getAverageL(image):

    im = np.array(image)

    w,h = im.shape

    return np.average(im.reshape(w*h))


def convertImageToAscii(fileName, cols, scale, moreLevels):

    global gscale1, gscale2

    # Abrir imagem e converter para grayscale
    image = Image.open(fileName).convert('L')

    W,H = image.size[0], image.size[1]

    w = W/cols

    h = w/scale

    rows = int(H/h)

    #verificar se o tamanho da imagem é pequeno demais
    if cols > W or rows > H:
        print("Imagem demasiado pequena!")
        exit(0)

    aimg = []

    #gerar lista de dimensões
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        if j == rows - 1:
            y2 = H 
        
        
        aimg.append("")

        for i in range(cols):
            x1 = int(i * w)
            x2 = int((i+1) * w)

            if i == cols - 1:
                x2 = W

            img = image.crop((x1, y1, x2, y2))

            avg = int(getAverageL(img))

            if moreLevels:
                gsval = gscale1[int((avg * 69)/255)]
            else:
                gsval = gscale2[int((avg * 9)/255)] 

            aimg[j] += gsval

    return aimg


def main():

    descStr = "Imagem para ASCII."
    parser = argparse.ArgumentParser(description=descStr)

    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels',dest='moreLevels',action='store_true')

    args = parser.parse_args()

    imgFile = args.imgFile

    newImgFile = Path(args.imgFile).stem

    folder_path = "C:\Projects\ImageToAscii\Output"

    outFile = 'out_%s.txt' % newImgFile

    outFile = os.path.join(folder_path, outFile)
    

    if args.outFile:
        outFile = args.outFile
    
    scale = 0.43
    if args.scale:
        scale = float(args.scale)

    cols = 80
    if args.cols:
        cols = int(args.cols)

    print('A gerar...')

    aimg = convertImageToAscii(imgFile, cols, scale, args.moreLevels)

    f = open(outFile, 'w')

    for row in aimg:
        f.write(row + '\n')

    f.close

    print("ASCII escrita no %s" % outFile)

if __name__ == '__main__':
    main()