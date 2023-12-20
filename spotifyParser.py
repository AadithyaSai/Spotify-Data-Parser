#!/bin/python3

from datetime import datetime, timedelta
from itertools import groupby
from glob import glob
from json import load


def list_ranges(data):
    # Lists possible data ranges in json file for each key with non-unique values
    skip_keys = (
        "ts",
        "ms_played",
        "master_metadata_track_name",
        "master_metadata_album_album_name",
        "master_metadata_album_artist_name",
        "master_metadata_album_album_name",
        "episode_name",
        "episode_show_name",
        "spotify_track_uri",
        "spotify_episode_uri",
        "offline_timestamp",
        "ip_addr_decrypted",
    )

    for key in data[0].keys():
        vals = set()

        if (
            key not in skip_keys
        ):  # skip unique value ranges like timestamp, track name, etc
            for song_data in data:
                val = song_data[key]
                if isinstance(val, str):
                    vals.add(val)
                else:
                    vals.add(str(val))

            print(key)
            print("-------")
            print("\n".join(vals), end="\n\n")


def print_most_listened_days(data, data_range=30):
    key_val = "master_metadata_track_name"
    data = [
        song_data for song_data in data if song_data[key_val]
    ]  # Removing song_datas where song_data[key_val] is None
    data.sort(key=lambda song_data: song_data["ts"])

    time_data = [
        (datetime.fromisoformat(song_data["ts"]), song_data["ms_played"])
        for song_data in data
    ]

    grouped_data = groupby(time_data, lambda time: time[0].date())

    times = [(date, sum([ms for _, ms in group])) for date, group in grouped_data]

    times.sort(key=lambda time: time[1], reverse=True)

    print(" Most Listened To days")
    print("-----------------------")
    for count, time in enumerate(times[:data_range]):
        print(f"{count+1 : >2}. {time[0]}: {timedelta(milliseconds=time[1])}")


def print_first_items(data, item, data_range=30):
    if item == "album":
        key_val = "master_metadata_album_album_name"
    elif item == "artist":
        key_val = "master_metadata_album_artist_name"
    elif item == "track":
        key_val = "master_metadata_track_name"
    else:
        print("Invalid item. Item should be one of these: (album, artist, track)")
        return

    data = [song_data for song_data in data if song_data[key_val]]
    data.sort(key=lambda song_data: song_data["ts"])

    print(f" First {item} listened")
    print("-------------------------")

    for count, song in enumerate(data[:data_range]):
        print(f"{count+1}. {song[key_val]}: {song['ts']}")


def print_most_on_repeat_item(data, item, data_range=30):
    if item == "album":
        key_val = "master_metadata_album_album_name"
    elif item == "artist":
        key_val = "master_metadata_album_artist_name"
    elif item == "track":
        key_val = "master_metadata_track_name"
    else:
        print("Invalid item. Item should be one of these: (album, artist, track)")
        return

    data = [
        song_data for song_data in data if song_data[key_val]
    ]  # Removing song_datas where song_data[key_val] is None
    data.sort(key=lambda song_data: song_data["ts"])  # sorting for grouping

    grouped_data = groupby(data, lambda song_data: song_data[key_val])
    songs = [
        (
            song_name,
            len(group_list := list(group)),
            (group_list[0]["ts"], group_list[-1]["ts"]),
        )
        for song_name, group in grouped_data
    ]

    print(f" Most On Repeat {item}")
    print("----------------------")

    songs.sort(key=lambda song: song[1], reverse=True)
    for count, song in enumerate(songs[:data_range]):
        print(f"{count+1 : >2}. {song[0]}: {song[1]} - ({song[2][0]} - {song[2][1]})")


def print_item_time(data, item, item_name):
    if item == "album":
        key_val = "master_metadata_album_album_name"
    elif item == "artist":
        key_val = "master_metadata_album_artist_name"
    elif item == "track":
        key_val = "master_metadata_track_name"
    else:
        print("Invalid item. Item should be one of these: (album, artist, track)")
        return

    data = [
        song_data for song_data in data if song_data[key_val]
    ]  # Removing song_datas where song_data[key_val] is None
    data.sort(key=lambda song_data: song_data[key_val])  # sorting for grouping

    grouped_data = groupby(data, lambda song_data: song_data[key_val])
    song = next(
        (
            (song_name, sum([song_data["ms_played"] for song_data in group]))
            for song_name, group in grouped_data
            if song_name == item_name
        ),
        None,
    )

    if song:
        print(f"{song[0]}: {timedelta(milliseconds=song[1])}")
    else:
        print(
            f"{item_name} does not exist! Please note that the search is case sensitive and also counts special characters that may be present in an item's name"
        )


def print_item_count(data, item, item_name):
    if item == "album":
        key_val = "master_metadata_album_album_name"
    elif item == "artist":
        key_val = "master_metadata_album_artist_name"
    elif item == "track":
        key_val = "master_metadata_track_name"
    else:
        print("Invalid item. Item should be one of these: (album, artist, track)")
        return

    data = [
        song_data for song_data in data if song_data[key_val]
    ]  # Removing song_datas where song_data[key_val] is None
    data.sort(key=lambda song_data: song_data[key_val])  # sorting for grouping

    grouped_data = groupby(data, lambda song_data: song_data[key_val])
    song = next(
        (
            (song_name, len(list(group)))
            for song_name, group in grouped_data
            if song_name == item_name
        ),
        None,
    )

    if song:
        print(f"{song[0]}: {song[1]}")
    else:
        print(
            f"{item_name} does not exist! Please note that the search is case sensitive and also counts special characters that may be present in an item's name"
        )


def print_most_played_item_by_time(data, item, data_range=30):
    if item == "album":
        key_val = "master_metadata_album_album_name"
    elif item == "artist":
        key_val = "master_metadata_album_artist_name"
    elif item == "track":
        key_val = "master_metadata_track_name"
    else:
        print("Invalid item. Item should be one of these: (album, artist, track)")
        return

    data = [
        song_data for song_data in data if song_data[key_val]
    ]  # Removing song_datas where song_data[key_val] is None
    data.sort(key=lambda song_data: song_data[key_val])  # sorting for grouping

    grouped_data = groupby(data, lambda song_data: song_data[key_val])
    songs = [
        (song_name, sum([song_data["ms_played"] for song_data in group]))
        for song_name, group in grouped_data
    ]

    print("Total: ", timedelta(milliseconds=sum(time for _, time in songs)), "\n\n")

    songs.sort(key=lambda song: song[1], reverse=True)
    for count, song in enumerate(songs[:data_range]):
        print(f"{count+1 : >2}. {song[0]}: {timedelta(milliseconds=song[1])}")


def print_most_played_item_by_count(data, item, data_range=30):
    if item == "album":
        key_val = "master_metadata_album_album_name"
    elif item == "artist":
        key_val = "master_metadata_album_artist_name"
    elif item == "track":
        key_val = "master_metadata_track_name"
    else:
        print("Invalid item. Item should be one of these: (album, artist, track)")
        return

    data = [
        song_data for song_data in data if song_data[key_val]
    ]  # Removing song_datas where song_data[key_val] is None
    data.sort(key=lambda song_data: song_data[key_val])  # sorting for grouping

    grouped_data = groupby(data, lambda song_data: song_data[key_val])
    songs = [
        (
            song_name,
            len([song_data for song_data in group if song_data["ms_played"] > 1500]),
        )
        for song_name, group in grouped_data
    ]

    print("Total: ", sum(time for _, time in songs), "\n\n")

    songs.sort(key=lambda song: song[1], reverse=True)
    for count, song in enumerate(songs[:data_range]):
        print(f"{count+1 : >2}. {song[0]}: {song[1]}")


def print_most_skipped_item(data, item, data_range=30):
    if item == "album":
        key_val = "master_metadata_album_album_name"
    elif item == "artist":
        key_val = "master_metadata_album_artist_name"
    elif item == "track":
        key_val = "master_metadata_track_name"
    else:
        print("Invalid item. Item should be one of these: (album, artist, track)")
        return

    data = [
        song_data for song_data in data if song_data[key_val]
    ]  # Removing song_datas where song_data[key_val] is None
    data.sort(key=lambda song_data: song_data[key_val])  # sorting for grouping

    grouped_data = groupby(data, lambda song_data: song_data[key_val])
    songs = [
        (
            song_name,
            len(
                [
                    song_data
                    for song_data in group
                    if song_data["reason_end"] in ("fwdbtn", "backbtn")
                    and song_data["ms_played"] < 2500
                ]
            ),
        )
        for song_name, group in grouped_data
    ]

    print("Total: ", sum(time for _, time in songs), "\n\n")

    songs.sort(key=lambda song: song[1], reverse=True)
    for count, song in enumerate(songs[:data_range]):
        print(f"{count+1 : >2}. {song[0]}: {song[1]}")


if __name__ == "__main__":
    file_names = [file_name for file_name in glob("./Streaming_History_Audio*.json")]
    data = []
    for file_name in file_names:
        with open(file_name) as f:
            data += load(f)

    # +--------------------------------------------------------------------+
    # | Uncomment the required function and replace $? with desired params |
    # | Item should be one of these (album, artist, track)                 |
    # |                                                                    |
    # | Note: All functions that print out a range of data supports an     |
    # |       optional parameter data_range which is initially set to 30   |
    # +--------------------------------------------------------------------+

    # list_ranges(data)
    # print_most_listened_days(data)
    # print_first_items(data, item=$?)
    # print_most_on_repeat_item(data, item=$?)
    # print_item_time(data, item=$?, item_name=$?)
    # print_item_count(data, item=$?, item_name=$?)
    # print_most_played_item_by_time(data, item=$?)
    # print_most_played_item_by_count(data, item=$?)
    # print_most_skipped_item(data, item=$?)
