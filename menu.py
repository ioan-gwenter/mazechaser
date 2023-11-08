from main import *


class Run_Menu():
    """Class which handles the start menu and acts as the parent to any sub-menus"""
    def __init__(self, game):
        self.window = Toplevel(game)
        self.game = game
        self.window.title("RayCast Maze Game Menu")
        self.window.geometry("500x500")
        self.window.maxsize(500, 500)

        # title labels
        self.main_title = Label(self.window, text="RayCast Maze Game", anchor=N,font='Helvetica 20 bold')
        self.main_title.pack()
        self.main_title = Label(self.window, text="Enter a name using letters and numbers. Min. length of 3.", anchor=N)
        self.main_title.pack()

        # Text box
        self.name_in = Text(self.window, height=5, width=20,)
        self.name_in.pack()
        # start button
        self.start_button = Button(self.window, text="Start Game", anchor=N, command=self.play_game)
        self.start_button.pack(pady=20)

        # leaderboard button
        self.leaderboard_button = Button(self.window, text="Leaderboard", anchor=N, command=self.show_leaderboard)
        self.leaderboard_button.pack(pady=20)

        # extra info
        self.main_title = Label(self.window, text="Wall colours changed based on position!\n,\n,Go find the screen square!", anchor=N)
        self.main_title.pack()

        # initalise player name
        self.player_name = ""

    def retrieve_input(self):
        """
        getter for the text box
        :return: string from the text entry
        """
        input = self.name_in.get("1.0", 'end-1c')
        return input

    def close_menu(self):
        self.window.destroy()

    def play_game(self):
        """
        call to initalise the initalise the game loop. Some validtion for strings.
        :return:
        """
        name = self.retrieve_input()
        if str(name).isalnum() and len(name) > 2:
            self.player_name = name
            self.close_menu()
            self.game.start_game()

    def show_leaderboard(self):
        # instantiates the leaderboard class
        leaderboard = LeaderBoard(self.game)


class LeaderBoard:
    """
    child window of the main menu, Leaderboard handles formatting the leaderboard window
    """
    def __init__(self, game):
        self.window = Toplevel(game.menu.window)
        self.game = game
        self.window.title("Leaderboards")
        self.window.geometry("500x500")
        self.window.maxsize(500, 500)

        self.lb_file = open("leaderboard.txt")

        self.main_title = Label(self.window, text="LEADERBOARD", anchor=N,font='Helvetica 25 bold')
        self.main_title.pack()
        self.read_scores()

    def read_scores(self):
        """
        Unpacks all scores from the scores file. String manipulation to format it to be attached to a label.
        :return:
        """
        score_list = []
        lines = [line.rstrip() for line in self.lb_file]
        for string in lines:
            score_list.append(string.split(','))
        score_list = sorted(score_list, key=lambda x: x[1])
        for score in score_list[:10]:
            label = Label(self.window, text=f" {score[0]}: {score[1]} Seconds", anchor=N,font='Helvetica 15')
            label.pack()

