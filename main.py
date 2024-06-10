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
# ========== main.py ==========
# Author : Euan Steven
# Date Created : 17/12/2023
# Date Modified : 17/12/2023
# Version : 1.2
# License : Apache 2.0
# Description : Main Menu for Recipe Scanner
# =============================

# ========== Module Imports ==========
print("========== Main ==========")
print("[OK] MAIN - Importing Modules")

# Built-in Modules
import os
import time

startTime = time.time()

# Local Modules
import reader
import parse

print("[OK] MAIN - Imported Modules")

# ========== Main Program ==========

def main():
    print("========== Reader ==========")
    print("[OK] MAIN - Reader Starting")
    os.system('python3 reader.py')
    print("[OK] MAIN - Reader Finished")
    print("========== Parser ==========")
    print("[OK] MAIN - Parser Starting")
    os.system('python3 parse.py')
    print("[OK] MAIN - Parser Finished")
    print("========== Export ==========")
    print("[OK] MAIN - Export Starting")
    os.system('python3 export.py')
    print("[OK] MAIN - Export Finished")

if __name__ == "__main__":
    main()
    endTime = time.time()
    timeTaken = endTime - startTime
    timeTakenFormatted = time.strftime("%H:%M:%S", time.gmtime(timeTaken))

    print("[OK] MAIN - Time Taken: " + str(timeTakenFormatted) + " minutes")