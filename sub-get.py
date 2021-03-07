import youtube_dl
import re
import requests
def captions_get(url):
    # download subtitles
    ydl = youtube_dl.YoutubeDL({'writesubtitles': True, 'allsubtitles': True, 'writeautomaticsub': True})
    
    # get subtitle info
    res = ydl.extract_info(url, download=False)
    
    # download English subtile (you can change to another language)
    if res['requested_subtitles'] and res['requested_subtitles']['en']:
        sub_url = res['requested_subtitles']['en']['url']
        print('Grabbing vtt file from ' + sub_url)
        response = requests.get(res['requested_subtitles']['en']['url'], stream=True)
        sub_text = response.text
        
        # judge sub type
        if sub_url.startswith('https://www.youtube.com/api/timedtext?lang'):
            sub_type = 'manual caption'
            print('manual caption')
        else:
            sub_type = 'auto caption'
        return sub_text,sub_type
    else:
        print('Youtube Video does not have any english captions')
def vtt2srt(vtt_file):
    pattern = r'<.*?>'
    repl = ''
    
    # remove pos format
    b = re.sub(pattern, repl, vtt_file).replace(' align:start position:0%','').replace('.',',')
    c = b.split('\n')[12:]
    sub = []
    index = 0
    
    # youtube webvtt 8 lines get 1 real sub
    for i in range(len(c)):
        if i% 8 == 0:
            sub.append(int((index + 1) /4))
            sub.append(str(c[i]))
            index += 2
        elif i% 8 == 1:
            sub.append(str(c[i]))

        elif i% 8 == 2:
            sub[index] = str(sub[index]) + ' ' + str((c[i]))
            sub.append('\n')
            index += 2
        else:
            pass
    return sub

if __name__ == '__main__':
    CAPTIONS,sub_type = captions_get("https://www.youtube.com/watch?v=uDqjIdI4bF4")
    if sub_type == 'auto caption':
        # if sub is auto caption, convert to srt list
        srt_content = vtt2srt(CAPTIONS)
    else:
        # if sub is manual caption, convert to srt list
        srt_content = re.sub("(\d{2}:\d{2}:\d{2}).(\d{3})", lambda m: m.group(1) + ',' + m.group(2), CAPTIONS).split('\n')[4:]
    print(srt_content)
    
