from PIL import Image, ImageEnhance

# Load the image
image = Image.open('Output/From_PDF/images/page_1.png')

# Enhance the contrast
enhancer = ImageEnhance.Contrast(image)
enhanced_image = enhancer.enhance(1.3)  # The factor is a number by which to adjust the contrast. Greater than 1 increases the contrast.

# Enhance the sharpness
sharpness_enhancer = ImageEnhance.Sharpness(enhanced_image)
sharper_image = sharpness_enhancer.enhance(2)  # 'factor' > 1 will increase sharpness

# Save the enhanced image
sharper_image.save('enhanced_image.png')
