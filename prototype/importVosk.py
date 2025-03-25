from PIL import Image

# Open the image
img = Image.open("TESS.png")

# Convert and save as .ico
img.save("TESS.ico", format="ICO")
