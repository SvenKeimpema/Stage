import pygame
import sys
import socket

IMAGES = {}
SQ_SIZE = 100
board = [["" for _ in range(8)] for _ in range(8)]

def parseFen(fen):
    pieces = ["P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"]
    boardIndex = charIndex = 0
    while fen[charIndex] != ' ':
        idx = 0
        foundPiece = False
        for piece in pieces:
            if piece[0 if idx <= 5 else 1] == fen[charIndex]:
                board[boardIndex//8][boardIndex%8] = piece[0 if idx <= 5 else 1]
                boardIndex += 1
                foundPiece = True
                break

        if not foundPiece:
            if fen[charIndex].isdigit():
                skip = int(fen[charIndex])
                boardIndex += skip

        charIndex += 1

def checkData(data):
    data = data[2:(len(data))]
    return data.decode('utf8')

def loadImages():
    images = ["P", "N", "B", "R", "Q", "K", "bp", "bn", "bb", "br", "bq", "bk"]
    idx = 0
    for image in images:
        IMAGES[image] = pygame.transform.scale(pygame.image.load("img/" + images[idx] + ".png"), (SQ_SIZE, SQ_SIZE))
        idx += 1

def draw(screen, board):
    drawBoard(screen)
    drawPieces(screen, board)

def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for x in range(8):
        for y in range(8):
            color = colors[(x+y)%2]
            pygame.draw.rect(screen, color, pygame.Rect(x*SQ_SIZE, y*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    blackPieces = ["p", "n", "b", "r", "q", "k"]
    for x in range(8):
        for y in range(8):
            piece = board[y][x]
            if piece != "" and piece not in blackPieces:
                print(piece)
                screen.blit(IMAGES[piece], pygame.Rect(x*SQ_SIZE, y*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif piece in blackPieces:
                screen.blit(IMAGES["b"+piece], pygame.Rect(x*SQ_SIZE, y*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 800))

    loadImages()

    HOST = "127.0.0.1"
    PORT = 9985
    data = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        data = checkData(data)

        parseFen(data)
        print(board)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        print("test")

            draw(screen, board)
            pygame.display.flip()