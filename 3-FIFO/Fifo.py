# Fifo declaration -- top level module similar to fifo.v
from collections import deque
from typing import Optional
from Drivers import packet_data 


class Fifo(deque):
    def __init__(self, len_data: int, len_fifo: int):
        super().__init__()
        self.len_data = len_data
        self.len_fifo = len_fifo

    def read(self) -> Optional[int]:
        if len(self) == 0:
            return None
        return self.popleft()

    def write(self, input) -> bool:
        if self.full():
            return False
        self.append(input)
        return True

    def send(self, pkg: packet_data):
        if pkg.write:
            self.write(pkg.data)
            return None  # no return value for write operation
        if pkg.read: 
            return self.read() # Returns element if available

    def empty(self) -> bool:
        return len(self) == 0
    
    def full(self) -> bool:
        return len(self) >= self.len_fifo

    def len(self) -> int:
        return len(self)
    
    def __str__(self):
        return f"Fifo(len_data={self.len_data},\
             len_fifo={self.len_fifo},\
             current_length={self.len()})"
    
    def get_signals(self):
        return {
            "empty": self.empty(),
            "full": self.full(),
            "len": self.len()
        }