# # Who is who in industry and business


## Purpose

This repo holds a scraper and processor to turn a book of biograpies into a dataset for historical and economic analysis.

### Structure

The project is such:

- Scrape the contents of the book at [this link](http://runeberg.org/vemindu/). (TODO: explain about the book...)
- Separate the text into individual biographies using regex
- Translate and structure the biographies into the Schema.org/Person format
- Extract the education and work histories of the individuals
