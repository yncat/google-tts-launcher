# -*- coding: utf-8 -*-
# Google tts launcher
# Copyright (C) 2020 Yukio Nozawa <personal@nyanchangames.com>

from consolemenu import *
from consolemenu.items import *
import glob
import json
import os
import sys
from google.cloud import texttospeech

def is_comment(elem):
    return len(elem)>0 and elem[0] == "#"

def make_name(name, setting_name, line_number):
    if len(name) <= 20:
        return "v_%d_%s_%s" % (line_number, setting_name, name)
    return "v_%d_%s_%s" % (line_number, setting_name,
                           name[0:20] + "(" + str(len(name) - 20) + ")")


def selectSetting():
    jsons = [os.path.basename(elem).split(".")[0]
             for elem in glob.glob("settings/*.json")]
    menu = SelectionMenu(jsons, title="使用する設定", show_exit_option=False)
    menu.show()
    return jsons[menu.selected_option]


if len(sys.argv) == 1:
    print("使い方: python ttslauncher.py filename.txt settingname")
    sys.exit()

key_file_name = "speech_key.json"
if not os.path.exists(key_file_name):
    print("キーファイルが見つかりません。")
    sys.exit()

content_filename = sys.argv[1]
if not os.path.exists(content_filename):
    print("コンテンツファイルが見つかりません。")
    sys.exit()

if len(sys.argv) == 2:
    setting_name = selectSetting()
else:
    if os.path.exists("settings/%s.json" % sys.argv[2]):
        setting_name = sys.argv[2]
    else:
        print("指定された設定ファイルが見つかりません。次の中から選んでください。")
        setting_name = selectSetting()
    # end no setting file
# end

print("設定: %s" % setting_name)

with open("settings/%s.json" % (setting_name), 'r', encoding='UTF-8') as f:
    settings = json.load(f)

if 'protocol_version' not in settings:
    print("この設定は、互換性がないので使えません。")
    sys.exit(0)
# end incompatible

contents = []
with open(content_filename, 'r', encoding='UTF-8') as f:
    for elem in f:
        if not is_comment(elem): contents.append(elem.rstrip())

print("入力ファイル %s" % content_filename)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(key_file_name)

if not os.path.isdir("out"):
    os.mkdir("out")
    print("out directory created.")

client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code=settings['language_code'],
    name=settings['name'],
    # ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    speaking_rate=float(settings['speaking_rate']),
    pitch=float(settings['pitch']),
    volume_gain_db=float(settings['volume_gain_db']),
    effects_profile_id=settings['effects_profile_id']
)

total = len(contents)
processed = 0
skipped = []
line_number = 0

for elem in contents:
    name = make_name(elem, setting_name, line_number)
    line_number += 1
    if os.path.exists("out/%s.wav" % name):
        processed += 1
        skipped.append(name)
        continue

    input_text = texttospeech.SynthesisInput(text=elem)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open("out/%s.wav" % (name), 'wb') as out:
        out.write(response.audio_content)

    processed += 1
    print(
        "\r%d%%(%d/%d)" %
        (processed /
         total *
         100,
         processed,
         total),
        end="")

print("")
if len(skipped) > 0:
    for elem in skipped:
        print("%s は、すでにあったのでスキップしました。" % elem)
    # end for
# end skipped display
print("OK!")
