from mutagen.mp4 import MP4


def file_properties(file_path):
    file_tags = MP4(file_path)
    print(file_tags.info)


file_properties("C:\\git\\WaaS_Alert\\hola.txt")