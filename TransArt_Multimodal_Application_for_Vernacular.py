import streamlit as st
from transformers import pipeline
import openai
from PIL import Image
from io import BytesIO
import requests

# Constants
translation_model_name = "Helsinki-NLP/opus-mt-ta-en"
text_to_image_model_name = "CompVis/stable-diffusion-v1-4"
text_generation_model_name = "gpt-3"  # Replace with the appropriate model if needed
openai.api_key = 'your_openai_api_key'  # Replace with your actual API key

# Initialize Pipelines
translator = pipeline("translation", model=translation_model_name)

def translate_text(tamil_text):
    """Translates Tamil text to English."""
    translation = translator(tamil_text)[0]['translation_text']
    return translation

def generate_text(english_text):
    """Generates creative text based on the translated English text."""
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=english_text,
        max_tokens=50
    )
    generated_text = response.choices[0].text.strip()
    return generated_text

def generate_image(prompt):
    """Generates an image based on the given prompt using the OpenAI API."""
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "512x512"
    }
    image_response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
    image_url = image_response.json()["data"][0]["url"]
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    return image

def main():
    """Main function to run the Streamlit app."""
    st.title("TransArt: Tamil to English Translation and Image Synthesis")

    # User Input
    tamil_text = st.text_area("Enter Tamil text for translation and image generation:")

    if st.button("Translate and Generate"):
        if tamil_text:
            # Translate text
            translation = translate_text(tamil_text)
            st.write("Translated Text (English):", translation)

            # Generate creative text
            generated_text = generate_text(translation)
            st.write("Generated Creative Text:", generated_text)

            # Generate image
            image = generate_image(translation)
            st.image(image, caption="Generated Image")
        else:
            st.error("Please enter Tamil text for translation and image generation.")

if __name__ == "__main__":
    main()