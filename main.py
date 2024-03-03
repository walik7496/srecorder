import tkinter as tk
import sounddevice as sd
import soundfile as sf
import threading
import time

class SoundRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sound Recorder")
        self.master.geometry("400x300")  # Set initial width and height of the window

        self.record_button = tk.Button(master, text="Record", command=self.record)
        self.record_button.pack()

        self.pause_button = tk.Button(master, text="Pause", command=self.pause, state=tk.DISABLED)
        self.pause_button.pack()

        self.stop_button = tk.Button(master, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack()

        self.status_label = tk.Label(master, text="Status: Stopped")
        self.status_label.pack()

        self.device_label = tk.Label(master, text="Available Devices:")
        self.device_label.pack()

        self.device_listbox = tk.Listbox(master, width=50)  # Wider listbox
        self.device_listbox.pack()

        self.update_device_list()

        self.stream = None
        self.recording = False
        self.paused = False
        self.frames = []
        self.output_file = None

    def update_device_list(self):
        devices = sd.query_devices()
        self.device_listbox.delete(0, tk.END)  # Clear previous list
        for i, device in enumerate(devices):
            self.device_listbox.insert(tk.END, f"{i + 1}. {device['name']}")

        if len(devices) > 0:
            self.device_listbox.select_set(0)  # Select the first device by default

    def record(self):
        if self.recording:
            return

        device_selection = self.device_listbox.curselection()
        if not device_selection:
            self.status_label.config(text="Status: Please select a device")
            return

        device_index = device_selection[0]
        device_info = sd.query_devices()[device_index]
        print("Default Sample Rate:", device_info['default_samplerate'])
        print("Max Input Channels:", device_info['max_input_channels'])

        self.recording = True
        self.paused = False
        self.status_label.config(text="Status: Recording")
        self.frames = []

        self.output_file = sf.SoundFile('output.wav', mode='w', samplerate=int(device_info['default_samplerate']), channels=device_info['max_input_channels'])

        def callback(indata, frames, time, status):
            if self.paused:
                return

            self.frames.append(indata.copy())
            self.output_file.write(indata.copy())

        self.stream = sd.InputStream(
            device=device_info['name'],
            channels=device_info['max_input_channels'],
            samplerate=device_info['default_samplerate'],
            callback=callback
        )
        self.stream.start()

        # Start a timer
        self.start_time = time.time()
        self.update_timer()

        self.record_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)

    def pause(self):
        if not self.recording:
            return

        self.paused = not self.paused  # Toggle pause state
        if self.paused:
            self.stream.stop()
            self.status_label.config(text="Status: Paused")
        else:
            self.stream.start()
            self.status_label.config(text="Status: Recording")

    def stop(self):
        if not self.recording:
            return

        self.recording = False
        self.stream.stop()
        self.stream.close()
        self.status_label.config(text="Status: Stopped")
        if self.output_file is not None:
            self.output_file.close()

        self.record_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    def update_timer(self):
        if self.recording and not self.paused:
            elapsed_time = time.time() - self.start_time
            self.status_label.config(text=f"Status: Recording - Time Elapsed: {elapsed_time:.2f} seconds")
        self.master.after(100, self.update_timer)

def main():
    root = tk.Tk()
    app = SoundRecorderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
