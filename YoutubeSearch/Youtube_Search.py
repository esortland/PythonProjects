from pandas import DataFrame as df 
from googleapiclient.discovery import build
from config import decouple

api_key = config('API_KEY')
export_location = config('EXPORT_DIRECTORY')
youtube = build('youtube', 'v3', developerKey = api_key)

def main():

    query1 = input("Enter Your Search: \n")
    
    #Grab video data
    print("Getting your search data now...\n")
    vids = get_videos(query1)

    #Create data lists
    vid_titles = list(map(lambda x:x['snippet']['title'], vids))
    vid_channel = list(map(lambda x:x['snippet']['channelTitle'], vids))
    vid_ids = list(map(lambda x:x['id']['videoId'], vids))

    #Grab stats data
    stats = get_stats(vid_ids)

    #create stats list 
    vid_views = list(map(lambda x:x['statistics'].get('viewCount'), stats))
    vid_likes = list(map(lambda x:x['statistics'].get('likeCount'), stats))
    vid_dislikes = list(map(lambda x:x['statistics'].get('dislikeCount'), stats))
    vid_comments =  list(map(lambda x:x['statistics'].get('commentCount'), stats))

    #Ceate list to be used for dataFrame
    video_data = {'Video': vid_titles, 
              'Channel': vid_channel, 
              'Views': vid_views, 
              'Likes': vid_likes, 
              'Dislikes': vid_dislikes, 
              'Comments': vid_comments}

    #Create dataframe
    vid_df = df(video_data, columns = ['Video', 
                                          'Channel', 
                                          'Views', 
                                          'Likes', 
                                          'Dislikes', 
                                          'Comments'])

    #export df to csv
    vid_df.to_csv(export_location, header = True, index = None)
    
    print('Your data has been saved to your desktop!\n')

def get_videos(query):
    videos = []
    next_page_token = None
    
    #Grab max of 1000 videos
    while len(videos) < 1000:
        
        #call for results 
        results = youtube.search().list(part = 'snippet', q = query, type = 'video', maxResults = 50, pageToken = next_page_token).execute()
        
        #add results to videos list
        videos += results['items']
        next_page_token = results.get('nextPageToken')
        
        #find next page of 50 videos
        if next_page_token is None:
            break
            
    return videos


def get_stats(video_ids):
    stats = []

    #Call for stats from ID and create list
    for i in range(0, len(video_ids), 50):
        result = youtube.videos().list(id= ','.join(video_ids[i:i+50]) , part = 'statistics').execute()
        stats += result['items']
        
    return stats



if __name__ == '__main__':
    main()






