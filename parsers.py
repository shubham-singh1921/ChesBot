import re

from bs4 import BeautifulSoup


class ChessLocationParser:

    def __init__(self):
        self.char_key = "abcdefgh"
        self.int_key = "12345678"
        self.prev_white_pos = []
        self.prev_black_pos = []
        self.moves_made = []

    def convertToUCIString(self, location_str):
        str_name = self.char_key[int(location_str[0]) - 1]
        int_name = self.int_key[int(location_str[1]) - 1]
        return str_name + int_name

    @staticmethod
    def detectPromotion(change, curr_pos, prev_pos):
        if len(change) == 4:
            prev_axis = change[0] + change[1]
            current_axis = change[2] + change[3]
            if int(current_axis[1]) == 1 or int(current_axis[1]) == 8:
                for square in prev_pos:
                    if square[0] == prev_axis and square[1][1] == 'p':
                        for square_now in curr_pos:
                            if square_now[0] == current_axis:
                                return square_now[1][1]

        return None

    def parseMoves(self, html_str):
        pass

    @staticmethod
    def getCastlingMove(curr_squares, prev_squares):
        move = ""
        for square in prev_squares:
            print(square)
            if len(square[1]) == 2 and square[1][1] == "k":
                move += square[0]

        for square in curr_squares:
            print(square)
            if len(square[1]) == 2 and square[1][1] == "k":
                move += square[0]

        return move

    def convertToSquarePositions(self, div_array):
        black_pos = []
        white_pos = []

        for div in div_array:
            class_string = " ".join(div["class"])
            search_result = re.search("square-[0-9][0-9]", class_string)
            if search_result:
                location_int = search_result.group(0).split("-")[-1]
                uci_location = self.convertToUCIString(location_int)
                piece_type = re.search("[wb][prnbkq]", class_string).group(0).strip()
                square_data = [uci_location, piece_type]

                if piece_type[0] == 'b':
                    black_pos.append(square_data)
                else:
                    white_pos.append(square_data)
        return [white_pos, black_pos]

    @staticmethod
    def getPositionChange(cr_square_data, prev_square_data):
        curr_position = [square[0] for square in cr_square_data]
        prev_position = [square[0] for square in prev_square_data]

        change = ""
        from_pos = list(set(prev_position) - set(curr_position))
        to_pos = list(set(curr_position) - set(prev_position))

        if len(from_pos) > 0 and len(to_pos) == 0:
            change = from_pos[0]
            return change

        if len(from_pos) == 2 and len(to_pos) == 2:
            change = "".join(from_pos) + "".join(to_pos)
        elif len(from_pos) > 0 and len(to_pos) > 0:
            change = from_pos[0] + to_pos[0]
        return change

    def detectChange(self, white_pos, black_pos) -> list:
        move_seq = []

        white_change = self.getPositionChange(white_pos, self.prev_white_pos)
        black_change = self.getPositionChange(black_pos, self.prev_black_pos)

        if len(white_change) == 2:
            for i in range(len(white_pos)):
                if white_change == white_pos[i]:
                    white_pos.pop(i)
                    break
            white_change = ""

        if len(black_change) == 2:
            for i in range(len(black_pos)):
                if black_change == black_pos[i]:
                    black_pos.pop(i)
                    break
            black_change = ""

        if len(white_change) == 8:
            result = self.getCastlingMove(white_pos, self.prev_white_pos)
            white_change = result

        if len(black_change) == 8:
            result = self.getCastlingMove(black_pos, self.prev_black_pos)
            black_change = result

        if len(white_change) != 0 and len(white_change) == 4:
            promotion = self.detectPromotion(white_change, white_pos, self.prev_white_pos)
            if promotion:
                white_change += promotion.upper()

        if len(black_change) != 0 and len(white_change) == 4:
            promotion = self.detectPromotion(black_change, black_pos, self.prev_black_pos)
            if promotion:
                black_change += promotion.upper()

        if white_change != "":
            move_seq.append(white_change)
        if black_change != "":
            move_seq.append(black_change)
        return move_seq

    def processPiecesLocation(self, html_str):
        soup = BeautifulSoup(html_str, "lxml")
        result = soup.find_all("div", attrs={"class": "piece"})
        square_positions = self.convertToSquarePositions(result)

        white_pos = square_positions[0]
        black_pos = square_positions[1]
        if self.prev_black_pos and self.prev_white_pos:
            changes = self.detectChange(white_pos, black_pos)
            if len(changes) != 0:
                for change in changes:
                    self.moves_made.append(change)

        self.prev_white_pos = white_pos
        self.prev_black_pos = black_pos

        return self.moves_made


string = "sqre zsqupra wp"
search = re.search("[wb][prnbkq]", string)
print(search.group(0))
