# Twitter2JSON
This project is using the Python to crawl Twitter tweet data, then output these data to the JSON file. It works with Python versions from 2.7+. In this project, we using the Python logging library with the aim of collecting any errors or warning in the case program failure, also we added Twitter API rate limit and error management capability, so we can ensure more resilient calls to Twitter without getting barred for tapping into the firehose.

##Data Source
The data source is from the [Twitter REST API](https://dev.twitter.com/rest/public).

##Data Format
The data set is using the JSON format.

##JSON Schema

|     Field     |    Type    |             Description                     |
| ------------- | :--------- | :----------------------------------------   
|  created\_at   |   String   | UTC time when this Tweet was created.       | 
|      id       |   Int64    | The integer representation of the unique identifier for this Tweet. |
|     id\_str    |   String   | The string representation of the unique identifier for this Tweet.|
|     text      |   String   | The actual UTF-8 text of the status update. |
|  source  |  String  | Utility used to post the Tweet, as an HTML-formatted string. Tweets from the Twitter website have a source value of web.|
|   truncated   |   Boolean  | Indicates whether the value of the text parameter was truncated.|
| in\_reply\_to\_status\_id  |  Int64 |  Nullable. If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s ID.        | 
| in\_reply\_to\_status\_id\_str |  String  |  Nullable. If the represented Tweet is a reply, this field will contain the string representation of the original Tweet’s ID.   |
|  in\_reply\_to\_user\_id  |  Int64  | Nullable. If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s author ID. |
| in\_reply\_to\_user\_id\_str  |  String  |  Nullable. If the represented Tweet is a reply, this field will contain the string representation of the original Tweet’s author ID. |
|  in\_reply\_to\_screen\_name  |  String  | Nullable. If the represented Tweet is a reply, this field will contain the screen name of the original Tweet’s author. |
| user  | Users |  The user who posted this Tweet. [More details.](https://dev.twitter.com/overview/api/users)|
|  geo  | Object | **Deprecated.** Nullable. Use the “coordinates” field instead. |
| coordinates |  Coordinates  | Nullable. Represents the geographic location of this Tweet as reported by the user or client application. [More details.](https://dev.twitter.com/overview/api/tweets#obj-coordinates)|
| place | Places  | Places	Nullable. When present, indicates that the tweet is associated (but not necessarily originating from) a Place. [More details.](https://dev.twitter.com/overview/api/places)|
| contributors | Collection of [Contributors](https://dev.twitter.com/overview/api/tweets#obj-contributors)  |  Nullable. An collection of brief user objects (usually only one) indicating users who contributed to the authorship of the tweet, on behalf of the official tweet author. |
| retweeted_status  |  [Tweet](https://dev.twitter.com/overview/api/tweets)  | Users can amplify the broadcast of tweets authored by other users by retweeting. Retweets can be distinguished from typical Tweets by the existence of a **retweeted_status** attribute. This attribute contains a representation of the original Tweet that was retweeted. |
| retweet_count | Int | Number of times this Tweet has been retweeted.|
| favorite_count | Integer | Nullable. Indicates approximately how many times this Tweet has been “liked” by Twitter users.|
| entities | Entities  | Entities which have been parsed out of the text of the Tweet. [More details.](https://dev.twitter.com/overview/api/entities)|
| favorited | Boolean  | Nullable. Perspectival. Indicates whether this Tweet has been liked by the authenticating user.|
| retweeted | Boolean | Perspectival. Indicates whether this Tweet has been retweeted by the authenticating user.|
| possibly_sensitive | Boolean  | Nullable. This field only surfaces when a tweet contains a link. The meaning of the field doesn’t pertain to the tweet content itself, but instead it is an indicator that the URL contained in the tweet may contain content or media identified as sensitive content.|
| filter_level | String |  Indicates the maximum value of the filter_level parameter which may be used and still stream this Tweet. So a value of medium will be streamed on none, low, and medium streams. |
| lang |  String  | Nullable. When present, indicates a [BCP 47](http://tools.ietf.org/html/bcp47) language identifier corresponding to the machine-detected language of the Tweet text, or “und” if no language could be detected. 

Reference from [Twitter Developer Document](https://dev.twitter.com/overview/api/tweets).

##Configuration
* Required configuration options in line 42 to line 45 of "source code/Twitter2JSON.py" file :
<pre>consumer_key = 'Your application\'s consumer key'
consumer_secret = 'Your application\'s consumer secret'
access_token = 'Your OAuth token'
access_secret = 'Your OAuth token secret'</pre>
* Set up the JSON output file path in line 69 of "source code/Twitter2JSON.py" file :
<pre>jsonFpath = '/home/william/Python/Twitter/Data/JSON'</pre>
* Set up the log message file path in line 59 of "source code/Twitter2JSON.py" file :
<pre>logPath = '/home/william/Python/Twitter/Log'</pre>

You need to create an application on Twitter, and paste the key on it. For more informations, you can follow the link: [https://apps.twitter.com/app/new](https://apps.twitter.com/app/new)


This program is reference from "[Spark for Python Developers](https://www.packtpub.com/big-data-and-business-intelligence/spark-python-developers)".