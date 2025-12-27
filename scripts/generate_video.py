from moviepy.editor import *
from gtts import gTTS

def create_video_from_images_and_voiceover(product_title, voiceover_script, product_images, output_filename="product_video.mp4"):
    # 1. Create a video from the product images (slideshow)
    image_clips = [ImageClip(img, duration=5) for img in product_images]  # 5 seconds per image
    slideshow = concatenate_videoclips(image_clips, method="compose")
    
    # 2. Create the voiceover (use OpenAI's generated script)
    tts = gTTS(voiceover_script, lang='en')
    tts.save("voiceover.mp3")
    
    # Add the voiceover to the video
    audio_clip = AudioFileClip("voiceover.mp3")
    video = slideshow.set_audio(audio_clip)

    # 3. Write video to file
    video.write_videofile(output_filename, codec="libx264", fps=24)

    print(f"Video created successfully: {output_filename}")

# Example usage
if __name__ == "__main__":
    product_images = ["image1.jpg", "image2.jpg", "image3.jpg"]  # Replace with actual image paths
    voiceover_script = "This is a high-end laptop with 16GB of RAM and a powerful Intel i7 processor. It is perfect for gaming, video editing, and productivity tasks."
    
    create_video_from_images_and_voiceover("High-End Laptop", voiceover_script, product_images)
