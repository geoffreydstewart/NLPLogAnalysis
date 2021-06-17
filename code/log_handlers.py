"""
This file contains the log handler interface and the log handler classes which implement it
"""

import abc


class LogHandlerInterface(object):
    """ This is the Log Handler interface class """
    __metaclass__ = abc.ABCMeta

    @staticmethod
    @abc.abstractmethod
    def get_log_file_prefixes():
        """
        Return the log file prefixes to match log files in directory
        :rtype: list of strings where each is a prefix which can be used to match log files
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def parse_log_file(path):
        """
        Parses the file at the specified path into log records
        :param path: the path to a log file
        :rtype: list of log records
        """
        pass


class ApacheErrorLogHandler(LogHandlerInterface):
    """
    A log handler class for Apache Web Server Error logs.
    A concrete implementation of the LogHandlerInterface.
    """

    @staticmethod
    def get_log_file_prefixes():
        """
        Return the log file prefixes to match log files in directory
        :rtype: list of strings where each is a prefix which can be used to match log files
        """
        prefixes = ['error_log', 'ssl_error_log']
        return prefixes

    @staticmethod
    def parse_log_file(path):
        """
        Parses the file at the specified path into log records
        :param path: the path to a log file
        :rtype: list of log records
        """
        log_record_list = []
        with open(path, "r") as file_to_read:
            lines = file_to_read.readlines()

            for line in lines:
                tmp_str_arr = line.split('] ')
                if len(tmp_str_arr) > 2:
                    log_record = ' '.join(tmp_str_arr[2:])
                    log_record_list.append(log_record)

        return log_record_list


class ApacheAccessLogHandler(LogHandlerInterface):
    """
    A log handler class for Apache Web Server Access logs.
    A concrete implementation of the LogHandlerInterface.
    """

    @staticmethod
    def get_log_file_prefixes():
        """
        Return the log file prefixes to match log files in directory
        :rtype: list of strings where each is a prefix which can be used to match log files
        """
        prefixes = ['access_log', 'ssl_access_log']
        return prefixes

    @staticmethod
    def parse_log_file(path):
        """
        Parses the file at the specified path into log records
        :param path: the path to a log file
        :rtype: list of log records
        """
        log_record_list = []
        with open(path, "r") as file_to_read:
            lines = file_to_read.readlines()

            for line in lines:
                tmp_str_arr = line.split(' - - [')
                client_ip = tmp_str_arr[0]
                rest_of_rec_arr = tmp_str_arr[1].split('] "')
                rest_of_rec = rest_of_rec_arr[1].replace('"', '')
                rest_of_rec = rest_of_rec.replace('-', '')
                log_record = '%s %s' % (client_ip, rest_of_rec)
                log_record_list.append(log_record)

        return log_record_list

# TODO: Add more log handlers!
