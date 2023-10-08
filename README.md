# Steam With Friends

This will give you a list of games that both you and your friends own. This is useful for finding games that you can all play together. There isn't a limit on the number of friends you can filter by, so you can add two friends to the list or two hundred (just be aware that the more people you add, the less likely it is for you to all have games in common).

## How do I download it?

- Open a Terminal and type `git clone https://github.com/Winning117/steam_with_friends.git`
- Run `pip3 install xmltodict requests`

## How do I run it?

- Edit `friends_list.txt` to include the urls of your friends' profiles (the profiles must be public). Replace the ones currently in the list as those are just an example. The name before the comma is just for reference and does not have to match the Steam profile. If you want to temporarily exclude someone from the search, just add a `#` to the beginning of the line, effectively commenting them out.
- Type `python3 find_shared_games.py`

---

# Developer Notes

## Updating pip dependencies:
```
pip freeze -l > pip_dependencies.txt
```

## Connecting to the database:
```
$ mysql -u root -h 127.0.0.1 --port=3306 -p steam_with_friends_bot
```

## Adding your Discord token so the bot can use it:
```
export DISCORD_TOKEN="129381092348901283091824"
```

## TODO:
- Add a database so we don't need to query the results every time
- Discord integration, allow for giving a list of users and find common games among them
- Support friends-only private profile scraping, can get in via my steam login
- Add something like an "!updateuser winning117" command
- Add ability to mark games as co-op capable
- Add non-steam games, i.e. Minecraft
