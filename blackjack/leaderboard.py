"""Модуль вывода табллицы лидеров"""

import pygame
import utils
import bdclass
from sys import exit

fps = 60
white = (255, 255, 255)
gray = (25, 25, 25)
border_color = (100, 100, 100)  # Цвет границ

table_x = 70
table_y = 100
row_height = 60
col_widths = [300, 150, 150]

def start():

    button_surface = pygame.Surface((0, 0))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    width_relative = width/1000
    height_relative = height/750
    pygame.font.match_font('font.otf')
    font_name = pygame.font.Font('font.otf', 32)
    font_table = pygame.font.Font('font.otf', 22)

    tname = font_name.render("LEADERBOARD", True, white)
    text_name = utils.Text(tname,
                           screen.get_size(),
                           (20 * width_relative, 20 * height_relative))
    tname_height = tname.get_size()[1]

    top_10 = sorted(bdclass.Scorelist("all").score_list(), key=lambda x: (x['win'], -x['lose']), reverse=True)[:10]

    headers = ["Nickname", "Win", "Lose"]
    
    total_table_width = sum(col_widths) * width_relative
    standard_col_spacing = 25 * width_relative
    total_spacing_width = standard_col_spacing * (len(headers) - 1)
    total_width_needed = total_table_width + total_spacing_width
    
    table_start_x = (width - total_width_needed) / 2
    

    table_start_y = (tname_height + 50) * height_relative
    col_spacing = standard_col_spacing
    

    border_width = 3
    cell_padding = 10
    
    header_texts = []
    header_x = table_start_x
    
    for i, header in enumerate(headers):
        header_text = font_table.render(header, True, white)
        header_texts.append({
            'text': header_text,
            'x': header_x + cell_padding,
            'y': table_start_y + cell_padding
        })

        header_x += col_widths[i] * width_relative + col_spacing
    
    player_texts = []
    
    header_to_first_row = 45 * height_relative 
    row_spacing = 40 * height_relative
    
    row_y_positions = []
    
    row_y_positions.append(table_start_y)
    
    for row_idx, player in enumerate(top_10):
        if row_idx == 0:
            player_y = table_start_y + header_to_first_row
        else:
            player_y = table_start_y + header_to_first_row + (row_idx * row_spacing)
            
        row_y_positions.append(player_y)
        
        player_x = table_start_x
        
        nickname_text = font_table.render(player['username'], True, white)
        player_texts.append({
            'text': nickname_text,
            'x': player_x + cell_padding,
            'y': player_y + cell_padding
        })
        
        player_x += col_widths[0] * width_relative + col_spacing
        win_text = font_table.render(str(player['win']), True, white)
        player_texts.append({
            'text': win_text,
            'x': player_x + cell_padding,
            'y': player_y + cell_padding
        })
        
        player_x += col_widths[1] * width_relative + col_spacing
        lose_text = font_table.render(str(player['lose']), True, white)
        player_texts.append({
            'text': lose_text,
            'x': player_x + cell_padding,
            'y': player_y + cell_padding
        })

    last_row_y = table_start_y + header_to_first_row + (len(top_10) * row_spacing)
    
    for i in range(len(top_10)):
        y_pos = table_start_y + header_to_first_row + (i * row_spacing)
        row_y_positions.append(y_pos)

    texit = font_table.render("BACK", True, white)
    texit_width, texit_height = texit.get_size()
    text_exit = utils.Text(texit,
                        screen.get_size(),
                        ((width - texit_width * width_relative) // 2,
                        (height - (texit_height + 10) * height_relative)))
    button_back_rect = pygame.Rect((width - texit_width * width_relative) // 2,
                                (height - (texit_height + 10) * height_relative),
                                texit_width * width_relative,
                                texit_height * height_relative)

    leaderboard = True
    while leaderboard:

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                leaderboard = False
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_back_rect.collidepoint(event.pos):
                    leaderboard = False

        screen.fill(gray)
        screen.blit(text_name.text_scale, text_name.text_rect)
        
        # Внешняя граница таблицы
        top_left = (table_start_x - 5, table_start_y - 5)
        top_right = (table_start_x + total_width_needed + 5, table_start_y - 5)
        bottom_left = (table_start_x - 5, last_row_y + 5)
        bottom_right = (table_start_x + total_width_needed + 5, last_row_y + 5)
        

        pygame.draw.line(screen, border_color, top_left, top_right, border_width)

        pygame.draw.line(screen, border_color, top_left, bottom_left, border_width)

        pygame.draw.line(screen, border_color, top_right, bottom_right, border_width)

        pygame.draw.line(screen, border_color, bottom_left, bottom_right, border_width)
        
        # 2. Горизонтальные границы между строками 
        for i in range(1, len(row_y_positions)):
            y_pos = row_y_positions[i] + cell_padding * 0.7 
            

            if i == 1:
                continue
                
            pygame.draw.line(
                screen, 
                border_color, 
                (table_start_x, y_pos),
                (table_start_x + total_width_needed, y_pos), 
                border_width
            )
        
        # 3. Вертикальные границы между колонками
        current_x = table_start_x
        for i in range(len(headers)):
            if i < len(headers) - 1:
                line_x = current_x + col_widths[i] * width_relative + col_spacing/2
                pygame.draw.line(
                    screen,
                    border_color,
                    (line_x, table_start_y),
                    (line_x, last_row_y),
                    border_width
                )
            
            current_x += col_widths[i] * width_relative + col_spacing
        
        for header in header_texts:
            screen.blit(header['text'], (header['x'], header['y']))
        
        for player_text in player_texts:
            screen.blit(player_text['text'], (player_text['x'], player_text['y']))
        
        screen.blit(button_surface, (button_back_rect.x, button_back_rect.y))
        screen.blit(text_exit.text_scale, text_exit.text_rect)
        pygame.display.update()