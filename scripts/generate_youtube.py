import openai
import json
import os

# Load OpenAI API Key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_youtube_content(product_title, product_features, affiliate_link):
    # Generate SEO optimized YouTube title
    title_prompt = f"Generate a catchy, SEO optimized YouTube title for a product titled '{product_title}', featuring: {product_features}. Make sure to include keywords for YouTube search."
    title_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=title_prompt,
        max_tokens=60,
        temperature=0.7
    )
    youtube_title = title_response.choices[0].text.strip()

    # Generate SEO optimized YouTube description
    description_prompt = f"Generate an engaging YouTube description for the product '{product_title}'. Make sure to start with the affiliate link: {affiliate_link}. Also, mention key features: {product_features}. Keep it within 250 words."
    description_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=description_prompt,
        max_tokens=200,
        temperature=0.7
    )
    youtube_description = description_response.choices[0].text.strip()

    # Generate voiceover script for the product (5-6 min)
    script_prompt = f"Generate a 5-6 minute voiceover script for a YouTube video about the product '{product_title}', highlighting its features: {product_features}. Make it conversational and informative."
    script_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=script_prompt,
        max_tokens=1200,  # About 5-6 min of voiceover
        temperature=0.7
    )
    voiceover_script = script_response.choices[0].text.strip()

    return youtube_title, youtube_description, voiceover_script

# Example usage
if __name__ == "__main__":
    product_title = "High-End Laptop"
    product_features = "16GB RAM, 512GB SSD, 4K Display, Intel i7 Processor"
    affiliate_link = "https://www.amazon.com/dp/B08P2M9JFF?tag=your_amazon_affiliate_tag"

    title, description, script = generate_youtube_content(product_title, product_features, affiliate_link)
    print("YouTube Title:", title)
    print("YouTube Description:", description)
    print("Voiceover Script:", script)
