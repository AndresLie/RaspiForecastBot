# RaspiForecastBot
## Demo
[Demo Video](https://drive.google.com/file/d/1gRndNQ9E7TrvrBrbEqhiwrrXLRA04zXJ/view?usp=sharing)

### This Project is Tested and Run on Raspberry Pi 3
## Required Equipment
1. Raspberry Pi 3 or Newer
2. Soundcard
3. Motor
4. Microphone
5. Speaker (Connect to Server)
## How to Use
1. Clone this Repository
```
  git clone https://github.com/AndresLie/RaspiForecastBot.git
```
2. Install all the dependencies on requirements.txt
3. For the efficient net fot Hotword detector kindly check the [EfficientWord-Net](https://github.com/Ant-Brain/EfficientWord-Net/tree/main) documentation
   
## In Raspberry Pi
1. Move the server file to your Raspberry Pi and move in to the server directory
   ```
   cd server
   ```
2. Run the main.py file in Raspberry Pi
   ```
   python main.py
   ```


## In Server( Computer)
1. Move to server directory
2. Run server.py
   ```
   python server.py
   ```

After That speak the wakeword "Mobile" and ask for questions(Preferable weather related)


### Process Flow
![Beige Colorful Minimal Flowchart Infographic Graph](https://github.com/AndresLie/RaspiForecastBot/assets/119865728/dc5a7e26-781e-4e78-8e65-fe1b90a35baf=100x10)
