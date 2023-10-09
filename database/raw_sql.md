```
create database if not exists steam_with_friends_bot;
use steam_with_friends_bot;

CREATE TABLE IF NOT EXISTS Users (
	SteamPlayerID VARCHAR(255) PRIMARY KEY NOT NULL,
	PlayerName VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS Games (
	GameName VARCHAR(255) NOT NULL,
	SteamPlayerID VARCHAR(64) NOT NULL,
	PRIMARY KEY(GameName, SteamPlayerID)
);
```
