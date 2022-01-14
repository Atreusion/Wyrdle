import random
import os
import sys

class wyrdle:
    def __init__(self):
        with open("D:\Documents\wyrdlelist.txt") as f:
            self.wordlist = f.read().splitlines()
    def highlight(self, s, color):
        color = color.lower()
        if color == "green": return "\x1b[0;30;42m" + s + "\x1b[0m"
        elif color == "red": return "\x1b[0;30;41m" + s + "\x1b[0m"
        elif color == "black": return "\x1b[0;30;40m" + s + "\x1b[0m"
        else: return s
    def resetGame(self):
        self.listOfGuesses = []
        self.attempts = 0
        self.chosenWord = random.choice(self.wordlist)
    def getHighlightedString(self, guess):
        printedString = ""
        for i in range(5):
            if guess[i] == self.chosenWord[i]: printedString = printedString + self.highlight(guess[i], "green")
            elif guess[i] in self.chosenWord: printedString = printedString + self.highlight(guess[i], "red")
            else: printedString = printedString + guess[i]
        return printedString
    def showMap(self):
        printedString = ""
        for guess in self.listOfGuesses:
            printedString = printedString + self.getHighlightedString(guess) + "\n"
        return printedString
    def endGame(self):
        printedString = "\n"
        for guess in self.listOfGuesses:
            for i in range(5):
                if guess[i] == self.chosenWord[i]: printedString = printedString + self.highlight(" ", "green")
                elif guess[i] in self.chosenWord: printedString = printedString + self.highlight(" ", "red")
                else: printedString = printedString + " "
            printedString = printedString + "\n"
        print(printedString)
        answer = input("Do you want to play again? Y/N\n")
        while True:
            if answer.lower() == "y":
                self.resetGame()
                os.systme("cls")
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
        print("""Take a guess! Or "showmap" to show a list of guesses.""")
        correctlyFormattedGuess = False
        while correctlyFormattedGuess == False:
            guess = input().lower()
            if guess == "showmap":
                print("\n" + wg.showMap() + """Take a guess! Or "showmap" to show a list of guesses.""")
                continue
            if not guess.isalpha():
                print("Needs to be an alphabetical word, try again.")
                continue
            if not len(guess) == 5:
                print("Needs to be 5 characters, try again.")
                continue
            correctlyFormattedGuess = True
        wg.listOfGuesses.append(guess)
        wg.attempts += 1
        if guess == wg.chosenWord:
            print(f"You got the word correct in {wg.attempts} guess{'es' if wg.attempts > 1 else ''}! Congrats!")
            wg.endGame()
        elif len(wg.listOfGuesses) < 6:
            print(wg.getHighlightedString(guess))
        else:
            print(f"You didn't find the word. The word was {wg.chosenWord}.")
            wg.endGame()

if __name__ == "__main__":
    main()
