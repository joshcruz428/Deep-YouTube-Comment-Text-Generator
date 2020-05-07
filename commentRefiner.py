import json_lines
import os
from hatesonar import Sonar

#Only includes the comments in a txt file, given that the comment has over a certain number of votes
#This also attempts to use Sonar to filter out hate speech
def refine_jsonl_file(path, votes_threshold=10, hate_limit=0.4, offensive_limit=0.7, general_limit=0.8):
    sonar = Sonar()
    name, _ = os.path.splitext(path)
    refined_name = "refined_{name}.txt".format(name = name)

    if os.path.exists(refined_name):
        os.remove(refined_name)
    refined_file = open(refined_name, mode='w')

    with open(path, 'rb') as f: # opening file in binary(rb) mode
        with refined_file as rf:
            for item in json_lines.reader(f):
                if int(item['votes']) > 0:
                    text = item['text']
                    hate_confidence = sonar.ping(text=text)['classes'][0]['confidence']
                    offensive_confidence = sonar.ping(text=text)['classes'][1]['confidence']
                    if not((hate_confidence > hate_limit) or (offensive_confidence > offensive_limit)
                        or (hate_confidence + offensive_confidence > general_limit)):
                            try:
                                print(text, file=rf)
                            except:
                                continue
            rf.close()
        f.close()
