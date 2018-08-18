# Humble-Downloader

Automatically download files from Humble Bundle - works for books, audio, etc.  Does not currently redeem Steam keys.

To install clone the project.  This will provide the two .py files you need:
    - DownloadHumble.py
    - auto_save_hb_html.py
    
Outside of the standard library the following are needed to run:
  - Requests
  - BeautifulSoup
  - clint
  - pyautogui
  
  
How To Use
On the command line run DownloadBundle.py from the root directory of where you wish to save the bundle.  There are several options you can use/activiate.
  '-a'    will turn on auto download.  This will give you a prompt to load the page of the bundle you wish to save.  Once you press enter           you have 5 seconds to click into that webpage and make it active.  The page will then be saved, scraped, and the files                   downloaded.  This will only work with browsers where 'CTRL+S' opens the save dialog so EDGE is not currently supported.  The             'captcha' protection on humble can be a real pain so this is the quickest/easy work around I could find at this time.
  
  '-dir'  followed by the path you would like to save the bundle. ex: -dir "books\Crypto 2" will save the bundle to your currently                   directory + books\Crypto 2. This is a requirement.
  
  '-b'    can change the byte size used to chunk the streaming file.  The default is 2048.
  
  '-f'    can specify type of file and will only download that file. ex: mp3, flac, pdf and  
  
  ex: DownloadBundle.py -a -dir "books/crypto" -b 1024
        This will prompt you to make the browser window with the bundle open active then download to books/cryto with a chunk size of 1024
        
      DownloadBundle.py -dir "read these first"
        This will ask you for the file name of the html for the bundle then download to a directory named "read these first" using the             default chunk size of 2048
        
        
     
