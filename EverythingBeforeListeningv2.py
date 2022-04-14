# Feb 12, 2022
# Consolidate & Evolve Work-to-Date
# Icebreaker.py
# inContactAPI_try*
# Goal: Everything (contextually file or data) that can be done before listening to a clip
# Horizon-Context: 2-Weeks (Table alternate time horizons/comparisons for later)
# Scope-Conext: DateTime, Skill, Team, In/Out, Phone (Area), ID, Length
# Parameters:
# Long Call: >= 120 min
# Flagged Silence: >= 120 sec (?)
# Ignore Inter-Silence: <=20 sec (?)
# Slice-Driver, Silence: 45 sec
# Silce-Driver, Call: 5 min
# (What is the cost vs benefit of analyzing post-silence "solution" 45 sec?)
# Length + Count by SliceX:  All -- Top 10 Tech-Skills
# Data: All Calls
# (Where to Slice; Analyse; Visualize? Python or Excel? or other)
# Length + Count by SliceX:  Long -- Top 10 Tech-Skills
# Data: Long Calls
# (Where to Slice; Analyse; Visualize? Python or Excel? or other)
# Length + Count by SliceX: SunVault (Extending ^^)
# Data: All Calls
# Files, Write to HD: 1-Week Longest 5 Calls
# Data: 1-Week Longest 5 Calls
# Files, Read from HD: 1-Week Longest 5 Calls
# Data, Generate: Analyze for Silence
# Previous, Read from HD: Earlier 1-Week Longest 5 Calls Silence Data
# (Where to Slice; Analyse; Visualize? Python or Excel? or other)
# Cut File, Generate Clips: 1-Week Longest 5 Calls
# Slice-Driver, Silence
# Silce-Driver, Call
# %% Import
import fcntl
from urlgrabber.grabber import URLGrabber
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import base64
import datetime as DT
import pandas as pd
import os
from dash import Dash, html, dcc
import plotly.express as px
#%% Change Working Directory
os.chdir('C:\\Users\\{}\\Sunpower Corporation\\ATSE.US - Documents\\Icebreaker\\v4_All-in-One'.format(os.getlogin()))
#os.chdir('.\\rawLogs_DeleteAfter2weeks\\')
#%% Prep0: Authorization
# https://developer.niceincontact.com/Documentation/BackendApplicationAuthentication

def nice_auth():
    url_token_viakey = 'https://api.incontact.com/InContactAuthorizationServer/token/access-key'

    APIUserKey = 'BUCK4USCOAJ7KGTQGKVNJ4LKF3KIVT7FSO4LPS47DZNG4PPC7YXA===='
    APIUser_Secret = 'FQGZWO2KZKZXOOYPJ5SPQFB6763CH7RKTAPYRJY4UWY2HXC4MHYA===='

    auth_payload = {
        'accessKeyId': APIUserKey,
        'accessKeySecret': APIUser_Secret
    }

    head = {'content-type': 'application/json'}
    r_token_viakey = requests.post(
        url=url_token_viakey, headers=head, json=auth_payload)
    # Retrieve Access Token
    atoken = r_token_viakey.json()['access_token']
    # Update head w/token
    head['Authorization'] = 'Bearer {}'.format(atoken)
    return head


#%% Prep1: Top 10 Tech Skills
skills = {
    'NA Sunvault Tech': 10519755,
    #'NA Master - TSE': 4305607,
    #'NA TSE': 4305606,
    #'NA CSR Technical':4305582,
    #'NA Commercial TSE': 4305602,
    #'NA TSE Indirect Commercial': 4305603,
    #'NA Escalations': 4305590,
    #'Commercial Commissioning':10463443,
    #'NA NH TSE':4313845,
    #'NA CSR Tech 2':10796840
}

# %% Prep2: Dates Range
#d0 = DT.date.today() - DT.timedelta(7 + (DT.date.today().weekday() + 1) % 7-6)+DT.timedelta(1)
d0 = DT.date.today() - DT.timedelta( (DT.date.today().weekday() + 1) % 7)+DT.timedelta(1)
d1 = d0-DT.timedelta(7)
#
week0 = mdates.num2date(mdates.drange(d1,d0,DT.timedelta(hours=6)))

wk = {'0':{'st':[],'end':[]},'1':{'st':[],'end':[]}}
i=0
while i+1<len(week0):
    wk['0']['st'].append(str(week0[i]))
    wk['0']['end'].append(str(week0[i+1]+DT.timedelta(seconds=-1)))
    wk['1']['st'].append(str(week0[i]-DT.timedelta(7)))
    wk['1']['end'].append(str(week0[i+1]-DT.timedelta(7)+DT.timedelta(seconds=-1)))
    i+=1
# %% Pull Data
# Programmatic Dates & cycle Through Skills
#Need these?
ct = 0
c = []
#
url_cluster = 'https://api-c29.incontact.com/inContactAPI/services/v23.0/'
api_nm = 'contacts/completed'
head = nice_auth()
result = []
for skill in skills:
    for k in wk:
        j = 0
        while j < i:
            query_contacts = {
                # 'top':'10', # For Testing
                'startDate': wk[k]['st'][j],
                'endDate': wk[k]['end'][j],
                'skillId': skills[skill],
                'mediaTypeId': 4,
                'fields': 'isOutbound, contactStart, totalDurationSeconds,contactId, fromAddr,mediaType,mediaTypeName,skillId,skillName,campaignId,campaignName,teamId,teamName',
            }
            j += 1
            r = requests.get(url=url_cluster+api_nm, headers=head, params=query_contacts)
            if r.status_code != requests.codes.ok:
                continue
            else:
                result.append(r.json()['completedContacts'])
                c.append(r.json()['totalRecords'])
                ct += r.json()['totalRecords']
                print('{}: {} - {}'.format(skill,query_contacts['startDate'],query_contacts['endDate']))

            
#%% result
con = []
for res in result:
    for cc in res:
        con.append(cc)
df = pd.DataFrame.from_records(con, columns=list(cc.keys()))
df['totalDurationSeconds'] = pd.to_numeric(df['totalDurationSeconds'], errors='coerce')
for x in df.index:
    df.loc[x,'aCode'] = df.loc[x,'fromAddr'][-10:][:3]
    if df.loc[x,'totalDurationSeconds']<30: # Must be > 30sec to count as Valid Call
        df.drop(x, inplace=True)
    else:
        df.loc[x,'totalDurationSeconds']=df.loc[x,'totalDurationSeconds']/60.0

df['LongTF']=df['totalDurationSeconds']>=120
df['contactStart']=pd.to_datetime(df['contactStart'])
df.set_index('contactStart', inplace=True)
df['wk'] = df.index.isocalendar().week
df['day'] = df.index.isocalendar().day
df['hour'] = df.index.hour

df['aCode']=pd.to_numeric(df['aCode'])
df.rename(columns={'totalDurationSeconds':'totalDurationMinutes'}, inplace=True)
#df.to_csv('test1.csv', index=False)
#%% Analyze
df_desc_stats = df.groupby(['skillName', 'wk','LongTF'])['totalDurationMinutes'].describe()
print(df_desc_stats)
#df_desc_stats.to_csv('T10Tech_stats_Week'+str(df['wk'].max())+'.csv')
#%% Little Bit of Charting
for sk in df['skillName'].drop_duplicates():
    df[["skillName","wk","totalDurationMinutes"]][df['skillName']==sk].pivot(columns='wk',values='totalDurationMinutes').plot.box(xlabel="2022 Work Week",ylabel="Duration (Min)", title= "{}: All Calls".format(sk))
    df[["skillName","wk","totalDurationMinutes"]][df['skillName']==sk].pivot(columns='wk',values='totalDurationMinutes').plot.hist(alpha=0.5,rwidth=0.75,xlabel="2022 Work Week",ylabel="Duration (Min)", title= "{}: All Calls".format(sk))
#
    if df[["skillName","LongTF","wk","totalDurationMinutes"]][(df['skillName']==sk) & (df['LongTF']==True)].size > 0:
        df[["skillName","LongTF","wk","totalDurationMinutes"]][(df['skillName']==sk) & (df['LongTF']==True)].pivot(columns='wk',values='totalDurationMinutes').plot.hist(alpha=0.5,rwidth=0.75,xlabel="2022 Work Week",ylabel="Duration (Min)", title= "{}: Long Calls".format(sk))
# %% Longest 5 SV Calls (IDs)
long5_sv_df = df[['contactId','totalDurationMinutes','wk']][(df['skillName']=='NA Sunvault Tech') & (df['wk']==df['wk'].max())].sort_values(by='totalDurationMinutes', ascending=False).head(5)
#long5_sv_json = long5_sv_df.to_json(orient='records')
#%% Prep to Download 5 x Longest SV Calls
for index, row in long5_sv_df.iterrows():
    #api_nm_files = 'contacts/' + str(row['contactId']) + '/files'
    api_nm_files = 'contacts/{}/files'.format(row['contactId'])

    r_file = requests.get(url=url_cluster+api_nm_files, headers=head)

    long5_sv_df.loc[index,'file_url'] = r_file.json()['files'][0]['fullFileName']
    long5_sv_df.loc[index,'file_name'] = r_file.json()['files'][0]['fileName']
    
# %% Download 5 x Longest SV Calls
api_nm_bin = 'files'

i = 0
for index_bin, row_bin in long5_sv_df.iterrows():
    head = nice_auth()
    g = URLGrabber(ssl_verify_peer = False, ssl_verify_host = False)
    ocal_filename = g.urlread(url=url_cluster + api_nm_bin + '?fileName=' + row_bin['file_url'], http_headers=tuple(head.items()))
    oocal_filename = base64.b64decode(str(ocal_filename).split(':')[2])

    print('Writing #{} ID-{}, {} min long'.format(i+1,row_bin['contactId'], int(row_bin['totalDurationMinutes'])))

    with open('wk{}_{}_{}min_{}.wav'.format(row_bin['wk'],i,int(row_bin['totalDurationMinutes']),row_bin['contactId']), 'wb') as f:
        f.write(oocal_filename)
    i += 1
# HERE WE GO!
#%% Dash
app = Dash(__name__)

fig = px.bar(long5_sv_df, x="totalDurationMinutes", y="contactId", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Icebreaker Dashboard'),

    html.Div(children='''
        Visualizing data from our calls
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server()
# %% Read
#Silence Params
# tuning_noise = -10
# tuning_min_silence = 120
# tuning_min_gap = 30
# #Snip Params
# driver_detect_call = 300
# driver_detect_sil = 45
# res_detect_sil = 45

# #new_long_wavs = [wav for wav in os.listdir() if (wav[:3]=='wk' + str(df['wk'].max())) & (wav[-3:] == 'wav')]
# new_long_wavs = [wav for wav in os.listdir() if (wav[:3]=='wk6') & (wav[-3:] == 'wav')] #script-test
# new_long_txt = [txt[:-4]+'.txt' for txt in new_long_wavs]
#%% 
# c = 0
# dd = pd.DataFrame()
# for dumwav in new_long_wavs:
#     wav = new_long_wavs[c]
#     #os.system(r'cmd /c ffmpeg -i ' + new_long_wavs[c] + r' -af silencedetect=noise=' + str(tuning_noise) + r'dB:duration=' + str(tuning_min_silence) + r',ametadata=print:file=' + new_long_txt[c] + r' -f null -')
#     os.system(r'cmd /c ffmpeg -i {} -af silencedetect=noise={}dB:duration={},ametadata=print:file={} -f null -'.format(wav, tuning_noise,tuning_min_silence,new_long_txt[c]))
#     long_df = pd.read_csv(new_long_txt[c], delimiter = '=', names = ['Name','Value'])
#     long_df = long_df[long_df['Value']>0]
#     if long_df.loc[long_df.index.max(),'Name'] == 'lavfi.silence_start':
#         long_df.loc[long_df.index.max()+1,'Name'] = 'lavfi.silence_end'
#         long_df.loc[long_df.index.max(),'Value'] = 99999
#         long_df.loc[long_df.index.max()+1,'Name'] = 'lavfi.silence_duration'
#         long_df.loc[long_df.index.max(),'Value'] = 99999
#     long_df.reset_index(inplace=True)
#     long_df['quasi_id']=long_df.index/3
#     long_df['quasi_id'] = long_df['quasi_id'].floordiv(1)
#     long_df = long_df.drop('index', axis=1).set_index('quasi_id').pivot(columns='Name',values='Value')

#     long_df_j = pd.merge(long_df,long_df.set_index(long_df.index-1),how='left',left_index=True,right_index=True)
#     long_df_j['gap'] = long_df_j['lavfi.silence_start_y']-long_df_j['lavfi.silence_end_x']

#     i = 0
#     for gr in long_df.index:
#         long_df.loc[gr,'gg'] = i
#         if long_df_j.loc[gr,'gap'] > tuning_min_gap:
#             i +=1
#     long_df_agg0 = pd.merge(long_df[['gg','lavfi.silence_duration']].groupby('gg').sum(),long_df[['gg','lavfi.silence_start']].groupby('gg').min(), how='inner', left_on='gg', right_on='gg')
#     long_df_agg1 = pd.merge(long_df_agg0,long_df[['gg','lavfi.silence_end']].groupby('gg').max(), how='inner', left_on='gg', right_on='gg')

#     long_df_agg1['call'] = wav

#     long_df_agg1['sil_driver'] = long_df_agg1['lavfi.silence_start'] - driver_detect_sil
#     long_df_agg1['sil_res'] = long_df_agg1['lavfi.silence_end'] + res_detect_sil

#     # Snip Files
#     #s = 0
#     os.system(r'cmd /c ffmpeg -i {} -ss 0s -t {}s -y -async 1 -strict -2 ..\\allC-Drivers-Snips\\{}_cdriver.wav'.format(wav, driver_detect_call,wav[:-4]))
#     for dum in long_df_agg1.index:
#         os.system(r'cmd /c ffmpeg -i {} -ss {}s -t {}s -y -async 1 -strict -2 ..\\allSilence-Snips\\{}_d{}.wav'.format(wav, long_df_agg1.loc[dum,'sil_driver'],driver_detect_sil,wav[:-4],long_df_agg1.loc[dum,'lavfi.silence_start']))
#         os.system(r'cmd /c ffmpeg -i {} -ss {}s -t {}s -y -async 1 -strict -2 ..\\allSilence-Snips\\{}_r{}.wav'.format(wav, long_df_agg1.loc[dum,'lavfi.silence_end'],res_detect_sil,wav[:-4],long_df_agg1.loc[dum,'lavfi.silence_start']))
#     #    s+=1
#     dd = pd.concat([dd,long_df_agg1], axis=0)
    
#     c+=1
# dd.reset_index(inplace=True, drop=True)
# dd['lavfi.silence_duration'] = dd['lavfi.silence_duration'].div(60)
# dd.groupby('call')['lavfi.silence_duration'].describe()
# %%
