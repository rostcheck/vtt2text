import webvtt
import glob
import os.path
import re

speaker = ""


# Trim repeated tokens at the end of the line
def fix_text(text):
    tokens = text.split(' ')
    if len(tokens) < 2:
        return text
    i_min = -1 * len(tokens)
    i = -2
    end_token = tokens[-1].lower()
    while tokens[i].lower() == end_token and i > i_min:
        i -= 1
    if i == -2:
        return ' '.join(tokens)
    else:
        return ' '.join(tokens[:i + 2])


def convert2text(vtt_text):
    global speaker
    current_speech = ""
    transcript = ""
    for line in vtt_text:
        # set current_speaker to the substring of line.text from the beginning to the first colon
        # if the line.text does not contain a colon, set current_speaker to the line.text itself
        text = fix_text(line.text)
        if ':' in line.text:
            parts = line.text.split(':')
            current_speaker = parts[0]
            if current_speaker == speaker:
                text = parts[1]
            else:
                transcript += "\n" + current_speech
                current_speech = "\n"
                speaker = current_speaker

        current_speech += text

    if current_speech:
        transcript += "\n" + current_speech

    return transcript


def main():
    global speaker
    fileset = [file for file in glob.glob("*.vtt", recursive=False)]
    for vtt_file_name in fileset:
        txt_name = re.sub(r'.vtt$', '.txt', vtt_file_name)
        if not os.path.exists(txt_name):
            speaker = ""
            vtt_text = webvtt.read(vtt_file_name)
            text = convert2text(vtt_text)
            with open(txt_name, 'w') as f:
                f.write(text)
            print(f"Created {txt_name} from {vtt_file_name}")


if __name__ == "__main__":
    main()
