import torch
from transformers import WhisperProcessor, WhisperModel

# Load processor and full model
processor = WhisperProcessor.from_pretrained("openai/whisper-base")
model = WhisperModel.from_pretrained("openai/whisper-base")

# Prepare dummy audio array (16kHz)
audio_input = torch.randn(16000)

# Extract log-Mel spectrogram features
input_features = processor(audio_input, sampling_rate=16000, return_tensors="pt").input_features

# Run forward pass through the encoder ONLY
with torch.no_grad():
    encoder_outputs = model.encoder(input_features)
    
# ciagla reprezentacja mowy  
latent_representations = encoder_outputs.last_hidden_state
print(latent_representations.shape)
print(latent_representations)
