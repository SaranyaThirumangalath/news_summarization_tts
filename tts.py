from gtts import gTTS    # Import the gTTS module, which converts text to speech.
from io import BytesIO   # Import BytesIO to work with in-memory binary streams.

def text_to_speech_hindi(text):
    """
    Converts the provided text to Hindi speech using gTTS and returns a BytesIO object.
    
    Parameters:
        text (str): The text to convert into speech.
        
    Returns:
        BytesIO: An in-memory binary stream containing the MP3 audio data.
    """
    # Create a gTTS object with the text and specify the language as Hindi ('hi').
    tts = gTTS(text=text, lang='hi')
    
    # Create a BytesIO object to hold the generated MP3 data in memory.
    mp3_fp = BytesIO()
    
    # Write the generated speech (in MP3 format) to the BytesIO object.
    tts.write_to_fp(mp3_fp)
    
    # Reset the file pointer to the beginning of the BytesIO object.
    # This is necessary so that when we later read from it, we start from the beginning.
    mp3_fp.seek(0)
    
    # Return the BytesIO object containing the MP3 audio.
    return mp3_fp
