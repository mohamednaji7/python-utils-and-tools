from openai import OpenAI
from openai import AzureOpenAI
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError


from .utils import make_output_path
from .utils import extract_audio

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
openai = OpenAI()
azure_openai = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2025-03-01-preview"
)

# Suppress specific warnings
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)



def convert_file_to_text(client, model, file_path, file_language, TRANSLATE, TIMESTAMP):
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

        tmp_output_mp3 = file_path + ".tmp.mp3"
        try:
            audio_segment = AudioSegment.from_file(file_path, 'mp4')
        except CouldntDecodeError as e:
            console.print(f"[ERROR] 🚫 CouldntDecodeError: ", style="error")
            success = extract_audio(file_path, tmp_output_mp3)
            if not success:
                return
            audio_segment = AudioSegment.from_mp3(tmp_output_mp3)


        ten_minutes = 10 * 60 * 1000
        result = {"segments": []}
        file_audio_segment = f"{file_name}-ten_minutes.mp3"
        for i in range(0, len(audio_segment), ten_minutes):
            # PyDub handles time in milliseconds

            #  subset 10 minutes audio not the first 10 minutes
            audio_10_minutes = audio_segment[i:i + ten_minutes]

            audio_10_minutes.export(file_audio_segment, format="mp3")

            audio_file = open(file_audio_segment, "rb")

            transcription = client.audio.transcriptions.create(
                # model="gpt-4o-transcribe", 
                model=model,
                file=audio_file, 
                # response_format="text"
            )
            # result = transcription.text
            result['segments'].append({"text": transcription.text})

        if os.path.exists(file_audio_segment):
            os.remove(file_audio_segment)

        # delete the tmp_output_mp3
        if os.path.exists(tmp_output_mp3):
            os.remove(tmp_output_mp3)

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

def convert_to_text(videos_json, provider="openai"):
    if provider == 'openai':
        client = openai
    elif provider == 'azure':
        client = azure_openai
    else:
        raise ValueError("Invalid provider. Use 'openai' or 'azure'.")
    
    
    files = videos_json['FILES']
    model_name = videos_json['MODEL']
    
    console.print(f"⬇Using model {model_name}", style="info")

    start_time = time.time()

    # Process files sequentially
    for i, file in enumerate(files):
        console.print(f"\n[PROCESSING] 📁 File {i+1}/{len(files)}", style="processing")
        convert_file_to_text(client, model_name, file['FILE_PATH'], file['FILE_LANGUAGE'], file['TRANSLATE'], file['TIMESTAMP'])

    end_time = time.time()
    elapsed_time = end_time - start_time

    console.print(f"\n🎉 Processing time: {elapsed_time:.2f} seconds", style="time")

    # Write the success log
    with open('success.log', 'a') as f:
        f.write('Date and Time: ' + time.ctime() + '\n')
        f.write(f'All processing completed successfully in {elapsed_time:.2f} seconds\n')