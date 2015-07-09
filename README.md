# AlBoom
Simple app for downloading music from VK.

You can choose artist, pick album and download every song from it with 
a single click. 

We are using ITunes Store API for getting info about musicians, albums, songs. After retrieving this information, 
we are downloading all songs from VK social network (dominant in Russia), so if you'd like to use our app - you must
have an account in this network.

On the current stage auth is very stupid, because after opening auth page in browser window you have to copy and paste 
redirected url in special textbox manually. Token expiration handled bad, so you have to do it manually, after app crashes.

For retrieving actual statistics, you have to clear fields inside XML file with program data, (set money to 0).

TODO:
1) Implement token expiration checking

2) Deploy app.
