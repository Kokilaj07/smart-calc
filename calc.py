import streamlit as st
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech."""
    tts_engine = pyttsx3.init()
    tts_engine.say(text)
    tts_engine.runAndWait()
    tts_engine.stop()

def get_audio():
    """Capture audio input from the microphone and convert it to text."""
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            st.write("Could not request results; check your network connection.")
            speak("Could not request results; check your network connection.")
            return ""

def process_expression(expression):
    """Convert spoken words to mathematical operators."""
    expression = expression.lower()
    expression = expression.replace("plus", "+")
    expression = expression.replace("minus", "-")
    expression = expression.replace("times", "*")
    expression = expression.replace("multiplied by", "*")
    expression = expression.replace("divided by", "/")
    expression = expression.replace("over", "/")
    st.write(f"Processed expression: {expression}")  # Debugging statement
    return expression

def calculate(expression):
    """Evaluate the arithmetic expression."""
    try:
        processed_expression = process_expression(expression)
        result = eval(processed_expression)
        return result
    except SyntaxError:
        speak("There is a syntax error in your calculation.")
        st.write("There is a syntax error in your calculation.")  # Debugging statement
        return None
    except Exception as e:
        speak(f"Error: {e}")
        st.write(f"Error: {e}")  # Debugging statement
        return None

def main():
    # Set the background image
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.wallpaperflare.com%2Fturned-on-iphone-4-displaying-calculator-480-on-workbook-mathematics-wallpaper-zdxdn&psig=AOvVaw34XmFJ-2t0yBabH4k7FzOy&ust=1721120413552000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCODv0avXqIcDFQAAAAAdAAAAABAE');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            font-family: 'Arial', sans-serif;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTextInput input {
            padding: 10px;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Voice Calculator")
    st.write("Click the button and say your calculation.")

    if st.button("Start Listening"):
        expression = get_audio()
        if expression:
            result = calculate(expression)
            if result is not None:
                result_text = f"The result is: {result}"
                st.write(result_text)
                speak(result_text)  # Speak the result
            else:
                st.write("Failed to calculate the result.")  # Debugging statement

if __name__ == "__main__":
    main()
