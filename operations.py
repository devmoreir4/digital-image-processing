import cv2
import numpy as np

def add_images(img1, img2):
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return cv2.add(img1, img2_resized)

def subtract_images(img1, img2):
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return cv2.subtract(img1, img2_resized)

def shading_correction(original_img, shading_img):
    shading_resized = cv2.resize(shading_img, (original_img.shape[1], original_img.shape[0]))

    # Normaliza a imagem de sombreamento para [0, 1]
    shading_norm = shading_resized.astype(np.float32) / 255.0
    shading_norm[shading_norm == 0] = 1e-6  # Evita divisão por zero

    original_float = original_img.astype(np.float32)
    corrected_float = original_float / shading_norm

    # Normaliza o resultado de volta para o intervalo [0, 255]
    return cv2.normalize(corrected_float, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

def image_negative(img):
    return 255 - img

def contrast_stretching(img):
    return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)

def bit_plane_slicing(img):
    # Gera uma imagem de grade com os 8 planos de bits
    planes = []
    for i in range(8):
        plane = (img >> i) & 1
        plane_img = (plane * 255).astype(np.uint8)
        planes.append(plane_img)

    rows, cols = 2, 4
    canvas_h, canvas_w = 150, 150
    grid = np.zeros((rows * canvas_h, cols * canvas_w), dtype=np.uint8)

    for i, plane in enumerate(planes):
        row = i // cols
        col = i % cols
        resized_plane = cv2.resize(plane, (canvas_w, canvas_h))
        grid[row*canvas_h:(row+1)*canvas_h, col*canvas_w:(col+1)*canvas_w] = resized_plane

    return grid

def histogram_equalization(img):
    return cv2.equalizeHist(img)

def apply_filter(img, filter_type, kernel_size):
    # Aplica um filtro espacial (média, mediana, gradiente, laplace)
    if filter_type == 'mean':
        return cv2.blur(img, (kernel_size, kernel_size))
    elif filter_type == 'median':
        return cv2.medianBlur(img, kernel_size)
    elif filter_type == 'gradient':
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=kernel_size)
        magnitude = cv2.magnitude(sobelx, sobely)
        return cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    elif filter_type == 'laplace':
        laplacian = cv2.Laplacian(img, cv2.CV_64F, ksize=kernel_size)
        return cv2.normalize(laplacian, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return img

def apply_frequency_filter(img, filter_class, filter_type, D0, order=1, D1=None):
    img_float = np.float32(img)
    dft = cv2.dft(img_float, flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2

    mask = np.zeros((rows, cols, 2), np.float32)

    for u in range(rows):
        for v in range(cols):
            D = np.sqrt((u - crow)**2 + (v - ccol)**2)
            value = 0

            # Filtros Passa-Baixa
            if filter_class == 'lowpass':
                if filter_type == 'ideal':
                    value = 1 if D <= D0 else 0
                elif filter_type == 'butterworth':
                    value = 1 / (1 + (D / D0)**(2 * order))
                elif filter_type == 'gaussian':
                    value = np.exp(-(D**2) / (2 * D0**2))

            # Filtros Passa-Alta
            elif filter_class == 'highpass':
                if D == 0: D = 1e-6 # Evita divisão por zero para butterworth
                if filter_type == 'ideal':
                    value = 1 if D > D0 else 0
                elif filter_type == 'butterworth':
                    value = 1 / (1 + (D0 / D)**(2 * order))
                elif filter_type == 'gaussian':
                    value = 1 - np.exp(-(D**2) / (2 * D0**2))

            # Filtros de Faixa
            elif filter_class in ['bandpass', 'bandreject']:
                if D1 is None: D1 = D0 * 0.2 # Largura de faixa padrão
                value_pass = 1 if (D0 - D1/2 <= D <= D0 + D1/2) else 0
                if filter_class == 'bandpass':
                    value = value_pass
                else: # bandreject
                    value = 1 - value_pass

            mask[u, v] = [value, value]

    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    return cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

def apply_notch_filter(img, mask):
    img_float = np.float32(img)
    dft = cv2.dft(img_float, flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    fshift = dft_shift * mask

    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])

    return cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
