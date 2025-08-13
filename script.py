from indextts.infer import IndexTTS
tts = IndexTTS(model_dir="checkpoints",cfg_path="checkpoints/config.yaml")
voice="test_data/input.wav"
text="For example, when building an approval workflow management backend, in the past, it would take at least several days to write the database modeling, permission system, and interface design by oneself. With NocoBase, the basic system can be completed in half a day, and the remaining time can be focused on optimizing the business logic."
output_path = "output.wav"
tts.infer(voice, text, output_path)