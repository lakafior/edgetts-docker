# edgetts-docker
Docker container for automated TTS process using Edge TTS based on edge-tts project: https://github.com/rany2/edge-tts

It's:
1. watching for new files (pdf,md or epub) in input_folder
2. automatically process them into mp3 audio to output_folder
3. deletes input files
4. voice and folders can be adjusted in docker-compose.yml

## How to run
1. Copy this repo:
```
git clone https://github.com/lakafior/edgetts-docker.git
```
2. Move inside directory:
```
cd edgetts-docker
```
3. Create folders for input and output (this is optional, you can point to whatever folders you want in docker-compose.yml)
```
mkdir input_folder && mkdir output_folder
```
4. Edit docker-compose.yml VOICE env (and folders path if needed)

> Voices can be found in voices.txt file

5. Build Docker container using docker-compose:
```
docker-compose up -d
```

## How to use
1. Place a text file into input folder

> Script can handle files with pdf, md and epub extension

2. Wait for log of completed task

![obraz](https://github.com/user-attachments/assets/f7aa17a1-a8b9-4bc7-9d82-9b1e8a4b8876)

