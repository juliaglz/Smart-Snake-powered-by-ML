This project implements the classic Snake game, enhanced with various Machine Learning (ML) approaches to teach the snake to play autonomously. The goal is to explore how different ML paradigms can be applied to solve a common reinforcement learning problem.

🎮 **Game Objective**
The primary objective of the Snake game is for the snake to grow by consuming apples scattered on the game board, while avoiding collisions with the surrounding walls and its own body. The game continues as long as the snake successfully navigates the environment without hitting obstacles.

🧠 **Machine Learning Approaches**
This project explores both supervised and unsupervised learning techniques to train the snake agent.

+ Supervised Learning
In the supervised approach, the snake learns to play based on labeled data. This involves:

  - Classification: The model is trained to classify optimal moves based on historical gameplay data (e.g., classifying whether moving "left", "right", "up", or "down" leads to a winning or higher-scoring state).

  - Prediction: The model might predict the next best action given the current game state, leveraging features like the snake's position, apple's position, and proximity to walls or its own body.

- Unsupervised Learning (Q-Learning)
The unsupervised approach utilizes Q-learning, allowing the snake to learn through trial and error. The snake agent interacts with the environment, receives rewards for desirable actions (like eating an apple) and penalties for undesirable ones (like colliding), and updates its "Q-values" accordingly.

  Two variations of Q-learning are implemented:
  
    - Q-learning (Without Body Awareness): In this simpler version, the agent primarily considers its position relative to the apple and walls, treating its body segments as static obstacles. The state representation is simplified, focusing on immediate surroundings.
    
    - Q-learning (With Body Awareness): This more complex variation incorporates the snake's entire body as part of the state representation. The agent learns to navigate not only around walls and towards the apple but also to explicitly avoid its own growing body, requiring a more sophisticated state-action space.

🛠️  **Technologies Used**
- Python: The core programming language for the game logic and ML implementations.

- NumPy: Essential for numerical operations and efficient array manipulation, particularly in state representation and Q-table management.

- Pygame (Optional/Implied): A common library for creating 2D games in Python, likely used for the game's visual interface.

- Weka (for Supervised): Used for implementing the classification and prediction models.

- Custom RL Implementation: Q-learning is implemented from scratch to provide a deeper understanding of the algorithm.
