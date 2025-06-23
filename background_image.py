import base64

# Load your image file
with open("futuristic-technology-concept.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Print the string so you can copy it
print("\n📄 COPY BELOW BASE64 STRING:\n")
print(encoded_string)
