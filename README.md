# Deep YouTube Comment Text Generator
Based off a keyword, downloads comments from YouTube videos and randomly uses one of the comments as a prefix for OpenAI's GPT-2 simple model.

##Background
This is a class project for Professor Marc Downie's Spring 2020 class 'New Media at a Distance' at the University of Chicago. I wanted to explore how any keyword implicitly creates bodies of text on the Internet, lots of which is completely irrelevant to the keyword itself. The forms of discussion found in YouTube comments is often  chaotic, but they are interesting explorations of the unpredictable but sometimes highly creative presentations of people's reactions to media on the Internet. I wanted to harness this unpredictability and see what happens if we let GPT-2 create sentences using a comment found through the use of any keyword. Namely, I wanted to see if different keywords provided unique enough prefixes to make the prompts of a vastly different character, or whether the keyword was irrelevant, which would suggest that the goal of a YouTube comment is to interact with the Internet as a piece of interactable media, rather than the presented media itself.

I hope to update this repo with interesting examples.

## Dependencies
* Python 2.7+
* requests
* lxml
* cssselect
* hatesonar
* google.oauth2.credentials
* googleapiclient
* google_auth_oauthlib
* httplib2

You will need to have gpt_2_simple running on your computer.

You will also need YouTube Data API v3 in a client_secret.json file. 

### Usage
```
usage: python3 downloader.py [--help] [--gptPath gp][--votesThreshold vt] [--hateLimit hl] [--offensiveLimit ol] [--generalLimit gl] [--length l] [--nsamples ns] [--batchSize bs] [--temperature t]

Only the --gptPath argument is mandatory. This argument specifies the path where gpt_2_simple is located.

Offensive and hate speech are filtered out using hatesonar, which returns probabilities of a body of text being considered offensive or hate speech. The optional hateLimit and offensiveLimit parameters limit set the limit for a comment to be considered relevant. The optional generalLimit parameter limits their sum.

If a keyword is searched, it will download the comments in a directory within the on

optional arguments:
  --help, -h            Show this help message and exit
  --votesThreshold vt, -vt vt
                        Minimum number of votes comment needs to be considered relevant
  --hateLimit hl, -hl hl  
                        Maximum hate value allowed (between 0 and 1)
  --offensiveLimit ol, -ol ol,
                        Maximum offensive value allowed (between 0 and 1)
  --generalLimit gl, -gl gl
                        Maximum sum of hate and offensive values (between 0 and 1)
  --length' l, '-l' l
                        Length of output parameter for GPT-2
  --nsamples ns, -ns ns
                        Number of samples parameter for GPT-2
  --batchSize bs, -bs bs
                        Batch size parameter for GPT-2
  --temperature t, -t t
                        Temperature parameter for GPT-2
  --output o, -o o
                        Output destination
```
