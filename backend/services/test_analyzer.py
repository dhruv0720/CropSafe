# test_analyzer.py
from services.crop_analyzer import CropAnalyzer
from PIL import Image
import glob

analyzer = CropAnalyzer()

# Test with multiple wheat images
wheat_images = glob.glob(r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\Final_Dataset\Wheat\*\*.jpg")[:5]

print("🔍 Testing Wheat Images:")
print("=" * 50)
for img_path in wheat_images:
    img = Image.open(img_path)
    result = analyzer.analyze(img, 'wheat')
    print(f"\n📸 {img_path.split('Wheat')[-1]}")
    print(f"   Disease: {result['prediction']['disease']}")
    print(f"   Severity: {result['prediction']['severity']['level']} ({result['prediction']['severity']['percentage']}%)")