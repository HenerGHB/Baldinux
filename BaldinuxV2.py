import random
import time
import sys
import os
import math


class BaldiGame:
    def __init__(self):
        self.game_over = False
        self.win = False
        self.player_pos = [2, 2]
        self.map_size = 15
        self.school_map = []
        self.baldi_pos = [12, 12]
        self.baldi_speed = 3
        self.baldi_timer = 0
        self.notebooks_found = 0
        self.total_notebooks = 12
        self.notebooks = []
        self.items = []
        self.inventory = []
        self.steps = 0
        self.score = 0
        self.energy = 150
        self.rooms = []
        self.doors = []
        self.generate_map()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def generate_map(self):
        self.school_map = []
        for i in range(self.map_size):
            row = []
            for j in range(self.map_size):
                if i == 0 or i == self.map_size - 1 or j == 0 or j == self.map_size - 1:
                    row.append('█')
                else:
                    if random.random() < 0.15:
                        row.append('█')
                    else:
                        row.append(' ')
            self.school_map.append(row)

        self.create_rooms()
        self.create_corridors()

        self.school_map[self.player_pos[0]][self.player_pos[1]] = ' '
        self.school_map[self.baldi_pos[0]][self.baldi_pos[1]] = ' '

        for _ in range(self.total_notebooks):
            while True:
                x = random.randint(1, self.map_size - 2)
                y = random.randint(1, self.map_size - 2)
                if self.school_map[x][y] == ' ' and [x, y] != self.player_pos and [x, y] != self.baldi_pos:
                    self.notebooks.append([x, y])
                    break

        item_types = ['S', 'B', 'E', 'T', 'K']
        for item in item_types:
            for _ in range(2):
                while True:
                    x = random.randint(1, self.map_size - 2)
                    y = random.randint(1, self.map_size - 2)
                    if self.school_map[x][y] == ' ' and [x, y] != self.player_pos and [x, y] != self.baldi_pos and [x,
                                                                                                                    y] not in self.notebooks:
                        self.items.append([x, y, item])
                        break

    def create_rooms(self):
        num_rooms = random.randint(5, 8)

        for _ in range(num_rooms):
            width = random.randint(3, 5)
            height = random.randint(3, 5)
            x = random.randint(1, self.map_size - width - 1)
            y = random.randint(1, self.map_size - height - 1)

            self.rooms.append((x, y, width, height))

            for i in range(height):
                for j in range(width):
                    if i == 0 or i == height - 1 or j == 0 or j == width - 1:
                        self.school_map[x + i][y + j] = '█'
                    else:
                        self.school_map[x + i][y + j] = ' '

            door_x = x + random.randint(1, height - 2)
            door_y = y + random.randint(1, width - 2)
            if random.choice([True, False]):
                door_x = x if random.choice([True, False]) else x + height - 1
                door_y = y + random.randint(1, width - 2)
            else:
                door_y = y if random.choice([True, False]) else y + width - 1
                door_x = x + random.randint(1, height - 2)

            self.school_map[door_x][door_y] = ' '
            self.doors.append([door_x, door_y])

    def create_corridors(self):
        for i in range(len(self.doors) - 1):
            start = self.doors[i]
            end = self.doors[i + 1]

            x1, y1 = start
            x2, y2 = end

            while x1 != x2:
                if x1 < x2:
                    x1 += 1
                else:
                    x1 -= 1
                if self.school_map[x1][y1] == '█':
                    self.school_map[x1][y1] = ' '

            while y1 != y2:
                if y1 < y2:
                    y1 += 1
                else:
                    y1 -= 1
                if self.school_map[x1][y1] == '█':
                    self.school_map[x1][y1] = ' '

    def print_map(self):
        print("\n" + "=" * 60)
        print(f"ТЕТРАДИ: {self.notebooks_found}/{self.total_notebooks}  ЭНЕРГИЯ: {self.energy}  ХОДЫ: {self.steps}")

        if self.baldi_timer > 0:
            print(f"БАЛДИ ПОЙДЁТ ЧЕРЕЗ: {self.baldi_timer} ход(ов)")
        else:
            print("БАЛДИ ДВИГАЕТСЯ СЛЕДУЮЩИМ ХОДОМ!")

        print("=" * 60 + "\n")

        for i in range(self.map_size):
            for j in range(self.map_size):
                if [i, j] == self.player_pos:
                    print('P', end=' ')
                elif [i, j] == self.baldi_pos:
                    print('B', end=' ')
                elif [i, j] in self.notebooks:
                    print('N', end=' ')
                elif any([i, j] == item[:2] for item in self.items):
                    for item in self.items:
                        if [i, j] == item[:2]:
                            print(item[2], end=' ')
                            break
                else:
                    print(self.school_map[i][j], end=' ')
            print()

        print("\n" + "=" * 60)
        print("ИНВЕНТАРЬ:", ', '.join(self.inventory) if self.inventory else "пусто")
        print("УПРАВЛЕНИЕ: WASD - движение, I - инвентарь, H - помощь, Q - выход")
        print("ПРЕДМЕТЫ: S - Сода, B - Лопата, E - Энергия, T - Телепорт, K - Ключ (открывает дверь)")
        print("=" * 60)

    def move_player(self, direction):
        new_pos = self.player_pos.copy()

        if direction == 'w':
            new_pos[0] -= 1
        elif direction == 's':
            new_pos[0] += 1
        elif direction == 'a':
            new_pos[1] -= 1
        elif direction == 'd':
            new_pos[1] += 1
        else:
            return False

        if 0 <= new_pos[0] < self.map_size and 0 <= new_pos[1] < self.map_size:
            if self.school_map[new_pos[0]][new_pos[1]] == '█':
                if 'Ключ' in self.inventory:
                    print("\nВы использовали ключ, чтобы открыть дверь!")
                    self.inventory.remove('Ключ')
                    self.school_map[new_pos[0]][new_pos[1]] = ' '
                else:
                    print("\nДверь закрыта! Нужен ключ.")
                    return False

            if self.school_map[new_pos[0]][new_pos[1]] != '█':
                self.player_pos = new_pos
                self.steps += 1
                self.energy = max(0, self.energy - 1)

                self.baldi_timer -= 1
                if self.baldi_timer <= 0:
                    self.move_baldi()
                    self.update_baldi_timer()

                self.check_position()
                return True

        return False

    def update_baldi_timer(self):
        if self.notebooks_found == 0:
            self.baldi_speed = random.randint(3, 4)
        elif self.notebooks_found < 4:
            self.baldi_speed = random.randint(2, 3)
        elif self.notebooks_found < 8:
            self.baldi_speed = random.randint(1, 2)
        else:
            self.baldi_speed = 1

        self.baldi_timer = self.baldi_speed

    def check_position(self):
        if self.player_pos == self.baldi_pos:
            self.game_over = True
            print("\nБалди поймал вас! Игра окончена!")
            return

        if self.player_pos in self.notebooks:
            self.notebooks.remove(self.player_pos)
            self.notebooks_found += 1
            self.score += 100
            print(f"\nНайдена тетрадь! Всего: {self.notebooks_found}/{self.total_notebooks}")

            if self.notebooks_found >= self.total_notebooks:
                self.win = True
                self.game_over = True
                print("\nВы нашли все тетради! ПОБЕДА!")

        for i, item in enumerate(self.items):
            if [item[0], item[1]] == self.player_pos:
                item_type = item[2]
                if item_type == 'S':
                    self.inventory.append('Сода')
                    print("\nНайдена Сода! Замедляет Балди на 1 ход")
                elif item_type == 'B':
                    self.inventory.append('Лопата')
                    print("\nНайдена Лопата! Можно отбиться от Балди")
                elif item_type == 'E':
                    self.energy = min(200, self.energy + 50)
                    print(f"\nНайдена энергия! Теперь у вас {self.energy} энергии")
                elif item_type == 'T':
                    print("\nТелепорт активирован! Вы перемещены в случайное место")
                    self.teleport_player()
                elif item_type == 'K':
                    self.inventory.append('Ключ')
                    print("\nНайден Ключ! Можете открыть одну дверь")

                self.items.pop(i)
                self.score += 50
                break

    def teleport_player(self):
        attempts = 0
        while attempts < 50:
            x = random.randint(1, self.map_size - 2)
            y = random.randint(1, self.map_size - 2)
            if self.school_map[x][y] == ' ':
                self.player_pos = [x, y]
                return
            attempts += 1

    def move_baldi(self):
        print(f"\n[Балди делает ход!]")

        if 'Сода' in self.inventory:
            print("Балди замедлен содой! Пропускает ход.")
            self.inventory.remove('Сода')
            return

        dx = self.player_pos[0] - self.baldi_pos[0]
        dy = self.player_pos[1] - self.baldi_pos[1]

        distance = abs(dx) + abs(dy)

        moves = []

        directions = [
            [self.baldi_pos[0] - 1, self.baldi_pos[1]],  # вверх
            [self.baldi_pos[0] + 1, self.baldi_pos[1]],  # вниз
            [self.baldi_pos[0], self.baldi_pos[1] - 1],  # влево
            [self.baldi_pos[0], self.baldi_pos[1] + 1]  # вправо
        ]

        for move in directions:
            x, y = move
            if 0 <= x < self.map_size and 0 <= y < self.map_size:
                if self.school_map[x][y] != '█':
                    new_distance = abs(x - self.player_pos[0]) + abs(y - self.player_pos[1])
                    moves.append(([x, y], new_distance))

        if moves:
            moves.sort(key=lambda x: x[1])
            self.baldi_pos = moves[0][0]

        if self.baldi_pos == self.player_pos:
            if 'Лопата' in self.inventory:
                print("Вы отбились от Балди лопатой!")
                self.inventory.remove('Лопата')
                self.teleport_baldi()
            else:
                self.game_over = True
                print("Балди поймал вас! Игра окончена!")

    def teleport_baldi(self):
        attempts = 0
        while attempts < 50:
            x = random.randint(1, self.map_size - 2)
            y = random.randint(1, self.map_size - 2)
            distance = math.sqrt((x - self.player_pos[0]) ** 2 + (y - self.player_pos[1]) ** 2)
            if self.school_map[x][y] == ' ' and distance > 5:
                self.baldi_pos = [x, y]
                return
            attempts += 1

    def show_inventory(self):
        self.clear_screen()
        print("\n" + "=" * 40)
        print("ИНВЕНТАРЬ:")
        print("=" * 40)

        if not self.inventory:
            print("Инвентарь пуст!")
        else:
            for item in self.inventory:
                print(f"- {item}")

        print("\n" + "=" * 40)
        input("Нажмите Enter для продолжения...")

    def show_help(self):
        self.clear_screen()
        print("\n" + "=" * 40)
        print("ПОМОЩЬ:")
        print("=" * 40)
        print("ЦЕЛЬ: Собрать 12 тетрадей (N), избегая Балди (B)")
        print("\nСИМВОЛЫ НА КАРТЕ:")
        print("P - Вы (игрок)")
        print("B - Балди (враг)")
        print("N - Тетрадь")
        print("█ - Стена/Дверь")
        print("  - Пустое пространство")
        print("S - Сода (замедляет Балди на 1 ход)")
        print("B - Лопата (отбивает Балди)")
        print("E - Энергия (+50 энергии)")
        print("T - Телепорт (случайное перемещение)")
        print("K - Ключ (открывает одну дверь)")
        print("\nУПРАВЛЕНИЕ:")
        print("W - Вверх")
        print("S - Вниз")
        print("A - Влево")
        print("D - Вправо")
        print("I - Инвентарь")
        print("H - Помощь")
        print("Q - Выход")
        print("=" * 40)
        input("\nНажмите Enter для продолжения...")

    def show_minimap(self):
        self.clear_screen()
        print("\n" + "=" * 40)
        print("МИНИ-КАРТА:")
        print("=" * 40)

        start_i = max(0, self.player_pos[0] - 5)
        end_i = min(self.map_size, self.player_pos[0] + 6)
        start_j = max(0, self.player_pos[1] - 10)
        end_j = min(self.map_size, self.player_pos[1] + 11)

        for i in range(start_i, end_i):
            for j in range(start_j, end_j):
                if [i, j] == self.player_pos:
                    print('P', end=' ')
                elif [i, j] == self.baldi_pos:
                    print('B', end=' ')
                elif [i, j] in self.notebooks:
                    print('N', end=' ')
                elif any([i, j] == item[:2] for item in self.items):
                    for item in self.items:
                        if [i, j] == item[:2]:
                            print(item[2], end=' ')
                            break
                else:
                    print(self.school_map[i][j], end=' ')
            print()

        print(f"\nВаша позиция: [{self.player_pos[0]}, {self.player_pos[1]}]")
        print(f"Балди: [{self.baldi_pos[0]}, {self.baldi_pos[1]}]")
        print("\n" + "=" * 40)
        input("Нажмите Enter для продолжения...")

    def run(self):
        self.clear_screen()
        self.update_baldi_timer()

        print("=" * 60)
        print("BALDI'S BASICS IN EDUCATION AND LEARNING")
        print("КОНСОЛЬНАЯ ВЕРСИЯ - БОЛЬШАЯ КАРТА")
        print("=" * 60)
        print("\nЦель: Собрать 12 тетрадей (N) по всей школе")
        print("Размер карты: 15x15 клеток")
        print("Избегайте Балди (B) - он будет преследовать вас!")
        print("Балди двигается каждые 2-4 хода (ускоряется с тетрадями)")
        print("Используйте предметы для выживания.")
        print("\nНовые возможности:")
        print("- Большая карта с комнатами и коридорами")
        print("- Закрытые двери (нужен ключ)")
        print("- Больше предметов и тетрадей")
        print("\nНажмите H во время игры для помощи")
        print("Нажмите M для просмотра мини-карты")
        input("\nНажмите Enter для начала игры...")

        while not self.game_over:
            self.clear_screen()
            self.print_map()

            if self.energy <= 0:
                self.game_over = True
                print("\nЗакончилась энергия! Вы упали без сил...")
                break

            command = input("\nВведите команду: ").lower()

            if command == 'q':
                print("\nВыход из игры...")
                break
            elif command == 'i':
                self.show_inventory()
                continue
            elif command == 'h':
                self.show_help()
                continue
            elif command == 'm':
                self.show_minimap()
                continue
            elif command in ['w', 'a', 's', 'd']:
                self.move_player(command)
            else:
                print("Неверная команда! Используйте WASD для движения")
                time.sleep(1)

        self.clear_screen()
        print("=" * 50)
        if self.win:
            print("ПОБЕДА!")
            print(f"Вы собрали все {self.total_notebooks} тетрадей!")
        else:
            print("ИГРА ОКОНЧЕНА")

        print(f"\nИтоговый счет: {self.score}")
        print(f"Сделано ходов: {self.steps}")
        print(f"Найдено тетрадей: {self.notebooks_found}/{self.total_notebooks}")
        print("=" * 50)
        input("\nНажмите Enter для выхода...")


if __name__ == "__main__":
    game = BaldiGame()
    game.run()