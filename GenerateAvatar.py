import PySimpleGUI as sg
import simpleaudio as sa

# Load the game music
wave_obj = sa.WaveObject.from_wave_file('game_music.wav')  # Replace 'game_music.wav' with the path to your game music file
play_obj = None  # Variable to hold the playback object

# Function to play or stop the game music
def toggle_music():
    global play_obj
    if play_obj and play_obj.is_playing():
        play_obj.stop()
        play_obj = None
    else:
        play_obj = wave_obj.play()

# Set theme
sg.theme('DarkBlue')

# Function to create and display the main window
def create_main_window():
    layout = [
        [sg.Text("Welcome to Avatar Generator", size=(30, 1), justification='center', font=("Helvetica", 20))],
        [sg.Button("START"), sg.Button("ABOUT"), sg.Button("OPTIONS"), sg.Button("EXIT")]
    ]
    window = sg.Window("Avatar Generator", layout, margins=(100, 50))
    return window

# Function to create and display the start page
def create_start_page():
    # Placeholder layout for start page
    layout = [
        [sg.Text("This is the START page")],
        # Add your questions and input fields here
        [sg.Button("Back"), sg.Button("Next")]
    ]
    window = sg.Window("Start Page", layout)
    return window

# Function to create and display the about page
def create_about_page():
    # Placeholder layout for about page
    layout = [
        [sg.Text("This is the ABOUT page")],
        # Add about information here
        [sg.Button("Back")]
    ]
    window = sg.Window("About Page", layout)
    return window

# Function to create and display the options page
def create_options_page():
    layout = [
        [sg.Text("Options", font=("Helvetica", 20))],
        [sg.Text("Audio Volume:")],
        [sg.Slider(range=(0, 100), orientation='h', size=(50, 20), default_value=50, tick_interval=10, key='-VOLUME_SLIDER-')],
        [sg.Button("Back")],
        [sg.Button("Toggle Music")]
    ]
    window = sg.Window("Options", layout)
    return window

def main():
    main_window = create_main_window()

    while True:
        event, _ = main_window.read()

        if event == sg.WINDOW_CLOSED or event == 'EXIT':
            if play_obj:
                play_obj.stop()  # Stop the music when exiting the application
            break
        elif event == 'START':
            main_window.hide()
            start_page = create_start_page()
            while True:
                event, _ = start_page.read()
                if event == sg.WINDOW_CLOSED or event == 'Back':
                    start_page.close()
                    main_window.un_hide()
                    break
                # Add logic for processing start page inputs and navigating further
        elif event == 'ABOUT':
            main_window.hide()
            about_page = create_about_page()
            while True:
                event, _ = about_page.read()
                if event == sg.WINDOW_CLOSED or event == 'Back':
                    about_page.close()
                    main_window.un_hide()
                    break
                # Add logic for about page interactions
        elif event == 'OPTIONS':
            main_window.hide()
            options_page = create_options_page()
            while True:
                event, values = options_page.read()
                if event == sg.WINDOW_CLOSED or event == 'Back':
                    options_page.close()
                    main_window.un_hide()
                    break
                elif event == '-VOLUME_SLIDER-':
                    volume = values['-VOLUME_SLIDER-']
                    # Adjust volume here (simpleaudio doesn't provide volume control)
                elif event == 'Toggle Music':
                    toggle_music()

    main_window.close()

if __name__ == "__main__":
    main()
