import random
import os
import sys
import json
from pathlib import Path

class wyrdle:
    def __init__(self):
        self.answerListPath = str(Path.cwd()) + "\\answerList.txt"
        self.allowedGuessListPath = str(Path.cwd()) + "\\allowedGuessList.txt"
        self.statsDictPath = str(Path.cwd()) + "\\statsDict.txt"
        # print(self.answerListPath)
        # print(self.allowedGuessListPath)
        # print(self.statsDictPath)
        try:
            with open(self.answerListPath) as f:
                self.answerList = f.read().splitlines()
        except:
            print("Cannot find answerList.txt, remember to download it and place it in the same directly as wyrdle.py, or change the path in the __init__ section of the wyrdle class.")
            sys.exit()
        try:
            with open(self.allowedGuessListPath) as f:
                self.allowedGuessList = f.read().splitlines()
        except:
            print("Cannot find allowedGuessList.txt, remember to download it and place it in the same directly as wyrdle.py, or change the path in the __init__ section of the wyrdle class.")
            sys.exit()
    def highlight(self, s, color):
        color = color.lower()
        if color == "green": return "\x1b[0;30;42m" + s + "\x1b[0m"
        elif color == "red": return "\x1b[0;30;41m" + s + "\x1b[0m"
        elif color == "black": return "\x1b[0;30;40m" + s + "\x1b[0m"
        else: return s
    def resetGame(self):
        self.listOfGuesses = []
        self.chosenWord = random.choice(self.answerList)
    def getHighlightedString(self, guess, endOfGame = False):
        printedString = ""
        correctGuesses = {}
        for i in range(5):
            correctGuesses[guess[i]] = 0
        for i in range(5):
            if guess[i] == self.chosenWord[i]:
                correctGuesses[guess[i]] += 1
        for i in range(5):
            if guess[i] == self.chosenWord[i]:
                printedString = printedString + (self.highlight(guess[i], 'green') if endOfGame == False else self.highlight(' ', 'green'))
            elif guess[i] not in self.chosenWord:
                printedString = printedString + (guess[i] if endOfGame == False else ' ')
            else: # guessed letter is not in the right place
                if self.chosenWord.count(guess[i]) == correctGuesses[guess[i]]: # if the guess already matched 1:1 the same letters in the secret word, but this one is extra
                    printedString = printedString + (guess[i] if endOfGame == False else ' ') # print grey
                else:
                    printedString = printedString + (self.highlight(guess[i], 'red') if endOfGame == False else self.highlight(' ', 'red'))
        return printedString
    def showMap(self):
        printedString = ""
        for guess in self.listOfGuesses:
            printedString = printedString + self.getHighlightedString(guess) + "\n"
        return printedString
    def endGame(self, boolWin):
        try:
            with open(self.statsDictPath) as f: statsDict = json.load(f)
        except:
            statsDict = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "losses": 0, "currentStreak": 0, "longestStreak": 0}
        if boolWin:
            statsDict[str(len(self.listOfGuesses))] += 1
            statsDict["currentStreak"] += 1
            if statsDict["currentStreak"] > statsDict["longestStreak"]: statsDict["longestStreak"] = statsDict["currentStreak"]
        else:
            statsDict["losses"] += 1
            statsDict["currentstreak"] = 0
        with open(self.statsDictPath, "w") as f: json.dump(statsDict, f)
        printedString = "\n"
        for guess in self.listOfGuesses:
            printedString = printedString + self.getHighlightedString(guess, endOfGame = True) + "\n"
        gamesWon = 0
        distribution = ""
        distributionDict = {}
        for i in range (6):
            distributionDict[i + 1] = statsDict[str(i + 1)]
        for i in range (6):
            i = i + 1
            gamesWon = gamesWon + statsDict[str(i)]
            if max(distributionDict) > 0:
                distribution = distribution + f"{i}: {statsDict[str(i)]}" + " " * (8 - len(str(statsDict[str(i)]))) + self.highlight(' ', 'green') * int(20 * (statsDict[str(i)] / max(distributionDict.values()))) + "\n"
            else: distribution = distribution + f"{i}: {statsDict[str(i)]}\n"
        printedString = printedString+ f'\nPlayed: {gamesWon + statsDict["losses"]}\nWin %: {round((gamesWon * 100) / (gamesWon + statsDict["losses"]))}\nCurrent Streak: {statsDict["currentStreak"]}\nLongest Streak: {statsDict["longestStreak"]}\n\n' + distribution
        print(printedString)
        answer = input("Do you want to play again? Y/N\n")
        while True:
            if answer.lower() == "y":
                self.resetGame()
                os.system("cls")
                break
            elif answer.lower() == "n":
                sys.exit()
            else:
                answer = input(""""Y" or "N", please and thank you.""")

def main():
    os.system("cls")
    wg = wyrdle()
    wg.resetGame()
    while True:
        print("""Take a guess! Or "showmap" to show a list of guesses, "quit" or "exit" to exit.""")
        while True:
            # wg.chosenWord = input("cheat\n")
            guess = input()
            guess = guess.lower()
            if guess == "showmap":
                print("\n" + wg.showMap() + """Take a guess! Or "showmap" to show a list of guesses, "quit" or "exit" to exit.""")
            elif guess == "quit" or guess == "exit":
                sys.exit()
            elif not len(guess) == 5:
                print("Needs to be 5 characters, try again.")
            elif not guess in wg.allowedGuessList:
                print("Needs to be a valied word, try agin.")
            else:
                break
        wg.listOfGuesses.append(guess)
        if guess == wg.chosenWord:
            print(f"You got the word correct in {len(wg.listOfGuesses)} guess{'es' if len (wg.listOfGuesses) > 1 else ''}! Congrats!")
            wg.endGame(True)
        elif len(wg.listOfGuesses) < 6:
            print(wg.getHighlightedString(guess))
        else:
            print(wg.getHighlightedString(guess) +"\n\nYou didn't find the word. The word was " + wg.chosenWord + ".")
            wg.endGame(False)

if __name__ == "__main__":
    main()
