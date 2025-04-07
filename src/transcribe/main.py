import torch 
import whisper
import os
import time 


# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)




def convert_file_to_text(model, file_path, file_language, TRANSLATE, TIMESTAMP):
    """
    Transcribe or translate audio to text using Whisper and save the result.
    """
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    file_dir = os.path.dirname(file_path)  # Get the directory where the file exists

    # Perform transcription or translation
    if not TRANSLATE:
        output_path = os.path.join(file_dir, f"{file_name}_transcription.txt")
        if os.path.isfile(output_path):
            print(f"[SKIP] Transcription already exists: {output_path}")
            return  # Skip transcription if the file already exists

        print(f"[INFO] Transcribing {file_path}...")
        result = model.transcribe(file_path, language=file_language)
    else:
        output_path = os.path.join(file_dir, f"{file_name}_translation.txt")
        if os.path.isfile(output_path):
            print(f"[SKIP] Translation already exists: {output_path}")
            return  # Skip translation if the file already exists

        print(f"[INFO] Translating {file_path} from {file_language} to English...")
        result = model.transcribe(file_path, language=file_language, task='translate')

    with open(output_path, 'w', encoding='utf-8') as f:
        for segment in result['segments']:
            if TIMESTAMP:
                start_time = segment['start']
                end_time = segment['end']
                formatted_start = f"{int(start_time // 60):02d}:{int(start_time % 60):02d}"
                formatted_end = f"{int(end_time // 60):02d}:{int(end_time % 60):02d}"
                line = f"[{formatted_start} - {formatted_end}] {segment['text']}\n"
            else:
                line = f"{segment['text']}\n"

            f.write(line)

    if TIMESTAMP:
        print(f"[SUCCESS] Output with timestamps saved to: {output_path}")
    else:
        print(f"[SUCCESS] Output without timestamps saved to: {output_path}")




def convert_to_text(videos_json):

    files = videos_json['FILES']
    model_name = videos_json['MODEL']
    gpu = videos_json['GPU']
    
    device = "cuda" if gpu and torch.cuda.is_available() else "cpu"
    print(f'Downloading model {model_name} to {device}')
    model = whisper.load_model(model_name, download_root="models").to(device)
    print(f"Loaded model to {device}")

    start_time = time.time()  # Record the start time

    # Process files sequentially
    for i, file in enumerate(files):
        print(f"\n[PROCESSING] File {i+1}/{len(files)}")
        convert_file_to_text(model, file['FILE_PATH'], file['FILE_LANGUAGE'], file['TRANSLATE'], file['TIMESTAMP'])

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    print(f"\n✅ Processing time: {elapsed_time:.2f} seconds")

    # Write the success log
    with open('success.log', 'a') as f:
        f.write('Date and Time: ' + time.ctime() + '\n')
        f.write(f'All processing completed successfully in {elapsed_time:.2f} seconds\n')