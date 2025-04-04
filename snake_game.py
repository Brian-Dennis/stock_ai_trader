#!/usr/bin/env python3
"""
Snake Game Implementation using curses
A classic snake game where the player controls a snake to eat food and grow longer
without hitting walls or itself.
"""
import curses
import random
import sys
import time
import locale

def setup_window():
    """Initialize and configure the curses window."""
    # Set locale to handle Unicode characters
    locale.setlocale(locale.LC_ALL, '')
    
    # Initialize curses
    stdscr = curses.initscr()
    # Don't echo keypresses to the screen
    curses.noecho()
    # React to keys instantly without Enter key
    curses.cbreak()
    # Hide the cursor
    curses.curs_set(0)
    # Enable special keys like arrows
    stdscr.keypad(True)
    # Set timeout for getch to handle both input and game updates
    stdscr.timeout(100)  # Refresh every 100ms
    
    # Start color if supported
    if curses.has_colors():
        curses.start_color()
        # Define color pairs
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Border
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score
    
    return stdscr

def cleanup(stdscr=None):
    """Clean up curses settings to restore terminal to normal state.
    Handles errors that might occur during cleanup.
    """
    try:
        if stdscr is not None:
            stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
    except Exception as e:
        print(f"Error during cleanup: {e}")
        # Make a final attempt to reset terminal
        try:
            curses.endwin()
        except:
            pass

def generate_food(snake, height, width):
    """Generate food at a random position that's not occupied by the snake."""
    # Create list of all valid positions
    valid_positions = []
    for y in range(1, height-1):
        for x in range(1, width-1):
            pos = [y, x]
            if pos not in snake:
                valid_positions.append(pos)
    
    # If no valid positions left, return a position near the border
    if not valid_positions:
        return [1, 1]
    
    # Get random valid position
    food_pos = random.choice(valid_positions)
    
    # Double-check that the position is valid
    if food_pos[0] <= 0 or food_pos[0] >= height-1 or food_pos[1] <= 0 or food_pos[1] >= width-1:
        # Fallback to a safe position
        return [height//2, width//2]
    
    return food_pos

def display_game_over(stdscr, score):
    """Display game over message and final score."""
    try:
        height, width = stdscr.getmaxyx()
        game_over_msg = "GAME OVER!"
        score_msg = f"Final Score: {score}"
        exit_msg = "Press 'q' to quit or 'r' to restart"
        
        # Add color if supported
        has_color = curses.has_colors()
        
        # Clear the screen
        stdscr.clear()
        
        # Display game over message centered (with error handling)
        try:
            # Display game over with red color
            if has_color:
                stdscr.attron(curses.color_pair(2))  # Red for game over
            stdscr.addstr(height//2 - 2, (width - len(game_over_msg))//2, game_over_msg)
            if has_color:
                stdscr.attroff(curses.color_pair(2))
            
            # Display score with yellow color
            if has_color:
                stdscr.attron(curses.color_pair(4))  # Yellow for score
            stdscr.addstr(height//2, (width - len(score_msg))//2, score_msg)
            if has_color:
                stdscr.attroff(curses.color_pair(4))
            
            # Display exit instructions
            stdscr.addstr(height//2 + 2, (width - len(exit_msg))//2, exit_msg)
        except curses.error:
            # Fallback if positioning fails
            try:
                stdscr.clear()
                stdscr.addstr(0, 0, f"{game_over_msg} - {score_msg}")
                stdscr.addstr(1, 0, exit_msg)
            except curses.error:
                pass  # Terminal might be too small
        
        stdscr.refresh()
    except Exception as e:
        # Handle any other errors that might occur
        try:
            stdscr.clear()
            safe_addstr(stdscr, 0, 0, "Game Over!")
            safe_addstr(stdscr, 1, 0, f"Score: {score}")
            stdscr.refresh()
        except:
            pass
    
    # Wait for user to quit or restart
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            return False  # Quit
        elif key == ord('r'):
            return True   # Restart

def safe_addstr(stdscr, y, x, string):
    """Safely add a string to the screen with error handling."""
    try:
        stdscr.addstr(y, x, string)
    except curses.error:
        pass  # Ignore if position is invalid

def safe_addch(stdscr, y, x, char):
    """Safely add a character to the screen with error handling."""
    try:
        stdscr.addch(y, x, char)
    except curses.error:
        pass  # Ignore if position is invalid

def can_use_unicode():
    """Check if the terminal supports Unicode characters."""
    try:
        return locale.getpreferredencoding().upper() in ('UTF-8', 'UTF8')
    except:
        return False

def main():
    """Main game function."""
    # Initialize stdscr to None before the try block
    stdscr = None
    
    try:
        # Setup the screen
        stdscr = setup_window()
        
        # Game initialization and loop
        while True:
            # Get terminal dimensions
            height, width = stdscr.getmaxyx()
            
            # Check if terminal is too small
            if height < 10 or width < 20:
                try:
                    stdscr.clear()
                    safe_addstr(stdscr, 0, 0, "Terminal too small!")
                    stdscr.refresh()
                    time.sleep(1)
                except curses.error:
                    # In case of error during display, still continue
                    pass
                continue
                
            # Initialize snake in the middle of the screen
            snake = [[height//2, width//4]]
            # Initialize snake direction (right)
            direction = [0, 1]
            
            # Generate initial food
            food = generate_food(snake, height, width)
            
            # Initialize score
            score = 0
            
            # Display instructions
            try:
                stdscr.clear()
                # Display score with color if supported
                if curses.has_colors():
                    stdscr.attron(curses.color_pair(4))
                safe_addstr(stdscr, 0, 0, f"Score: {score}")
                if curses.has_colors():
                    stdscr.attroff(curses.color_pair(4))
                
                safe_addstr(stdscr, height-1, 0, "Controls: Arrow Keys/WASD | Quit: q")
            except curses.error:
                # Continue even if display fails
                pass
            
            # Draw border with box drawing characters if supported
            try:
                # Set border color if supported
                if curses.has_colors():
                    stdscr.attron(curses.color_pair(3))
                
                use_unicode = can_use_unicode()
                
                # Draw the border with box drawing characters or ASCII fallback
                if use_unicode:
                    # Top-left corner
                    safe_addstr(stdscr, 0, 0, "┌")
                    # Top-right corner
                    safe_addstr(stdscr, 0, width-1, "┐")
                    # Bottom-left corner
                    safe_addstr(stdscr, height-1, 0, "└")
                    # Bottom-right corner
                    safe_addstr(stdscr, height-1, width-1, "┘")
                    
                    # Top and bottom edges
                    for x in range(1, width-1):
                        safe_addstr(stdscr, 0, x, "─")
                        safe_addstr(stdscr, height-1, x, "─")
                    
                    # Left and right edges
                    for y in range(1, height-1):
                        safe_addstr(stdscr, y, 0, "│")
                        safe_addstr(stdscr, y, width-1, "│")
                else:
                    # ASCII fallback
                    for y in range(height):
                        for x in range(width):
                            if y == 0 or y == height-1 or x == 0 or x == width-1:
                                safe_addch(stdscr, y, x, '#')
                
                if curses.has_colors():
                    stdscr.attroff(curses.color_pair(3))
                
                # Draw initial snake with different head and body
                use_unicode = can_use_unicode()
                
                # Apply green color for snake if supported
                if curses.has_colors():
                    stdscr.attron(curses.color_pair(1))
                
                # Draw head with special character
                if use_unicode:
                    safe_addstr(stdscr, snake[0][0], snake[0][1], "⚪")
                else:
                    safe_addch(stdscr, snake[0][0], snake[0][1], 'O')
                
                # Draw body segments if any
                for segment in snake[1:]:
                    if use_unicode:
                        safe_addstr(stdscr, segment[0], segment[1], "●")
                    else:
                        safe_addch(stdscr, segment[0], segment[1], 'o')
                
                if curses.has_colors():
                    stdscr.attroff(curses.color_pair(1))
                
                # Draw food with apple character if Unicode supported
                # Apply red color for food if supported
                if curses.has_colors():
                    stdscr.attron(curses.color_pair(2))
                
                if can_use_unicode():
                    safe_addstr(stdscr, food[0], food[1], "🍎")
                else:
                    safe_addch(stdscr, food[0], food[1], '*')
                
                if curses.has_colors():
                    stdscr.attroff(curses.color_pair(2))
            except curses.error:
                # Continue even if drawing fails
                pass
            
            stdscr.refresh()
            
            # Game loop
            game_over = False
            while not game_over:
                # Check for terminal resize
                new_height, new_width = stdscr.getmaxyx()
                if new_height != height or new_width != width:
                    # Terminal resized, restart the game setup
                    break
                
                # Get user input
                key = stdscr.getch()
                
                # Parse key input
                if key == ord('q'):
                    return  # Quit the game
                
                # Store previous direction to detect rapid changes
                prev_direction = direction.copy()
                
                # Only change direction if it's not the opposite direction
                if key in [curses.KEY_UP, ord('w'), ord('W')]:
                    if direction != [1, 0]:  # Not moving down
                        direction = [-1, 0]  # Up
                elif key in [curses.KEY_DOWN, ord('s'), ord('S')]:
                    if direction != [-1, 0]:  # Not moving up
                        direction = [1, 0]   # Down
                elif key in [curses.KEY_LEFT, ord('a'), ord('A')]:
                    if direction != [0, 1]:  # Not moving right
                        direction = [0, -1]  # Left
                elif key in [curses.KEY_RIGHT, ord('d'), ord('D')]:
                    if direction != [0, -1]:  # Not moving left
                        direction = [0, 1]   # Right
                
                # Calculate new head position based on direction
                new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
                
                # Check if new head would collide with body (except tail which will move)
                # Only apply this check for snakes with more than 3 segments
                if len(snake) > 3 and new_head in snake[:-1]:
                    # Revert to previous direction if this would cause collision
                    direction = prev_direction
                    new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
                
                # New head position already calculated above
                snake.insert(0, new_head)
                
                # Check for collisions with wall
                if (new_head[0] == 0 or new_head[0] == height-1 or 
                    new_head[1] == 0 or new_head[1] == width-1):
                    game_over = True
                    
                # Check for collisions with self (except when just starting)
                # Don't check the last segment (tail) as it will be removed unless food was eaten
                if len(snake) > 1:
                    collision_body = snake[1:-1] if len(snake) > 2 else snake[1:]
                    if new_head in collision_body:
                        game_over = True
                
                # Check if snake ate the food
                # Check if snake ate the food
                if snake[0] == food:
                    # Generate new food
                    food = generate_food(snake, height, width)
                    
                    # Debug check to ensure food is in a valid position
                    if food[0] <= 0 or food[0] >= height-1 or food[1] <= 0 or food[1] >= width-1:
                        # If somehow food is in an invalid position, force a valid position
                        stdscr.addstr(0, width-20, "DEBUG: Fixed invalid food position")
                        food = [height//2, width//2]
                        # Ensure it's not on the snake
                        while food in snake:
                            food[0] = max(1, min(height-2, food[0] + 1))
                            food[1] = max(1, min(width-2, food[1] + 1))
                    
                    # Increase score
                    score += 10
                    # Update score display with color
                    if curses.has_colors():
                        stdscr.attron(curses.color_pair(4))
                    safe_addstr(stdscr, 0, 0, f"Score: {score}    ")
                    if curses.has_colors():
                        stdscr.attroff(curses.color_pair(4))
                else:
                    # Remove tail segment only if we didn't eat food
                    tail = snake.pop()
                    # Erase the tail segment on screen
                    safe_addch(stdscr, tail[0], tail[1], ' ')
                
                # Always draw the food (moved outside the if-else block)
                # Draw food with color
                if curses.has_colors():
                    stdscr.attron(curses.color_pair(2))
                if can_use_unicode():
                    safe_addstr(stdscr, food[0], food[1], "\U0001F34E")
                else:
                    safe_addch(stdscr, food[0], food[1], '*')
                if curses.has_colors():
                    stdscr.attroff(curses.color_pair(2))
                # Draw new head with special character
                try:
                    if curses.has_colors():
                        stdscr.attron(curses.color_pair(1))
                    
                    # Draw head (first segment)
                    if can_use_unicode():
                        safe_addstr(stdscr, snake[0][0], snake[0][1], "⚪")
                    else:
                        safe_addch(stdscr, snake[0][0], snake[0][1], 'O')
                    
                    # If snake has more than one segment, update the second segment
                    # to be a body character (it was previously a head)
                    if len(snake) > 1:
                        if can_use_unicode():
                            safe_addstr(stdscr, snake[1][0], snake[1][1], "●")
                        else:
                            safe_addch(stdscr, snake[1][0], snake[1][1], 'o')
                    
                    if curses.has_colors():
                        stdscr.attroff(curses.color_pair(1))
                except Exception:
                    # This can happen during resizing or terminal errors
                    break
                
            # Game over logic
            if game_over:
                if display_game_over(stdscr, score):
                    continue  # Restart
                else:
                    break  # Quit
    
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nGame terminated by user (Ctrl+C)")
    except curses.error as e:
        # Specific handling for curses errors
        print(f"Terminal error: {e}")
    except Exception as e:
        # Ensure terminal is always restored even if another error occurs
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up and restore terminal
        cleanup(stdscr)

if __name__ == "__main__":
    main()

