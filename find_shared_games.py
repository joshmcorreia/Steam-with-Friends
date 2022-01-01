import sys
from User import User, PrivateProfileException, PrivateGameListException

def create_user_objects():
    friends = []
    with open("friends_list.txt") as file_in:
        for line in file_in:
            if "#" in line: # ignore users that are commented out
                continue
            line_list = line.split(",")
            username = line_list[0].strip()
            profile_url = line_list[1].strip()
            friend = User(username=username, url=profile_url)
            friends.append(friend)

    num_friends = len(friends)
    if num_friends == 1: # 1 is a special case because we change the plurality (are -> is, users -> user)
        print(f"ERROR: Two or more users are required to compare games. There is currently {num_friends} user in 'friends_list.txt'.")
        sys.exit(1)
    elif num_friends < 2:
        print(f"ERROR: Two or more users are required to compare games. There are currently {num_friends} users in 'friends_list.txt'.")
        sys.exit(1)

    return friends

def main():
    try:
        friends = create_user_objects()
        common_games_set = None
        for friend in friends:
            if common_games_set == None:
                common_games_set = friend.games_dict
            else:
                common_games_set = common_games_set.intersection(friend.games_dict)
        
        if common_games_set != None:
            print(f"\nGames that everyone owns:\n--------------------------")
            common_games_list = list(common_games_set)
            common_games_list.sort()
            for game in common_games_list:
                print(game)
        else:
            print("There don't appear to be any common games between all of the users specified in 'friends_list.txt'!")
    except (PrivateProfileException, PrivateGameListException) as err:
        print(err)
        sys.exit(1)

if __name__ == "__main__":
    main()
