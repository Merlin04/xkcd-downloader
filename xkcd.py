import os, requests, sys, webbrowser, shelve, bs4

url = "http://xkcd.com"
args = sys.argv

db = shelve.open('db', writeback=True) # Yay SO

def getNewXkcd():
    # TODO: not need network to display. 
    print("Downloading latest comic...")
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    # Find the title. 
    titleElem = soup.select('#ctitle')[0].string
    print("\"" + titleElem + "\"")
    # Find the image. 
    comicElem = soup.select('#comic img')
    # Find the comic roll-over text. 
    comicText = comicElem[0].get('title')
    # Find the number of the comic with a very primitive method. 
    num = soup.text.split("Permanent link to this comic: http://xkcd.com/")[1][:4] # Splits html where the comic num is, then gets first 4 numbers. Will change on comic 10000. 
    # Do you have it?
    if (checkIfHave(num)):
        # Yes you do. 
        print("You already have that comic! Showing hover-over text...")
        input()
        print("\"" + comicText + "\"")
    else:
        # Nope. 
        # save the rollover text to db. 
        db[str(num)] = comicText
        # If nothing was downloaded...
        if (comicElem == []):
            # Self-explanatory. 
            print('Could not find comic. ')
        else:
            # Get the URL for the image. 
            comicUrl = ('http:' + comicElem[0].get('src'))
            # Find the extension. 
            extension = comicUrl.split('.')
            # print(extension)
            # Sort the thing. 
            extension.sort()
            # Don't ask. '
            extension = extension[2]
            # print(extension)
            print('Downloading image...')
            res = requests.get(comicUrl)
            res.raise_for_status()
            
            imageFile = open(os.path.join('xkcd' + str(num) + '.' + extension), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            print('Saved!')
            input("Press enter for hover-over text...")
            print("\"" + comicText + "\"")

def getNumXkcd(num):
    if (checkIfHave(num)):
        print("Downloading comic #" + str(num) + "...") # make it the same for both functions. 
        res = requests.get(url + '/' + str(num))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        titleElem = soup.select('#ctitle')[0].string
        print("\"" + titleElem + "\"")
        print("You already have that comic! Showing hover-over text...")
        input()
        print("\"" + db[str(num)] + "\"")
    else:
        print("Downloading comic #" + str(num) + "...")
        res = requests.get(url + '/' + str(num))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        titleElem = soup.select('#ctitle')[0].string
        print("\"" + titleElem + "\"")
        comicElem = soup.select('#comic img')
        comicText = comicElem[0].get('title')
        db[str(num)] = comicText
        if (comicElem == []):
            print('Could not find comic. ')
        else:
            comicUrl = ('http:' + comicElem[0].get('src'))
            extension = comicUrl.split('.')
            # print(extension)
            extension.sort()
            extension = extension[2]
            # print(extension)
            print('Downloading image...')
            res = requests.get(comicUrl)
            res.raise_for_status()
            imageFile = open(os.path.join('xkcd' + str(num) + '.' + extension), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            print('Saved!')
            input("Press enter for hover-over text...")
            print("\"" + comicText + "\"")

def checkIfHave(num):
    return (str(num) in str(os.listdir()))

def visit():
    webbrowser.open(url)

def update():
    raise(NotImplementedError)

def bookmarkView():
    # raise(NotImplementedError)
    try:
        print(db['bookmarks'])
    except:
        print('No bookmarks yet!')

def addBookmark(num, notes):
    print([str(num), str(notes)])
    try:
        db['bookmarks'].append([str(num), str(notes)])
    except:
        db['bookmarks'] = [[str(num), str(notes)]]

def downloadBookmark(num):
    raise(NotImplementedError)

def about():
    print("xkcd.py by Merlin04\nVisit me on Github!\n v0.1")
    print("A xkcd webcomic viewer. Automaticly names files according to number,\nand selects the file type to ensure they can be read. ")
    print("Based off of the XKCD Downloader in Automate the Boring Stuff with Python. ")

def usage():
    print("Just type 'python3 xkcd.py''")

def menu():
    print("""Choose an option:
    [1] Get latest comic
    [2] Get comic by number
    [3] View bookmarks list
    [4] Add bookmark
    [5] Download bookmark
    [6] Visit xkcd.com
    [7] Check for updates
    [8] About this program
    [9] Usage
    [0] Exit""")
    choice = int(input(">>> "))
    if choice == 1:
        getNewXkcd()
    elif choice == 2:
        getNumXkcd(input("Which one? "))
    elif choice == 3:
        bookmarkView()
    elif choice == 4:
        num = input("Number of comic to add: ")
        notes = input("Notes about it: ")
        addBookmark(num, notes)
    elif choice == 5:
        bookmarkView()
        downloadBookmark(input("Which one? "))
    elif choice == 6:
        visit()
    elif choice == 7:
        update()
    elif choice == 8:
        about()
    elif choice == 9:
        usage()
    elif choice == 0:
        exit


menu()
db.close()