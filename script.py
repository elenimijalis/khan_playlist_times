import argparse
import json
import urllib


def print_times(vids):
    ''' prints individual video times and total playlist time '''

    total_time = 0
    for vid in vids:
        total_time += vids[vid]

        print vid
        m, s = divmod(vids[vid], 60)
        h, m = divmod(m, 60)
        print '%d:%02d:%02d' % (h, m, s)

    m, s = divmod(total_time, 60)
    h, m = divmod(m, 60)

    # at 2x speed
    fast_m, fast_s = divmod(total_time/2, 60)
    fast_h, fast_m = divmod(fast_m, 60)

    print '****************'
    print 'TOTAL TIME:'
    print '%d:%02d:%02d' % (h, m, s)
    print '****************'
    print 'Note: if you watch at 2x speed, it will only take %d:%02d:%02d!' % (fast_h, fast_m, fast_s)


def get_video_times(url):
    ''' returns dictionary of video names and lengths '''

    response = urllib.urlopen("http://www.khanacademy.org/api/v1/topic/" + url)
    data = json.loads(response.read())
    title = data['standalone_title']
    vids = {}

    for child in data['children']:
        seconds = 0
        subtopic = urllib.urlopen("http://www.khanacademy.org/api/v1/topic/" + child['id'] + '/videos')
        videos = json.loads(subtopic.read())

        for video in videos:
            seconds += video['duration']
        vids[child['translated_title']] = seconds
    return vids, title


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Khan Playlist Durations')
    parser.add_argument('url', help='Enter url of playlist')
    args = parser.parse_args()

    vid_times, title = get_video_times(args.url.rsplit('/', 1)[-1])
    print '//////////////////////////////'
    print 'Playlist: %s' % title
    print '//////////////////////////////'
    print_times(vid_times)
