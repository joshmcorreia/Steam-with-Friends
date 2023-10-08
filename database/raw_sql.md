```
create database if not exists steam_with_friends_bot;
use steam_with_friends_bot;

CREATE TABLE IF NOT EXISTS Users (
	SteamID VARCHAR(255) PRIMARY KEY NOT NULL,
	Name VARCHAR(64) NOT NULL
);
```
