# -*- coding: utf-8 -*-

import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

def process_bmp ():
    parser = argparse.ArgumentParser(description='BMP reader')
    #parametre de fichier entrée (bitmap ou lena)
    parser.add_argument('--bmp', metavar='<bmp file name>', help='image file to parse', default= 'lena.bmp', required=True)
    args = parser.parse_args()
    file_name = args.bmp
    
    if not os.path.isfile(file_name):
        print('"{}" does not exist'.format(file_name), file=sys.stderr)
        sys.exit(-1)
    print('Success Opening {}...'.format(file_name))
    
    #Appel des fonctions du programme
    pixels, RGB, hauteur_image, largeur_image, taille_fichier = lecture_entête(file_name)
    
    print_pixel(RGB)
    copie_image(file_name, taille_fichier)
    img_rot = rotate_image90(pixels, largeur_image, hauteur_image)
    save_picture(file_name, img_rot, 1)
    img_rot = rotate_image180(pixels, largeur_image, hauteur_image)
    save_picture(file_name, img_rot, 2)
    img_rot = rotate_image270(pixels, largeur_image, hauteur_image)
    save_picture(file_name, img_rot, 3)
    
    niveau_de_gris(file_name, taille_fichier)
    noir_blanc(file_name, taille_fichier)
    negatif(file_name, taille_fichier)
    une_couleur(file_name, taille_fichier, 1)
    une_couleur(file_name, taille_fichier, 2)
    une_couleur(file_name, taille_fichier, 3)
    deux_couleurs(file_name, taille_fichier, 1)
    deux_couleurs(file_name, taille_fichier, 2)
    deux_couleurs(file_name, taille_fichier, 3)
    contraste(file_name, taille_fichier)
    histogramme(file_name, taille_fichier)
    
    modification_image(file_name, taille_fichier, largeur_image, hauteur_image, 1)
    modification_image(file_name, taille_fichier, largeur_image, hauteur_image, 2)
    modification_image(file_name, taille_fichier, largeur_image, hauteur_image, 3)
    modification_image(file_name, taille_fichier, largeur_image, hauteur_image, 4)
    modification_image(file_name, taille_fichier, largeur_image, hauteur_image, 5)
    sepia(file_name, taille_fichier)
    

def save_picture(file_name, image, choix): #fonction de sauvegarde de l'image dans le fichier de sortie
    f_lecture = open(file_name, 'rb')
    
    if(choix == 1):
        f_ecriture = open("Rot90.bmp", 'wb')
    elif(choix == 2):
        f_ecriture = open("Rot180.bmp", 'wb')
    elif(choix == 3):
        f_ecriture = open("Rot270.bmp", 'wb')
        
    header = f_lecture.read(54) #lire et ecrire le header dans le fichier de sortie
    f_ecriture.write(header)
    np.savetxt(f_ecriture, image, fmt='%s') #ecrire l'image modifiée
    f_lecture.close
    f_ecriture.close
    
#fonction pour copier une image à l'identique
def copie_image(file_name, taille_fichier):
    f_lecture = open(file_name, 'rb')
    f_ecriture = open("CopieIdentique.bmp", 'wb')
    i = 1

    while (i<=54): #on lit et écrit l'entête dans le fichier de sortie
        header = f_lecture.read(1)
        f_ecriture.write(header)
        i+=1
	
    while (i<=taille_fichier): #on lit et écrit chaque pixel en le décomposant avec ses trois composantes RGB
        blue = f_lecture.read(1)  
        green = f_lecture.read(1)
        red = f_lecture.read(1)
        f_ecriture.write(blue)
        f_ecriture.write(green)
        f_ecriture.write(red)
        i+=3
    f_lecture.close
    f_ecriture.close
    
def lecture_entête(file_name):
    f_lecture = open(file_name, 'rb')
    
    i=1
    octet = bytes([0])
    octet_bis = bytes([0])
    octets = []
    RGB = []
    pixels = []
    
    #Lecture du MAGIC NUMBER
    while (i <=2): #lecture Magic number sur 2 octets
        octet=f_lecture.read(1) #Lecture octet par octet
        octets.append(ord(octet))
        print (octet.decode('utf-8')," dec=",ord(octet))
        i=i+1
    print(" =>Magic Number =", octets, " BM => BitMap")  
    
    #affichage des parties de l'entête
    #le for in range permet d'avoir un code plus propre qu'une suite de while
    #int(octet[::-1].hex(), 16) nous permet de faire un little endian
    #nous inversons les valeurs avant de transformer le tout en hexadecimal puis en entier base 16
    for i in range (3, 27):
        if(i == 3):
            octet = f_lecture.read(4)
            taille_fichier = int(octet[::-1].hex(), 16)
            print(octet.hex(), " =>taille de fichier =", taille_fichier, "octets")
        if(i == 7):
            octet = f_lecture.read(4)
            print(octet.hex(), " =>application image =", int(octet[::-1].hex(), 16), "noms")
        if(i == 11):
            octet = f_lecture.read(4)
            print(octet.hex(), " =>taille entête =", int(octet[::-1].hex(), 16), "octets")
        if(i == 15):
            octet = f_lecture.read(4)
            print(octet.hex(), " =>header size =", int(octet[::-1].hex(), 16))
        if(i == 19):
            octet = f_lecture.read(4)
            print(octet.hex(), " =>largeur image =", int(octet[::-1].hex(), 16), "pixels")
            largeur_image = int(octet[::-1].hex(), 16)
        if(i == 23):
            octet = f_lecture.read(4)
            print(octet.hex(), " =>hauteur image =", int(octet[::-1].hex(), 16), "pixels")
            hauteur_image = int(octet[::-1].hex(), 16)
        i = i+4
    
    for i in range (27, 31):
        if(i == 27):
            octet = f_lecture.read(2)
            print(octet.hex(), " =>NB plan image =", int(octet[::-1].hex(), 16), "plan")
        if(i == 29):
            octet = f_lecture.read(2)
            print(octet.hex(), " =>NB couleur image =", int(octet[::-1].hex(), 16), "couleurs")
        i = i+2
        
    #BLOC ENTETE 54 octets en standard
    while (i<=54):
        octet=f_lecture.read(1)
        i=i+1
     
    #On écrit toutes les valeurs de l'image une par une dans une liste
    #cette liste sera utilisée pour afficher le pixel demandé au clavier
    for i in range(55, taille_fichier+2):
        octet = f_lecture.read(1)
        RGB.append(octet)
    RGB.pop(0)
    
    f_lecture.seek(54) #on se place au 54ème octet
    
    #On écrit toutes les valeurs de l'image 3 par 3 (composantes RGB) dans une liste
    #cette liste sera utilisée pour la rotation de l'image    
    for i in range(55, taille_fichier+2, 3):
        octet_bis = f_lecture.read(3)
        pixels.append(octet_bis)
    pixels.pop()

    f_lecture.close
    return pixels, RGB, hauteur_image, largeur_image, taille_fichier

#Fonction pour afficher le pixel demandé au clavier
def print_pixel(RGB):
    
    #on récupère la position du pixel au clavier
    p_str = input('Quel pixel voulez-vous afficher ?: ')
    p_int = int(p_str)
    
    #on se positionne dans la liste à l'indice de la premiere composante du pixel
    p_int = p_int * 3 - 3
    
    #on écrit les trois composantes RBG du pixel choisi
    print("Composante Bleue: ", int(RGB[p_int].hex(), 16))
    print("Composante Verte: ", int(RGB[p_int + 1].hex(), 16))
    print("Composante Rouge: ", int(RGB[p_int + 2].hex(), 16))
  
#fonctions pour la rotation de 90, 180 et 270 degrés
#Dans ces trois fonctions, nous transformons notre liste de pixels en tableau 2D
#Nous faisons ensuite la rotation des valeurs du tableau en fonction de la rotation choisie
def rotate_image90(pixels, largeur_image, hauteur_image):
    img = np.array(pixels)
    new_img = img.reshape(hauteur_image, largeur_image)
    img_rot = np.rot90(new_img)
    return(img_rot)

def rotate_image180(pixels, largeur_image, hauteur_image):
    img = np.array(pixels)
    new_img = img.reshape(hauteur_image, largeur_image)
    img_rot = np.rot90(new_img, 2)
    return(img_rot)

def rotate_image270(pixels, largeur_image, hauteur_image):
    img = np.array(pixels)
    new_img = img.reshape(hauteur_image, largeur_image)
    img_rot = np.rot90(new_img, 3)
    return(img_rot)

def niveau_de_gris(file_name, taille_fichier):
    f_lecture = open(file_name, 'rb')
    f_ecriture = open("greyscale.bmp", 'wb')
    i = 1

    while (i<=54): #on lit et écrit l'entête dans le fichier de sortie
        header = f_lecture.read(1)
        f_ecriture.write(header)
        i+=1
	
    while (i<=taille_fichier): #on lit et écrit chaque pixel en le décomposant avec ses trois composantes RGB
        blue = f_lecture.read(1)  
        green = f_lecture.read(1)
        red = f_lecture.read(1)
        grey_level = int(( ord(blue) + ord(green) + ord(red) )/3) #on récupère la moyenne des valeurs des pixels pour avoir le niveau de gris
        f_ecriture.write(bytes([grey_level]))
        f_ecriture.write(bytes([grey_level]))
        f_ecriture.write(bytes([grey_level]))
        i+=3
    f_lecture.close
    f_ecriture.close
        
def noir_blanc(file_name, taille_fichier):
    f_lecture = open(file_name, 'rb')
    f_ecriture = open("NoirBlanc.bmp", 'wb')
    i = 1

    while (i<=54): #on lit et écrit l'entête dans le fichier de sortie
        header = f_lecture.read(1)
        f_ecriture.write(header)
        i+=1
	
    while (i<=taille_fichier): #on lit et écrit chaque pixel en le décomposant avec ses trois composantes RGB
        blue = f_lecture.read(1)  
        green = f_lecture.read(1)
        red = f_lecture.read(1)
        
        grey_level = int(( ord(blue) + ord(green) + ord(red) )/3) #on calcule la moyenne
        
        if(grey_level > 128): #on attribue la valeur correspondant au noir ou au blanc en fonction de la valeur de la moyenne
            value = 255
        else:
            value = 0
            
        f_ecriture.write(bytes([value]))
        f_ecriture.write(bytes([value]))
        f_ecriture.write(bytes([value]))
        i+=3
    f_lecture.close
    f_ecriture.close
        
def negatif(file_name, taille_fichier):
    f_lecture = open(file_name, 'rb')
    f_ecriture = open("Negatif.bmp", 'wb')
    i = 1

    while (i<=54): #on lit et écrit l'entête dans le fichier de sortie
        header = f_lecture.read(1)
        f_ecriture.write(header)
        i+=1
	
    while (i<=taille_fichier): #on lit et écrit chaque pixel en le décomposant avec ses trois composantes RGB
        octet = f_lecture.read(1)
        
        valeur = ord(octet) #on récupère la valeur décimale de l'octet lu
        negatif = 255 - valeur #Pour obtenir le négatif, on fait 255 - la valeur décimale
        new_valeur = int.to_bytes(negatif,1, byteorder = "little")#On transforme le négatif en valeur binaire
        
        f_ecriture.write(new_valeur)
        i+=1
    f_lecture.close
    f_ecriture.close

def une_couleur(file_name, taille_fichier, choix):
    f_lecture = open(file_name, 'rb')
    i = 1
    
    #on ouvre le fichier de sortie en fonction du choix de l'utilisateur
    if(choix == 1):#Rouge
        f_ecriture = open("Rouge.bmp", 'wb')
    elif(choix == 2):#Vert
        f_ecriture = open("Vert.bmp", 'wb')
    elif(choix == 3):#bleu
        f_ecriture = open("Bleu.bmp", 'wb')
        
    while (i<=54): #on lit et écrit l'entête dans le fichier de sortie
        header = f_lecture.read(1)
        f_ecriture.write(header)
        i+=1
	
    while (i<=taille_fichier): #on lit et écrit chaque pixel en le décomposant avec ses trois composantes RGB
        blue = f_lecture.read(1)  
        green = f_lecture.read(1)
        red = f_lecture.read(1)
        
        #Pour chaque couleur, on va mêttre à 0 toutes les composantes RGB qui ne sont pas de la couleur choisie
        if(choix == 1):#Rouge
            f_ecriture.write(bytes([0]))
            f_ecriture.write(bytes([0]))
            f_ecriture.write(red)
        elif(choix == 2):#Vert
            f_ecriture.write(bytes([0]))
            f_ecriture.write(green)
            f_ecriture.write(bytes([0]))
        elif(choix == 3):#bleu
            f_ecriture.write(blue)
            f_ecriture.write(bytes([0]))
            f_ecriture.write(bytes([0]))
        i+=3
    f_lecture.close
    f_ecriture.close

def deux_couleurs(file_name, taille_fichier, choix):
    f_lecture = open(file_name, 'rb')
    i = 1
    
    #on ouvre le fichier de sortie en fonction du choix de l'utilisateur
    if(choix == 1):#Rouge + Vert
        f_ecriture = open("RougeVert.bmp", 'wb')
    elif(choix == 2):#Rouge + Bleu
        f_ecriture = open("RougeBleu.bmp", 'wb')
    elif(choix == 3):#Vert + bleu
        f_ecriture = open("VertBleu.bmp", 'wb')
    
    while (i<=54): #on lit et écrit l'entête dans le fichier de sortie
        header = f_lecture.read(1)
        f_ecriture.write(header)
        i+=1
	
    while (i<=taille_fichier): #on lit et écrit chaque pixel en le décomposant avec ses trois composantes RGB
        blue = f_lecture.read(1)  
        green = f_lecture.read(1)
        red = f_lecture.read(1)
        
        #Même principe que pour une couleur, sauf que nous avons qu'une composante à 0
        if(choix == 1):#Rouge + Vert
            f_ecriture.write(bytes([0]))
            f_ecriture.write(green)
            f_ecriture.write(red)
        elif(choix == 2):#Rouge + Bleu
            f_ecriture.write(blue)
            f_ecriture.write(bytes([0]))
            f_ecriture.write(red)
        elif(choix == 3):#Vert + bleu
            f_ecriture.write(blue)
            f_ecriture.write(green)
            f_ecriture.write(bytes([0]))
        i+=3
    f_lecture.close
    f_ecriture.close
        
def contraste(file_name, taille_fichier):
    f_lecture = open(file_name, 'rb')
    f_ecriture = open("Contraste.bmp", 'wb')
    i = 1
    
    while (i<=54): #on lit et écrit l'entête dans le fichier de sortie
        header = f_lecture.read(1)
        f_ecriture.write(header)
        i+=1
    
    while (i<=taille_fichier): #on lit et écrit chaque pixel en le décomposant avec ses trois composantes RGB
        blue = f_lecture.read(1)  
        green = f_lecture.read(1)
        red = f_lecture.read(1)
        
        moyenne = int(( ord(blue) + ord(green) + ord(red)) /3) #On calcule la moyenne des trois composantes pour chaque pixel

        #On calcule la valeur de contraste pour chaque composante RGB
        c_blue = (moyenne + ord(blue) - 128) %255 
        c_green = (moyenne + ord(green) - 128) %255
        c_red = (moyenne + ord(red) - 128) %255
        
        #on écrit dans le fichier de sortie la valeur des contrastes en binaire
        f_ecriture.write(int.to_bytes(c_blue,1, byteorder = "little"))
        f_ecriture.write(int.to_bytes(c_green,1, byteorder = "little"))
        f_ecriture.write(int.to_bytes(c_red,1, byteorder = "little"))
        
        i+=3
    f_lecture.close
    f_ecriture.close

def histogramme(file_name, taille_fichier):
    f_lecture = open(file_name, 'rb')
    i = 1
    octet = bytes([0])
    
    #On crée trois liste pour chaque composante RGB d'un pixel
    red_list = []
    green_list = []
    blue_list = []
    
    while (i<=54): #on lit l'entête
        octet = f_lecture.read(1)
        i+=1
    
    while (i<=taille_fichier): #on lit et écrit chaque pixel en le décomposant avec ses trois composantes RGB
        blue_list.append(ord(f_lecture.read(1)))
        green_list.append(ord(f_lecture.read(1)))
        red_list.append(ord(f_lecture.read(1)))
        i+=3
    
    #on crée et affiche l'histogramme
    pixel_list = [blue_list, green_list, red_list]
    plt.hist(pixel_list, color = 'bgr', bins = range(256))
    plt.xlabel("Valeur de pixels")
    plt.ylabel("Fréquence d'apparition")
    plt.savefig("histogramme.png")
    plt.show()
    
    f_lecture.close

#fonction pour choisir le kernel en fonction du filtre choisi
def choix_kernel(choix):
    
    if(choix == 1):#Detection des contours
        kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    elif(choix == 2):#Renforcement des bords
        kernel = np.array([[0, 0, 0], [-1, 1, 0], [0, 0, 0]])
    elif(choix == 3):#Flou
        kernel = np.array([[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]])
    elif(choix == 4):#Repoussage
        kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
    elif(choix == 5):#Innovation
        kernel = np.array([[42, -42, 3], [-5, 7, -25], [69, -66, 2]])
    
    return kernel

#fonction pour effectuer le calcul entre les pixels et la matrice de concolution choisie
#nous effectuons les calculs pour les valeurs autour du pixel de démarage
def calcul_convolution(image, kernel, largeur_image, hauteur_image):
    new_img = []
    somme = 0
    
    for p in range(len(image)):
        somme = somme + image[p]*kernel[1][1]
        
        if p - (largeur_image + 1) >= 0 and (p - 1) % largeur_image != 0:
            somme = somme + image[p - (largeur_image + 1)] * kernel[0][0]
            
        if p - (largeur_image) >= 0:
            somme = somme + image[p - (largeur_image)] * kernel[0][1]
            
        if p - (largeur_image - 1) >= 0 and (p + 1) % largeur_image != 0:
            somme = somme + image[p - (largeur_image - 1)] * kernel[0][2]
            
        if (p - 1) % largeur_image != 0:
            somme = somme + image[p - 1]* kernel[1][0]
            
        if (p + 1) % largeur_image != 0:
            somme = somme + image[p + 1] * kernel[1][2]
            
        if p + (largeur_image - 1) < largeur_image * hauteur_image and (p - 1) % largeur_image !=0:
            somme = somme + image[p + (largeur_image - 1)] * kernel[2][0]
            
        if p + (largeur_image) < largeur_image * hauteur_image:
            somme = somme + image[p + (largeur_image)] * kernel[2][1]
            
        if p + (largeur_image + 1) < largeur_image * hauteur_image and (p + 1) % largeur_image !=0:
            somme = somme + image[p + (largeur_image + 1)] * kernel[2][2]
        
        new_img.append(somme)
        somme = 0
        
    return new_img

#Fonction pour effectuer la modification de l'image en fonction du kernel choisi
#Nous récupérons les trois composantes du pixel et effectuons les calculs pour chacune d'entre elles
#Enfin, nous sauvegardons les pixels modifiés dans le fichier de sortie
def modification_image(file_name, taille_fichier, largeur_image, hauteur_image, choix):
    f_lecture = open(file_name, 'rb')
    kernel = choix_kernel(choix)
    i = 1
    red = []
    green = []
    blue = []
    
    if(choix == 1):#Detection des contours
        f_ecriture = open("DetectionDesContours.bmp", 'wb')
    elif(choix == 2):#Renforcement des bords
        f_ecriture = open("RenforcementDesBords.bmp", 'wb')
    elif(choix == 3):#Flou
        f_ecriture = open("Flou.bmp", 'wb')
    elif(choix == 4):#Repoussage
        f_ecriture = open("Repoussage.bmp", 'wb')
    elif(choix == 5):#Innovation
        f_ecriture = open("Innovation.bmp", 'wb')
        
    
    while (i<=54): #on lit et écrit l'entête dans le fichier de sortie
        header = f_lecture.read(1)
        f_ecriture.write(header)
        i+=1
        
    while (i<=taille_fichier): #on lit et écrit chaque pixel en le décomposant avec ses trois composantes RGB
        blue.append(ord(f_lecture.read(1)))
        green.append(ord(f_lecture.read(1)))
        red.append(ord(f_lecture.read(1)))
        i+=3
    
    blue = calcul_convolution(blue, kernel, largeur_image, hauteur_image)
    green = calcul_convolution(green, kernel, largeur_image, hauteur_image)
    red = calcul_convolution(red, kernel, largeur_image, hauteur_image)

    color_list=[blue,green,red]
    j=0
    while(j<len(red)):
        for k in range(3):
            if color_list[k][j]<0:
                f_ecriture.write(bytes([0]))
            elif color_list[k][j]>255:
                f_ecriture.write(bytes([255]))
            else :
                f_ecriture.write(bytes([int(color_list[k][j])]))
        j+=1

    f_lecture.close
    f_ecriture.close

#Fonction pour coder le filtre sépia
#On récupère les pixels de l'image puis on les transforme grâce à des coefficients
#Enfin, nous sauvegardons les pixels modifiés dans le fichier de sortie
def sepia(file_name, taille_fichier):
    f_lecture = open(file_name, 'rb')
    f_ecriture = open("Sepia.bmp", 'wb')
    i = 1

    while (i<=54): #on lit et écrit l'entête dans le fichier de sortie
        header = f_lecture.read(1)
        f_ecriture.write(header)
        i+=1
	
    while (i<=taille_fichier): #on lit et écrit chaque pixel en le décomposant avec ses trois composantes RGB
        blue = f_lecture.read(1)  
        green = f_lecture.read(1)
        red = f_lecture.read(1)
        
        new_blue = int(0.131 * ord(blue) + 0.534 * ord(green) + 0.272 * ord(red))
        new_green = int(0.168 * ord(blue) + 0.686 * ord(green) + 0.349 * ord(red))
        new_red = int(0.189 * ord(blue) + 0.769 * ord(green) + 0.393 * ord(red))
        
        if(new_blue > 255):
            new_blue = 255
        if(new_green > 255):
            new_green = 255
        if(new_red > 255):
            new_red = 255
            
        f_ecriture.write(int.to_bytes(new_blue, 1, byteorder = "little"))
        f_ecriture.write(int.to_bytes(new_green, 1, byteorder = "little"))
        f_ecriture.write(int.to_bytes(new_red, 1, byteorder = "little"))
        i+=3
        
    f_lecture.close
    f_ecriture.close
    

if __name__ == '__main__':
    process_bmp()
    sys.exit(0)