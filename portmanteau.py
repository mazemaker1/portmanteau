consonants = 'bcdfghjklmnpqrstvwxyz'
vowels = 'aeiou'
consonants += consonants.upper()
vowels += vowels.upper()
letter_types = [consonants, vowels]

def combine(word1, word2):
    ''' Combines two words to form a portmanteau.'''
    word1, word2 = (word1, word2) if word1 > word2 else (word2, word1)  # Order the words so input order doesn't change the result.
    result1, score1 = combine_in_order(word1, word2)
    result2, score2 = combine_in_order(word2, word1)
    return result1 if score1 > score2 else result2

def combine_in_order(word1, word2):
    # Break words into chunks of letters.
    word1_chunks = split_into_chunks(word1)
    word2_chunks = split_into_chunks(word2)

    # Handle the case where the words overlap by at least 1 full chunk.
    for chunk in reversed(word1_chunks[1:]):                                        # Don't include the start of word 1 for overlap, because that'll just look like word 2.
        if chunk in word2 and not word2.index(chunk) == len(word2) - len(chunk):    # Don't include the end of word 2 for overlap, because that'll just look like word 1.
            result = word1[:word1.rindex(chunk)] + word2[word2.index(chunk):]
            overlap_score = len(chunk)
            return result, overlap_score

    # Handle the case where the words don't have significant overlap.
    split1 = find_split(word1_chunks)
    split2 = find_split(word2_chunks)
    if len(word1_chunks) <= 3 and len(word2_chunks) > 3:    # If one word is short and the other is long, include the whole short word.
        split1 = 3
    if len(word1_chunks) > 3 and len(word2_chunks) <= 3:
        split2 = 0

    front_half = ''.join(word1_chunks[:split1])
    back_half = ''.join(word2_chunks[split2:])
    result = front_half + back_half

    # Slight score boost if they overlap by a letter or two.
    unused1 = ''.join(word1_chunks[split1:])
    unused2 = ''.join(word2_chunks[:split2])
    overlap_score = 0
    if unused1 and back_half.startswith(unused1[0]):
        overlap_score += 0.1
    if unused2 and front_half.endswith(unused2[-1]):
        overlap_score += 0.1

    return result, overlap_score

def split_into_chunks(word):
    ''' Breaks a word down into chunks of like letters (vowels or consonants).
        Returns chunks as a list of strings.'''
    chunks = []
    chunk = ''
    current_type = word[0] in vowels    # This is a bool, but it's going to be used as an index (0 or 1) of the letter_types list.
    for letter in word:
        if letter in letter_types[not current_type]:    # End a chunk if the letters switched type, but not if there's an unrecognized character.
            chunks.append(chunk)
            chunk = ''
            current_type = not current_type
        chunk += letter
    chunks.append(chunk)
    return chunks

def find_split(word_chunks):
    ''' Finds where to split a word for combining.
        Tries to split so that the front half of a word ends on a vowel
        and the back half starts on a consonant.'''
    if len(word_chunks) == 1:
        return 0
    middle_index = len(word_chunks) // 2
    if word_chunks[middle_index][0] in consonants:
        return middle_index
    else:
        return middle_index + 1








