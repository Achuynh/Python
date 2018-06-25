import sys
import spotipy
import spotipy.util as util


#export SPOTIPY_CLIENT_ID = 'eed22472233a4b98b2c13c1db5cbd030'
#export SPOTIPY_CLIENT_SECRET = '279136bca0d24eb2985189bda17436aa'
#export SPOTIPY_REDIRECT_URI = 'spotify:user:1255782308'

username = 'Andy Huynh'
scope = 'user-read-currently-playing'

token = util.prompt_for_user_token(username, scope, client_id='eed22472233a4b98b2c13c1db5cbd030',client_secret='279136bca0d24eb2985189bda17436aa',redirect_uri='http://localhost/')
sp = spotipy.Spotify(auth=token)
