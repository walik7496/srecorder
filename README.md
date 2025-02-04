# Sound Recorder Application

This is a simple sound recording application built using `Tkinter` for the graphical user interface, `sounddevice` for audio recording, and `soundfile` for saving the recorded audio to a `.wav` file. The app allows users to select an available recording device, start, pause, and stop the recording, and view the status of the recording.

## Features
- Select from available audio input devices.
- Start and stop recording with corresponding buttons.
- Pause and resume recording at any time.
- Display the recording status and elapsed time during the recording session.
- Save the recorded audio in `.wav` format.

## Requirements
- Python 3.x
- `Tkinter` (Usually bundled with Python)
- `sounddevice` library (for audio input)
- `soundfile` library (for saving audio to file)

### Installation
To install the required dependencies, run:

```bash
pip install sounddevice soundfile
