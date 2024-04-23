from utils import send_confirmation, receive_data, transfer_data, string2bytes
import socket
import json
import os
from STT import STT
from ChatGPT_Request import query_chatgpt
from FetchWeather import fetch_weather_data
from TTS import TTS
from WordTagger import getTag
import time
## >> PARAMETERS
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 1277
stt_token = "btRkfZr5Ndy2tkpnRfZ3b9ER9ndEC6rxYEg5Vu8XCCuK85KRDKw9cFhcYQ3VdXBQ"
language = "華語"
segment = "False"
stt = STT(token=stt_token, language=language, segment=segment)
weather_token = "CWA-547A664B-85B9-4716-9B09-2C2BD7297F8E"
# 36-hour forecast URL
short_term_url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={weather_token}"
weatherFetchTime=time.perf_counter()
weather_data=fetch_weather_data(short_term_url)
## << PARAMETERS
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.settimeout(2.0)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
def receive_arguments(client_socket : socket.socket) -> dict:
    received_data = b""
    while True:
        temp = client_socket.recv(4096)
        if not temp:
            break
        received_data += temp
        if (received_data[-1:] == b"@"):
            received_data = received_data[:-1]
            break
    return json.loads(string2bytes(received_data.decode("utf-8")).decode("utf-8"))
print("Server running...\n")
try:
    while True:
        elapsedTime = time.perf_counter() - weatherFetchTime
        if elapsedTime >= 10800:
            weather_data=fetch_weather_data(short_term_url)
            elapsedTime=0
        try:
            client_socket, client_address = server_socket.accept()
            print("Incoming connection from {}:{}".format(client_address[0], client_address[1]))
            arguments = receive_arguments(client_socket)
            print("Method: {}\n".format(arguments["method"]))
            send_confirmation(client_socket)
            if (arguments["method"] == "send"):
                dst_path = os.path.join(os.path.dirname(__file__), os.path.basename(arguments["path"]))
                receive_data(client_socket, dst_path)
                client_socket.close()
                continue
            # if not os.path.exists(os.path.dirname(arguments["path"])):
            #     send_confirmation(client_socket, b"$$$")
            #     client_socket.close()
            #     continue 
            # if not os.path.isfile(arguments["path"]):
            #     send_confirmation(client_socket, b"$$$")
            #     client_socket.close()
            #     continue 
            send_confirmation(client_socket)
            audio_path = "recording.wav"
            sentence = stt.request(audio_path=audio_path)
            sentenceTag=getTag(sentence)
            locInfo="我目前在台南\n"
            additionalInfo="請簡單回答\n"
            prompt=additionalInfo
            if sentence!="":
                if "LOC" not in sentenceTag and 'GPE' not in sentenceTag:
                    prompt+=locInfo
                prompt+=sentence+"?\n\n參考資料:\n"
                print("result : "+prompt)
                prompt = f"{prompt}{weather_data}"
                response=query_chatgpt(prompt)
                with open('response.txt', 'w',encoding="utf-8") as file:
                    file.write(response)
                transfer_data(client_socket, arguments["path"])
                TTS(response,"chinese")
            client_socket.close()
        except KeyboardInterrupt:
            raise
        except IOError:
            pass
except KeyboardInterrupt:
    pass
server_socket.close()
print("Server stopped...")