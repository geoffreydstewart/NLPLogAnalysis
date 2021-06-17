# NLPLogAnalysis

This project uses NLP techniques to automatically perform analysis on set of log files. Specifically, the application uses sklearn's TfidfVectorizer to identify the most important log messages which are n-grams, from the logs. This is a fast and effective way to gain valuable insights about a collection of log files.

The project contains four sets of example log files in the **logSamples** directory which can be used to test the application. The actual application code is in the **code** directory.

### How to use the application

The first thing to do is see the available options by running the application with the help option:

```
./get_log_insights.py -h

```

To find the top 10 6-grams in a set of Apache Web Server error logs the following command would be used:

```
./get_log_insights.py -t apache-error -n 6 -i ../logSamples/error1/

```

The application also supports Apache Web Server access logs. To find the most common 5-grams in a set of Apache access logs the following command would be used:

```
./get_log_insights.py -t apache-error -n 6 -i ../logSamples/access2/

```

The project currently supports the analysis of Apache Web Server error log and access logs. The application can easily support any type of log file by implementing the LogHandlerInterface class, which mostly requires to code a parser specific to that log file type.