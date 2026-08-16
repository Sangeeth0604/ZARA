import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

engine.say("Hello Sai Sangeeth. This is NOVA voice test.")
engine.runAndWait()