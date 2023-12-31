# SLOScraper

## Context

The SLOScraper is the task assigned to Butte College's Programming Project class for Spring 2019, the capstone course for the Computer Programming AS degree.

Course instructor: April Browne

## Purpose

The purpose of the SLOScraper is to scrape the Butte College website's [list of academic programs](https://butte.edu/academicprograms) for data and store it in an authoritative database.

For each program, we will collect:
* The program's name
* The program's type (AA, AS, CERT, etc.)
* The program learning outcomes (PLOs)

This information will then be sent to the database to be stored.

## Project Requirements

Find our detailed project requirements [here](project_reqs.md).

## Installation

Find our installation guide [here](Installation%20Guide.md).

## Code Documentation

Find our code documentation [here](https://github.com/Mechami/slo_scraper/wiki/Documentation).

## Usage

As the SLOScraper is only designed for use at Butte College, the user base and application for the software is narrow.

### User Base

The user base will consist mainly of department chairs and the PLO Coordinator.

### Expected Output

SLOScraper should collect changes to the programs and PLOs and send them to the database. The database should ignore duplicates. The python script should print status updates as it runs, and should count the number of programs it collects. At the time of publishing, that number should be 190.

### How to Use SLOScraper

For detailed instructions on how to use the software, see our user guide [here](User_Guide/).

## Authors and Acknowledgments

The authors for SLOScraper, in no particular order, are:
* Isaac Vander Sluis (Project Manager)
* Kaden Hurlimann (Testing Lead)
* Philip Muzzall (Tech Lead)
* Nick Leyson (Database Architect)
* Cyrus Lopez (Software Architect)

The starting code was written and given to us by Boyd Trolinger.

Our instructor April Browne helped us apply development methodologies and best practices to this project.

## Roadmap

For future Programming Project classes, there is more to do to enhance the SLOScraper. Namely, the student learning outcomes (SLOs) for all Butte College courses should also be scraped and stored in the database. Also, as SLOScraper is used and adopted, there will undoubtedly be bugs or usability issues that should be fixed.

## Project Status

Development for this project will stop by the end of the current semester (May 24th, 2019). However, future Programming Project classes may well branch the project to continue it with further versions. In that event, this readme should be updated and linked to the current version of the SLOScraper.
