
# Split a string into a list where each word is a list item
# Returns LIST of words with '\n' on the end of each word
# Used by the two functions below
def split_into_words_w_newline(text):
    lines = text.split('\n')
    split_text = [line.split(None) for line in lines if line]
    return split_text

# Removes last N words of a STRING input
# Calls split_into_words_w_newline
# returns STRING
def remove_last_n_words(text, n):
    split_text = split_into_words_w_newline(text)
    i = 1
    lines_to_slice = 0
    while True:
        line = split_text[-i]
        if line:
            n_words = len(line)
            if n_words < n:
                n -= n_words
                lines_to_slice += 1
            else:
                split_text[-i] = line[:-n]
                break
        i += 1
        if i > len(split_text):
            break
    split_text = split_text[:-lines_to_slice]
    text = "\n".join([" ".join(line) for line in split_text])
    return text.strip()

# Keeps last N words of a STRING input
# Calls split_into_words_w_newline
# returns STRING
def keep_last_n_words(text, n):
    split_text = split_into_words_w_newline(text)
    i = 1
    lines_to_slice = 0
    while True:
        line = split_text[-i]
        if line:
            n_words = len(line)
            if n_words < n:
                n -= n_words
                lines_to_slice += 1
            else:
                split_text[i] = line[-n:]
                break
        i += 1
        if i > len(split_text):
            break
    split_text = split_text[-(lines_to_slice+1):]
    text = "\n".join([" ".join(line) for line in split_text])
    return text.strip()
