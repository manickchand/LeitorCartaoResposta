from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import cv2

path_images = "../images/"
nm_imagem = None
gray = None
blurred = None
edged = None
paper = None
warped = None
image = None

#variaveis que recebem resultados
resultNumProva = ""
resultCdAluno = ""
resultResponses = ""

# acha o gabarito na imagem
def findPaper(img):

    # acha contornos e os inicializa
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
            # ordenar os contornos de acordo com seu tamanho em
            # ordem decrescente
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

            # loop sobre os contornos classificados
            for c in cnts:
                    # aproximar o contorno de formas geometricas
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                    # se o contorno aproximado tiver quatro pontos
                    # entao podemos supor que encontramos o papel
                    if len(approx) == 4:
                            return approx
                            break
            
#fim findPaper

def cropPaper(ap):
    cp_image = image
    cp_gray = gray
    return four_point_transform(cp_image, ap.reshape(4, 2)),four_point_transform(cp_gray, ap.reshape(4, 2))


def findPainted(img):

    thresh = cv2.adaptiveThreshold (img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV , 31,2)

    # find contours in the thresholded image, then initialize
    # the list of contours that correspond to questions
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []

    #print len(cnts)

    if len(cnts) < 500:
        return 0

    # loop over the contours
    for c in cnts:
            # compute the bounding box of the contour, then use the
            # bounding box to derive the aspect ratio
            (x, y, w, h) = cv2.boundingRect(c)

            # informacoes dos retangulos de preenchimento
            #if h >= 10 and h <= 18 and w >= 15 and w <=42 and y > 50:
            if h >= 20 and h <= 38 and w >= 25 and w <=62 and y > 50:
                #print x,y,w,h
                questionCnts.append(c)
                cv2.drawContours(paper, [c], -1, (0,234,0), 1)
                
    # sort the question contours top-to-bottom, then initialize
    # the total number of correct answers
    questionCnts = contours.sort_contours(questionCnts,method="top-to-bottom")[0]
    correct = 0
    
    #print "len(questionCnts) ",len(questionCnts)
    getTestNumber(questionCnts[:110],thresh)
    getAlunoCode(questionCnts[112:199],thresh)
    getResponses(questionCnts[201:],thresh)

#end findPainted


def getTestNumber(provaCnts,thresh):
    
    for (q, i) in enumerate(np.arange(0, len(provaCnts), 11)):
    
            cnts = contours.sort_contours(provaCnts[i:i + 11])[0]
            bubbled = None
            pos = None

            for (j, c) in enumerate(cnts):
                    
                    mask = np.zeros(thresh.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)

                    # apply the mask to the thresholded image, then
                    # count the number of non-zero pixels in the
                    # bubble area
                    mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                    total = cv2.countNonZero(mask)

                    # if the current total has a larger number of total
                    # non-zero pixels, then we are examining the currently
                    # bubbled-in answer
                    # aqui que vejo qual bola foi pintada
                    if bubbled is None or total > bubbled[0]:
                            bubbled = (total, j)
                            pos = j

            color = (0, 0, 255)

            global resultNumProva
            
            resultNumProva += toNumber(bubbled[1])
            
            cv2.drawContours(paper, [cnts[pos]], -1, color, 3)


def getAlunoCode(alunoCnts,thresh):
    
    for (q, i) in enumerate(np.arange(0, len(alunoCnts), 11)):
    
            cnts = contours.sort_contours(alunoCnts[i:i + 11])[0]
            bubbled = None
            pos = None

            for (j, c) in enumerate(cnts):
                    
                    mask = np.zeros(thresh.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)

                    # apply the mask to the thresholded image, then
                    # count the number of non-zero pixels in the
                    # bubble area
                    mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                    total = cv2.countNonZero(mask)

                    #cv2.drawContours(paper, [c], -1, (255,0,0), 3)

                    # if the current total has a larger number of total
                    # non-zero pixels, then we are examining the currently
                    # bubbled-in answer
                    # aqui que vejo qual bola foi pintada
                    if bubbled is None or total > bubbled[0]:
                            bubbled = (total, j)
                            pos = j

            color = (0, 0, 255)

            global resultCdAluno

            resultCdAluno += toNumber(bubbled[1])
            
            # check to see if the bubbled answer is correct
            #if k == bubbled[1]:
             #       color = (0, 125, 0)
              #      correct += 1

            # draw the outline of the correct answer on the test
            cv2.drawContours(paper, [cnts[pos]], -1, color, 3)


def getResponses(gabaritoCnts,thresh):
    
    for (q, i) in enumerate(np.arange(0, len(gabaritoCnts), 13)):
    
            cnts2 = contours.sort_contours(gabaritoCnts[i:i + 13])[0]
            bubbled = None

            cnts = contours.sort_contours(cnts2[2:7])[0]

            for (j, c) in enumerate(cnts):
                    
                    mask = np.zeros(thresh.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)

                    # apply the mask to the thresholded image, then
                    # count the number of non-zero pixels in the
                    # bubble area
                    mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                    total = cv2.countNonZero(mask)

                    #cv2.drawContours(paper, [c], -1, (255,0,0), 3)
                    

                    # if the current total has a larger number of total
                    # non-zero pixels, then we are examining the currently
                    # bubbled-in answer
                    # aqui que vejo qual bola foi pintada
                    if bubbled is None or total > bubbled[0]:
                            #print total
                            bubbled = (total, j)
                            pos = j

            if bubbled[0] > 800 :
                global resultResponses

                resultResponses += toResponse(bubbled[1])
            
                # check to see if the bubbled answer is correct
                #if k == bubbled[1]:
                 #       color = (0, 125, 0)
                  #      correct += 1

                # draw the outline of the correct answer on the test
                cv2.drawContours(paper, [cnts[bubbled[1]]], -1, (0,0,255), 3)

def toResponse(position):
     return {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D',
        4: 'E',
    }[position]

def toNumber(position):
     return {
        0: 'X',
        1: '0',
        2: '1',
        3: '2',
        4: '3',
        5: '4',
        6: '5',
        7: '6',
        8: '7',
        9: '8',
        10: '9',
    }[position]

# aplicar uma perspectiva de quatro pontos transformar a ambos
# seleciona apenas area do papael e papel em P&B
# paper = four_point_transform(image, dcnt.reshape(4, 2))

def execPaper(img):
    appr = findPaper(img)
    if appr is not None:
        global paper, warped
        paper, warped = cropPaper(appr)

        r = findPainted(warped)
        if r == 0:
            execPaper(cv2.adaptiveThreshold (img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV , 31,2))


def init(nm_image):

        img = path_images+"g3.jpg"

        #imagem Original
        image = cv2.imread(img)

        #efeitos para destacar contornos
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 10, 100)

        execPaper(edged)

        print "CD Prova = ",resultNumProva
        print "Cd aluno = ", resultCdAluno
        print "respostas = ", resultResponses

        cv2.imwrite("contornos.jpg",paper)
        cv2.waitKey(0)
        cv2.destroyAllWindows()   


# init("g3.jpg")

def ola():
        return "ola mundo"
