# Scavenger: A Rogue-like Adventure Game (In Development)

## Introduction

Scavenger is a text-based Rogue-like adventure game where you control a voyager drone exploring a perilous area of a distant planet in search of oxygen cores. Your mission is to collect as many cores as possible, defeat hostile bogeys to gain extra cores, and ultimately reach the exit to successfully complete each mission.

**Note: This game is still in development, and improvements are ongoing.**

## Table of Contents
- [Introduction](#introduction)
- [How to Play](#how-to-play)
- [Game Mechanics](#game-mechanics)
- [Rules](#rules)
- [Installation](#installation)
- [Controls](#controls)
- [Acknowledgements](#acknowledgements)

## How to Play

1. **Deploy Drone**: Start the game by selecting the "Deploy Drone (D)" option from the main menu.
2. **Navigate the Drone**: Use the WASD keys to navigate the drone across the map.
3. **Collect Cores**: Collect oxygen cores (I) scattered throughout the map.
4. **Combat**: Encounter bogeys (C, N, R) and engage in combat to gain extra cores.
5. **Reach the Exit**: Navigate to the exit (E) to complete the mission.
6. **Emergency Exit**: At any time, you can use the emergency exit option (E) to redeploy the drone and start a new instance of the game. Use this option wisely, as it can only be used once.

## Game Mechanics

- **Player (P)**: Represented by 'P' on the map, the player navigates the drone through the map to collect cores and reach the exit.
- **Cores (I)**: Collect oxygen cores to increase your score. Each core contributes to your total collected items.
- **Bogeys (C, N, R)**: Encounter and defeat common (C), normal (N), and rare (R) bogeys to gain extra cores. Combat costs steps, and different bogey levels yield different rewards.
- **Exit (E)**: Reach the exit to successfully complete the mission and tally your total collected cores.
- **Obstacles (#)**: Obstacles block the drone's path. Plan your movements strategically to avoid obstacles.

## Rules

1. **Navigation**: Use the WASD keys to move the drone (P) across the map.
2. **Emergency Exit**: You can use the emergency exit option (E) at the beginning of the game to redeploy the drone. Use it wisely, as it can only be used once.
3. **Combat**: Encounter bogeys to initiate combat. Choose between attacking (A) or running away (R). Combat costs steps, and the outcome determines the number of extra cores obtained.
4. **Mission Completion**: Reach the exit to successfully complete the mission. The game evaluates your performance based on the number of cores collected, bogeys defeated, and steps taken.
5. **Drone Malfunction**: If the number of steps exceeds three times the initial number of items collected, the drone malfunctions, and the mission fails.

## Installation

Clone the repository to your local machine and run the game using Python 3.

```bash
git clone https://github.com/donmaruko/scavenger.git
cd scavenger
python scavenger.py
```

## Controls

- **W/A/S/D**: Navigate the drone up/left/down/right.
- **E**: Use the emergency exit at the beginning of each game.

## Acknowledgements

This game is inspired by classic Rogue-like games, showcasing procedural level generation, strategic movement, and combat mechanics. The concept of collecting cores and reaching a certain goal the more you progress has also been inspired by Lethal Company! I created this as a programming exercise and is open for contributions and improvements. Feel free to explore and enhance the game's features!

Enjoy your journey with the Scavenger drone!
