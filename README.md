# Steam With Friends

This will give you a list of games that both you and your friends own. This is useful for finding games that you can all play together. There isn't a limit on the number of friends you can filter by, so you can add two friends to the list or two hundred (just be aware that the more people you add, the less likely it is for you to all have games in common).

## How do I download it?

 - Open a Terminal and type `git clone https://github.com/Winning117/steam_with_friends.git`
 - Run `pip3 install xmltodict requests`

## How do I run it?

 - Edit `friends_list.txt` to include the urls of your friends' profiles (the profiles must be public). Replace the ones currently in the list as those are just an example. The name before the comma is just for reference and does not have to match the Steam profile. If you want to temporarily exclude someone from the search, just add a `#` to the beginning of the line, effectively commenting them out.
 - Type `python3 find_shared_games.py`
