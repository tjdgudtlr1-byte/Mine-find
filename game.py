import pygame
import sys
import random

# 상수
CELL_SIZE = 28
COL = 8
ROW = 8
MINE = 10
WIDTH = 225
HEIGHT = 225
FPS = 15

# Board Class 게임판 상태 출력 담당 클래스
class Board:
    def __init__(self):
        self.field = [[0 for _ in range(COL)] for _ in range(ROW)] #게임 보드를 2차원 리스트로 초기화
        self.clicked = [[False for _ in range(COL)] for _ in range(ROW)] # 열림/ 닫힘 상태

    def set_mines(self, total_mines): #보드애 지뢰를 랜덤하게 배치
        mines_placed = 0 # 현재까지 몇개 심었는지 확인하는 카운터 0 부터 시작

        while mines_placed < total_mines: # 목표한 지뢰 개수만큼 다 심을 때 까지 반복
            y = random.randint(0, ROW - 1) #무작위 행(y)과 열(x) 좌표를 하나 뽑음
            x = random.randint(0, COL - 1)

            if self.field[y][x] == 0: # 지뢰가 심어졌나? 체크
                self.field[y][x] = -1  # 지뢰 설치(지뢰는 -1로 표기)
                mines_placed += 1 # 설치 성공시 카운트 1증가 9까지가면 종료(0~9 총10개)
                #print(f'지뢰 {mines_placed}개째 매설 중...') # 지뢰 매설 테스트1(완)
        #print(f'지뢰 {total_mines}개 매설완료') # 지뢰 매설 테스트2(완)
    
    def calculate_numbers(self): #지뢰 주변 8칸에 숫자를 채워넣는 메소드
        for y in range(ROW): #행과 열을 훑는 이중 for문
            for x in range(COL):
                if self.field[y][x] == -1: #해당 칸이 -1(지뢰)라면

                    for dy in [-1, 0, 1]: # dy, dx는 상대 좌표 
                        for dx in [-1, 0,1]: # y, dx [-1, 0, 1]에 포함된 모두를 스캔해서
                            if dy == 0 and dx == 0: # 0, 0)은 지뢰닌깐 포함없으니
                                continue # 진행해

                            ny, nx = y + dy, x + dx #주소 계산 next y, next x 8방향을 확인하기 위함

                            if 0 <= ny < ROW and 0 <= nx < COL: #지뢰가 왼쪽구석 1번칸에 존재할떄 (-1 -1) 검사시에indexError방지
                                if self.field[ny][nx] != -1: #지뢰 옆에 지뢰가 있을때를 위한 필터링
                                    self.field[ny][nx] += 1 # 검사 통과시 숫자를 올림, 빈칸들은 내 주변에 지뢰가 총 몇개인지 알게됨
                                
# Game Class게임 실행 및 렌더링 담당 클래스
class Game:
    def __init__(self):
        pygame.init()
        self.background = pygame.display.set_mode((WIDTH, HEIGHT)) # 게임 창 사이즈
        pygame.display.set_caption("FinD Mines!") # 게임 이름
        self.clock = pygame.time.Clock() # 시계 객체 생성
        self.font = pygame.font.SysFont("malgungothic", 10, True, False)
        self.clicked = [[False for _ in range(COL)] for _ in range(ROW)] # 처음엔 모든칸이 닫혀있게 만듦

        self.running = True
        self.board = Board()
        self.board.set_mines(MINE) # 지뢰 설치
        self.board.calculate_numbers() #지뢰 주변 숫자 표시

    def draw_grid(self):  #격자 그려 넣는 메소드
        for y in range(ROW):
            for x in range(COL):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.background, (255, 255, 255), rect, 1)

                if self.board.clicked[y][x]: # 먼저 이칸이 열렸는가 확인
                    if self.board.field[y][x] == -1: #지뢰 그리기
                        pygame.draw.rect(self.background, (255, 255, 0), rect)
                        pygame.draw.rect(self.background, (255, 255, 255), rect, 1) #테두리
            
                    elif self.board.field[y][x] > 0: #숫자 그리기 1~8
                        text_surf = self.font.render(str(self.board.field[y][x]), True, (255, 255, 0))
                        text_rect = text_surf.get_rect(center=rect.center) #숫자를 격자 칸의 중앙에 배치
                        self.background.blit(text_surf, text_rect) # 화면에 그리기
                
                    #else: #바닥 표시 해주는건데 굳이..넣어야하나..?
                        #pygame.draw.rect(self.background, (50, 50, 50), rect) # 회색 바닥
                        #pygame.draw.rect(self.background, (255, 255, 255), rect, 1) #테두리
                
                else: # 아직 클릭 안된(False) 칸이라면 아래 조건을 따라감
                    pygame.draw.rect(self.background, (100, 100, 100), rect) #내용물 상관없이 전부 덮어
                    pygame.draw.rect(self.background, (255, 255, 255), rect, 1) #테두리
                
    def events(self): #게임 종료 담당 메소드
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos() # 클릭한 마우스의 실제 좌표 가져옴
                grid_x = m_x // CELL_SIZE # 좌표를 격자 인덱스(x, y)로 변환
                grid_y = m_y // CELL_SIZE

                if 0 <= grid_x < COL and 0 <= grid_y < ROW: # 보드 범위 안을 클릭했으면 확인 후 열기
                    self.board.clicked[grid_y][grid_x] = True
                    #print(f"{grid_y}행 {grid_x}열 오픈!") 테스트 완료 마우스 정상 인식

                    if self.board.field[grid_y][grid_x] == -1: # 해당 격자 안이 -1(지뢰)이면 
                        print("Game Over!") # 터미널에 Game Over 출력
                        self.running = False # 게임을 종료시킴

    def run(self): #게임 실행시 메소드 호출 순서 담당해줌
        while self.running:
            self.events()

            self.background.fill((0, 0, 0))
            self.draw_grid()
            

            pygame.display.flip()
            self.clock.tick(FPS) # 초당 프레임 제한

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()