## 🚀 YouTube Downloader & MP3 Converter

Este projeto oferece scripts Python simples para **baixar vídeos do YouTube** e, opcionalmente, **converter arquivos de vídeo existentes para MP3**. É fácil de usar e te ajuda a organizar seu conteúdo! ✨

---

### 🛠️ Como Usar

Para começar, você precisará ter as bibliotecas corretas instaladas.

1.  **Instale os `requerimentos`**:
    Você pode instalar todas as bibliotecas necessárias de uma vez. Se você tiver um arquivo `requirements.txt` (que é uma boa prática para listar as dependências do seu projeto), use:
    ```bash
    pip install -r requirements.txt
    ```
    Ou, instale-as manualmente:
    ```bash
    pip install pytubefix moviepy
    ```

2.  **Baixar Vídeos do YouTube**:
    Use o script de download (ex: `app.py` ou `download_video.py`). Vá até a pasta do seu projeto no terminal e execute-o, adicionando o link do YouTube logo depois:
    ```bash
    python app.py "LINK_DO_VIDEO_DO_YOUTUBE_AQUI"
    ```
    **Exemplo:**
    ```bash
    python app.py "[https://www.youtube.com/watch?v=dQw4w9WgXcQ](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
    ```

3.  **Converter Vídeos Locais para MP3**:
    Se quiser, é possível usar o script de conversão `convert.py`, que pegará um arquivo de vídeo que voce passe o caminho e o transformará em MP3, pra facilitar se o video em questão já nao estiver na pasta videos na raiz desse projeto, ponha o video que quer converter lá e apenas rode no terminal:
    ```bash
    python convert.py "videos/nome_do_video.mp4"
    ```

---

### 📁 Onde os Arquivos Vão Parar?

* **Vídeos baixados:** Todos os vídeos do YouTube serão salvos em uma pasta chamada `videos`, criada automaticamente no diretório do projeto.
* **Áudios MP3 convertidos:** Todos os arquivos MP3 resultantes da conversão serão salvos em uma nova pasta chamada `MP3`, também criada automaticamente no diretório do projeto.

---

Aproveite seus downloads e suas novas faixas de áudio! 🎉