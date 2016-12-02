# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: sco1
# Collaborators:
# Time: 1:30

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate = pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        """
        Initialize a News Story object
        Attributes include:
            guid - Globally Unique Identifier, string
            title - Story title, string
            description - Story description, string
            link - http link to more content, string
            pubdate - Publication date, datetime
        """
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        """
        Globally Unique Identifier getter
        Returns a string
        """
        return self.guid
    
    def get_title(self):
        """
        News story title getter
        Returns a string
        """
        return self.title

    def get_description(self):
        """
        News story description getter
        Returns a string
        """
        return self.description

    def get_link(self):
        """
        http link getter
        Returns a string
        """
        return self.link

    def get_pubdate(self):
        """
        Publication date getter
        Returns a datetime
        """
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    
    def __init__(self, phrase):
        """
        Initialize a Title Trigger object
        Attributes include:
            phrase - Trigger phrase, string

        evaluate will trigger if phase is contained in the story's title
        """
        self.phrase = phrase.lower()  # Triggers are not case sensitive

    def get_phrase(self):
        """
        Trigger phrase getter
        Returns a string
        """
        return self.phrase

    def is_phrase_in(self, text):
        """
        Tests to see if the object's trigger phrase is contained by the input
        text string

        Returns True if the input text string contains the object's trigger 
        phrase
        """
        # Use a regex to split the input string on one or more non-word 
        # characters. This should take care of one or more whitespace characters
        # along with one or more punctuation characters
        splitinput = re.split('\W+', text.lower())  # Lowercase because we're case insensitive

        # Join the words with spaces for comparison to the phrase. Per the 
        # problem statement, phrase is assumed to not contain punctuation or 
        # multiple consecutive spaces
        testtxt = ' '.join(splitinput)
        # Bracket our trigger phrase with \b to keep the regex from matching our
        # phrase if any of the strings are part of other words. Strings like 
        # 'apurple cow' and 'purple cowpie' would trigger with 'purple cow' 
        # otherwise
        if re.findall(r'\b' + self.phrase + r'\b', testtxt):
            return True
        else:
            return False

# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """
        Initialize a Title Trigger object
        Attributes include:
            phrase - Trigger phrase, string

        evaluate will trigger if phase is contained in the story's title
        """
        super().__init__(phrase)
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """

        # Test to see if phrase is contained in the input story's title
        # string. Return True if the phrase is in the title, False
        # otherwise.
        if self.is_phrase_in(story.get_title()):
            return True
        else:
            return False

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """
        Initialize a Description Trigger object
        Attributes include:
            phrase - Trigger phrase, string

        evaluate will trigger if phase is contained in the story's description
        """
        super().__init__(phrase)
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """

        # Test to see if phrase is contained in the input story's Description
        # string. Return True if the phrase is in the description, False
        # otherwise.
        if self.is_phrase_in(story.get_description()):
            return True
        else:
            return False

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, timeinput):
        """
        Initialize a Time Trigger object
        Attributes include:
            timeinput - Trigger time, string "%d %b %Y %H:%M:%S" 
            
        Input time is assumed to be Eastern Standard Time
        """

        datetimeinput = datetime.strptime(timeinput, "%d %b %Y %H:%M:%S")  # Parse input time string
        datetimeinput = datetimeinput.replace(tzinfo=pytz.timezone('EST'))  # Switch TZ to EST without conversion
        self.triggertime = datetimeinput
    
    def get_triggertime(self):
        """
        Trigger time getter
        Returns a datetime
        """
        
        return self.triggertime

# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, triggertime):
        """
        Initialize a Before Time Trigger object
        Attributes include:
            triggertime - Query time, string "%d %b %Y %H:%M:%S" 
            
        Input time is assumed to be Eastern Standard Time

        evaluate will trigger if publication datetime is before triggertime
        """
        super().__init__(triggertime)
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """

        # Test the trigger's query datetime against the input story's 
        # publication datetime. Return True if the publication datetime is
        # before the trigger's query datetime, False otherwise.
        if self.get_triggertime() > story.get_pubdate():
            return True
        else:
            return False

class AfterTrigger(TimeTrigger):
    def __init__(self, triggertime):
        """
        Initialize an After Time Trigger object. 
        Attributes include:
            triggertime - Query time, string "%d %b %Y %H:%M:%S" 
            
        Input time is assumed to be Eastern Standard Time

        evaluate will trigger if publication datetime is after triggertime
        """
        super().__init__(triggertime)
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        
        # Test the trigger's query datetime against the input story's 
        # publication datetime. Return True if the publication datetime is
        # after the trigger's query datetime, False otherwise.
        if self.get_triggertime() < story.get_pubdate():
            return True
        else:
            return False


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    """
    Inverts the output of the input trigger

    othertrigger: Trigger object with an evaluate method that returns a boolean

    Returns: Boolean
    """
    def __init__(self, othertrigger):
        self.othertrigger = othertrigger
    
    def evaluate(self, story):
        # Call the other trigger's evaluate method on the input story and invert
        # the boolean output
        return not self.othertrigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    """
    Performs a logical AND on the outputs of the evaluate methods of two trigger
    objects

    othertrigger1: Trigger object with an evaluate method that returns a boolean
    othertrigger2: Trigger object with an evaluate method that returns a boolean

    Returns: Boolean
    """
    def __init__(self, othertrigger1, othertrigger2):
        self.othertrigger1 = othertrigger1
        self.othertrigger2 = othertrigger2
    
    def evaluate(self, story):
        # Call the other triggers` evaluate methods on the input story and
        # perform a logical AND on their boolean outputs
        return self.othertrigger1.evaluate(story) and self.othertrigger2.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    """
    Performs a logical OR on the outputs of the evaluate methods of two trigger
    objects

    othertrigger1: Trigger object with an evaluate method that returns a boolean
    othertrigger2: Trigger object with an evaluate method that returns a boolean

    Returns: Boolean
    """
    def __init__(self, othertrigger1, othertrigger2):
        self.othertrigger1 = othertrigger1
        self.othertrigger2 = othertrigger2
    
    def evaluate(self, story):
        # Call the other triggers` evaluate methods on the input story and
        # perform a logical OR on their boolean outputs
        return self.othertrigger1.evaluate(story) or self.othertrigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    triggeredstories = []
    # Iterate through the stories in stories
    for story in stories:
        # Call each trigger in triggerlist on the story. If the trigger returns
        # True, add the story to the list of triggered stories
        for trigger in triggerlist:
            if trigger.evaluate(story):
                triggeredstories.append(story)
    
    return triggeredstories

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """

    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    triggerlist = []  # Initialize the output trigger list
    triggers = {}  # Initialize a dictionary to keep track of the generated triggers by name
    # Iterate over the lines returned by the above parser.
    for triggerstr in lines:
        # Split the line on the commas to get the generation parameters
        triggerparameters = triggerstr.split(',')
        
        # First word on each line should be either ADD or the name of a trigger
        # If it's not ADD, assume it's the name of the trigger
        if triggerparameters[0] == 'ADD':
            # Remaining words in the line should correspond to the triggers to 
            # add to the output list. Assume each word corresponds to a key in 
            # our dictionary of triggers
            for triggerkey in triggerparameters[1:]:
                triggerlist.append(triggers[triggerkey])
        else:
            # Not an ADD line so a trigger object needs to be generated
            # First word on the line should be the name of the trigger, which 
            # we'll use as the dictionary key in triggers.
            # Second word should be the trigger type, the remaining words should
            # correspond to the relevant trigger class' constructor parameters.
            # We'll pass all of these to our helper function.
            triggername = triggerparameters[0]
            triggertype = triggerparameters[1]

            # Check for the conditional triggers, in this case the remaining 
            # strings on the line should correspond to keys in our triggers dict
            # We need to get the corresponding trigger object(s) so we're not 
            # passing a string to the constructor when it's expecting an object
            conditionaltriggers = ['NOT', 'AND', 'OR']
            if triggertype in conditionaltriggers:
                subtriggers = []
                for triggerkey in triggerparameters[2:]:
                    subtriggers.append(triggers[triggerkey])
                # Pass the appropriate parameters to the trigger helper
                triggers[triggername] = buildtrigger(triggertype, subtriggers)
            else:
                # Pass the appropriate parameters to the trigger helper
                triggers[triggername] = buildtrigger(triggertype, triggerparameters[2:])
    
    return triggerlist
        

def buildtrigger(triggertype, triggerinput):
    """
    Helper function that acts as a faux switch/case block for generating the 
    appropriate trigger given the input trigger type

    triggertype: A string corresponding to one of our trigger classes (e.g. TITLE, DESCRIPTION, etc.)

    triggerinput: List of inputs to the relevant trigger class' constructor. The
                  length and object type of this list is dependent on the 
                  the relevant class' constructor inputs:

                  e.g. TITLE is length 1, the phrase string
                       AFTER is length 1, the date string
                       AND is length 2, the trigger objects
                       

    Returns: A trigger object. If no valid trigger type was passed, buildtrigger
             returns None
    """
    
    # Switch until we get our case and call the appropriate class' constructor
    triggertype = triggertype.upper()  # Uppercase for a more generous comparison
    if triggertype == 'TITLE':
        trigger = TitleTrigger(triggerinput[0])
    elif triggertype == 'DESCRIPTION':
        trigger = DescriptionTrigger(triggerinput[0])
    elif triggertype == 'AFTER':
        trigger = AfterTrigger(triggerinput[0])
    elif triggertype == 'BEFORE':
        trigger = BeforeTrigger(triggerinput[0])
    elif triggertype == 'NOT':
        trigger = NotTrigger(triggerinput[0])
    elif triggertype == 'AND':
        trigger = AndTrigger(triggerinput[0], triggerinput[1])
    elif triggertype == 'OR':
        trigger = OrTrigger(triggerinput[0], triggerinput[1])
    else:
        # No match for our triggertype
        # Let Python handle any other errors
        trigger = None

    return trigger

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("election")
        # t2 = DescriptionTrigger("Trump")
        # t3 = DescriptionTrigger("Clinton")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
