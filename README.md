# Spotify-Data-Parser
A python script to parse your spotify extended history and provide interesting statistics

**NOTE:** This only works for the extended history generated via [Spotify's official data download request](https://www.spotify.com/account/privacy/). The process may take upto 30 days

# Description
This is a simple python script to go through your spotify data and provide interesting statistics such as the most played songs/albums/artists or the most Listened songs/albums/artists. Unlike spotify 
wrapped, spotify's extended history lets you view your lifetime streaming history

# Requirements
Python 3.7.17+

# Usage
* Clone this repo/download the spotifyParser.py file
* Place spotifyParser.py into a folder containing all of the spotify history extended jsons
* Open spotifyParser.py in a text editor of your choice and in `if __name__ == __main__` uncomment the required function
* Run spotifyParser.py

| Function                          | Use                                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------ |
| `list_ranges`                     | Lists out the possible range of values each key in the json file can have (Debug Purposes) |
| `print_most_listened_days`        | Prints a list of the days where most time was spent on Spotify                             |
| `print_first_items`               | Prints a list of the first items a user has listened to in spotify                         |
| `print_most_on_repeat_item`       | Prints out the longest streak of repeating songs                                           |
| `print_item_time`                 | For a given item, it prints out the total time listened                                    |
| `print_item_count`                | For a given item, it prints out the total number of times listened                         |
| `print_most_played_item_by_time`  | Displays a list of the most played items based on total listening time                     |
| `print_most_played_item_by_count` | Displays a list of the most played items based on total play count                         |
| `print_most_skipped_item`         | Displays a list of the most skipped item<br>                                               |

**Note:** An item may be `"artist"`, `"album"` or `"track"`

# TODO List
* Create a CLI interface for the script
* Create a GUI for the script
* Make the script more efficient by using pandas
* Add typing support
* Turn the script into a python module and instead of printing values, return them instead
