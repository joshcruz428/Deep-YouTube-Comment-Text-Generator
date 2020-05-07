import searcher
import downloader
import commentRefiner

import os
import argparse
import sys
import shutil
import random

#Randomly choose a video and comment to be the prefix for GPT-2
def get_random_comment(youtube_IDs,keyword):
    try:
        random_ID = youtube_IDs[random.randint(0,len(youtube_IDs)-1)]
    except:
        return get_random_comment(youtube_IDs, keyword)

    comments_path = "{kw}_comments/refined_comments_{ID}.txt".format(kw=keyword, ID =random_ID)

    with open(comments_path, 'r') as f:
        comments = f.readlines()
        try:
            if len(comments) == 0:
                return get_random_comment(youtube_IDs, keyword)
            comment = comments[random.randint(0,len(comments)-1)]
            comment.encode('ascii')
            if len(list(comment)) < 20 or list(comment)[0] == '@' or comment.find("'") != -1:
                f.close()
                return get_random_comment(youtube_IDs, keyword)
            else:
                f.close()
                return comment
        except:
            return get_random_comment(youtube_IDs, keyword)


def main(argv):
    parser = argparse.ArgumentParser(add_help=False, description=('Generate text based off a keyword using YouTube comments as a prefix for GPT-2'))
    parser.add_argument('--votesThreshold', '-vt', type=float, help='Minimum number of votes comment needs to be considered relevant')
    parser.add_argument('--hateLimit', '-hl', type=float, help='Maximum hate value allowed (between 0 and 1)')
    parser.add_argument('--offensiveLimit', '-ol', type=float, help='Maximum offensive value allowed (between 0 and 1)')
    parser.add_argument('--generalLimit', '-gl', type=float, help='Maximum sum of hate and offensive values (between 0 and 1)')
    parser.add_argument('--gptPath', '-gp', help='Path where gpt_2_simple_generate is located')
    parser.add_argument('--length', '-l', type=int, help='Length of output parameter for GPT-2')
    parser.add_argument('--nsamples', '-ns', type=int, help='Number of samples parameter for GPT-2')
    parser.add_argument('--batchSize', '-bs', type=int, help='Batch size parameter for GPT-2')
    parser.add_argument('--temperature', '-t', type=float, help='Temperature parameter for GPT-2')
    parser.add_argument('--output', '-o', help='Output destination')

    try:
        args = parser.parse_args(argv)

        vt = args.votesThreshold
        hl = args.hateLimit
        ol = args.offensiveLimit
        gl = args.generalLimit
        gp = args.gptPath
        l  = args.length
        ns = args.nsamples
        bs = args.batchSize
        t  = args.temperature
        output = args.output

        if not vt: vt = 20
        if not hl: hl = 0.4
        if not ol: ol = 0.7
        if not gl: gl = 0.8
        if not l:   l = 512
        if not ns: ns = 1
        if not bs: bs = 1
        if not t:   t = 0.7

        if not gp:
            parser.print_usage()
            raise ValueError('you need to specify where gpt_2_simple is')

        #Array of video IDs
        keyword, youtube_IDs = searcher.get_video_IDs()
        comment_directory = "{keyword}_comments".format(keyword=keyword)
        if not os.path.isdir(comment_directory):
            os.mkdir(comment_directory)

        for youtube_ID in youtube_IDs:
            jsonl_output = "comments_" + youtube_ID + ".jsonl"
            refined_comments = "refined_comments_{ID}.txt".format(ID=youtube_ID)

            if os.path.exists("{dir}/{file}".format(dir=comment_directory, file=refined_comments)):
                continue

            os.system('python downloader.py --youtubeid {ID} --output {output} --limit 1000'.format(ID=youtube_ID, output=jsonl_output))
            commentRefiner.refine_jsonl_file(jsonl_output, votes_threshold=vt, hate_limit=hl, offensive_limit=ol, general_limit=gl)
            shutil.move(jsonl_output, comment_directory)
            shutil.move(refined_comments, comment_directory)

        #Randomly choose a video and comment to be the prefix for GPT-2
        comment = get_random_comment(youtube_IDs, keyword)

        #Run GPT-2 using the random comment as the prefix
        cmdline = "{path}/gpt_2_simple generate --prefix '{comment}' --length {l} --batch_size {bs} --nsample {ns} --temperature {t}".format(path=gp,comment=comment,l=l,bs=bs,ns=ns,t=t)
        os.system(cmdline)

        if output:
            os.system(r"cat gen/* >> {output}".format(output=output))

    except Exception as e:
        print('Error:', str(e))
        sys.exit(1)

main(sys.argv[1:])
