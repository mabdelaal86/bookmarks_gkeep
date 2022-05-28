# Bookmarks from Google Keep

Export bookmarks from Google Keep into Pocket/Instapaper

## Why I wrote this script?

I used to save all my bookmarks, mainly useful articles that I might need to read again, into Google Keep. 
For some reasons, I wanted to export my bookmarks from *Google Keep* and same them into another application, 
such as *Pocket* or *Instapaper*.

Since I didn't find any tool to export my bookmarks from *Google Keep*, I have written this script.

## Usage

### 1. Download bookmarks from Google Keep

Go to https://takeout.google.com/settings/takeout and make sure to select **Keep** product.

*Optional* Deselect all products first then select **Keep** to download the content of **Keep** only.

Click *Next Step* then *Create export*. Then Google will collect you data and send an email with a link for downloading.  

Check you email, after a while you will receive an email to download you data. 
After downloading, extract the downloaded .zip file. 

### 2. Run the script

Copy the path into *Keep* directory (`<path to extracted directory>/Takeout/Keep`).

Run the script with the path to *Keep* directory as argument:
```
cd "<path to script>"
python main.py "<path to keep directory>"
```

After running the script, three files will be created:

* `ignore.txt`: Contains a list of bookmarks that have ignored.
* `instapaper.html`: Contains bookmarks in Instapaper html format.
* `instapaper.csv`: Contains bookmarks in Instapaper csv format.

### 3. Import bookmarks

#### Instapaper

* Go to https://www.instapaper.com/user
* Click *Import from Instapaper CSV* and choose `instapaper.csv` file

#### Pocket

* Go to https://getpocket.com/import/instapaper
* Choose `instapaper.html` from your computer
* Click *Import*
