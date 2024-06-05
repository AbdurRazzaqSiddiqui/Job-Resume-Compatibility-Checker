# K214945 ASAD ULLAH KHAN 
import pygame
import sys
from tkinter import Tk, filedialog
import shutil
    
# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Vector Space Model")
destination_path = 'C:/Users/razza/OneDrive/Desktop/Resume_Compatibility-main/data/resume'

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Function to create a button
def draw_button(surface, color, x, y, width, height, text):
    pygame.draw.rect(surface, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    draw_text(text, font, (211, 211, 211), surface, x + width / 2, y + height / 2)

# Function to clear the screen
def clear_screen(surface):
    surface.fill((30, 30, 30))

# Function to check if a point is inside a rectangle
def point_inside_rect(x, y, rect):
    return rect.left <= x <= rect.right and rect.top <= y <= rect.bottom

def select_file():
    Tk().withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()  # Show file dialog to select a file
    return file_path

def copy_file(source_path, destination_path):
    try:
        shutil.copy(source_path, destination_path)
        print("File copied successfully.")
    except IOError as e:
        print(f"Unable to copy file. {e}")
    except:
        print("Unexpected error:", sys.exc_info())

def main_event():
    # Main loop
    state = "start_screen"  # Initial state
    running = True
    query = ""  # Variable to store user input
    input_rect = pygame.Rect((SCREEN_WIDTH - 500) / 2, (SCREEN_HEIGHT / 2) - 30, 500, 35)  # Rectangular box for text input
    back_button_rect = pygame.Rect(SCREEN_WIDTH - 100, 10, 70, 50)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the "Start" button or rectangular box is clicked
                mouse_pos = pygame.mouse.get_pos()
                if state == "start_screen" and start_button_rect.collidepoint(mouse_pos):
                    state = "find_screen"  # Change state to "find_screen"
                elif state == "find_screen" and find_button_rect.collidepoint(mouse_pos):
                    state = "display_query"  # Change state to "display_query"
                elif state == "find_screen" and back_button_rect.collidepoint(mouse_pos):
                    clear_screen(screen)
                    main_event()     
            elif event.type == pygame.KEYDOWN:
                # Check if user is typing when in "find_screen" state
                if state == "find_screen":
                    if event.key == pygame.K_BACKSPACE:
                        # Remove last character from query
                        query = query[:-1]
                    elif len(query) < 100:  # Limiting to 100 characters
                        # Add typed character to query
                        query += event.unicode

        # Draw appropriate content based on the current state
        if state == "start_screen":
            # Clear the screen
            clear_screen(screen)

            # Draw "Start" button
            button_width = 200
            button_height = 50
            start_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) / 2, (SCREEN_HEIGHT - button_height) / 2, button_width, button_height)

            # Title Page titles
            font = pygame.font.Font(None, 50)
            draw_text("INFORMATION RETRIEVAL ASSIGNMENT 2", font, (211, 211, 211), screen, SCREEN_WIDTH // 2, 50)
            font = pygame.font.Font(None, 30)
            draw_text("K214945 Asad Ullah Khan", font, (211, 211, 211), screen, SCREEN_WIDTH // 2, 100)
            draw_button(screen, (62, 62, 66), start_button_rect.x, start_button_rect.y, button_width, button_height, "Proceed")

        elif state == "find_screen":
            # Clear the screen
            clear_screen(screen)

            # # Draw the title "SEARCH"
            # font = pygame.font.Font(None, 60)
            # draw_text("S", font, (66, 133, 244), screen, SCREEN_WIDTH // 2 - 100, (SCREEN_HEIGHT // 2) - 70)
            # draw_text("E", font, (219, 68, 5), screen, SCREEN_WIDTH // 2 - 60, (SCREEN_HEIGHT // 2) - 70)
            # draw_text("A", font, (244, 180, 0), screen, SCREEN_WIDTH // 2 - 20, (SCREEN_HEIGHT // 2) - 70)
            # draw_text("R", font, (66, 133, 244), screen, SCREEN_WIDTH // 2 + 20, (SCREEN_HEIGHT // 2) - 70)
            # draw_text("C", font, (15, 157, 88), screen, SCREEN_WIDTH // 2 + 60, (SCREEN_HEIGHT // 2) - 70)
            # draw_text("H", font, (219, 68, 5), screen, SCREEN_WIDTH // 2 + 100, (SCREEN_HEIGHT // 2) - 70)

            # # Draw text input box
            # pygame.draw.rect(screen, (62, 62, 66), input_rect)
            # font = pygame.font.Font(None, 24)
            # draw_text(query, font, (211, 211, 211), screen, input_rect.centerx, input_rect.centery)

            # # Draw "Find" button
            # button_width = 30
            # button_height = 30
            # find_button_rect = pygame.Rect(input_rect.right + 10, input_rect.y, button_width, button_height)
            # draw_button(screen, (62, 62, 66), find_button_rect.x, find_button_rect.y, button_width, button_height,"Upload")
            # pygame.draw.rect(screen, (62, 62, 66), back_button_rect)
            # font = pygame.font.Font(None, 24)
            # draw_text("Back", font, (211, 211, 211), screen, back_button_rect.center[0], back_button_rect.centery)

            pygame.display.set_caption("File Upload Example")
            font = pygame.font.Font(None, 36)
            upload_text = font.render("Click to Upload File", True, (255, 255, 255))

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if upload_text.get_rect(center=(200, 150)).collidepoint(event.pos):
                            file_path = select_file()
                            if file_path:
                                print("Selected file:", file_path)
                                copy_file(file_path, destination_path)

                screen.fill((30, 30, 30))
                screen.blit(upload_text, upload_text.get_rect(center=(200, 150)))
                pygame.display.flip()

        elif state == "display_query":
            # Display the query results at the bottom of the screen
            font = pygame.font.Font(None, 24)
            result_rect = pygame.Rect(200, (SCREEN_HEIGHT / 2) + 20, 400, 260)
            pygame.draw.rect(screen, (62, 62, 66), result_rect)

            rank = {}
            rank = query_processing(query)

            draw_text("Resulting Documents: ", font, (211, 211, 211), screen, 400, (SCREEN_HEIGHT / 2) + 40)
            list_width = 400
            list_height = (SCREEN_HEIGHT / 2) + 80
            for r,d in rank:
                if r >= 0.025:
                # Adjusting height and width of results box docids
                    draw_text("Document " + d + "          " + "Rank " + str(round(r,5)), font, (211, 211, 211), screen, list_width, list_height)
                    list_height += 20
                    if list_height == (SCREEN_HEIGHT / 2) + 240:
                        list_height = (SCREEN_HEIGHT / 2) + 80
                        list_width += 100

        # Update the display
        pygame.display.flip()

        mouse_pos = pygame.mouse.get_pos()
        if back_button_rect.collidepoint(mouse_pos):
            main_event()
    
    # Quit Pygame
    pygame.quit()
    sys.exit()

main_event()    
