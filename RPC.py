# rock-paper-scissors-games on opencv and pyhon3
from distutils.debug import DEBUG
import cv2
from cvzone.HandTrackingModule import HandDetector
import random
import numpy as np
import os

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 200)

detector = HandDetector(detectionCon=0.8, maxHands=1)

os.chdir(os.getcwd())

path="rock-paper-scissors.jpg"


def computer_chos():
    choiceComputer = random.choice(['r', 's', 'p'])
    img = choiceComputerPictuer(choiceComputer)
    return choiceComputer, img


def choiceComputerPictuer(resualt):
    img = cv2.imread(path)

    if resualt == 'r':
        imgResize = img[545:880, 560:900]  # Rock
    if resualt == 'p':
        imgResize = img[115:500, 285:660]  # Paper
    if resualt == 's':
        imgResize = img[505:885, 45:325]  # Scissor
    
    h = int((imgResize.shape[0:1][0])/4)  # y
    w = int((imgResize.shape[1:2][0])/4)  # x
    imgResize = cv2.resize(imgResize, (h, w))  # 270-237

    return imgResize


wins = 0
losses = 0


def resualtGame(userChoice, computerChoice):
    global wins
    global losses
    if (userChoice == 'r' and computerChoice == 's') or (userChoice == 'p' and computerChoice == 'r') or (userChoice == 's' and computerChoice == 'p'):
        resualt = 'Win'
        wins += 1
    elif computerChoice == userChoice:
        resualt = "Equal"
    else:
        resualt = 'Losses'
        losses += 1

    return resualt


start = False
imgCom = np.ones([100, 100, 3])

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=True)  # With Draw
    
    if hands:

        fingers1 = detector.fingersUp(hands[0])

        if start == True:  # for begin Games hand show

            if fingers1 == [0, 1, 1, 0, 0]:
                com, imgCom = computer_chos()
                esualt_RPS = resualtGame('s', com)

            if fingers1 == [0, 0, 0, 0, 0]:
                com, imgCom = computer_chos()
                resualt_RPS = resualtGame('r', com)

            if fingers1 == [1, 1, 1, 1, 1]:
                com, imgCom = computer_chos()
                resualt_RPS = resualtGame('p', com)

            start = False

        h, w, c = imgCom.shape
        img[0:h, 0:w] = imgCom
    else:
        resualt_RPS = ''
        start = True
    cv2.putText(img, resualt_RPS, (220, 420), 2, 2, (255, 255, 100), 3)
    cv2.putText(img, f"Wins= {str(wins)}", (5, 400), 1, 2, (255, 20, 100), 3)
    cv2.putText(img, f"Losses= {str(losses)}",
                (5, 450), 1, 2, (255, 20, 100), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('q'):
        break
