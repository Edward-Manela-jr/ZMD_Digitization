from PIL import Image
import random

#image size
width = 256
height = 256

#create random pixels
image = Image.new("RGB", (width, height))
pixels = image.load()

for i in range(width):
    for j in range(height):
        pixels[i, j] = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)  
        )

image.save("random_image1.png")
image.save("random_image2.png")
image.save("random_image3.png")
image.save("random_image4.png")
image.save("random_image5.png")
image.save("random_image6.png")
image.save("random_image7.png")
image.save("random_image8.png")
image.save("random_image9.png")
image.save("random_image10.png")
image.save("random_image11.png")
image.save("random_image12.png")
print("Random image saved as random_image.png")