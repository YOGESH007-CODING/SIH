from src.photo_extractor import MetadataExtractor

image_path = "E:/CivicSpotter/test/photo_extractor/test_data/test_photo.jpg"
extractor = MetadataExtractor()
info = extractor.extract_metadata(image_path)
print("Metadata Extracted:")
print(info)