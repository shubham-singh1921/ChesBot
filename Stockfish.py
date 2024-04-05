from subprocess import Popen, PIPE
import multiprocessing
import threading


class Stockfish:
    obj_file = "stockfish.o"

    def __init__(self):
        self.command_string = "position startpos moves "
        self.process = None

    def reset(self):
        pass

    def getNextMove(self, moves_list):
        self.runCommand(self.command_string + " ".join(moves_list))
        self.runCommand("go depth 10")
        return self.readNextMove()

    def readNextMove(self):
        while True:
            line = self.process.stdout.readline()
            if line.split(" ")[0] == "bestmove":
                return line

    def readOutput(self):
        while True:
            line = self.process.stdout.readline()
            print(line.replace("\n", ""))
            if line.split(" ")[0] == "bestmove":
                return line

    def readSingleLine(self):
        line = self.process.stdout.readline()
        print(line.replace("\n", "::"))

    def startReadProcess(self):
        thread = threading.Thread(target=self.readOutput)
        thread.start()
        thread.join(timeout=5)
        if thread.is_alive():
            print("thread alive")

    def init(self):
        self.process = Popen(f"./{self.obj_file}", stdin=PIPE, stdout=PIPE, text=True)
        self.readSingleLine()
        self.runCommand("isready")
        self.readSingleLine()
        self.runCommand("ucinewgame")
        self.runCommand("position startpos")

    def runCommand(self, command):
        cmd = command + "\n"
        print("[CMD]", cmd)
        self.process.stdin.write(cmd)
        self.process.stdin.flush()
