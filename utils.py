def filter_obj(obj, keys_to_add):
    # Function for filtering objects
    buffer_obj = {}

    for key, value in obj.items():
        if key in keys_to_add:
            buffer_obj[key] = value

    return buffer_obj


def filtering_track_process(track, keys_to_leave=None):
    buffer_obj = {"track": "", "artists": []}
    name = filter_obj(track, keys_to_leave).get("name")

    if name:
        buffer_obj["track"] = name

    for artist in track["artists"]:
        name = filter_obj(artist, keys_to_leave).get("name")
        if name:
            buffer_obj["artists"].append(name)

    return buffer_obj


# V1
# def convert_arr_into_obj(arr):
#     # Only for the arrays which are structured in this style [key,value,...]
#     obj = {}
#     i = 0

#     for key in arr:
#         if i % 2 == 0 and i < len(arr):
#             i += 1
#             obj[key] = arr[i]
#         else:
#             i += 1
#             continue

#     return obj


# V2
def convert_arr_into_obj(arr):
    # Only for arrays structured like [key, value, key, value, ...]
    obj = {}

    # Loop over indices, stepping by 2 (key at i, value at i+1)
    for i in range(0, len(arr), 2):
        key = arr[i]
        # Make sure there is a value after the key

        if i + 1 < len(arr):
            obj[key] = arr[i + 1]

    return obj
