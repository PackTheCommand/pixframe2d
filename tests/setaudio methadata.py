from mutagen import File


def set_metadata(audio_file_path, title=None, artist=None):
    audio = File(audio_file_path, easy=True)


    if audio:
        if title:
            audio["title"] = title
        if artist:
            audio["artist"] = artist
        audio.save()
        print("Metadata updated successfully.")
    else:
        print("Failed to update metadata.")


def main():
    audio_file_path = r"C:\Users\ctind\PycharmProjects\Experimental\mygame\sounds\415804__sunsai__mushroom-background-music.ogg"  # Replace with your audio file path

    new_title = "Mushroom Background Music"
    new_artist = "@Sunsai https://freesound.org"


    set_metadata(audio_file_path, new_title, new_artist)


if __name__ == "__main__":
    main()
