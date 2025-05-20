This microservice is a webscraper of alternatehistory.com that fetches the thread author, thread title, and page number.
To request DATA I am using python library requests which allows me to take the user input of the desired URL
        import requests
        response = req.get(url) This is example code of how the program is requesting information

The service receives data with the help of python library beautifulsoup4 which is an HTML parser so that when we request data from the URL
the parser makes it easier for us to extract information from the given elements of the webpage for example:
                title_tag = soup.find("h1", class_="p-title-value")
this will parse the information from header 1 which will be the title of each story. 
