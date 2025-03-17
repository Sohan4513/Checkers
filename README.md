# **Checkers Game**

## **Overview**
The **Checkers Game** is a two-player board game implementing standard checkers rules, including diagonal movement, jumping over opponents, and king promotions.

## **Rules**
1. A checker **moves diagonally** toward the opponent’s side.
2. A checker can **capture an opponent’s piece** by jumping over it.
3. A checker can perform **multiple jumps** if possible.
4. A checker becomes a **king** upon reaching the last row, allowing movement in both directions.

## **Installation**
### **Dependencies**
To run the game, install the required dependencies from `requirements.txt`:
```sh
pip install -r requirements.txt
```
Dependencies:
- `colorama==0.4.6`
- `pygame==2.1.2`
- `pytest==7.2.1`
- `termcolor==2.2.0`

## **How to Play**
1. Open a terminal and navigate to the project folder.
2. Run the game using:
   ```sh
   python playgame.py
   ```
3. Follow the instructions on the screen to play checkers.

---
