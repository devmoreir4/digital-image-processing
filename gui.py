import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Toplevel
import cv2
from PIL import Image, ImageTk
import numpy as np
import operations as ops

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ferramenta de Processamento de Imagens")
        self.root.geometry("1200x700")

        self.image_original = None
        self.image_processed = None
        self.image_tk_original = None
        self.image_tk_processed = None

        self._create_widgets()
        self._create_menus()

    def _create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        frame_original = tk.Frame(main_frame, bd=2, relief=tk.SUNKEN)
        frame_original.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(frame_original, text="Imagem Original").pack()
        self.label_original = tk.Label(frame_original)
        self.label_original.pack(fill=tk.BOTH, expand=True)

        frame_processed = tk.Frame(main_frame, bd=2, relief=tk.SUNKEN)
        frame_processed.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(frame_processed, text="Imagem Processada").pack()
        self.label_processed = tk.Label(frame_processed)
        self.label_processed.pack(fill=tk.BOTH, expand=True)

    def _create_menus(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Carregar Imagem", command=self.load_image)
        file_menu.add_command(label="Salvar Imagem Processada", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

        # Menu Operações Aritméticas
        arithmetic_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="1. Op. Aritméticas", menu=arithmetic_menu)
        arithmetic_menu.add_command(label="a. Adição (redução de ruído)", command=self.ui_add_images)
        arithmetic_menu.add_command(label="b. Subtração (diferença)", command=self.ui_subtract_images)
        arithmetic_menu.add_command(label="c. Correção de Sombreamento (Mult/Div)", command=self.ui_shading_correction)

        # Menu Transformações de Intensidade
        intensity_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="2. Transf. de Intensidade", menu=intensity_menu)
        intensity_menu.add_command(label="a. Negativo", command=self.ui_image_negative)
        intensity_menu.add_command(label="b. Alongamento de Contraste", command=self.ui_contrast_stretching)
        intensity_menu.add_command(label="c. Fatiamento de Planos de Bits", command=self.ui_bit_plane_slicing)
        intensity_menu.add_command(label="d. Equalização de Histograma", command=self.ui_histogram_equalization)

        # Menu Filtros Espaciais
        spatial_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="3. Filtros Espaciais", menu=spatial_menu)
        for size in [3, 5, 7]:
            spatial_menu.add_command(label=f"a. Filtro Média {size}x{size}", command=lambda s=size: self.ui_apply_filter('mean', s))
            spatial_menu.add_command(label=f"b. Filtro Mediana {size}x{size}", command=lambda s=size: self.ui_apply_filter('median', s))
            spatial_menu.add_command(label=f"c. Filtro Gradiente (Sobel) {size}x{size}", command=lambda s=size: self.ui_apply_filter('gradient', s))
            spatial_menu.add_command(label=f"d. Filtro Laplace {size}x{size}", command=lambda s=size: self.ui_apply_filter('laplace', s))
            if size != 7:
                spatial_menu.add_separator()

        # Menu Filtros de Frequência
        freq_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="4. Filtros Frequência", menu=freq_menu)
        for f_class, f_name in [("lowpass", "Passa-Baixa"), ("highpass", "Passa-Alta")]:
            sub_menu = tk.Menu(freq_menu, tearoff=0)
            freq_menu.add_cascade(label=f_name, menu=sub_menu)
            for f_type in ["ideal", "butterworth", "gaussian"]:
                sub_menu.add_command(label=f_type.capitalize(), command=lambda fc=f_class, ft=f_type: self.ui_frequency_filter(fc, ft))

        selective_menu = tk.Menu(freq_menu, tearoff=0)
        freq_menu.add_cascade(label="Seletiva", menu=selective_menu)
        selective_menu.add_command(label="Passa-Faixa", command=lambda: self.ui_frequency_filter('bandpass', 'ideal'))
        selective_menu.add_command(label="Rejeita-Faixa", command=lambda: self.ui_frequency_filter('bandreject', 'ideal'))
        selective_menu.add_command(label="Notch", command=self.ui_notch_filter)

    # --- Funções de Interface e Manipulação de Arquivos ---

    def load_image(self):
        path = filedialog.askopenfilename()
        if not path: return
        self.image_original = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.image_processed = self.image_original.copy()
        self.display_image(self.image_original, 'original')
        self.display_image(self.image_processed, 'processed')

    def save_image(self):
        if self.image_processed is None:
            messagebox.showerror("Erro", "Nenhuma imagem processada para salvar.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if not path: return
        cv2.imwrite(path, self.image_processed)
        messagebox.showinfo("Sucesso", f"Imagem salva em {path}")

    def display_image(self, img_cv, panel):
        panel_widget = self.label_original if panel == 'original' else self.label_processed
        panel_width, panel_height = panel_widget.winfo_width(), panel_widget.winfo_height()
        if panel_width < 2 or panel_height < 2:
            panel_width, panel_height = 580, 650

        h, w = img_cv.shape[:2]
        ratio = min(panel_width / w, panel_height / h)
        new_size = (int(w * ratio), int(h * ratio))
        img_resized = cv2.resize(img_cv, new_size, interpolation=cv2.INTER_AREA)

        img_pil = Image.fromarray(img_resized)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        if panel == 'original':
            self.image_tk_original = img_tk
            self.label_original.config(image=self.image_tk_original)
        else:
            self.image_tk_processed = img_tk
            self.label_processed.config(image=self.image_tk_processed)

    def check_image_loaded(self):
        if self.image_original is None:
            messagebox.showerror("Erro", "Por favor, carregue uma imagem primeiro.")
            return False
        return True

    def _update_processed_image(self, new_image):
        self.image_processed = new_image
        self.display_image(self.image_processed, 'processed')

    # --- Funções "UI" que chamam as operações ---

    def ui_add_images(self):
        if not self.check_image_loaded(): return
        path = filedialog.askopenfilename(title="Selecione a segunda imagem")
        if not path: return
        img2 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        result = ops.add_images(self.image_original, img2)
        self._update_processed_image(result)

    def ui_subtract_images(self):
        if not self.check_image_loaded(): return
        path = filedialog.askopenfilename(title="Selecione a imagem a ser subtraída")
        if not path: return
        img2 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        result = ops.subtract_images(self.image_original, img2)
        self._update_processed_image(result)

    def ui_shading_correction(self):
        if not self.check_image_loaded(): return
        path = filedialog.askopenfilename(title="Selecione a imagem de sombreamento")
        if not path: return
        shading_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        result = ops.shading_correction(self.image_original, shading_img)
        self._update_processed_image(result)

    def ui_image_negative(self):
        if not self.check_image_loaded(): return
        result = ops.image_negative(self.image_original)
        self._update_processed_image(result)

    def ui_contrast_stretching(self):
        if not self.check_image_loaded(): return
        result = ops.contrast_stretching(self.image_original)
        self._update_processed_image(result)

    def ui_bit_plane_slicing(self):
        if not self.check_image_loaded(): return
        result = ops.bit_plane_slicing(self.image_original)
        self._update_processed_image(result)
        messagebox.showinfo("Fatiamento", "Os 8 planos de bits (0-7) foram combinados na janela de processamento.")

    def ui_histogram_equalization(self):
        if not self.check_image_loaded(): return
        result = ops.histogram_equalization(self.image_original)
        self._update_processed_image(result)

    def ui_apply_filter(self, filter_type, kernel_size):
        if not self.check_image_loaded(): return
        result = ops.apply_filter(self.image_original, filter_type, kernel_size)
        self._update_processed_image(result)

    def ui_frequency_filter(self, filter_class, filter_type):
        if not self.check_image_loaded(): return

        D0 = simpledialog.askinteger("Input", f"Digite o raio de corte (D0) para o filtro {filter_type.capitalize()}:", parent=self.root, minvalue=1, maxvalue=500)
        if D0 is None: return

        order, D1 = 1, None
        if filter_type == 'butterworth':
             order = simpledialog.askinteger("Input", "Digite a ordem do filtro Butterworth:", parent=self.root, minvalue=1, maxvalue=10)
             if order is None: return

        if filter_class in ['bandpass', 'bandreject']:
            D1 = simpledialog.askinteger("Input", "Digite a largura da faixa (D1):", parent=self.root, minvalue=1)
            if D1 is None: return

        result = ops.apply_frequency_filter(self.image_original, filter_class, filter_type, D0, order, D1)
        self._update_processed_image(result)

    def ui_notch_filter(self):
        if not self.check_image_loaded(): return

        rows, cols = self.image_original.shape
        mask = np.ones((rows, cols, 2), np.float32)

        # Janela de visualização do espectro para seleção dos pontos
        dft_shift = np.fft.fftshift(cv2.dft(np.float32(self.image_original), flags=cv2.DFT_COMPLEX_OUTPUT))
        magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]) + 1)
        spectrum_norm = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        win = Toplevel(self.root)
        win.title("Selecione os pontos do Notch")
        img_pil = Image.fromarray(spectrum_norm)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        canvas = tk.Canvas(win, width=cols, height=rows)
        canvas.pack()
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

        def get_coords(event):
            u, v = event.x, event.y
            D0 = simpledialog.askinteger("Input", "Digite o raio do notch:", parent=win, minvalue=1)
            if D0 is None: return

            # Desenha círculos na máscara para rejeitar frequências
            cv2.circle(mask, (u, v), D0, (0, 0), -1)
            cv2.circle(mask, (cols - u, rows - v), D0, (0, 0), -1)

            # Feedback visual no canvas
            canvas.create_oval(u-D0, v-D0, u+D0, v+D0, outline='red', width=2)
            canvas.create_oval((cols-u)-D0, (rows-v)-D0, (cols-u)+D0, (rows-v)+D0, outline='red', width=2)

        canvas.bind("<Button-1>", get_coords)

        def on_apply():
            result = ops.apply_notch_filter(self.image_original, mask)
            self._update_processed_image(result)
            win.destroy()

        tk.Button(win, text="Aplicar Filtro e Fechar", command=on_apply).pack()
        win.transient(self.root)
        win.grab_set()
        self.root.wait_window(win)
