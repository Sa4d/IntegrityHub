import torch
from seamless_communication.models.inference import Translator
import torchaudio
from speechbrain.pretrained import EncoderClassifier
import pandas as pd
import openai
import os
import pandas as pd
import time
openai.api_key = "INSERT YOUR OWN API KEY"

# Initialize a Translator object with a multitask model, vocoder on the GPU.
translator = Translator("seamlessM4T_large", vocoder_name_or_card="vocoder_36langs", device=torch.device("cuda:0"))
language_id = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")

# Language dict
language_code_to_name = {
    "afr": "Afrikaans",
    "amh": "Amharic",
    "arb": "Modern Standard Arabic",
    "ary": "Moroccan Arabic",
    "arz": "Egyptian Arabic",
    "asm": "Assamese",
    "ast": "Asturian",
    "azj": "North Azerbaijani",
    "bel": "Belarusian",
    "ben": "Bengali",
    "bos": "Bosnian",
    "bul": "Bulgarian",
    "cat": "Catalan",
    "ceb": "Cebuano",
    "ces": "Czech",
    "ckb": "Central Kurdish",
    "cmn": "Mandarin Chinese",
    "cym": "Welsh",
    "dan": "Danish",
    "deu": "German",
    "ell": "Greek",
    "eng": "English",
    "est": "Estonian",
    "eus": "Basque",
    "fin": "Finnish",
    "fra": "French",
    "gaz": "West Central Oromo",
    "gle": "Irish",
    "glg": "Galician",
    "guj": "Gujarati",
    "heb": "Hebrew",
    "hin": "Hindi",
    "hrv": "Croatian",
    "hun": "Hungarian",
    "hye": "Armenian",
    "ibo": "Igbo",
    "ind": "Indonesian",
    "isl": "Icelandic",
    "ita": "Italian",
    "jav": "Javanese",
    "jpn": "Japanese",
    "kam": "Kamba",
    "kan": "Kannada",
    "kat": "Georgian",
    "kaz": "Kazakh",
    "kea": "Kabuverdianu",
    "khk": "Halh Mongolian",
    "khm": "Khmer",
    "kir": "Kyrgyz",
    "kor": "Korean",
    "lao": "Lao",
    "lit": "Lithuanian",
    "ltz": "Luxembourgish",
    "lug": "Ganda",
    "luo": "Luo",
    "lvs": "Standard Latvian",
    "mai": "Maithili",
    "mal": "Malayalam",
    "mar": "Marathi",
    "mkd": "Macedonian",
    "mlt": "Maltese",
    "mni": "Meitei",
    "mya": "Burmese",
    "nld": "Dutch",
    "nno": "Norwegian Nynorsk",
    "nob": "Norwegian Bokm\u00e5l",
    "npi": "Nepali",
    "nya": "Nyanja",
    "oci": "Occitan",
    "ory": "Odia",
    "pan": "Punjabi",
    "pbt": "Southern Pashto",
    "pes": "Western Persian",
    "pol": "Polish",
    "por": "Portuguese",
    "ron": "Romanian",
    "rus": "Russian",
    "slk": "Slovak",
    "slv": "Slovenian",
    "sna": "Shona",
    "snd": "Sindhi",
    "som": "Somali",
    "spa": "Spanish",
    "srp": "Serbian",
    "swe": "Swedish",
    "swh": "Swahili",
    "tam": "Tamil",
    "tel": "Telugu",
    "tgk": "Tajik",
    "tgl": "Tagalog",
    "tha": "Thai",
    "tur": "Turkish",
    "ukr": "Ukrainian",
    "urd": "Urdu",
    "uzn": "Northern Uzbek",
    "vie": "Vietnamese",
    "xho": "Xhosa",
    "yor": "Yoruba",
    "yue": "Cantonese",
    "zlm": "Colloquial Malay",
    "zsm": "Standard Malay",
    "zul": "Zulu",
}

reversed_dict = {value: key for key, value in language_code_to_name.items()}
df = pd.DataFrame(columns=['Edited_transcripts', 'raw_transcript'])



def input_audio(audio_path):
    ## Function to detect language
    # Download Thai language sample from Omniglot and cvert to suitable form
    signal = language_id.load_audio(audio_path)
    prediction =  language_id.classify_batch(signal)
    # The identified language ISO code is given in prediction[3]
    lang = prediction[3][0].split(': ')[1]
    #  ['th: Thai']
    corresponding_key = reversed_dict.get(lang, None)
    #print(corresponding_key, ":",lang)


    ## Function to generate text from audio and translate to english
    # Resample audio
    resample_rate = 44100
    waveform, sample_rate = torchaudio.load(audio_path)
    resampler = torchaudio.transforms.Resample(sample_rate, resample_rate, dtype=waveform.dtype)
    resampled_waveform = resampler(waveform)
    torchaudio.save(audio_path, resampled_waveform, resample_rate)

    translated_text, _, _ = translator.predict(audio_path, "s2tt", 'eng')
    return translated_text


text = input_audio('/home/sraozuq/learning_exp/Qatar/telegram_audio.wav')
print(text)


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=0,
    )

    return response.choices[0].message["content"]
prompt = f"I will give a text of a person who reported a crime, and I want you to delete any private information about the person, like if he or she mentioned their own name or age or gender or job name and so on, please remove them and keep the report same as it is, and only return the report with removed info, if there is not any, just return the same report, this is the report {text}"

response = get_completion(prompt)

print(response)


# Create a new row in the DataFrame for the response
new_row = {'Edited_transcripts': response, 'raw_transcript': text}

df = df.append(new_row,  ignore_index=True)


from sqlalchemy import create_engine, String
# Define the connection parameters
server = 'processed.database.windows.net'
database = 'processed_data'
uid = 'processed_data'
pwd = 'Saad1234.'

# Construct the SQLAlchemy connection string
connection_string = (
    f"mssql+pymssql://{uid}:{pwd}@{server}/{database}"
)
engine = create_engine(connection_string)


# Cast the DataFrame columns to str
df = df.astype(str)

# Specify the data types when writing to SQL (no dtype_mapping needed)## to be inserted to the 
df.to_sql('YourTableName', engine, if_exists='append', index=False)