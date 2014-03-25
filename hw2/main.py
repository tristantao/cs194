import pandas as pd
from pylab import *

DATA_PATH = "/Users/t-rex-Box/Desktop/work/cs194/hw2/" # Make this the /path/to/the/data

def parse_artists_tags(filename):
    df = pd.read_csv(filename, sep="|", names=["ArtistID", "ArtistName", "Tag", "Count"])
    return df

def parse_user_artists_matrix(filename):
    df = pd.read_csv(filename)
    return df

artists_tags = parse_artists_tags(DATA_PATH + "/artists-tags.txt")
user_art_mat = parse_user_artists_matrix(DATA_PATH + "/userart-mat-training.csv")

print artists_tags.head()

print "Number of tags %d" % len(artists_tags) # Change this line. Should be 952803
print "Number of artists %d" % len(user_art_mat) # Change this line. Should be 17119

# TODO Implement this. You can change the function arguments if necessary
# Return a data structure that contains (artist id, artist name, top tag) for every artist
def calculate_top_tag(all_tags):
    grouped = all_tags.groupby("ArtistID")
    result = {}
    for name, group in grouped:
        ArtistId = name
        ArtistName = group["ArtistName"].irow(0)
        MaxTag = group["Tag"][group['Count'].argmax()]
        result[tuple([ArtistId, ArtistName])] = MaxTag
    return result
    #return grouped.Tag.count().idxmax()

top_tags = calculate_top_tag(artists_tags)

# Print the top tag for Nirvana
# Artist ID for Nirvana is 5b11f4ce-a62d-471e-81fc-a69a8278c7da
# Should be 'Grunge'
print "Top tag for Nirvana is %s" % top_tags[("5b11f4ce-a62d-471e-81fc-a69a8278c7da","Nirvana")] # Complete this line