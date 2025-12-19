import customtkinter as ctk
from pytubefix import YouTube
import os
import threading

class YouTubeDownloaderApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("YouTube Downloader")
        self.window.geometry("600x400")
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.window, 
            text="📥 YouTube Downloader",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)
        
        # Frame para entrada de URL
        self.url_frame = ctk.CTkFrame(self.window)
        self.url_frame.pack(pady=10, padx=40, fill="x")
        
        self.url_label = ctk.CTkLabel(
            self.url_frame, 
            text="Cole o link do vídeo:",
            font=ctk.CTkFont(size=14)
        )
        self.url_label.pack(pady=(10, 5))
        
        self.url_entry = ctk.CTkEntry(
            self.url_frame,
            placeholder_text="https://www.youtube.com/watch?v=...",
            width=500,
            height=40
        )
        self.url_entry.pack(pady=(0, 10), padx=10)
        
        # Botão de download
        self.download_btn = ctk.CTkButton(
            self.window,
            text="⬇️ Baixar Vídeo",
            command=self.start_download,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=200
        )
        self.download_btn.pack(pady=20)
        
        # Área de status
        self.status_frame = ctk.CTkFrame(self.window)
        self.status_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        self.status_text = ctk.CTkTextbox(
            self.status_frame,
            font=ctk.CTkFont(size=12),
            height=150
        )
        self.status_text.pack(pady=10, padx=10, fill="both", expand=True)
        self.status_text.configure(state="disabled")
        
    def log_status(self, message):
        """Adiciona mensagem ao log de status"""
        self.status_text.configure(state="normal")
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")
        self.status_text.configure(state="disabled")
        
    def download_video(self, url):
        """Função que realiza o download do vídeo"""
        try:
            self.log_status("🔍 Buscando informações do vídeo...")
            
            yt = YouTube(url)
            
            self.log_status(f"📹 Título: {yt.title}")
            self.log_status(f"👁️ Visualizações: {yt.views:,}")
            
            self.log_status("⏳ Iniciando download...")
            
            yd = yt.streams.get_highest_resolution()
            
            download_folder = 'videos'
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
            
            yd.download(output_path=download_folder)
            
            self.log_status(f"✅ Download concluído em '{download_folder}/'!")
            self.log_status("─" * 50)
            
        except Exception as e:
            self.log_status(f"❌ Erro: {str(e)}")
            
        finally:
            # Reabilitar botão
            self.download_btn.configure(state="normal", text="⬇️ Baixar Vídeo")
    
    def start_download(self):
        """Inicia o download em uma thread separada"""
        url = self.url_entry.get().strip()
        
        if not url:
            self.log_status("⚠️ Por favor, cole um link do YouTube!")
            return
        
        if "youtube.com" not in url and "youtu.be" not in url:
            self.log_status("⚠️ Link inválido! Use um link do YouTube.")
            return
        
        # Desabilitar botão durante download
        self.download_btn.configure(state="disabled", text="⏳ Baixando...")
        
        # Executar download em thread separada para não travar a interface
        download_thread = threading.Thread(target=self.download_video, args=(url,))
        download_thread.daemon = True
        download_thread.start()
    
    def run(self):
        """Inicia a aplicação"""
        self.window.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.run()
