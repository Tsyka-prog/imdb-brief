# Ajout au df principal d'une série regroupant les années en décennies
def decade(year):
    if year <= 1930:
        return '1920/30'
    elif (year > 1930) & (year <= 1940):
        return '1930/40'
    elif (year > 1940) & (year <= 1950):
        return '1940/50'
    elif (year > 1950) & (year <= 1960):
        return '1950/60'
    elif (year > 1960) & (year <= 1970):
        return '1960/70'
    elif (year > 1970) & (year <= 1980):
        return '1970/80'
    elif (year > 1980) & (year <= 1990):
        return '1980/90'
    elif (year > 1990) & (year <= 2000):
        return '1990/00'
    elif (year > 2000) & (year <= 2010):
        return '2000/10'
    else :
        return '2010/20'
    

def add_decade(imdb):
    imdb['decade'] = imdb['year'].map(decade)