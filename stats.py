
class Stats():

    def __init__(self):
        self.reset_stats()
        self.run_games = True
        with open('Record.txt', 'r') as f:
            self.high_score = int(f.readline())

    def reset_stats(self):

        self.guns_left = 3
        self.score = 0