# -*- coding: utf-8 -*-
#Google tts launcher
#Copyright (C) 2020 Yukio Nozawa <personal@nyanchangames.com>

import json
import os
import sys
from google.cloud import texttospeech

"""
初回のインストール時には、 pip install -r requirements.txt を実行して、必要なライブラリを入れます。
speech_key.json に、認証情報のJSONを保存して、このプログラムと同じフォルダに置きます。
その後、
python ttslauncher.py ファイル名.txt
とします。
ファイル名.txt には、しゃべらせたい言葉を改行で句切って書いたテキストファイルを指定します。
1行で1ファイルになります。
出力される音声ファイルのファイル名は、行の最初の10文字をとって、適当につけられます。
出力される音声ファイルは、 out フォルダの中に作られます。
設定は、 ttssetting.py を実行して行います。
"""

def make_name(name):
	if len(name)<=20: return name
	return name[0:20]+"("+str(len(name)-20)+")"

if len(sys.argv)==1:
	print("Usage: python ttslauncher.py filename.txt")
	sys.exit()

key_file_name="speech_key.json"
if not os.path.exists(key_file_name):
	print("Key file not found.")
	sys.exit()

content_filename=sys.argv[1]
if not os.path.exists(content_filename):
	print("Content file not found.")
	sys.exit()

SETTINGS_FILE_NAME='settings.json'
if not os.path.exists(SETTINGS_FILE_NAME):
	print("Please run python ttssetting.py before using this script.")
	sys.exit()
#end no settings

with open(SETTINGS_FILE_NAME, 'r', encoding='UTF-8') as f:
	settings=json.load(f)

contents=[]
with open(content_filename,'r',encoding='UTF-8') as f:
	for elem in f:
		contents.append(elem.rstrip())

print("From %s" % content_filename)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(key_file_name)

if not os.path.isdir("out"):
	os.mkdir("out")
	print("out directory created.")

client = texttospeech.TextToSpeechClient()
voice = texttospeech.types.VoiceSelectionParams(
	language_code='ja-JP',
	name='ja-JP-Standard-A',
	ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE
)
audio_config = texttospeech.types.AudioConfig(
	audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16,
	speaking_rate=float(settings['speaking_rate']),
	pitch=float(settings['pitch']),
	volume_gain_db=float(settings['volume_gain_db'])
)

total=len(contents)
processed=0
skipped=0

for elem in contents:
	name=make_name(elem)
	if os.path.exists("out/%s.wav" % name):
		processed+=1
		skipped+=1
		continue

	input_text = texttospeech.types.SynthesisInput(text=elem)
	response = client.synthesize_speech(input_text, voice, audio_config)
	with open("out/%s.wav" % (name), 'wb') as out:
		out.write(response.audio_content)

	processed+=1
	print("\r%d%%(%d/%d)" % (processed/total*100,processed,total), end="")

print("")
ret="OK!" if skipped==0 else "OK! (%d skipped)" % skipped
print(ret)
