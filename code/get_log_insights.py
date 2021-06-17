#!/usr/bin/env python3

"""
This is an executable Python3 script to identify the important log messages from a directory
of a common type of log messages.

Currently, the following log file types are supported:
- Apache error logs
- Apache access logs

To process all the apache error log files from the provided directory using 5-grams:
./get_log_insights.py -t apache-error -n 5 -i /Users/gstewart/mscs/cpsc57400/project/error-logs

"""

import glob
import os
import sys
import traceback

from optparse import OptionParser
from sklearn.feature_extraction.text import TfidfVectorizer

from log_handlers import ApacheErrorLogHandler, ApacheAccessLogHandler


class GetLogInsightsException(Exception):
    """ Exception to indicate errors during program execution. """
    def __init__(self, message='', exitcode=1):
        super(GetLogInsightsException, self).__init__(message)
        self.message = message
        self.exitcode = exitcode


SUPPORTED_LOG_TYPES = ['apache-error', 'apache-access']


def validate_input():
    """
    Validates script inputs
    :rtype: options - the provided options
    :raises:  GetLogInsightsException
    """
    usage = "Usage: %prog [options]"
    # Since we are using Python3, it actually might be better to use argparse instead of optparse
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--log-type", dest="log_type", default="",
                      help="The type of logs to be analyzed. Currently supports: %s" % SUPPORTED_LOG_TYPES)
    parser.add_option("-n", "--num-grams", dest="num_grams", default=5, help="Number n in n-grams")
    parser.add_option("-i", "--input-dir", dest="input_dir", default="", help="Input dir")

    options, args = parser.parse_args()

    if not options.input_dir:
        raise GetLogInsightsException('The option "i" must be provided as -i /path/to/server/logs')

    if options.log_type not in SUPPORTED_LOG_TYPES:
        raise GetLogInsightsException('The option "t" must be provided as -t <log_type>. Valid log types are %s' %
                                      SUPPORTED_LOG_TYPES)

    return options


def analyze_log_files(log_handler, input_dir, n):
    """
    Perform the log file analysis
    :param LogHandlerInterface log_handler: the Log Handler implementation to be used during analysis
    :param path input_dir: the path to check for matching log files
    :param int n: the number n of n-grams. 3 would show trigrams.
    """
    if not os.path.exists(input_dir):
        raise GetLogInsightsException('The input_dir at path %s does not seem to exist' % input_dir)

    paths = get_matching_log_files(input_dir, log_handler.get_log_file_prefixes())
    print()
    print('Identified %s files for parsing' % len(paths))

    log_record_list = []
    for path in paths:
        log_record_list.extend(log_handler.parse_log_file(path))

    print('There are %s log records in this data' % len(log_record_list))
    print()

    common_words = get_top_ngrams(log_record_list, n)
    n_gram_label = '%s-GRAMS' % str(n)
    print("{0:65}{1:5}".format(n_gram_label, 'TF-IDF VALUE'))
    for word, freq in common_words:
        print("{0:70}{1:5.2f}".format(word, freq))


def get_matching_log_files(input_dir, log_prefixes_list):
    """
    Expand the list of matching log files
    :param path input_dir: the path to check for matching log files
    :param str log_prefixes_list: the list of patterns to use for matching log files
    :rtype: list - a list of full paths for every matched log file
    """
    error_file_list = []
    for log_prefix in log_prefixes_list:
        error_file_list.extend(glob.glob('%s/%s*' % (input_dir, log_prefix)))
    return sorted(error_file_list, key=os.path.getmtime)


def get_top_ngrams(record_list, n):
    """
    Uses the scikit-learn TfidfVectorizer to compute the top 10 n-grams
    :param list record_list: the list of all log records
    :param int n: the number n of n-grams. 3 would show trigrams.
    :rtype: words_freq[:10] - a list of the top 10 n-grams
    """
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(n, n), lowercase=False, token_pattern=r'\S+', smooth_idf=False)
    bag_of_words = tfidf_vectorizer.fit_transform(record_list)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in tfidf_vectorizer.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:10]


def print_exception(message):
    print(message)
    print(traceback.format_exc())


def main():
    print()
    print('Starting the Get Log Insights application!')

    try:
        options = validate_input()
    except GetLogInsightsException as ve:
        print(ve.message)
        sys.exit(ve.exitcode)

    try:
        if options.log_type == 'apache-error':
            log_handler = ApacheErrorLogHandler()
        # TODO: as more log handlers are supported, this logic needs to be updated
        else:
            log_handler = ApacheAccessLogHandler()
        analyze_log_files(log_handler, options.input_dir, int(options.num_grams))
    except GetLogInsightsException as e:
        print_exception(e.message)
        sys.exit(e.exitcode)
    except Exception as e:
        print_exception(e)
        sys.exit(1)


if __name__ == "__main__":
    main()

