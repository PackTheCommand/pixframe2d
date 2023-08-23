import subprocess

def convert_wav_to_ogg(input_path, output_path):
    command = ["ffmpeg", "-i", input_path, "-c:a", "libvorbis", "-q:a", "4", output_path]
    subprocess.run(command)

def main():
    input_wav_file = r"C:\Users\ctind\PycharmProjects\Experimental\mygame\sounds\415804__sunsai__mushroom-background-music.ogg"  # Replace with the path to your input WAV file
    output_ogg_file = "mushroom-background-music.ogg"  # Replace with the desired output OGG file name

    convert_wav_to_ogg(input_wav_file, output_ogg_file)
    print("Conversion complete.")

if __name__ == "__main__":
    main()