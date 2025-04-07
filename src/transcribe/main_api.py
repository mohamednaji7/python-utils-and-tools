from openai import OpenAI
from pydub import AudioSegment



from .utils import make_output_path


import os
import time
from rich.console import Console
from rich.theme import Theme

# Initialize rich console with a custom theme
custom_theme = Theme({
    "info": "cyan",
    "success": "green",
    "error": "red",
    "skip": "yellow",
    "processing": "blue",
    "time": "magenta"
})
console = Console(theme=custom_theme)
client = OpenAI()

# Suppress specific warnings
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)



def convert_file_to_text(model, file_path, file_language, TRANSLATE, TIMESTAMP):
    """
    Transcribe or translate audio to text using Whisper and save the result.
    """
    # Check if file exists
    if not os.path.exists(file_path):
        console.print(f"[ERROR] 🚫 File not found: {file_path}", style="error")
        return

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    file_dir = os.path.dirname(file_path)

    # Perform transcription or translation
    output_path = make_output_path(file_path, TRANSLATE)

    if not TRANSLATE:
        if os.path.isfile(output_path):
            console.print(f"[SKIP] ⏭️ Transcription already exists: {output_path}", style="skip")
            return

        console.print(f"[INFO] 🎙️ Transcribing {file_path}...", style="info")


        mp4_file = AudioSegment.from_file(file_path, "mp4")
        ten_minutes = 10 * 60 * 1000
        result = {"segments": []}
        for i in range(0, len(mp4_file), ten_minutes):
            # PyDub handles time in milliseconds

            audio_10_minutes = mp4_file[:ten_minutes]

            audio_10_minutes.export(f"{file_name}-ten_minutes.mp3", format="mp3")

            audio_file = open(f"{file_name}-ten_minutes.mp3", "rb")

            transcription = client.audio.transcriptions.create(
                # model="gpt-4o-transcribe", 
                model=model,
                file=audio_file, 
                # response_format="text"
            )
            # result = transcription.text
            result['segments'].append({"text": transcription.text})

    else:
        raise ValueError("Translation is not supported in this version.")
        if os.path.isfile(output_path):
            console.print(f"[SKIP] ⏭️ Translation already exists: {output_path}", style="skip")
            return

        console.print(f"[INFO] 🌐 Translating {file_path} from {file_language} to English...", style="info")
        result = model.transcribe(file_path, language=file_language, task='translate')

    with open(output_path, 'w', encoding='utf-8') as f:
        for segment in result['segments']:
            if TIMESTAMP:
                raise ValueError("Timestamp is not supported in this version.")
                start_time = segment['start']
                end_time = segment['end']
                formatted_start = f"{int(start_time // 60):02d}:{int(start_time % 60):02d}"
                formatted_end = f"{int(end_time // 60):02d}:{int(end_time % 60):02d}"
                line = f"[{formatted_start} - {formatted_end}] {segment['text']}\n"
            else:
                line = f"{segment['text']}\n"
            f.write(line)

    if TIMESTAMP:
        console.print(f"[SUCCESS] ✅ Output with timestamps saved to: {output_path}", style="success")
    else:
        console.print(f"[SUCCESS] ✅ Output without timestamps saved to: {output_path}", style="success")

def convert_to_text(videos_json):
    files = videos_json['FILES']
    model_name = videos_json['MODEL']
    
    console.print(f"⬇️ Using model {model_name}", style="info")

    start_time = time.time()

    # Process files sequentially
    for i, file in enumerate(files):
        console.print(f"\n[PROCESSING] 📁 File {i+1}/{len(files)}", style="processing")
        convert_file_to_text(model_name, file['FILE_PATH'], file['FILE_LANGUAGE'], file['TRANSLATE'], file['TIMESTAMP'])

    end_time = time.time()
    elapsed_time = end_time - start_time

    console.print(f"\n🎉 Processing time: {elapsed_time:.2f} seconds", style="time")

    # Write the success log
    with open('success.log', 'a') as f:
        f.write('Date and Time: ' + time.ctime() + '\n')
        f.write(f'All processing completed successfully in {elapsed_time:.2f} seconds\n')