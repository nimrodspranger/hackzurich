import os
import glob
import speech_recognition as sr

def get_latest_audio_file(folder_path):
    list_of_files = glob.glob(os.path.join(folder_path, "*.mp3"))  # Use "*.wav" if your files are not in mp3 format
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def transcribe_audio(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

def structure_text_for_algo(text):
    # Add your logic to structure the text here
    # For now, let's assume you simply split the sentences
    structured_text = text.split('. ')
    return structured_text

def save_text_to_file(text, output_file):
    with open(output_file, 'w') as f:
        for line in text:
            f.write(f"{line}\n")

if __name__ == "__main__":
    folder_path = "audio_files"
    latest_audio_file = get_latest_audio_file(folder_path)

    if latest_audio_file:
        print(f"Processing latest audio file: {latest_audio_file}")

        transcript = transcribe_audio(latest_audio_file)
        print(f"Original transcript: {transcript}")

        structured_text = structure_text_for_algo(transcript)
        print(f"Structured text: {structured_text}")

        # Generate the text file name based on the audio file name
        txt_file_name = os.path.splitext(os.path.basename(latest_audio_file))[0] + ".txt"
        txt_file_path = os.path.join(folder_path, txt_file_name)

        # Save the structured text to a file
        save_text_to_file(structured_text, txt_file_path)
        print(f"Saved structured text to {txt_file_path}")

    else:
        print("No audio files found.")
