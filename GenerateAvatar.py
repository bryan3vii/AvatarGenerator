import PySimpleGUI as sg
import random
import simpleaudio as sa
import statistics
import webbrowser
from openai import OpenAI
client = OpenAI(api_key="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") # this might not work with everyone

# Load the game music
wave_obj = sa.WaveObject.from_wave_file('game_music.wav')  # music file
play_obj = None  # Variable to hold the playback object

# print(sg.theme_list()) In case you want to change the theme
sg.theme('DarkBlue') 

# Function to play or stop the game music
def toggle_music():
    global play_obj
    if play_obj and play_obj.is_playing():
        play_obj.stop()
        play_obj = None
    else:
        play_obj = wave_obj.play()

# Function to prompt user for answers to questions and calculate archetype
def calculate_archetype(question_file):
    archetypes = {
        "The Hero": 0, "The Caregiver": 0, "The Lover": 0, "The Mentor": 0,
        "The Rebel": 0, "The Jester": 0, "Explorer": 0, "The Innocent": 0,
        "The Magician": 0, "The Everyman": 0, "The Ruler": 0, "Villain": 0,
        "Trickster": 0, "Warrior": 0, "BOSS": 0, "Guardian": 0,
        "Sidekick": 0, "The Herald": 0, "The Seducer": 0, "Antagonist": 0,
        "Artist": 0, "Clown": 0, "Outlaw": 0, "Protagonist": 0
    }
    with open(question_file, 'r') as file:
        questions = file.readlines()
    random.shuffle(questions)
    questions = questions[:15]  # Select a random subset of 15 questions

    toggle_music()  # Start playing the music

    for line in questions:
        parts = line.strip().split('|')
        if len(parts) < 2:  # Check if the line is properly formatted
            continue  # Skip lines that are not properly formatted
        question, traits = parts
        traits = traits.split(',')
        layout = [
            [sg.Text(question, size=(50, 3), font=("Helvetica", 16))],
            [sg.Button("Yes", size=(10, 2)), sg.Button("No", size=(10, 2)), sg.Button("Quit", size=(10, 2))]
        ]
        window = sg.Window("Question", layout, modal=True)
        event, _ = window.read()
        window.close()

        if event == "Yes":
            for trait in traits:
                if trait in archetypes:
                    archetypes[trait] += 1
        elif event == "Quit":
            confirm_layout = [
                [sg.Text("Are you sure you want to quit?", size=(30, 2), font=("Helvetica", 16))],
                [sg.Button("Yes", size=(10, 2)), sg.Button("No", size=(10, 2))]
            ]
            confirm_window = sg.Window("Confirm Quit", confirm_layout, modal=True)
            confirm_event, _ = confirm_window.read()
            confirm_window.close()

            if confirm_event == "Yes":
                toggle_music()  # Stop playing the music
                return None  # Return None to indicate the quiz was quit

    toggle_music()  # Stop playing the music
    # Determine dominant archetype based on highest score
    dominant_archetype = max(archetypes, key=archetypes.get)
    return dominant_archetype


# Function to create and display the main window
def create_main_window():
    # Styling buttons and text
    button_size = (10, 1)
    button_font = ("Helvetica", 16)
    text_font = ("Helvetica", 20)
    layout = [
        [sg.Text("Welcome to Avatar Generator", size=(30, 1), justification='center', font=("Helvetica", 24))],
        [sg.Button("START", size=button_size, font=button_font, button_color=('white', 'blue')), 
         sg.Button("ABOUT", size=button_size, font=button_font, button_color=('white', 'blue')), 
         sg.Button("OPTIONS", size=button_size, font=button_font, button_color=('white', 'blue')), 
         sg.Button("EXIT", size=button_size, font=button_font, button_color=('white', 'red'))]
    ]
    window = sg.Window("Avatar Generator", layout, margins=(200, 100))
    return window

# Function to create and display the start page
def create_start_page(font=("Helvetica", 16)):
    layout = [
        [sg.Text("Click 'Next' to begin the questionnaire.", font=font)],
        [sg.Button("Back", font=font), sg.Button("Next", font=font)]
    ]
    window = sg.Window("Start Page", layout)
    return window

# Function to create and display the about page
def create_about_page(font=("Helvetica", 16)):
    layout = [
        [sg.Text("About Avatar Generator", font=("Helvetica", 20))],
        [sg.Text("Version 1.0")],
        [sg.Text("Description:", font=font)],
        [sg.Text("Avatar Generator is a Python application designed to create custom avatars based on user input. It offers a range of customization options and allows users to create unique characters for various purposes.", font=font)],
        [sg.Text("Credits:", font=font)],
        [sg.Text("This application uses PySimpleGUI for the graphical user interface.", font=font)],
        [sg.Text("Contact Information:", font=font)],
        [sg.Text("For support or feedback, please contact us through canvas.", font=font)],
        [sg.Button("Back", font=font)]
    ]
    window = sg.Window("About Avatar Generator", layout)
    return window

# Function to create and display the options page
def create_options_page(font=("Helvetica", 16)):
    layout = [
        [sg.Text("Options", font=("Helvetica", 20))],
        [sg.Text("Audio Volume:", font=font)],
        [sg.Slider(range=(0, 100), orientation='h', size=(50, 20), default_value=50, tick_interval=10, key='-VOLUME_SLIDER-', font=font)],
        [sg.Button("Toggle Music", font=font)],
        [sg.Button("Apply Volume Changes", font=font), sg.Button("Back", font=font)]
    ]
    window = sg.Window("Options", layout)
    return window

# Main
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
                elif event == 'Next':
                    archetype = calculate_archetype('questions.txt')  # Pass the file containing questions
                    if archetype:
                        response = client.images.generate(
                                    model="dall-e-3",
                                    prompt=archetype,
                                    size="1024x1024",
                                    quality="standard",
                                    n=1,
                                )
                        image_url = response.data[0].url
                        sg.popup("Your character archetype is:", archetype)
                        webbrowser.open(image_url)
        elif event == 'ABOUT':
            main_window.hide()
            about_page = create_about_page()
            while True:
                event, _ = about_page.read()
                if event == sg.WINDOW_CLOSED or event == 'Back':
                    about_page.close()
                    main_window.un_hide()
                    break
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
                elif event == 'Apply Volume Changes':
                    volume = values['-VOLUME_SLIDER-']
                    sg.popup("Volume changes applied successfully!")
    main_window.close()


if __name__ == "__main__":
    main()
