from fetch_amazon import fetch_amazon_products
from generate_youtube import generate_youtube_content
from generate_video import create_video_from_images_and_voiceover
from upload_video import upload_video_to_youtube, authenticate_youtube

def main():
    # Fetch profitable products from Amazon
    products = fetch_amazon_products()

    for product in products:
        title = product.get("ItemInfo", {}).get("Title", {}).get("DisplayValue", "")
        features = product.get("ItemInfo", {}).get("Features", {}).get("DisplayValues", ["N/A"])
        affiliate_link = product.get("DetailPageURL", "")
        images = [img["URL"] for img in product.get("Images", {}).get("Primary", {}).get("Medium", [{}])]

        # Generate YouTube title, description, and voiceover script using OpenAI
        youtube_title, youtube_description, voiceover_script = generate_youtube_content(title, features, affiliate_link)
        
        # Generate video from images and voiceover script
        create_video_from_images_and_voiceover(youtube_title, voiceover_script, images)
        
        # Authenticate YouTube and upload the video
        youtube = authenticate_youtube()
        upload_video_to_youtube(youtube, "product_video.mp4", youtube_title, youtube_description, ["electronics", "tech"])

if __name__ == "__main__":
    main()
