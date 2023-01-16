# Scraping Test Report

## Technical decisions:

Selenium is an excellent scraping option, it's a flexible tool for edge cases where its automation engine can perform actions like click buttons and select dropdown menus. 

## Coding steps:

- *Extracting the variation_id from the url*: I created a separate function that extracts the query params then another one that extracts the *variation_id* from the params.
- I checked the different links I have and they all seem to have the component *product_main*(except a few that have product not found).
- From the product I can access the title and the price with their classname but I have to do some extra work for the size.
- For the size, I either have it in the title, in a select component or in a list, my solution was to extract the product component that contains all different component having the size then search for the size with a regex expression, and since some have many different sizes I went with the default selected one in the page ( the first option).
- Finally, I tried to clean my code and add the necessary comments for a better developer experience.

## Performance wise:

**Before optimization:** The first test on the whole excel file lasted for **1 hour and a half**.

- I worked with default chrome driver options and I created a driver for every iteration.

**After optimization:** The improved test lasted for **approximately 20 minutes**.

- Adding the right arguments to the driver options (no-sandbox & headless) allow us to run every scraping iteration in a minimalist browser, also creating one driver outside all iterations saves time.

