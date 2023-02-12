import ffmpeg

def convert_to_webm(input_file, output_file):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, vcodec='vp9', crf=20, preset='medium')
        .run()
    )

def convert_to_hevc(input_file, output_file):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, vcodec='libx265', crf=20, preset='medium')
        .run()
    )

def convert_to_h264(input_file, output_file):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, vcodec='h264', crf=20, preset='medium')
        .run()
    )


def convert_to_vp9(input_file, output_file):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, vcodec='vp9', crf=20, preset='medium')
        .run()
    )