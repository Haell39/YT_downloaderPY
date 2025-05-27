import os
import argparse
from moviepy.editor import VideoFileClip


def convert_to_mp3():
    parser = argparse.ArgumentParser(description="Converte um arquivo de vídeo para MP3.")
    parser.add_argument("video_path", help="Caminho completo para o arquivo de vídeo a ser convertido.")

    args = parser.parse_args()

    # 'video_path' agora conterá o caminho que o usuário digitou na linha de comando
    video_path = args.video_path

    #Verifica se o arquivo fornecido pelo usuário existe
    if not os.path.exists(video_path):
        print(f'Erro: O arquivo "{video_path}" não foi encontrado.')
        return

    # Definir pasta de destino do áudio:
    audio_folder = "MP3"
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    try:
        print(f'Convertendo "{os.path.basename(video_path)}"...')
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio

        mp3_filename = os.path.splitext(os.path.basename(video_path))[0] + '.mp3'
        mp3_filepath = os.path.join(audio_folder, mp3_filename)

        audio_clip.write_audiofile(mp3_filepath)

        # Fechar os clipes para liberar recursos
        audio_clip.close()
        video_clip.close()

        print(f'Conversão para MP3 concluída em "{mp3_filepath}"!')

    except Exception as e:
        print(f'Erro durante a conversão para MP3: {e}')


if __name__ == "__main__":
    convert_to_mp3()
