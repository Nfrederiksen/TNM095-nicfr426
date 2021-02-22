# TNM095-nicfr426
Project for Artificial Intelligence for Interactive Media course. The game is console-based for simplicity.

  - HE = Heuristics Player (obeys if-statements)
  - RA = Random Player
  - QT = Q table Player

Files ending with _ duel are where you can play games against the AI.
The other are for training. 

## Summary:
This project was made during the course TNM095 Artificial Intelligence in Interactive Media at Linkoping University.
A new game inspired by Tic-tac-toe was created, named Tic-trap-toe and was implemented in Python 3. 
The game is a turn based board game, much like Tic-tac-toe but with a twist. New rules have the players trying
to predict the other ones actions.

An AI agent was trained to play the game using Reinforcement Learning
technique Q-learning. Q-learning is a version of machine learning where the agent learns to optimize the policy
by the rewards given.

It generally explores the world by doing an action and seeing what reward it receives. The
world is represented as different states and for each state the agent can make a few actions. In this case, the
state was represented by the layout of the board together with a players current prediction. The possible actions
were piece placements, piece prediction and piece removal.

There were many different methods for solving a problem like this. In this instance, Q-learning was chosen and was proven to be a good method. The agent
was able to learn the game and play it at a reasonably competitive level versus an average human player.

Even though it was trained to never lose the same way twice it still did not always know what the optimal play was at
states in which it had only seen once or twice. This was one of the major reasons why a perfectly playing AI
agent could not be trained in this project.
