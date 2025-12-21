import customtkinter as ctk
from pytubefix import YouTube, request
from moviepy.video.io.VideoFileClip import VideoFileClip
from tkinter import filedialog
import os
import threading
import ssl

# Reduz o tamanho dos chunks de download para evitar erros SSL em algumas redes
request.default_range_size = 2 * 1024 * 1024  # 2 MB

class YouTubeDownloaderApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("YouTube Downloader & MP3 Converter")
        self.window.geometry("700x500")
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.window, 
            text="🎬 YouTube Downloader & MP3 Converter",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=15)
        
        # Criar abas
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Aba de Download
        self.tab_download = self.tabview.add("📥 Download")
        self.setup_download_tab()
        
        # Aba de Conversão
        self.tab_convert = self.tabview.add("🎵 Converter MP3")
        self.setup_convert_tab()
    
    def setup_download_tab(self):
        """Configura a aba de download"""
        # Frame para entrada de URL
        url_frame = ctk.CTkFrame(self.tab_download)
        url_frame.pack(pady=10, padx=20, fill="x")
        
        url_label = ctk.CTkLabel(
            url_frame, 
            text="Cole o link do vídeo:",
            font=ctk.CTkFont(size=14)
        )
        url_label.pack(pady=(10, 5))
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="https://www.youtube.com/watch?v=...",
            width=500,
            height=40
        )
        self.url_entry.pack(pady=(0, 10), padx=10)

        # Seleção de resolução
        res_frame = ctk.CTkFrame(self.tab_download)
        res_frame.pack(pady=(0, 10), padx=20, fill="x")

        res_label = ctk.CTkLabel(
            res_frame,
            text="Escolha a resolução (progressive):",
            font=ctk.CTkFont(size=13)
        )
        res_label.pack(pady=(10, 5))

        self.resolution_option = ctk.CTkComboBox(
            res_frame,
            values=["Auto (melhor disponível)", "1080p", "720p", "480p", "360p"],
            state="readonly",
            width=220
        )
        self.resolution_option.set("Auto (melhor disponível)")
        self.resolution_option.pack(pady=(0, 10))
        
        # Botão de download
        self.download_btn = ctk.CTkButton(
            self.tab_download,
            text="⬇️ Baixar Vídeo",
            command=self.start_download,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=200
        )
        self.download_btn.pack(pady=15)
        
        # Área de status do download
        status_frame = ctk.CTkFrame(self.tab_download)
        status_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.download_status_text = ctk.CTkTextbox(
            status_frame,
            font=ctk.CTkFont(size=12),
            height=150
        )
        self.download_status_text.pack(pady=10, padx=10, fill="both", expand=True)
        self.download_status_text.configure(state="disabled")
    
    def setup_convert_tab(self):
        """Configura a aba de conversão para MP3"""
        # Frame para seleção de arquivo
        file_frame = ctk.CTkFrame(self.tab_convert)
        file_frame.pack(pady=10, padx=20, fill="x")
        
        file_label = ctk.CTkLabel(
            file_frame, 
            text="Selecione o arquivo de vídeo:",
            font=ctk.CTkFont(size=14)
        )
        file_label.pack(pady=(10, 5))
        
        # Frame para entrada e botão
        input_frame = ctk.CTkFrame(file_frame)
        input_frame.pack(pady=(0, 10), padx=10, fill="x")
        
        self.file_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Clique em 'Procurar' para selecionar...",
            height=40
        )
        self.file_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        browse_btn = ctk.CTkButton(
            input_frame,
            text="📁 Procurar",
            command=self.browse_file,
            width=120,
            height=40
        )
        browse_btn.pack(side="right")
        
        # Botão de conversão
        self.convert_btn = ctk.CTkButton(
            self.tab_convert,
            text="🎵 Converter para MP3",
            command=self.start_convert,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=220
        )
        self.convert_btn.pack(pady=15)
        
        # Área de status da conversão
        convert_status_frame = ctk.CTkFrame(self.tab_convert)
        convert_status_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.convert_status_text = ctk.CTkTextbox(
            convert_status_frame,
            font=ctk.CTkFont(size=12),
            height=150
        )
        self.convert_status_text.pack(pady=10, padx=10, fill="both", expand=True)
        self.convert_status_text.configure(state="disabled")
    
    def log_download_status(self, message):
        """Adiciona mensagem ao log de status do download"""
        self.download_status_text.configure(state="normal")
        self.download_status_text.insert("end", f"{message}\n")
        self.download_status_text.see("end")
        self.download_status_text.configure(state="disabled")
    
    def log_convert_status(self, message):
        """Adiciona mensagem ao log de status da conversão"""
        self.convert_status_text.configure(state="normal")
        self.convert_status_text.insert("end", f"{message}\n")
        self.convert_status_text.see("end")
        self.convert_status_text.configure(state="disabled")
    
    def browse_file(self):
        """Abre diálogo para selecionar arquivo de vídeo"""
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo de vídeo",
            initialdir="videos",
            filetypes=[
                ("Arquivos de vídeo", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if filename:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, filename)
    
    def download_video(self, url):
        """Função que realiza o download do vídeo"""
        try:
            self.log_download_status("🔍 Buscando informações do vídeo...")
            
            yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
            
            self.log_download_status(f"📹 Título: {yt.title}")
            self.log_download_status(f"👁️ Visualizações: {yt.views:,}")
            
            self.log_download_status("⏳ Iniciando download...")
            desired_res = self.resolution_option.get()

            progressive_streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()

            selected_stream = None
            if desired_res != "Auto (melhor disponível)":
                selected_stream = progressive_streams.filter(res=desired_res).first()
                if selected_stream is None:
                    self.log_download_status("ℹ️ Resolução desejada não disponível. Usando a melhor disponível.")

            if selected_stream is None:
                selected_stream = progressive_streams.first()

            if selected_stream is None:
                raise Exception("Nenhum stream progressivo com áudio foi encontrado.")
            
            download_folder = 'videos'
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
            
            # Tenta baixar com algumas tentativas em caso de erro SSL intermitente
            attempts = 0
            last_error = None
            while attempts < 3:
                try:
                    selected_stream.download(output_path=download_folder)
                    break
                except ssl.SSLError as e:
                    last_error = e
                    attempts += 1
                    self.log_download_status(f"⚠️ Erro SSL, tentando novamente ({attempts}/3)...")
                    if attempts == 3:
                        raise
                except Exception as e:
                    raise e
            
            self.log_download_status(f"✅ Download concluído em '{download_folder}/'!")
            self.log_download_status("─" * 50)
            
        except Exception as e:
            self.log_download_status(f"❌ Erro: {str(e)}")
            
        finally:
            # Reabilitar botão
            self.download_btn.configure(state="normal", text="⬇️ Baixar Vídeo")
    
    def convert_video(self, video_path):
        """Função que realiza a conversão para MP3"""
        try:
            if not os.path.exists(video_path):
                self.log_convert_status(f"❌ Erro: O arquivo não foi encontrado!")
                return
            
            self.log_convert_status(f"🔄 Convertendo '{os.path.basename(video_path)}'...")
            
            video_clip = VideoFileClip(video_path)
            audio_clip = video_clip.audio
            
            audio_folder = "MP3"
            if not os.path.exists(audio_folder):
                os.makedirs(audio_folder)
            
            mp3_filename = os.path.splitext(os.path.basename(video_path))[0] + '.mp3'
            mp3_filepath = os.path.join(audio_folder, mp3_filename)
            
            audio_clip.write_audiofile(mp3_filepath, logger=None)
            
            # Fechar os clipes para liberar recursos
            audio_clip.close()
            video_clip.close()
            
            self.log_convert_status(f"✅ Conversão concluída!")
            self.log_convert_status(f"📁 Salvo em: {mp3_filepath}")
            self.log_convert_status("─" * 50)
            
        except Exception as e:
            self.log_convert_status(f"❌ Erro durante a conversão: {str(e)}")
            
        finally:
            # Reabilitar botão
            self.convert_btn.configure(state="normal", text="🎵 Converter para MP3")
    
    def start_download(self):
        """Inicia o download em uma thread separada"""
        url = self.url_entry.get().strip()
        
        if not url:
            self.log_download_status("⚠️ Por favor, cole um link do YouTube!")
            return
        
        if "youtube.com" not in url and "youtu.be" not in url:
            self.log_download_status("⚠️ Link inválido! Use um link do YouTube.")
            return
        
        # Desabilitar botão durante download
        self.download_btn.configure(state="disabled", text="⏳ Baixando...")
        
        # Executar download em thread separada para não travar a interface
        download_thread = threading.Thread(target=self.download_video, args=(url,))
        download_thread.daemon = True
        download_thread.start()
    
    def start_convert(self):
        """Inicia a conversão em uma thread separada"""
        video_path = self.file_entry.get().strip()
        
        if not video_path:
            self.log_convert_status("⚠️ Por favor, selecione um arquivo de vídeo!")
            return
        
        # Desabilitar botão durante conversão
        self.convert_btn.configure(state="disabled", text="⏳ Convertendo...")
        
        # Executar conversão em thread separada para não travar a interface
        convert_thread = threading.Thread(target=self.convert_video, args=(video_path,))
        convert_thread.daemon = True
        convert_thread.start()
    
    def run(self):
        """Inicia a aplicação"""
        self.window.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.run()
