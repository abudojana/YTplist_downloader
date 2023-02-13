from pytube import YouTube, Playlist
import time
import certifi
import ssl

# url of the YouTube playlist
playlist_url = 'https://youtube.com/playlist?list=PLfqMhTWNBTe3LtFWcvwpqTkUSlB32kJop'

# create a playlist object
playlist = Playlist(playlist_url)

# iterate through the videos in the playlist
for video_url in playlist:
    # create a YouTube object for each video
    video = YouTube(video_url)
    
    # select the video stream with 1080p resolution and mp4 format
    video_stream = video.streams.filter(res='1080p', mime_type='video/mp4').first()
    audio_stream = video.streams.filter(only_audio=True).first()
    
    if video_stream and audio_stream:
        # Get the total file size in bytes
        total_bytes = video_stream.filesize + audio_stream.filesize
        print("Video file size: ", total_bytes/1048576, "MB" )
        
        # get the video title
        video_title = video.title
        print("Video title: ", video_title)
        
        # download the video
        video_stream.download(filename=f'{video_title}_video')
        audio_stream.download(filename=f'{video_title}_audio')
        context = ssl.create_default_context(cafile=certifi.where())
        
        # get the time at which the download started
        start_time = time.time()
        # get the size of the downloaded file
        downloaded_bytes = video_stream.filesize + audio_stream.filesize
        print("Downloaded file size: ", downloaded_bytes/1048576, "MB" )
        
        while downloaded_bytes < total_bytes:
            
            downloaded_bytes = video_stream.filesize + audio_stream.filesize
            
            # get the time taken to download
            time_taken = time.time() - start_time
            
            # calculate the download speed
            download_speed = downloaded_bytes / time_taken
            
            # calculate the remaining bytes
            remaining_bytes = total_bytes - downloaded_bytes
            
            # calculate the remaining time
            remaining_time = remaining_bytes / download_speed
            
            # Print the download details
            print(f'Downloading {video_title}...')
            print(f'{downloaded_bytes / (1024 * 1024):.2f} MB of {total_bytes / (1024 * 1024):.2f} MB downloaded.')
            print(f'Download speed: {download_speed / (1024 * 1024):.2f} MB/s.')
            print(f'Time remaining: {remaining_time:.2f} seconds.')
            
            time.sleep(1)
            
        print(f'{video_title} has been downloaded.')
        
    else:
        print(f'No 1080p mp4 stream or audio stream found for {video.title}.')
