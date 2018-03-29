# Ironman
This repository looks at some rudimentary statistics for Ironman Nice.  The question "what is a good time?" is generally met with the response "well that depends on...." The goal here is to show the distribution of times, and based on your perceived capability with respect to your peers, make yourself a goal. 

If anyone takes the time to read through this, or better still use it, I hope it helps you, and good luck on the day.

Scraping the website is done in 3 different stages:
 - The races
 - The results in summary (times only)
 - The detailed resuts from the athletes page
 
 Currently the project offers the following modules and classes to help process the information:
 
  - site_scraping_classes
      - results_parser (get results from a page of race listings)
      - single_race (insert the results from results_parser to a database)
      - race_parser (reads all race information present on the race list page and returns a list of articles which can be passed to the single_race class)
      
  - site_parsing_classes
      - single_results_page (processes a results page stored as an html file, returns the event results table, which can be fed to personal_result to process individual performances)
      - personal_result (Specifically for summary results pages, takes input from single_results_page, inserts information to the base)
      - athlete_meta (Given a file path this extracts useful metadata from meta page saved as text)
      
Utilisation of these classes is handled in the files prefixed with a number.  Generally speaking, these should be run in order:
0_initial_setup.py
  -  Runs set up for the program.  Creates database and tables if necessary, as well as folders
1_update_race_list.py
  - Collects information from the race page list (a list with links to results from all races)
  
2_scrape_races.py
  - Using the links collected in step 1, move to the first page of the results, then cycle through all pages, writing results to .html files in the page_contents direcory
  
3_process_parsed.py
  - Parse the stored pages containing race results to the database
  
4_scrape_athlete_meta.py
  - Using the results inserted into the database from step 4, go to individual athletes pages and take detailed information (clearly this is a time consuming stage, requests should be made slowly to avoid high server traffic)
  
5_process_athlete_meta.py
  - process the athlete meta data, insert to the base (athlete_meta)
