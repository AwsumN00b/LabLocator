# School of Computing &mdash; Year 4 Project Proposal Form

## SECTION A

|                     |                    |
|---------------------|--------------------|
|Project Title:       | Lab Locator        |
|Student 1 Name:      | Ethan Clarke       |
|Student 1 ID:        | 19372086           |
|Student 2 Name:      | Evelina Prosyankina|
|Student 2 ID:        | 19368013           |
|Project Supervisor:  | Darragh OBrien     |

## SECTION B

### Introduction

> Our project, titled Lab Locator, aims to make it easier to check on the occupancy of the 
> computer labs in the McNulty Building to help students find a suitable room to do work and study.
> We want to create a mobile app that can tell a user information about the various computer labs.
> This would include the ability to check how busy labs are at the present moment, allowing students
> who might want a quieter space to work in to find a less populated room. We also wish to integrate
> with lab timetables to show what times are taken by actual classes so students can avoid those
> times, plan around them, or keep track of their own classes.
> Lab Locator will also be able to make predictions for future busy times based on previous data,
> to further assist students in planning their lab usage. The users will be able to visualise a daily
> timetable for each lab, displaying bookings made on rooms and how congested the rooms are at any
> given time.

### Outline

> Outline the proposed project.

### Background

> We picked up on this idea from Dr Darragh O'Brien's list of projects on his DCU page. It stood out
> to us because it highlighted a particular issue we were experiencing with the McNulty labs. We
> often use the labs as study or work rooms, as they are well suited for focusing on project and study
> work. However, it is difficult to predict when rooms will be generally available. Many courses
> use these rooms for labs and classes, and it is a lot of effort to manually keep track of which
> labs are available at any point of the day. In addition, many other students seek to use the labs
> as study rooms. There are many instances where labs can become full, at which point they may become
> loud and less suited for doing some peaceful work. We believe if we can harness the information
> available to us, we can alleviate these problems.

### Achievements

> What functions will the project provide? Who will the users be?

### Justification

> We believe our Lab Locator mobile app will be of use to all students of DCU who use the McNulty
> labs. It can help with productivity and allow students to plan their use of the labs, and avoid
> unwanted interruptions and distractions when they are utilising them. This could lead to increased
> productivity as students can make informed decisions about when and how they use the computer labs.
> The app will be usable both on and off campus with different available functionalities. While on
> campus users will be able to automatically be identified as part of a certain lab based on their
> connection to wireless networks. While away from the labs a user can check the current and future
> predictions for how busy the computer labs will be.

### Programming language(s)

> List the proposed language(s) to be used.

### Programming Tools / Tech stack

> Our project will operate largely out of the Android Studio IDE. We will be using Java as the main
> language that the phone application runs on. We will be using Gradle to help build the app, and
> the binaries will be running in Android Run Time, which is a specialised virtual machine designed
> for modern Android devices. This uses a register-based architecture, which differs from the typical
> JVM setup which would typically run a stack-based architecture.
> 
> We will be using a MySQL database to store information about labs and network connections, which
> we will use to determine a user's location by cross referencing the information we have with the
> user's environment. We intend to host both dev and live versions of the database, and we will make
> use of online cloud service platforms to assist us.
> 
> We intend on interfacing the database using a backend written in Python, which will be using the
> FastAPI library to function as a set of API endpoints. We will use a library such as MySQL Connector
> in order to communicate with the database.
> 
> We intend to use TensorFlow to create Machine Learning algorithms that can make predictions of
> the busiest times for each computer lab, and to help with identifying the lab that a student using
> our app is currently residing in. TensorFlow is a platform that allows you to configure and train
> ML models for your needs. We will be gathering data for all labs to use as training data. We will
> then use this data to train a model that will be able to make accurate guesses as to what room a
> student may be residing in.

### Hardware

> Describe any non-standard hardware components which will be required.

### Learning Challenges

> For this project, we will be working primarily out of the Android Studio integrated development
> environment. While we have experience using similar IDEs, such as IntelliJ, there are some features
> that Android Studio has that are important for the development of our mobile app that we will need
> to become accustomed to. This includes features like the android emulator, allowing us to run and
> test our project without the need for a real android device. We hope to use this for quick testing
> of the application. Android Studio also allows us to transfer the application binary over to our
> own android phones for proper testing in a real android environment. We will need to learn about
> appropriate build instructions and methods of testing in Android environments.
> 
> We intend to create a MySQL database to store information about networks that we will collect. We
> will need to plan our approach to creating a database model that makes sense and can efficiently
> store and retrieve data as needed. While we have worked with SQL database technology before, 
> creating and maintaining a database from scratch will be a new challenge.
> 
> We intend to use TensorFlow to create a model for predicting the busiest times of the computer
> labs. While we have some experience using TensorFlow to create machine learning models from previous
> projects, the application we want to employ this time is quite different and will require careful
> thought to make sure we use it in a way that creates a useful result.

### Breakdown of work

> Clearly identify who will undertake which parts of the project.
>
> It must be clear from the explanation of this breakdown of work both that each student is responsible for
> separate, clearly-defined tasks, and that those responsibilities substantially cover all of the work required
> for the project.

#### Student 1

> Ethan will be working primarily on the following sections of the project:
> - Database setup. From designing tables, to configuring MySQL. Designing a suitable and efficient
> database for use with the application. Setting up the database on an online cloud platform service
> so that the same data set can be accessed by both members of the team. Maintaining the database with
> proper, valid information.
> - Retrieving data from computer lab rooms, things like all WiFi connections in reach of a device
> from all rooms, and from several positions within each room. This will be collected, filtered, and
> used for both the database and for use with training a data model with machine learning.
> - Writing code that runs on the mobile application with the effect of collecting information about
> a user's current situation in the labs. This will run in the background of the app and shall be
> used to determine the whereabouts of the user based on the information gathered. This code will
> run constantly and check for changes in the device's surroundings, and will pass data to the
> backend to check for matching room signatures. It will not store any of this data, however.
> - Integrating with DCU official timetable systems to provide additional information on the
> general availability of computer labs. This will pull from existing APIs if they are available,
> otherwise it will scrape from timetabling sites to retrieve data.

#### Student 2

> *Student 2 should complete this section.*
