import os
from pydub import AudioSegment

phoneme_mapping = {
    " ": "space.wav",
    "ހަން": "ހަން.wav",
    "ހު": "ހު.wav",
    "ހުން": "ހުން.wav",
    "ށެ": "ށެ.wav",
    "ނަ": "ނަ.wav",
    "ނީ": "ނީ.wav",
    "ރި": "ރި.wav",
    "ރު": "ރު.wav",
    "ބާ": "ބާ.wav",
    "ބޮ": "ބޮ.wav",
    "ޅު": "ޅު.wav",
    "ކު": "ކު.wav",
    "ކެ": "ކެ.wav",
    "އޮ": "އޮ.wav",
    "ވާ": "ވާ.wav",
    "ވެ": "ވެ.wav",
    "މޮ": "މޮ.wav",
    "ފީ": "ފީ.wav",
    "ދާ": "ދާ.wav",
    "ތަ": "ތަ.wav",
    "ތީ": "ތީ.wav",
    "ލް": "ލް.wav",
    "ގެ": "ގެ.wav",
    "ގައި": "ގައި.wav",
    "ޏާ": "ޏާ.wav",
    "ސި": "ސި.wav",
    "ޑު": "ޑު.wav",
    "ޒާ": "ޒާ.wav",
    "ޓް": "ޓް.wav",
    "ޔަ": "ޔަ.wav",
    "ޕޯސް": "ޕޯސް.wav",
    "ޖަ": "ޖަ.wav",
}

def collect_sound_pieces(phonemes_dir, sentence):
    sound_pieces = []
    i = 0
    while i < len(sentence):
        found = False
        for phoneme_length in range(5, 0, -1):
            phoneme_candidate = sentence[i:i + phoneme_length]
            phoneme_filename = phoneme_mapping.get(phoneme_candidate)
            if phoneme_filename:
                phoneme_path = os.path.join(phonemes_dir, phoneme_filename)
                if os.path.exists(phoneme_path):
                    sound_piece = AudioSegment.from_wav(phoneme_path)
                    sound_pieces.append(sound_piece)
                    i += phoneme_length
                    found = True
                    break
        if not found:
            print(f"Phoneme not found for: {sentence[i]}")
            i += 1 
    return sound_pieces

def generate_sentence_with_dynamic_overlap(sound_pieces):
    if not sound_pieces:
        return AudioSegment.silent(duration=0)

    # Initialize the final sentence with the first sound piece
    sentence = sound_pieces[0]

    # Iterate over the remaining sound pieces
    for i in range(1, len(sound_pieces)):
        # Calculate the maximum overlap duration based on the durations of the two phonemes
        previous_duration = len(sentence)
        current_duration = len(sound_pieces[i])
        max_overlap_duration = min(previous_duration, current_duration) - 247 # Adjust this as needed
        max_overlap_duration = max(max_overlap_duration, 0)  # Ensure overlap duration is not negative

        # Apply crossfade with the calculated overlap duration
        sentence = sentence.append(sound_pieces[i], crossfade=max_overlap_duration)

    return sentence

def save_sentence(sentence, output_file):
    sentence.export(output_file, format="wav")

def main():
    phonemes_dir = "C:/Python/dhivehi-phoneme-based-tts/phonemes"
    output_file = "C:/Python/dhivehi-phoneme-based-tts/generated_sentence.wav" 

    # Input Dhivehi sentence
    input_sentence = "ބޮޑު ބާޒާރުގައި ހުންނަ މޮޅު ތަކެތީގައި ސިލްޖަހަންޏާ ޕޯސްޓް އޮފީހުގެ ވެރިޔަކު ވާނީ ދާށެވެ"

    sound_pieces = collect_sound_pieces(phonemes_dir, input_sentence)
    if not sound_pieces:
        print("No sound pieces found for the input sentence.")
        return

    sentence = generate_sentence_with_dynamic_overlap(sound_pieces)
    save_sentence(sentence, output_file)
    print(f"Sentence saved to {output_file}")

if __name__ == "__main__":
    main()