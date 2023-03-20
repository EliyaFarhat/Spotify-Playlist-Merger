import spotipy
client_id = ""
client_secret = ""
scopes = 'playlist-modify-public'

def get_playlist_content(sp, sid):
    '''
    :param sp: Spotify token.
    :param sid: I.D. of the playlist.
    :return: List of the content of the playlist (URI's), with the playlist I.D. at the first index.
    '''
    try:
        r = sp.playlist_tracks(playlist_id=sid)
    except spotipy.SpotifyOauthError:

        r = sp.playlist_tracks(playlist_id=sid)
    t = r['items']
    ids = [sid]
    while r['next']:
        r = sp.next(r)
        t.extend(r['items'])
    for s in t: ids.append(s["track"]['uri'])

    return ids

def merge_playlists(first_content, second_content):
    '''
    :param first_content: Content of the first playlist.
    :param second_content: Content of the second playlist.
    Songs in the first playlist that are not in the second are added to the second playlist.
    '''
    del first_content[0]
    id2 = second_content.pop(0)

    add_content = list()
    for uri in first_content:
        if uri not in second_content and uri[0:13] != "spotify:local":
            add_content.append(uri)
    start = 0
    stop = 100

    for offset in range(len(first_content)//100):
        try:
            sp.playlist_add_items(playlist_id=id2, items=add_content[start:stop], position=None)
            start = stop
            stop += 100
        except spotipy.exceptions.SpotifyException:
            continue

if __name__ == '__main__':
    sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=client_id,
                                                           client_secret=client_secret,
                                                           redirect_uri="https://github.com/EliyaFarhat",
                                                           scope=scopes))

    try:
        merge_playlists(get_playlist_content(sp, ""), get_playlist_content(sp, ""))
    except spotipy.SpotifyOauthError as e:
        sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=client_id,
                                                       client_secret=client_secret,
                                                       redirect_uri="https://github.com/EliyaFarhat",
                                                       scope=scopes))

