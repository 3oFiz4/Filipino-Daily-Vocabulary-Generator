# Anki Daily filipino vocabulary generator
This is a simple script I made in 3 hours, to leverage Anki to generate a daily vocabulary that I will memorize each day.. This is also for me and my friend. The use of this script is to generate a "[n] Daily vocabulary" deck that contains a list of Tagalog words for n is each number of days. 

## ✨ Features:
- **Randomized Word Generation (RWG) (adjective, verb, and etc)**: where the Randomized Word Generation (RWG) are make sure to not collide (a problem where a note have it's own duplicated version with another note somewhere with other deck) with other note in previous number of day of "Daily Vocabulary". This ensures that, there will be no repeated vocabulary, therefore, making the field consistent.
- **Reverse Card (RC)**: it's the field being used, it's simply create a duplicated note, but a reverse version of it.
- **API Request (HTTP)**: this script utilizes HTTP Request to Tagalog-English dictionary, for creating the fields.
- **Every Day Automation (EDA)**: this script run every day, this can be configured.

## ⚙ Set Up
1. __(optional) If you already had any "[n] Daily Vocabulary" or a similar daily vocabulary deck.__ Export it via "Notes in Plain text (.txt)", and un-checkmarked everything. And then it should give you the exported file. Now you are gonna store the exported text to "Exclude_deck" and then run "Exclude_Vocabulary.py", this will copy the very first word for each line in the exported text, and append it to "Exclude_Vocabulary.txt", so for any next "[n] Daily Vocabulary" you don't have to re-check if the same vocabulary are being used.
2. Open Task Scheduler
3. Click 'Create Basic Task...'
4. Provide the Name and Description by your choice.
5. Set the Trigger to 'Daily' 
6. You'll be given a date and a time, modify them by your choice, but make sure the 'Recur every:' is 1
7. If inquired to 'What action do you want the task to perform', select 'Start a program'
8. You'll be given a 'Program/Script', click browse, and select the 'Automaton.bat' in this folder. 
9. Click Finish.

## 🚫 Warning
- **Do no try to edit any of the file that starts with "__" without any idea of what you are doing, it's the file that is used for the script to exclude such vocabulary, unless you understand what you are doing! Note that, the text in the file contains a list of words that will not be generated. You can add yours too, but it should be only a word. Not 2. Not 3. Example: Joint. But not: Joint and**

## 📜 Instructions:
1. **Clone the repository:**
```bash
git clone https://github.com/DaemonPooling/Filipino-Daily-Vocabulary-Generator.git
```

2. **Navigate to the Project Folder:**
```bash
cd Filipino-Daily-Vocabulary-Generator
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```