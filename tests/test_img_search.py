import unittest
from unittest.mock import patch
from services.img_service import find_images_by_description

import os

# נניח שאנחנו משתמשים בקוד הקודם של find_images_by_description
from services.img_service import find_images_by_description

class TestImageSearch(unittest.TestCase):
    print("1")
    @patch('services.img_service.detect_labels')
    def test_find_images_by_description_with_matches(self, mock_detect_labels):
        # מחזיקים mock לפונקציה detect_labels שתשיב תוצאה מותאמת
        mock_detect_labels.return_value = ['dog', 'flower']

        description = "dog flower"
        folder_path = "M:\check"  # תיקיית התמונות לבדיקה

        # יצירת תיקיית בדיקה
        os.makedirs(folder_path, exist_ok=True)
        print("2")
        # יצירת קובץ תמונה לדוגמה בתיקיה (פשוט קובץ ריק לצורך הטסט)
        with open(os.path.join(folder_path, 'dog_playing_flower.jpg'), 'w') as f:
            f.write('test')  # יכול להיות שתצטרך להחליף עם תמונה אמיתית לפלאבל את הפונקציה

        # הרצת הפונקציה
        matched_images = find_images_by_description(description, folder_path, open_images=False)
        
        # ודא שהתמונה נמצאה בתוצאות
        self.assertEqual(len(matched_images), 1)
        self.assertIn('dog_playing_flower.jpg', matched_images)
        print("3")
        # מחיקת תיקיית בדיקה אחרי הבדיקה
        for file in os.listdir(folder_path):
            os.remove(os.path.join(folder_path, file))
        os.rmdir(folder_path)
        print("4")
    @patch('services.img_service.detect_labels')
    def test_find_images_by_description_no_matches(self, mock_detect_labels):
        # מחזיקים mock לפונקציה detect_labels שתשיב תוצאה שאינה תואמת לתיאור
        mock_detect_labels.return_value = ['dog', 'flower']

        description = "cat flower"
        folder_path = "test_folder"

        # יצירת תיקיית בדיקה
        os.makedirs(folder_path, exist_ok=True)
        
        # יצירת קובץ תמונה לדוגמה בתיקיה
        with open(os.path.join(folder_path, 'dog_playing_ball.jpg'), 'w') as f:
            f.write('test')
        print("5")
        # הרצת הפונקציה
        matched_images = find_images_by_description(description, folder_path, open_images=False)
        
        # ודא שאין תמונות תואמות
        self.assertEqual(len(matched_images), 0)

        # מחיקת תיקיית בדיקה אחרי הבדיקה
        for file in os.listdir(folder_path):
            os.remove(os.path.join(folder_path, file))
        os.rmdir(folder_path)

if __name__ == '__main__':
    unittest.main()
