import numpy as np
from PIL import Image
from io import BytesIO
import requests
from scipy.spatial.distance import cosine
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
import clipboard
import pyautogui
import time

__all__ = ['requests']

class DeepImageComparator:
    def __init__(self):
        # Initialize VGG16 model for feature extraction
        self.model = VGG16(weights='imagenet', include_top=False)
    
    def load_and_preprocess_image(self, url):
        """Load and preprocess image from URL"""
        #response = requests.get(url)
        img = Image.open(url)
        
        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            img = img.convert('RGB')
            
        return img
    
    def get_vgg_features(self, img):
        """Extract VGG16 features from image"""
        # Resize image to VGG16 expected size
        img_resized = img.resize((224, 224))
        img_array = image.img_to_array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Get features from second-to-last layer
        features = self.model.predict(img_array)
        features_flat = features.flatten()
        
        return features_flat
    
    def compare_images(self, url1, url2):
        """Compare two images using VGG16 features"""
        try:
            # Load images
            img1 = self.load_and_preprocess_image(url1)
            img2 = self.load_and_preprocess_image(url2)
            
            # Get deep features
            features1 = self.get_vgg_features(img1)
            features2 = self.get_vgg_features(img2)
            
            # Calculate cosine similarity
            similarity = 1 - cosine(features1, features2)
            
            print(f"\nDeep Feature Similarity: {similarity:.3f}")
            
            return similarity

            
        except Exception as e:
            print(f"Error comparing images: {str(e)}")
            return None

     
def find_UPC():
    try:
        # Use Ctrl+F to open find
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
                
        # Press Enter to go to position of the UPC number
        pyautogui.press('enter')
        time.sleep(2)
         
        pyautogui.tripleClick(100, 633) # <-- Edit this
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1.5)
        
        # Get clipboard content
        upc_number = int(clipboard.paste())
        
        # Clear clipboard content
        clipboard.copy("")     
        return upc_number
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def take_screenshot(region=None):
    """Take a screenshot of a specific region or full screen"""
    if region:
        return pyautogui.screenshot(region=region)
    return pyautogui.screenshot()
