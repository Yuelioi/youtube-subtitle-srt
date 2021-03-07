import youtube_dl
import re
import requests
def captions_get(url,lang = 'en'):
    # download subtitles
    ydl = youtube_dl.YoutubeDL({'writesubtitles': True, 'allsubtitles': True, 'writeautomaticsub': True})
    # get subtitle info
    res = ydl.extract_info(url, download=False)
    # download subtile (you can change to another language)
    if res['requested_subtitles'] and res['requested_subtitles'][lang]:
        sub_url = res['requested_subtitles']['en']['url']
        print('Grabbing vtt file from ' + sub_url)
        response = requests.get(res['requested_subtitles'][lang]['url'], stream=True)
        sub_text = response.text
        
        # judge sub type
        if sub_url.startswith('https://www.youtube.com/api/timedtext?lang'):
            sub_type = 'manual caption'
            print('manual caption')
        else:
            sub_type = 'auto caption'
        return sub_text,sub_type
    else:
        print('Np captions')
def vtt2srt(vtt_file,sub_type):
    '''
    :param vtt_file: webvtt字幕或者用户上传字幕
    :return: srt列表
    '''
        if sub_type == 'auto caption':
        pattern = r'<.*?>'
        repl = ''
        no_POS = re.sub(pattern, repl, vtt_file).replace(' align:start position:0%', '')
        CPTS = re.sub("(\d{2}:\d{2}:\d{2}).(\d{3})", lambda m: m.group(1) + ',' + m.group(2), no_POS).split('\n')[4:]
        srt_list = []
        index = 0
        for i in range(len(CPTS)):
            if i % 12 == 0:
                srt_list.append(str(int((index + 1) / 4)))
                srt_list.append('')
                index += 2
            elif i % 12 == 8:
                s_c1 = CPTS[i - 8].find('-->')
                startTime = CPTS[i - 8][0: s_c1 - 1]
                s_c2 = CPTS[i].find('-->')
                endTime = CPTS[i][s_c2 + 3:].strip()
                print(startTime,endTime,srt_list,i)
                srt_list[index - 1] = (str(startTime) + ' --> ' + str(endTime))
                index += 1
            elif i % 12 == 9:
                srt_list.append(str(CPTS[i] + ' ' + CPTS[i + 1]).strip())
                srt_list.append('')
                index += 1
            else:
                pass
        return srt_list[:-3]
    else:
        srt_list = re.sub("(\d{2}:\d{2}:\d{2}).(\d{3})", lambda m: m.group(1) + ',' + m.group(2), vtt_file).split('\n')[4:]
    return srt_list

if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=uDqjIdI4bF4'
    vtt_file, sub_type = captions_get(url, 'en')
    sub = vtt2srt(vtt_file, sub_type)
    print(sub)


    
