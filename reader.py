# Copyright 2023 Euan Steven
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- encoding: utf-8 -*-
# ========== reader.py ==========
# Author : Euan Steven
# Date Created : 16/12/2023
# Date Modified : 17/12/2023
# Version : 1.8
# License : Apache 2.0
# Description : Scan Recipes to Text File
# =============================

# ========== Module Imports ==========
print("[OK] READER - Importing Modules")

# Built-in Modules
import os

# Third-party Modules
import easyocr
import subprocess
import cv2

print("[OK] READER - Imported Modules")

# ========== Read Text from Image ==========
def read_text_from_image(image_path):
    print("[OK] READER - OCR Reader Loading")
    reader = easyocr.Reader(['en'])
    print("[OK] READER - OCR Reader Created")

    print("[OK] READER - Loading Image")
    img = cv2.imread(image_path)
    print("[OK] READER - Image Loaded")

    print("[OK] READER - Converting Image to Grayscale")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("[OK] READER - Image Converted to Grayscale")

    print("[OK] READER - Performing OCR")
    result = reader.readtext(gray, batch_size=1)
    print("[OK] READER - OCR Performed")

    print("[OK] READER - Extracting Text")
    text = ' '.join([entry[1] for entry in result])
    print("[OK] READER - Text Extracted")
    
    return text

# ========== Write Text to File ==========
def write_to_file(output_folder, filename, content):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, filename)
    print("[OK] READER - Writing Text to File")
    with open(output_path, 'a', encoding='utf-8') as file:
        file.write(content + '\n' + '=' * 10 + '\n')
        print(f"[OK] READER - Text Written to {output_path}")

# ========== Main Program ==========
if __name__ == "__main__":
    images_directory = "./images"
    output_folder = "./scanned"
    python_file = 'noteshrink.py'

    for filename in os.listdir(images_directory):
        inimg = os.path.join(images_directory, filename).replace("\\", "/")
        outimg = os.path.join("images", os.path.splitext(filename)[0])
        cmd_args = [inimg, '-b', outimg]
        command = ['python3', python_file] + cmd_args

        print("========== Noteshrink ==========")
        subprocess.run(command)
        print("[OK] READER - Noteshrink Complete")
        print("========== Reader ==========")

    for filename in os.listdir(images_directory):    
        if filename.endswith(".png"):
            image_path = os.path.join(images_directory, filename)
            print("[OK] READER - Reading Text...")
            result_text = read_text_from_image(image_path)
            write_to_file(output_folder, f"{os.path.splitext(filename)[0]}_output.txt", f"Text from {filename}:\n{result_text}")
        else:
            pass
    