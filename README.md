# Ferramenta de Processamento de Imagens

Este projeto é uma aplicação de desktop escrita em Python, utilizando a biblioteca Tkinter para a interface gráfica. A ferramenta permite carregar imagens e aplicar diversas operações de Processamento de Imagens, desde manipulações aritméticas básicas até filtragens avançadas no domínio da frequência.<br>
Desenvolvido como parte da disciplina de Processamento Digital de Imagens (PDI).


## Funcionalidades

A aplicação possui suporte as seguintes operações:

**1. Operações Aritméticas**

- **Adição**: Soma duas imagens (redução de ruído por média).
- **Subtração**: Calcula a diferença entre duas imagens (detecção de mudanças).
- **Remoção de Sombreamento**: Corrige iluminação não uniforme dividindo pela imagem de referência de sombreamento.

**2. Transformações de Intensidade**

- **Negativo**: Inverte as cores.
- **Alongamento de Contraste**: Melhora visibilidade em imagens de baixo contraste.
- **Fatiamento de Planos de Bits**: Decompõe em 8 planos de 1 bit para análise.
- **Equalização de Histograma**: Realça contraste de forma automática.

**3. Filtros Espaciais**

- **Filtro da Média** (3×3, 5×5, 7×7): Suavização e redução de ruído.
- **Filtro da Mediana** (3×3, 5×5, 7×7): Remove ruído "sal e pimenta" preservando bordas.
- **Filtro Gradiente (Sobel)** (3×3, 5×5, 7×7): Detecção e realce de bordas.
- **Filtro de Laplace** (3×3, 5×5, 7×7): Realço de detalhes finos e bordas.

**4. Filtros no Domínio da Frequência**

- **Passa-Baixa** (Ideal, Butterworth, Gaussiano): Suavização e atenuação de ruído.
- **Passa-Alta** (Ideal, Butterworth, Gaussiano): Realce de bordas e detalhes.
- **Filtragem Seletiva**:

  - Passa-Faixa / Rejeita-Faixa: Isola ou remove faixas de frequência.
  - **Notch**: Remove ruídos periódicos específicos (padrões de linhas, interferências).


## Pré-requisitos

- Python 3.x
- Git


### Instalação e Execução

1. Clone o repositório e navegue até a pasta do projeto:

   ```bash
   git clone https://github.com/devmoreir4/digital-image-processing.git
   cd digital-image-processing
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:

   ```bash
   python main.py
   ```

A janela da aplicação deverá abrir, pronta para carregar e processar as suas imagens.


## Licença

Este projeto está sob a licença MIT.
