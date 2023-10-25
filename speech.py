from gtts import gTTS
import os
import time

class Speech:
    already_called = set()  # Use a set for faster lookups

    def __init__(self, info):
        self.info = info
        self.names = list(self.info)

    def run(self):
        output_folder = "speech_files"

        for name in self.names:
            if name not in self.already_called:
                text = "Hello " + name
                file_path = os.path.join(output_folder, f"{name}_hello.mp3")

                if not os.path.exists(file_path):
                    tts = gTTS(text)
                    tts.save(file_path)

                # Play the audio file
                os.system(f"mpg123 {file_path}")  # Adjust the player as needed

                # Append name to names already called
                self.already_called.add(name)
                print(f"Already called: {self.already_called}")

            else:
                pass