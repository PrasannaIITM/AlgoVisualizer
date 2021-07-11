set s1=Quick

ffmpeg -y -r 60 -i "frames/%s1%_frame%%05d.png" -i "%s1%_sound.wav" -filter_complex "[0]scale=w=1440:-1:flags=lanczos[a]" -c:v libx264 -pix_fmt yuv420p -preset veryslow -tune animation -c:a aac -crf 0 -map "[a]":v -map 1:a "%s1%_sort.mp4"
ffmpeg -y -r 60 -i Quick_frame%05d.png -c:v libx264 -preset veryslow -crf 0 "QuickSort.mp4"
