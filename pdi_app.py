import cv2
import numpy as np
import sys

def load_gray(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        sys.exit(f"Erro ao carregar {path}")
    return img


def show(img, title):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def add_images(img1):
    path = input("Caminho da segunda imagem: ")
    img2 = load_gray(path)
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return cv2.add(img1, img2)


def subtract_images(img1):
    path = input("Caminho da imagem a subtrair: ")
    img2 = load_gray(path)
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return cv2.subtract(img1, img2)


def shading_correction(img):
    path = input("Caminho da imagem de sombreamento: ")
    shade = load_gray(path)
    shade = cv2.resize(shade, (img.shape[1], img.shape[0])).astype(np.float32)/255
    shade[shade==0] = 1e-6
    corrected = img.astype(np.float32)/shade
    return cv2.normalize(corrected, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def negative(img):
    return 255 - img


def contrast_stretch(img):
    return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)


def bit_plane_slicing(img):
    planes = []
    for i in range(8):
        plane = ((img >> i) & 1) * 255
        planes.append(plane.astype(np.uint8))
    grid = np.zeros((2*plane.shape[0], 4*plane.shape[1]), np.uint8)
    for idx, p in enumerate(planes):
        r, c = divmod(idx, 4)
        h, w = plane.shape
        grid[r*h:(r+1)*h, c*w:(c+1)*w] = p
    return grid


def histogram_equalization(img):
    return cv2.equalizeHist(img)


def main():
    path = input("Caminho da imagem: ")
    img = load_gray(path)
    while True:
        print("\nMenu:")
        print("1. Adição")
        print("2. Subtração")
        print("3. Correção de Sombreamento")
        print("4. Negativo")
        print("5. Alongamento de Contraste")
        print("6. Fatiamento de Planos de Bits")
        print("7. Equalização de Histograma")
        print("0. Sair")
        choice = input("Escolha: ")
        if choice == '0':
            break
        ops = {
            '1': add_images,
            '2': subtract_images,
            '3': shading_correction,
            '4': negative,
            '5': contrast_stretch,
            '6': bit_plane_slicing,
            '7': histogram_equalization
        }
        if choice in ops:
            result = ops[choice](img)
            show(result, "Resultado")
        else:
            print("Opção inválida")

if __name__ == '__main__':
    main()
