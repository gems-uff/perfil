Para ler esse documento em português brasileiro [clique aqui](/README.md)

# Perfil

This project allows the review of researchers' profiles using both Lattes and Google Scholar to collect data, afterward generating reports and visualizations.

## Documentation

[Term paper about the second version](https://github.com/gems-uff/perfil/raw/master/doc/TCC%20Arthur%20Paiva.pdf)

## Installation

### Requirements
We assume that you have Python 3.8+ installed on your computer

### Steps to Installations

1. Clone our repository:

`~$ git clone https://github.com/gems-uff/perfil.git`

2. Access the project's directory:

`~$ cd perfil`

3. Install pipenv (if you haven't installed it yet)

`~/perfil$ python -m pip install pipenv`

4. Install the necessary libraries:

`~/perfil$ pipenv sync`

## Running the scripts:

1. Access the project's directory:

`~$ cd perfil`

2. Activate the conda environment you just created:

`~/perfil$ pipenv shell`

3. Update the file that contains the researchers (e.g., pgc.xlsx) adding Nome (name), ID Lattes, and ID Scholar for the ones that must be considered and write its path in the variable "researchers_file" in the file [config.py](/config.py). You shouldn't worry about the other columns, because they're going to be filled automatically.

**BE CAUTIOUS** when you paste the ID Lattes. You have to assure that the ID Lattes is going to be pasted as text because if it's pasted as a number, the Excel is going to round the number and the IDs will become invalid or will match a Lattes ID of a different researcher.

4. Update the collection/analysis horizon (variables start_year and end_year) and indicate the path of the file that contains the researcher (e.g., pgc.xlsx) in config.py.

5. Turn on or off the unification variables, for conference papers (unify_conference_paper), journal papers(unify_journal_paper), projects(unify_project), books(unify_book), books' chapters (unify_chapter) and patents(unify_patent).

6. Choose the minimum similarity value for conferences' names(variable conferences_minimum_similarity), journals' names(variable journals_minimum_similarity), conference papers' titles(variable conferences_papers_title_minimum_similarity), journal papers' titles(variable journals_papers_title_minimum_similarity) and projects' names(variable project_name_minimum_similarity) in config.py.

7. Use download.py to download the Lattes curriculum. This can take a while (30 seconds for each CV), but it doesn't need to be done every time. You should do it only when there is an update of the curriculums in your analysis horizon.

`~/perfil$ python download.py`

8. The program is going to open up a new tab with the download link of the Lattes curriculum in your main browser, do the captcha and the download is going to start. After the download is finished, move the .zip download to the folder [lattes](/lattes) (or save it directly in the folder).

9. If there are still more Lattes curriculum to be downloaded, the program is going to repeat step 8, so you have to do it until there aren't any more files to update.

10. populate_database.py populates the database, in-memory, using the researchers' lattes that there are in the researchers' file (step 3 above) and generates the similarity files in the folder "output/similarity_xlsx".

`~/perfil$ python populate_database.py`

11. If you want, edit the [synonym files](/resources/synonyms) with the output you got from the similarity files. And if there is any wrong output in the similarity files, you should increase the minimum similarity value of the respective variable(step 6) and redo steps 10 and 11.

12. In the log file, "log_file.log", there will be reports of possible duplications in the curriculum Lattes of the researchers, of the researchers' file, if any. It also reports if a unification has been done (they only will be done if they were turned on in step 5). You must delete the log file each time you run a script.

13. Use write_profile.py to populate the other columns of the researchers' file(e.g. pgc.xlsx) with the current data from Lattes and Google Scholar. The file must be closed while the script is running.

`~/perfil$ python write_profile.py`

14. If you want to highlight the results of a specific researcher, go to the file [config.py](/config.py), add his data in the variable "subject" and assign the value True to the variable "print_subject". The data of this researcher don't need to be in the researchers' file (step 3 above). Furthermore, this researcher's Lattes needs to be downloaded manually (the program only downloads the Lattes of the researchers that are in the file referred to in step 3 above).

15. Use visualize.py to generate the boxplots. And visualize-jcr.1.5.py to generate boxplots evaluating only journal papers with JCR value > 1,5.

`~/perfil$ python visualize.py`

`~/perfil$ python visualize-jcr1.5.py`

16. Use generate_researcher_progression_report.py to generate reports to help in a researcher's progression, of the researchers' file, using data from the years designated in [config.py](/config.py). The files generated can be found in the folder "output/generate_reseacher_progression_report" with the name of its researcher.    
	1. `~/perfil$ python generate_reseacher_progression_report.py` show an interactive command line to the user to choose **one** researcher to generate the file or generate files for **all** researchers.
	2. `~/perfil$ python generate_reseacher_progression_report.py --all` generates the files of all researchers without the command line interaction.
	3. `~/perfil$ python generate_reseacher_progression_report.py --researchers (researcher.id|researcher.lattes_id) +`	replace "(researcher.id|researcher.lattes_id) +" for one or more ids of the database or lattes ids of the researchers to generate only their files without the need to interact with the command line. The database id is the same as the researchers' file order.
	4. `~/perfil$ python generate_reseacher_progression_report.py --ids` shows in the command line the ids that the researchers of the researchers' file are going to have in the database.
    
17. Use generate_datacapes.py to generate reports about the production of the post-graduation program and its [accredited teachers](/resources/affiliations). This script also generates the report to help choose the "4n" papers. You must assign the value of "normalize_conference_paper" and "normalize_journal_paper", in [config.py](/config.py), as False. Remember, its output is accordingly the researchers' file. The files generated can be found in the folder "output/datacapes".

`~/perfil$ python generate_datacapes.py`

18. Use generate_configured_reports.py to generate customized reports. To do it, you only need to fill the dictionary "configured_reports" in [config.py](/config.py). The names of the reports must be the keys and strings. The values of the keys must be the list/array of attributes of the entities/classes that you want the information from. The generated files can be found in the folder "output/configured_reports".
	 * The variable "reports_as_new_worksheets", in [config.py](/config.py), can be assigned as True if you want all the reports as tabs in a single file with the name "configured_reports.xlsx".
	 * The variable "new_worksheet_if_conflict", also in [config.py](/config.py), can be assigned as True if you want that the conflicts in the same report to be written in different tabs. Conflicts happen when there are one or more different entities/classes in the same report. (This doesn't apply to "Pesquisador". "Pesquisador" **may** be accompanied by **one** other class/entity).
	 * The entities/classes available to be queried are Banca, Capitulo, Conferencia, Corpo_Editorial, Livro, Organizacao_Evento, Orientacao, Patente, Periodico, Pesquisador, Projeto, Artigo. Highlighting that Artigo has the common information between Periodico and Conferencia, however, it's considered as another entity/class if a conflict happens.

`~/perfil$ python generate_configured_reports.py`

19. Use generate_collaboration_graphs.py to visualize graphs about the collaboration between the researchers in the analysis horizon. The variables "collaboration_graphs_alpha" and "collaboration_graphs_alpha_decay", in [config.py](/config.py), set the intensity of the expansion force of the graph from its center and its decay rate until 0, respectively (their values must be between 0 and 1). To visualize the output access http://127.0.0.1:5000/ with the script running.

`~/perfil$ python generate_collaboration_graphs.py`

## Running the tests:

1. Enter in the project directory:

`~$ cd perfil`

2. Activate the conda environment you just created:

`~/perfil$ pipenv shell`

3. Call the command below to run the tests:

`~/perfil$ python -m unittest database_test.py -v`

## Purpose of the runnable scripts:

### database_test.py
Test script to ascertain that the lattes' data are being collected and inserted in the in-memory database.

### download.py
Script to help the user to download the lattes of the researcher in the researchers' file.

### generate_collaboration_graphs.py
Script with the purpose to generate graphs illustrating the collaboration in papers' authorship between the researchers and its intensity in the analysis horizon.

### generate_configured_reports.py
Script with the purpose of generating customized reports by the user accordingly with the variables configured_reports, reports_as_new_worksheets, and new_worksheet_if_conflict using data collected from the Lattes curriculum.

### generate_datacapes.py
Script to generate reports of a post-graduation program as requested by CAPES. The reports are based on journal papers, conference papers, and their respective Qualis, using only the researchers accredited in the analysis horizon.

### generate_reseacher_progression_report.py
Script with the purpose of generating reports with information, about the researchers in the researchers' file, that help in the researchers' progress.

### populate_database.py
Script that populates the in-memory database with the information of the researchers' lattes that are in the researchers' file and generates the similarity files for the names of conferences, journals, and projects. It also writes the possible duplications in the curriculums Lattes and the unifications made in the log file.

### visualize.py
Script that generates the boxplots based on the researchers' file already filled by the script [write_profile.py](write_profile.py).

### visualize-jcr.1.5.py
Script that generates the boxplot of journal papers with JCR bigger than 1,5 from the quantitative data of an already filled researchers' file.

### write_profile.py
Script with the purpose of filling the quantitative information of researchers of the researchers' file in the same file. It uses the data from the Lattes curriculum and from Google Scholar.

## Variables of the file config.py

* **resources_path**: Path to the [resources folder](/resources).
* **output_path**: Path to the output folder of the program.
* **researchers_file**: variable with the path to the researchers' file.
* **start_year**: initial year of the collection horizon/analysis horizon (including it).
* **end_year**: end year of the collection horizon/analysis horizon (including it).
* **unify_conference_paper**: If its assigned value is True, the conference papers are going to be unique in the database, that means, after registering a certain conference paper of a researcher's Lattes, if in the researchers' Lattes read afterward there is the same conference paper, it isn't registered again. And, after registering all the researchers, all the researchers of a certain conference paper, that are in the database, are going to be related to the conference paper.
* **unify_journal_paper**: If its assigned value is True, the journal papers are going to be unique in the database, that means, after registering a certain journal paper of a researcher's Lattes, if in the researchers' Lattes read afterward there is the same journal paper, it isn't registered again. And, after registering all the researchers, all the researchers of a certain journal paper, that are in the database, are going to be related to the journal paper.
* **unify_project**: If its assigned value is True, the projects are going to be unique in the database, that means, after registering a certain project of a researcher's Lattes, if in the researchers' Lattes read afterward there is the same project, it isn't registered again. And after registering all the researchers, all the members of a certain project, that are in the database, are going to be related to the project.
* **unify_book**: If its assigned value is True, the books are going to be unique in the database, that means, after registering a certain book of a researcher's Lattes, if in the researchers' Lattes read afterward there is the same book, it isn't registered again.
* **unify_chapter**: If its assigned value is True, the books' chapters are going to be unique in the database, that means, after registering a certain book chapter of a researcher's Lattes, if in the researchers' Lattes read afterward there is the same chapter, it isn't registered again.
* **unify_patent**: If its assigned value is True, the patents are going to be unique in the database, that means, after registering a certain patent of a researcher's Lattes, if in the researchers' Lattes read afterward there is the same patent, it isn't registered again.
* **conferences_minimum_similarity** : minimum similarity between conference names to the software regard them as the same (value between 0 and 1).
* **journals_minimum_similarity** : minimum similarity between journal names to the software regard them as the same (value between 0 and 1).
* **conferences_papers_title_minimum_similarity** : minimum similarity between conference papers' titles to the software regard them as the same (value between 0 and 1).
* **journals_papers_title_minimum_similarity** : minimum similarity between journal papers' titles to the software regard them as the same (value between 0 and 1).
* **project_name_minimum_similarity** : minimum similarity between project names to the software regard them as the same (value between 0 and 1).
* **datacapes_minimum_similarity_titles**: minimum similarity between papers' titles to the software regard them as the same when filtering the articles to make the post-graduation program production in the script [generate_datacapes.py](/generate_datacapes.py).
* **subject** : researcher to be highlighted when the boxplots are generated.
* **print_subject** : If assigned the value True, turns on the function of highlighting the researcher of the variable "subject" when the boxplots are generated.
* **reports_as_new_worksheets** : If the value True is assigned, when the user runs the script [generate_configured_reports.py](generate_configured_reports.py), instead of the output being a file for each report, it's going to be in a single file. Its name will be "configured_reports.xlsx", and the reports are going to be its tabs.
* **new_worksheet_if_conflict** : If the value assigned is True, when the user runs the script [generate_configured_reports.py](generate_configured_reports.py) when a conflict happens, that means, two entities/classes (not being "Pesquisidor") in the same report, instead of reporting an error, the software is going to put each conflicting entity/class in a tab of the file making a cartesian product with "Pesquisador" if it was requested in the report.
* **configured_reports** : Dictionary in which its keys must be strings and its values lists/arrays with the attributes of the entities/classes that the user wishes to generate a report about.
* **class QualisLevel** : Enum class with the Qualis levels that the program must use.
* **qualis_journal_points**: Dictionary with the values of the points of each Qualis level of journal papers.
* **qualis_conference_points**:  Dictionary with the values of the points of each Qualis level of conference papers.
* **collaboration_graphs_alpha**: Value of the initial force that the nodes of the graph of the script [generate_collaboration_graphs.py](generate_collaboration_graphs.py) expand from the center. Its value must be between 0 and 1.
* **collaboration_graphs_alpha_decay**: Value that the initial force of the nodes of the graph of the script [generate_collaboration_graphs.py](generate_collaboration_graphs.py) decay to 0, which means, the decay rate until the nodes stop moving. Seu valor deve ser entre 0 e 1.
* **df_jcr** : Path to the file with the journals' JCR.
* **df_qualis_conferences** : Path to the file with the conferences' Qualis level.
* **df_qualis_journals** : Path to the file with the journals' Qualis level.
* **conferences_synonyms** : Path to the file with the synonyms of the conferences' names.
* **journals_synonyms** : Path to the file with the synonyms of the journals' names.
* **projects_synonyms** : Path to the file with the synonyms of the projects' names.
* **lattes_dir** : Path to the folder that contains the Lattes curriculums.
* **affiliations_dir**: Path to the folder that contains the files of the researchers accredited to the post-graduation program.

## Files

### Synonyms
The synonyms files can be found in the folder [/resources/synonyms](/resources/synonyms), they are conferences_synonyms.xlsx, journals_synonyms.xslx, and projects_synonyms.xlsx. Each line of each file represents texts that the software is going to recognize as the same, and when registering in the database it is going to use the name in the first column. For example, the texts written in the columns B5, C5, D5, and E5 are all synonyms for the one in column A5.

### Similarity
The similarity files can be found in the folder "output/similarity_xlsx", they are conferences_similar.xlsx, journals_similar.xlsx, and projects_similar.xlsx. They are generated accordingly with the minimum values in the file [config.py](config.py). Each line contains the names that the program judged as the same(equal or bigger than the minimum value), and the first column is the name that it used to register in the database (in the same way as the synonyms files work).

### Accredited
The accredited to the post-graduation program files can be found in the folder [/resources/affiliations](/resources/affiliations), they are indicated by their respective years. Each file represents the researchers that were accredited that year. Each line must contain (only) one researcher.

## Logs

### log_file.log
* The log file shows the possible duplicated information in the Lattes, each line has information with the data to help identify the possible duplication, including the name of the table and the function in which it happened. The information is divided by a blank space(" ") followed by the researcher's name of the Lattes that it happened.
* The file shows the crossed references that happened if one (or more) of the variables unify_conference_paper, unify_journal_paper, unify_project, unify_book, unify_chapter, unify_patent (in [config.py](config.py)) is(are) with its(their) value assigned as True.

It's advised to delete the file after each time a script is run because the log file is incremental.

## References

The code of the file [index.html](/collaboration_graphs/templates/index.html) was based on the code available in https://bl.ocks.org/heybignick/3faf257bbbbc7743bb72310d03b86ee8.