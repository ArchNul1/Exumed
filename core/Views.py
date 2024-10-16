import pyfiglet
from termcolor import colored
from tqdm import tqdm
from core.Dorks import Dorks
import asyncio


#view menu 
class View:
    def __init__(self, font:str) -> None:
        self.font = font=font
    
    #method menu     
    def View_window(self) -> str:
       
        
        fist_title = pyfiglet.figlet_format('Exu', font='slant')
        two_title = pyfiglet.figlet_format('me', font='slant')
        three_title = pyfiglet.figlet_format('d', font='slant')


        fist_lines = fist_title.splitlines()
        two_lines = two_title.splitlines()
        three_lines = three_title.splitlines()

        
        fist_lines = [colored(line, 'light_cyan') for line in fist_lines]
        two_lines = [colored(line, 'light_blue') for line in two_lines]
        three_lines = [colored(line, 'light_cyan') for line in three_lines]

        combined_lines = [f"{f}{t}{r}"for f,t,r in zip(fist_lines,two_lines,three_lines)]
        combined_title = "\n".join(combined_lines)
        print(combined_title.strip('\n'))
    
        print(colored('-' * 33, 'cyan'))
        print(colored('|\tBy:Arch_0x3f5\t\t|', 'light_blue'),end='\n')
        print(colored("|\tDiscord:Arch_0x3f5\t|",'light_blue'),end='\n')
        print(colored("|\tGitHub:Archboot07\t|",'light_blue'),end='\n')
        print(colored('-' * 33, 'cyan'))
        user_input = input(colored("\n\nSearch target: ", 'cyan'))
        
        if user_input:
            print(colored("\nStart ...\n",'light_blue'))
            dorks = Dorks(user_input)
            asyncio.run(dorks.fetch())
        else:
            print(colored("Start ...\n",'light_blue'))
            dorks = Dorks()
            asyncio.run(dorks.fetch())

        
      
        
    
  

