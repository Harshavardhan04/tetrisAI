from adversary import RandomAdversary
from arguments import parser
from board import Board, Direction, Rotation
from constants import BOARD_WIDTH, BOARD_HEIGHT, DEFAULT_SEED
from player import Player, SelectedPlayer

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

CELL_WIDTH = 20
CELL_HEIGHT = 20

FORCE_DOWN_INTERVAL = 1000
EVENT_FORCE_DOWN = pygame.USEREVENT + 1
FRAMES_PER_SECOND = 60


class Square(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()

        self.image = pygame.Surface([CELL_WIDTH, CELL_HEIGHT])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_WIDTH
        self.rect.y = y * CELL_HEIGHT


def render(screen, board):
    screen.fill(BLACK)

    sprites = pygame.sprite.Group()

    # Add the cells already on the board for drawing.
    for (x, y) in board:
        sprites.add(Square(WHITE, x, y))

    if board.falling is not None:
        # Add the cells of the falling block for drawing.
        for (x, y) in board.falling:
            sprites.add(Square(RED, x, y))

    sprites.draw(screen)

    # Update window title with score.
    pygame.display.set_caption(f'Score: {board.score}')


class UserPlayer(Player):
    """
    A simple user player that reads moves from the command line.
    """

    key_to_move = {
        pygame.K_RIGHT: Direction.Right,
        pygame.K_LEFT: Direction.Left,
        pygame.K_DOWN: Direction.Down,
        pygame.K_SPACE: Direction.Drop,
        pygame.K_UP: Rotation.Clockwise,
        pygame.K_z: Rotation.Anticlockwise,
        pygame.K_x: Rotation.Clockwise,
    }

    def move(self, board):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.KEYUP:
                if event.key in self.key_to_move:
                    move = self.key_to_move[event.key]
                elif event.key == pygame.K_ESCAPE:
                    raise SystemExit
            elif event.type == EVENT_FORCE_DOWN:
                return Direction.Down

        return move


def run():
    board = Board(BOARD_WIDTH, BOARD_HEIGHT)
    adversary = RandomAdversary(DEFAULT_SEED)

    args = parser.parse_args()
    if args.manual:
        player = UserPlayer()
    else:
        player = SelectedPlayer()

    pygame.init()

    screen = pygame.display.set_mode([
        BOARD_WIDTH * CELL_WIDTH,
        BOARD_HEIGHT * CELL_HEIGHT
    ])

    clock = pygame.time.Clock()

    # Set timer to force block down when no input is given.
    pygame.time.set_timer(EVENT_FORCE_DOWN, FORCE_DOWN_INTERVAL)

    for move in board.run(player, adversary):
        render(screen, board)
        pygame.display.flip()

        # If we are not playing manually, clear the events.
        if not args.manual:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    raise SystemExit
                elif event.type == pygame.QUIT:
                    raise SystemExit

        clock.tick(FRAMES_PER_SECOND)

    pygame.quit()


if __name__ == '__main__':
    run()