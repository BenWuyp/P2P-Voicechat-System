from pydub import AudioSegment
from pydub.playback import play

# Load .wav file
sound = AudioSegment.from_wav("1.wav")

# Shift the pitch up by half an octave (speed will not increase)
octaves = 0.25
new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

# Keep the same samples but tell the computer they ought to be played at the
# new, higher sample rate. This file sounds like a chipmunk but has a weird sample rate.
hipitch_sound = sound._spawn(sound.raw_data, overrides={"frame_rate": new_sample_rate})

# Convert it to a common sample rate (44.1k - standard audio CD) to 
# make sure it works in regular audio players. Other than potentially losing audio quality (if
# you set it too low - 44.1k is plenty) this should now noticeable change how the audio sounds.
hipitch_sound = hipitch_sound.set_frame_rate(44100)

# Export the high pitch sound to a wav file
hipitch_sound.export("high_pitch.wav", format="wav")
