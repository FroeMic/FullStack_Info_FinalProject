EMPTY_STAR = '☆'
FULL_STAR = '★'


def rating_to_stars(rating, max=5):
    ''' Turn a rating into an array of stars, e.g. ['★', '★', '★' , '☆', '☆'] '''
    result = []
    for i in range(1, max+1):
        if rating > i:
            result.append(FULL_STAR)
        else:
            result.append(EMPTY_STAR)
    return result
