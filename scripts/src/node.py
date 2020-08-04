import utils

class Node:
    def __init__(self):
        self.keys = utils.generate_ec_key_pairs()
