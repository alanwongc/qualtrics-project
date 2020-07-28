# qualtrics-project

This script will download responses from a qualtrics survey and input them into a Google Sheet. I chose python for this project as it is a modern and versatile language with many useful libraries written for it.

### Installing

```
pip install -r requirements.txt
```

### How to run

```
python start.py 
```

### Built With

* [Qualtrics API](https://api.qualtrics.com/)
* [gspread](https://gspread.readthedocs.io/en/latest/)

### Current Limitations

* Need to allow user to select sheet and survey 
* Gspread clears all other sheets from the spreadsheet when script is run. If we want to perform manipulation on the data, it would have to be from a separate spreadsheet. Useful: https://support.google.com/docs/answer/3093340

### Acknowlegments
* https://gist.github.com/PurpleBooth/109311bb0361f32d87a2
* https://medium.com/knerd/best-practices-for-python-dependency-management-cc8d1913db82
