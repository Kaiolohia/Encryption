b62_table_encode = {
    0:"0",
    1:"1",
    2:"2",
    3:"3",
    4:"4",
    5:"5",
    6:"6",
    7:"7",
    8:"8",
    9:"9",
    10:"a",
    11:"b",
    12:"c",
    13:"d",
    14:"e",
    15:"f",
    16:"g",
    17:"h",
    18:"i",
    19:"j",
    20:"k",
    21:"l",
    22:"m",
    23:"n",
    24:"o",
    25:"p",
    26:"q",
    27:"r",
    28:"s",
    29:"t",
    30:"u",
    31:"v",
    32:"w",
    33:"y",
    34:"x",
    35:"z",
    36:"A",
    37:"B",
    38:"C",
    39:"D",
    40:"E",
    41:"F",
    42:"G",
    43:"H",
    44:"I",
    45:"J",
    46:"K",
    47:"L",
    48:"M",
    49:"N",
    50:"O",
    51:"P",
    52:"Q",
    53:"R",
    54:"S",
    55:"T",
    56:"U",
    57:"V",
    58:"W",
    59:"Y",
    60:"X",
    61:"Z",
}

b62_table_decode = dict([(value, key) for key, value in b62_table_encode.items()])

def encode(input):
    output = ""
    while input != 0:
        output += b62_table_encode[input % 62]
        input = input // 62
    return output

def decode(input):
    output = 0
    for i in reversed(range(len(input))):
        output += b62_table_decode[input[i]] * (62 ** i)
    return output

class seeded():
    def __init__(self,seed):
        self.seed = seed
        self.gen_tables()

    def gen_tables(self):
        self.b62_encode = {}
        for x in range(len(self.seed)):
            self.b62_encode[x] = self.seed[x]
        self.b62_decode = dict([(value, key) for key, value in self.b62_encode.items()])

    def encode(self, input):
        output = ""
        while input != 0:
            output += self.b62_encode[input % 62]
            input = input // 62
        return output

    def decode(self, input):
        output = 0
        for i in reversed(range(len(input))):
            output += self.b62_decode[input[i]] * (62 ** i)
        return output