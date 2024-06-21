from tkinter import *
from tkinter.messagebox import showinfo
import random
import time


class Button_(Button):
    def __init__(self, text, function,  **kwargs):
        self.text = text
        self.is_shown = False
        self.function=function
        self.pos_kwargs = kwargs 

    def display(self, master):
        super().__init__(master)
        self.bind("<Button-1>", self.command_function)
        self.place(**self.pos_kwargs)

    def command_function(self, event):
        self.function(self)

    def show(self):
        self.is_shown = True
        self.config(text=self.text)
    def reset(self):
        self.is_shown = False
        self.config(text="")

class Game(Tk):
    def __init__(self) -> None:
        super().__init__()

        self.size = 4
        self.buttons = None
        self.current = None

        self.geometry("150x150")
        self.title("Memory Game")
        self.resizable(0, 0)

        self.__set_grid()
        self.__display_grid()
        self.mainloop()

    def __set_grid(self):
        flatten_grid = list(range((self.size*self.size)//2))  + list(range((self.size*self.size)//2))
        random.shuffle(flatten_grid)
        grid = [ flatten_grid[i:i+self.size] for i in range(0, len(flatten_grid), self.size) ]

        self.buttons = []
        for row_index, row in enumerate(grid):
            for column_index, text in enumerate(row):
                button = Button_(text=text, function=self.button_click_handler, relx=column_index/self.size, rely=row_index/self.size, relwidth=1/self.size, relheight=1/self.size  )
                self.buttons.append(button)

    def __display_grid(self):
        self.grid_frame  = Frame(self)
        self.grid_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

        for button in self.buttons:
            button.display(self.grid_frame)


    def button_click_handler(self, button:Button_):
        if button.is_shown:
            return
        if self.current is None:
            button.show()
            self.current = button
        else:
            button.show()
            button.update()
            
            if button.text==self.current.text:
                self.current=None
                if self.__check_win():
                    showinfo("Won", "You Won")
                    self.grid_frame.destroy()
                    self.__set_grid()
                    self.__display_grid()
                return 
            
            time.sleep(0.2)
            button.reset()
            self.current.reset()
            self.current = None

    def __check_win(self):
        return all(map(lambda button : button.is_shown, self.buttons))
    
if __name__ == "__main__":
    Game()