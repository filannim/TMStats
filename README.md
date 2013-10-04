TMStats
=======
This software simulates an NLP scientific challenge with a variable number of participants, ranges and epochs. I developed it to show how confident a participant can be of his rank. I generate N participants, with their relative final F1 score. I then order them to obtain a rank. I iterate this process EPOCH times and count how many times the expected rank is equal to the simulated rank. The process is affected by the numbers of istances in the test set. You can easily see from the pictures that when you have small test sets the reliability of the rank is low. As expected, the official ranking becomes reliable as soon as we increase the number of test istances.

This was to show that the final ranking of a scientific challenge (that has a certain number of participants) has a statistical significance only if the official benchmark test set is larger than a certaing threshold.
