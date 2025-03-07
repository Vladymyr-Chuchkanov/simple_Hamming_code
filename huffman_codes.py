import heapq
from collections import Counter


class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [HuffmanNode(char=char, freq=freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, parent)

    return heapq.heappop(heap)

def build_codebook(root, code="", codebook=None):
    if codebook is None:
        codebook = {}
    if root is not None:
        if root.char is not None:
            codebook[root.char] = code
        build_codebook(root.left, code + "0", codebook)
        build_codebook(root.right, code + "1", codebook)
    return codebook

def encode(text, codebook):
    return ''.join(codebook[char] for char in text)

def decode(encoded_text, codebook):
    reverse_codebook = {v: k for k, v in codebook.items()}
    current_code = ""
    decoded_text = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codebook:
            decoded_text += reverse_codebook[current_code]
            current_code = ""

    return decoded_text

def write_encoded_data(encoded_text, codebook, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        escaped_codebook = {k.replace('\n', '\\n').replace(',', 'sep').replace(':','two'): v for k, v in codebook.items()}
        f.write(','.join([f"{k}:{v}" for k, v in escaped_codebook.items()]) + '\n')
        f.write(encoded_text)

def read_encoded_data(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        codebook_line = f.readline().strip()
        codebook = {}
        for item in codebook_line.split(','):
            if ':' in item:
                key, value = item.split(':', 1)
                key = key.replace('\\n', '\n').replace('sep',',').replace('two',":")
                codebook[key] = value
        encoded_text = f.readline().strip()
    return encoded_text, codebook

def main():
    input_file = "huffman_input.txt"
    encoded_file = "huffman_output_enc.txt"
    decoded_file = "huffman_output_dec.txt"

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    huffman_tree = build_huffman_tree(text)
    codebook = build_codebook(huffman_tree)
    encoded_text = encode(text, codebook)
    write_encoded_data(encoded_text, codebook, encoded_file)
    print(f"Закодований текст записано у файл: {encoded_file}")

    encoded_text, codebook = read_encoded_data(encoded_file)

    decoded_text = decode(encoded_text, codebook)

    with open(decoded_file, 'w', encoding='utf-8') as f:
        f.write(decoded_text)
    print(f"Декодований текст записано у файл: {decoded_file}")
    print("Тексти співпадають: "+str(decoded_text == text))

if __name__ == "__main__":
    main()