# Image Captioning Overview

- Image captioning automatically generates textual descriptions of images by combining computer vision and natural language processing (NLP).
- It helps classify and describe images quickly and accurately, such as organizing vacation photos by year and destination.

## Image Captioning Process

- Input processing involves receiving the image and optional text prompt, then normalizing and resizing the image for the model.
- Image validation and encoding check the image's suitability and convert it into a base64 encoded string for processing.
- Multimodal LLM processing fuses visual features extracted from the image with text embeddings to generate a descriptive caption.

## Implementation with Meta’s Llama 4 Maverick

- The model uses 90 billion parameters designed for visual reasoning, accessed via IBM WatsonX API.
- Images are encoded to a text-based format, combined with text prompts, and sent to the model.
- The model processes both image and text inputs using attention mechanisms to produce relevant captions describing the images.