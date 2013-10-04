TMStats
=======
![ScreenShot](https://raw.github.com/filannim/TMStats/master/_gfx/21_0748_0005.png)

This script simulates NLP scientific challenges with a variable number of participants, score ranges and epochs.
I developed it to show how confident a participant can be of a final official rank. Of course, it is just a statistical simulation with some assumptions which can be too strict.

I generate N participants, with their relative final F1 score. I then order them to obtain a rank. I iterate this process EPOCH times and count how many times the expected rank is equal to the simulated rank. The process is affected by the numbers of istances in the test set. You can easily see from the pictures that when you have small test sets the reliability of the rank is low. As expected, the official ranking becomes reliable as soon as we increase the number of test istances.

This was to show that the final ranking of a scientific challenge (that has a certain number of participants) has a statistical significance only if the official benchmark test set is larger than a certaing threshold.











##How to

###read the graph

The picture above shows you the results for a challenge with 21 participant, expected top score 74.8% F1, standard deviation of 0.0005. Each simulation has been generated 5000 times.
The Top N curve shows, depending on the size of the test set, how many times the real top N participants corresponded to the simulated top N participants.
In the graph above you can see that, for 2000 samples, only 50% of the time the real full ranking corresponded to the simulated ones. For the same test set size, 85% of the time the real top 8 participants corresponded to the top 8 simulated ones in that very order.

###simulate a challenge
To visualize other simulated rankings with different parameter, use:

    $ python participant.py <minimum test set size> 
                            <maximum test set size>
                            <step test set size>
                            <trials>
                            <number of participants>
                            <expected top score>
                            <standard deviation>
                            <% of CPU to use>

For example:

    $ python participant.py 0 6000 25 5000 21 0.748 0.0005 0.5
will compute the graph above using half of the CPU cores you have on your machine.














##Content
* batch_simulation.py
* participant.py
* temp.mem

The file temp.mem contains all the pre-computed simulated rankings generate by batch_simulation.py.

Those are the parameters:
* number of participants = [1,30]
* trials = 10000
* minimum test set size = 0 samples
* step for test set size = 25 samples
* maximum test set size = 6000 samples
* expected maximum score per challenge = from 30% to 100%, step=5%
* standard deviations = [0.0001, 0.0002, 0.0005, 0.001, 0.005]








##Examples

    $ python participant.py 0 5000 25 10000 30 0.95 0.0001
![ScreenShot](https://raw.github.com/filannim/TMStats/master/_gfx/30_095_0001.png)
    
    $ python participant.py 0 5000 25 10000 10 0.95 0.0001
![ScreenShot](https://raw.github.com/filannim/TMStats/master/_gfx/10_095_0001.png)

    $ python participant.py 0 5000 25 10000 10 0.95 0.0005
![ScreenShot](https://raw.github.com/filannim/TMStats/master/_gfx/10_095_0005.png)














##License

(GPL v2)

Copyright (c) 2012 Michele Filannino, <http://www.cs.man.ac.uk/~filannim/>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

##Contact
- Email: filannim@cs.man.ac.uk
- Web: http://www.cs.man.ac.uk/~filannim/
