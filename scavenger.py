import random
import os
import time
import msvcrt
from enum import Enum

class GameState(Enum):
    PLAYING = 1
    VIEWING_RULES = 2
    VIEWING_LORE = 3

# bureau of orbital observatives & enforcement
# penalty for not clearing the entire area
# report on potential item value efficiency (algorithm)

class RogueLikeGame:
    def __init__(self, width, height, num_items_to_collect):
        self.width = width
        self.height = height
        self.player_x = 0
        self.player_y = 0
        self.exit_x = 0
        self.exit_y = 0
        self.num_items_to_collect = num_items_to_collect
        self.items_collected = 0
        self.total_items_collected = 0
        self.initial_items = 0
        self.initial_monsters = 0
        self.steps = 0
        self.monsters = []
        self.monsters_defeated = 0
        self.monster_levels = {'Common': 1, 'Normal': 2, 'Rare': 3}
        self.game_state = GameState.PLAYING
        self.prev_game_state = None

    def generate_level(self):
        # Initialize the level with empty spaces
        self.level = [['.' for _ in range(self.width)] for _ in range(self.height)]

        # Place the player at a random location
        self.player_x = random.randint(0, self.width - 1)
        self.player_y = random.randint(0, self.height - 1)
        self.level[self.player_y][self.player_x] = 'P'

        # Add some random obstacles
        num_obstacles = random.randint(5, 15)
        for _ in range(num_obstacles):
            obstacle_x = random.randint(0, self.width - 1)
            obstacle_y = random.randint(0, self.height - 1)

            # Make sure obstacles are not placed on the player
            while (obstacle_x == self.player_x and obstacle_y == self.player_y):
                obstacle_x = random.randint(0, self.width - 1)
                obstacle_y = random.randint(0, self.height - 1)

            self.level[obstacle_y][obstacle_x] = '#'

        # Place the exit in a location that is not blocked by obstacles
        while True:
            self.exit_x = random.randint(0, self.width - 1)
            self.exit_y = random.randint(0, self.height - 1)

            # Make sure the exit is not blocked by obstacles
            if self.level[self.exit_y][self.exit_x] == '.':
                break

        self.level[self.exit_y][self.exit_x] = 'E'

        # Place items on the map
        for _ in range(self.num_items_to_collect):
            while True:
                item_x = random.randint(0, self.width - 1)
                item_y = random.randint(0, self.height - 1)

                # Make sure the item is not blocked by obstacles, the player, or the exit
                if (
                    self.level[item_y][item_x] == '.' and
                    (item_x != self.player_x or item_y != self.player_y) and
                    (item_x != self.exit_x or item_y != self.exit_y)
                ):
                    break

            self.level[item_y][item_x] = 'I'

        # Place monsters on the map with random levels
        # Change the upper limit of num_monsters to increase the chances of bogeys appearing
        num_monsters = random.randint(1, 4)  # You can adjust the upper limit as needed
        for _ in range(num_monsters):
            while True:
                monster_x = random.randint(0, self.width - 1)
                monster_y = random.randint(0, self.height - 1)
                monster_level = random.choice(list(self.monster_levels.keys()))

                # Make sure the monster is not blocked by obstacles, the player, the exit, or other monsters
                if (
                    self.level[monster_y][monster_x] == '.' and
                    (monster_x != self.player_x or monster_y != self.player_y) and
                    (monster_x != self.exit_x or monster_y != self.exit_y)
                ):
                    break

            # Use different symbols for different monster levels
            monster_symbol = self.get_monster_symbol(monster_level)
            self.level[monster_y][monster_x] = monster_symbol
            self.monsters.append({'x': monster_x, 'y': monster_y, 'level': monster_level})


        # Record the initial number of items
        self.initial_items = sum(row.count('I') for row in self.level)
        self.initial_monsters = len(self.monsters)
        
    def move_monsters(self):
        for monster in self.monsters:
            # Attempt to move the monster away from the player while avoiding obstacles and other objects
            move_options = []

            for dx in [-1, 0, 1]:  # Only consider horizontal movements
                for dy in [-1, 0, 1]:  # Only consider vertical movements
                    # Skip diagonal movements
                    if dx != 0 and dy != 0:
                        continue

                    new_x, new_y = monster['x'] + dx, monster['y'] + dy

                    # Check if the new position is within the boundaries
                    if 0 <= new_x < self.width and 0 <= new_y < self.height:
                        # Check if the new position is not an obstacle and is not occupied by items, the player, or the exit
                        if (
                            self.level[new_y][new_x] == '.' and
                            not any(item['x'] == new_x and item['y'] == new_y for item in self.monsters) and
                            not (new_x == self.player_x or new_y == self.player_y) and
                            not (new_x == self.exit_x or new_y == self.exit_y)
                        ):
                            move_options.append((dx, dy))

            if move_options:
                # Randomly choose one of the available moves
                move_direction = random.choice(move_options)
                new_x, new_y = monster['x'] + move_direction[0], monster['y'] + move_direction[1]

                # Check if the player is adjacent to the monster
                if abs(new_x - self.player_x) <= 1 and abs(new_y - self.player_y) <= 1:
                    # Player is facing the monster, initiate combat
                    monster_level = monster['level']
                    items_dropped = self.combat(monster_level)
                    # Update the number of items collected
                    self.items_collected += items_dropped

                    # Remove the defeated monster from the map
                    self.level[monster['y']][monster['x']] = '.'
                    self.monsters.remove(monster)
                    self.monsters_defeated += 1

                else:
                    # Move the monster
                    self.level[monster['y']][monster['x']] = '.'  # Clear the current monster position
                    self.level[new_y][new_x] = self.get_monster_symbol(monster['level'])
                    monster['x'], monster['y'] = new_x, new_y

    def animate_text(self, text, delay=0.1):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def combat(self, monster_level):
        monster_symbol = self.get_monster_symbol(monster_level)
        print(f"Combat! You encountered a {monster_level} bogey ({monster_symbol}).")
        
        # Calculate the number of steps based on the monster's level
        steps_cost = self.monster_levels.get(monster_level, 0)
        print(f"Attacking a {monster_level} bogey costs {steps_cost} step(s).")
        
        while True:
            action = input("Choose your action (Attack[A]/Run[R]): ").upper()
            if action == 'A':
                print(f"You attacked the {monster_level} bogey!")
                # Get the number of items dropped based on monster level
                items_dropped = self.monster_levels.get(monster_level, 0)
                print(f"You obtained {items_dropped} core(s) from the {monster_level} bogey.")
                
                # Deduct steps based on the monster's level
                self.steps += steps_cost
                
                return items_dropped
            elif action == 'R':
                print("You ran away from the bogey.")
                return 0  # No items dropped if the player runs away
            else:
                print("Invalid action. Try again.")

    def clear_screen(self):
        # Check the operating system and use the appropriate command to clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_monster_symbol(self, monster_level):
        # Map monster levels to symbols
        level_symbol_map = {'Common': 'C', 'Normal': 'N', 'Rare': 'R'}
        return level_symbol_map.get(monster_level, 'M')  # Default to 'M' if level is not recognized

    def print_level(self):
        self.clear_screen()  # Clear the console screen
        for row in self.level:
            print(" ".join(row))

    def animate_logo(self, logo, delay=0.1):
        for frame in logo:
            self.clear_screen()
            print(frame)
            time.sleep(delay)

    def display_rules(self):
        self.clear_screen()
        rules = """
        Welcome to Scavenger!

        Rules:
        - Navigate the map using WASD keys.
        - Collect as many cores (I) as you can.
        - Defeat bogeys (C, N, R) to gain extra cores.
        - Common bogeys yield 1 core and cost 1 step.
        - Normal bogeys yield 2 cores and cost 2 steps.
        - Rare bogeys yield 3 cores and cost 3 steps.
        - Reach the exit (E) to finish the game.
        - Be cautious! The number of steps should not exceed 3 times the cores collected.

        Legend:
        P - Player
        E - Exit
        I - Core
        C, N, R - Common, Normal, Rare bogeys
        # - Obstacle

        Good luck!
        """
        print(rules)
        print("Press any key to exit")
        msvcrt.getch()
        self.game_state = self.prev_game_state

    def display_lore(self):
        self.clear_screen()
        lore = """
        You are remote-controlling a voyager drone on a perilous area of a 
        planet in search for oxygen cores. Collect as many cores as you can. 
        You can choose to engage in combat with bogeys to obtain extra cores, 
        but remember that your drone can only handle so many steps.

        MODEL: BOEE OXE9
        """
        print(lore)
        print("Press any key to resume the game")
        msvcrt.getch()
        self.game_state = self.prev_game_state

    def play(self):
        logo_frames = [
            r"""
   ______   _______  _______  _______    _______           _______  _______ 
  (  ___ \ (  ___  )(  ___  )(  ____ \  (  ___  )|\     /|(  ____ \(  ____ )
  | (   ) )| (   ) || (   ) || (    \/  | (   ) |( \   / )| (    \/| (    )|
  | (__/ / | |   | || |   | || (__      | |   | | \ (_) / | (__    | (____)|
  |  __ (  | |   | || |   | ||  __)     | |   | |  ) _ (  |  __)   (_____ ( 
  | (  \ \ | |   | || |   | || (        | |   | | / ( ) \ | (            ) )
  | )___) )| (___) || (___) || (____/\  | (___) |( /   \ )| (____/\/\____) |
  |/ \___/ (_______)(_______/(_______/  (_______)|/     \| (_______/\_______)
                                                          
            """,
            r"""
   ______   _______  _______  _______    _______           _______  _______ 
  (  ___ \ (  ___  )(  ___  )(  ____ \  (  ___  )|\     /|(  ____ \(  ____ )
  | (   ) )| (   ) || (   ) || (    \/  | (   ) |( \   / )| (    \/| (    )|
  | (__/ / | |   | || |   | || (__      | |   | | \ (_) / | (__    | (____)|
  |  __ (  | |   | || |   | ||  __)     | |   | |  ) _ (  |  __)   (_____ ( 
  | (  \ \ | |   | || |   | || (        | |   | | / ( ) \ | (            ) )
  | )___) )| (___) || (___) || (____/\  | (___) |( /   \ )| (____/\/\____) |
  |/ \___/ (_______)(_______/(_______/  (_______)|/     \| (_______/\_______)
                                                           
            """,
        ]
        self.animate_text("Welcome to Scavenger", delay=0.1)
        time.sleep(1)
        while True:
            self.clear_screen()
            print("Main Menu:")
            print("1. Read Rules (H)")
            print("2. Read Lore (L)")
            print("3. Deploy Drone (D)")

            option = input("Select an option: ").upper()

            if option == 'H':
                self.display_rules()
            elif option == 'L':
                self.display_lore()
            elif option == 'D':
                break
            else:
                print("Invalid option. Please try again.")

        self.animate_logo(logo_frames, delay=1.0)
        time.sleep(1) 
        self.animate_text("Deploying...", delay=0.2)
        time.sleep(1)
        self.generate_level()

        while True:
            self.items_collected = 0
            self.steps = 0
            self.monsters_defeated = 0
            self.generate_level()
            self.print_level()
         
            emergency_exit = input("Enter 'E' for emergency exit, or any other key to continue: ").upper()

            if emergency_exit == 'E':
                print("Emergency exit activated. Deploying a new drone...")
                time.sleep(1)
                continue  # Start a new instance of the game

            while True:
                # Check if the player reached the exit
                if self.player_x == self.exit_x and self.player_y == self.exit_y:
                    print(f"You reached the exit with {self.items_collected} core(s) while defeating {self.monsters_defeated} bogey(s) in {self.steps} steps.")

                    # Check for missed items and monsters
                    missed_items = self.num_items_to_collect - self.items_collected
                    missed_monsters = len(self.monsters)

                    if missed_items > 0:
                        print(f"You missed {missed_items} core(s) on the map.")
                    if missed_monsters > 0:
                        print(f"You missed {missed_monsters} bogey(s) on the map.")

                    if missed_items == 0 and missed_monsters == 0:
                        print("You cleared the field, well done!")
                    
                    # Check for drone malfunction condition
                    if self.steps > 3 * self.items_collected:  # Compare with three times the initial number of items
                        print("Drone malfunctioned, mission failed.")
                        self.total_items_collected = 0
                    else:
                        # Update the total_items_collected attribute
                        self.total_items_collected += self.items_collected
                        print(f"You collected a total of {self.total_items_collected} core(s).")
                    break

                self.print_level()

                # Check if there's an item at the player's location
                if self.level[self.player_y][self.player_x] == 'I':
                    print("You found a core!")
                    self.items_collected += 1
                    self.level[self.player_y][self.player_x] = '.'  # Remove the collected item from the map

                # Check if there's a monster at the player's location
                for monster in self.monsters:
                    if self.player_x == monster['x'] and self.player_y == monster['y']:
                        monster_level = monster['level']
                        # Combat occurs if the player bumps into a monster
                        items_dropped = self.combat(monster_level)
                        # Update the number of items collected
                        self.items_collected += items_dropped

                        # Remove the defeated monster from the map
                        self.level[monster['y']][monster['x']] = '.'
                        self.monsters.remove(monster)
                        self.monsters_defeated += 1

                        break  # Exit the loop after encountering and defeating one monster

                # Get player input for movement
                move = input("Enter (W/A/S/D) to move: ").upper()

                # Save the player's current position for potential use in combat
                self.prev_player_x, self.prev_player_y = self.player_x, self.player_y

                # Update player position based on input
                new_player_x, new_player_y = self.player_x, self.player_y
                if move == 'W' and self.player_y > 0:
                    new_player_y -= 1
                elif move == 'A' and self.player_x > 0:
                    new_player_x -= 1
                elif move == 'S' and self.player_y < self.height - 1:
                    new_player_y += 1
                elif move == 'D' and self.player_x < self.width - 1:
                    new_player_x += 1
                else:
                    print("Invalid move. Try again.")
                    continue

                # Check if the new position is not an obstacle
                if self.level[new_player_y][new_player_x] != '#':
                    # Clear the old player position
                    self.level[self.player_y][self.player_x] = '.'

                    # Check if there's an item at the new position
                    if self.level[new_player_y][new_player_x] == 'I':
                        print("You found a core!")
                        self.items_collected += 1
                        self.level[new_player_y][new_player_x] = '.'  # Remove the collected item from the map

                    # Update the player's position
                    self.player_x, self.player_y = new_player_x, new_player_y
                    # Set the new player position in the level
                    self.level[self.player_y][self.player_x] = 'P'

                    # Move monsters away from the player
                    self.move_monsters()

                    # Increment the step counter
                    self.steps += 1
                else:
                    print("You cannot move through obstacles. Try again.")

            replay = input("Deploy drone? (Y/N): ").upper()
            if replay != 'Y':
                # Display a summary message about missed items or monsters
                missed_items = self.num_items_to_collect - self.items_collected
                missed_monsters = len(self.monsters)

                if missed_items > 0:
                    print(f"You missed {missed_items} core(s) on the map.")
                if missed_monsters > 0:
                    print(f"You missed {missed_monsters} bogey(s) on the map.")

                print("Until next time.")
                break

if __name__ == "__main__":
    game = RogueLikeGame(width=10, height=5, num_items_to_collect=3)
    game.play()