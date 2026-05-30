import chardet
with open('debug_output.txt', 'rb') as f:
    raw = f.read()
    encoding = chardet.detect(raw)['encoding']

text = raw.decode(encoding, errors='ignore')
with open('log_parsed.txt', 'w', encoding='utf-8') as f:
    f.write(text)
