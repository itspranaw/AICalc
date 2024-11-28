# tests/test_api.py
import requests
import base64
from pathlib import Path
import json

class TestAPI:
    def __init__(self, base_url="http://localhost:8900"):
        self.base_url = base_url
        self.calculation_id = None

    def encode_image(self, image_path):
        """Convert image to base64 string"""
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded_string}"

    def test_process_image(self, image_path):
        """Test the image processing endpoint"""
        encoded_image = self.encode_image(image_path)
        
        payload = {
            "image": encoded_image,
            "dict_of_vars": {"x": 5, "y": 10}  # Example variables
        }

        response = requests.post(
            f"{self.base_url}/calculate",
            json=payload
        )
        
        print("\nProcess Image Response:")
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            self.calculation_id = response.json().get('calculation_id')
            return True
        return False

    def test_get_history(self):
        """Test the history endpoint"""
        response = requests.get(f"{self.base_url}/calculate/history")
        
        print("\nGet History Response:")
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        
        return response.status_code == 200

    def test_update_notes(self):
        """Test updating notes for a calculation"""
        if not self.calculation_id:
            print("No calculation ID available. Run process_image first.")
            return False

        notes = "Test notes for this calculation"
        response = requests.put(
            f"{self.base_url}/calculate/{self.calculation_id}/notes",
            params={"notes": notes}
        )
        
        print("\nUpdate Notes Response:")
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
        
        return response.status_code == 200

def main():
    # Create test images directory if it doesn't exist
    Path("tests/test_images").mkdir(parents=True, exist_ok=True)
    
    # Create a simple test image with a math expression
    from PIL import Image, ImageDraw, ImageFont
    
    def create_test_image(text, filename):
        img = Image.new('RGB', (400, 100), color='white')
        d = ImageDraw.Draw(img)
        # Use default font
        d.text((10, 10), text, fill='black')
        img.save(f'tests/test_images/{filename}')
        return f'tests/test_images/{filename}'
    
    # Create test images with different math expressions
    test_images = [
        create_test_image("2 + 2 = ?", "simple_addition.png"),
        create_test_image("x^2 + 2x + 1 = 0", "quadratic.png"),
        create_test_image("y = 5", "assignment.png")
    ]
    
    # Run tests
    tester = TestAPI()
    
    print("Testing API endpoints...")
    
    for img_path in test_images:
        print(f"\nTesting with image: {img_path}")
        if tester.test_process_image(img_path):
            tester.test_get_history()
            tester.test_update_notes()

if __name__ == "__main__":
    main()