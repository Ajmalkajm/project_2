# Dataset Analysis Report

## Basic Statistics

|        |   book_id |   goodreads_book_id |     best_book_id |         work_id |   books_count |           isbn |         isbn13 | authors      |   original_publication_year | original_title   | title          | language_code   |   average_rating |    ratings_count |   work_ratings_count |   work_text_reviews_count |   ratings_1 |   ratings_2 |   ratings_3 |      ratings_4 |       ratings_5 | image_url                                                                                | small_image_url                                                                        |
|:-------|----------:|--------------------:|-----------------:|----------------:|--------------:|---------------:|---------------:|:-------------|----------------------------:|:-----------------|:---------------|:----------------|-----------------:|-----------------:|---------------------:|--------------------------:|------------:|------------:|------------:|---------------:|----------------:|:-----------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|
| count  |  10000    |     10000           |  10000           | 10000           |    10000      | 9300           | 9415           | 10000        |                    9979     | 9415             | 10000          | 8916            |     10000        |  10000           |      10000           |                  10000    |    10000    |    10000    |     10000   | 10000          | 10000           | 10000                                                                                    | 10000                                                                                  |
| unique |    nan    |       nan           |    nan           |   nan           |      nan      | 9300           |  nan           | 4664         |                     nan     | 9274             | 9964           | 25              |       nan        |    nan           |        nan           |                    nan    |      nan    |      nan    |       nan   |   nan          |   nan           | 6669                                                                                     | 6669                                                                                   |
| top    |    nan    |       nan           |    nan           |   nan           |      nan      |    4.39023e+08 |  nan           | Stephen King |                     nan     |                  | Selected Poems | eng             |       nan        |    nan           |        nan           |                    nan    |      nan    |      nan    |       nan   |   nan          |   nan           | https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png | https://s.gr-assets.com/assets/nophoto/book/50x75-a91bf249278a81aabab721ef782c4a74.png |
| freq   |    nan    |       nan           |    nan           |   nan           |      nan      |    1           |  nan           | 60           |                     nan     | 5                | 4              | 6341            |       nan        |    nan           |        nan           |                    nan    |      nan    |      nan    |       nan   |   nan          |   nan           | 3332                                                                                     | 3332                                                                                   |
| mean   |   5000.5  |         5.2647e+06  |      5.47121e+06 |     8.64618e+06 |       75.7127 |  nan           |    9.75504e+12 | nan          |                    1981.99  | nan              | nan            | nan             |         4.00219  |  54001.2         |      59687.3         |                   2919.96 |     1345.04 |     3110.89 |     11475.9 | 19965.7        | 23789.8         | nan                                                                                      | nan                                                                                    |
| std    |   2886.9  |         7.57546e+06 |      7.82733e+06 |     1.17511e+07 |      170.471  |  nan           |    4.42862e+11 | nan          |                     152.577 | nan              | nan            | nan             |         0.254427 | 157370           |     167804           |                   6124.38 |     6635.63 |     9717.12 |     28546.4 | 51447.4        | 79768.9         | nan                                                                                      | nan                                                                                    |
| min    |      1    |         1           |      1           |    87           |        1      |  nan           |    1.9517e+08  | nan          |                   -1750     | nan              | nan            | nan             |         2.47     |   2716           |       5510           |                      3    |       11    |       30    |       323   |   750          |   754           | nan                                                                                      | nan                                                                                    |
| 25%    |   2500.75 |     46275.8         |  47911.8         |     1.00884e+06 |       23      |  nan           |    9.78032e+12 | nan          |                    1990     | nan              | nan            | nan             |         3.85     |  13568.8         |      15438.8         |                    694    |      196    |      656    |      3112   |  5405.75       |  5334           | nan                                                                                      | nan                                                                                    |
| 50%    |   5000.5  |    394966           | 425124           |     2.71952e+06 |       40      |  nan           |    9.78045e+12 | nan          |                    2004     | nan              | nan            | nan             |         4.02     |  21155.5         |      23832.5         |                   1402    |      391    |     1163    |      4894   |  8269.5        |  8836           | nan                                                                                      | nan                                                                                    |
| 75%    |   7500.25 |         9.38223e+06 |      9.63611e+06 |     1.45177e+07 |       67      |  nan           |    9.78083e+12 | nan          |                    2011     | nan              | nan            | nan             |         4.18     |  41053.5         |      45915           |                   2744.25 |      885    |     2353.25 |      9287   | 16023.5        | 17304.5         | nan                                                                                      | nan                                                                                    |
| max    |  10000    |         3.32886e+07 |      3.55342e+07 |     5.63996e+07 |     3455      |  nan           |    9.79001e+12 | nan          |                    2017     | nan              | nan            | nan             |         4.82     |      4.78065e+06 |          4.94236e+06 |                 155254    |   456191    |   436802    |    793319   |     1.4813e+06 |     3.01154e+06 | nan                                                                                      | nan                                                                                    |

## Missing Values

|                           |    0 |
|:--------------------------|-----:|
| book_id                   |    0 |
| goodreads_book_id         |    0 |
| best_book_id              |    0 |
| work_id                   |    0 |
| books_count               |    0 |
| isbn                      |  700 |
| isbn13                    |  585 |
| authors                   |    0 |
| original_publication_year |   21 |
| original_title            |  585 |
| title                     |    0 |
| language_code             | 1084 |
| average_rating            |    0 |
| ratings_count             |    0 |
| work_ratings_count        |    0 |
| work_text_reviews_count   |    0 |
| ratings_1                 |    0 |
| ratings_2                 |    0 |
| ratings_3                 |    0 |
| ratings_4                 |    0 |
| ratings_5                 |    0 |
| image_url                 |    0 |
| small_image_url           |    0 |

## Outliers Detection

### book_id
- **Bounds:** Lower Bound = -4998.5, Upper Bound = 14999.5
- **Number of Outliers:** 0
- **Analysis:** Outliers in 'book_id' could indicate no significant impact on this column..

### goodreads_book_id
- **Bounds:** Lower Bound = -13957648.5, Upper Bound = 23386149.5
- **Number of Outliers:** 345
- **Analysis:** Outliers in 'goodreads_book_id' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### best_book_id
- **Bounds:** Lower Bound = -14334389.375, Upper Bound = 24018413.625
- **Number of Outliers:** 357
- **Analysis:** Outliers in 'best_book_id' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### work_id
- **Bounds:** Lower Bound = -19254519.875, Upper Bound = 34781109.125
- **Number of Outliers:** 601
- **Analysis:** Outliers in 'work_id' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### books_count
- **Bounds:** Lower Bound = -43.0, Upper Bound = 133.0
- **Number of Outliers:** 844
- **Analysis:** Outliers in 'books_count' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### isbn13
- **Bounds:** Lower Bound = 9779544316725.0, Upper Bound = 9781602653445.0
- **Number of Outliers:** 556
- **Analysis:** Outliers in 'isbn13' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### original_publication_year
- **Bounds:** Lower Bound = 1958.5, Upper Bound = 2042.5
- **Number of Outliers:** 1031
- **Analysis:** Outliers in 'original_publication_year' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### average_rating
- **Bounds:** Lower Bound = 3.3550000000000004, Upper Bound = 4.674999999999999
- **Number of Outliers:** 158
- **Analysis:** Outliers in 'average_rating' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### ratings_count
- **Bounds:** Lower Bound = -27658.375, Upper Bound = 82280.625
- **Number of Outliers:** 1163
- **Analysis:** Outliers in 'ratings_count' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### work_ratings_count
- **Bounds:** Lower Bound = -30275.625, Upper Bound = 91629.375
- **Number of Outliers:** 1143
- **Analysis:** Outliers in 'work_ratings_count' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### work_text_reviews_count
- **Bounds:** Lower Bound = -2381.375, Upper Bound = 5819.625
- **Number of Outliers:** 1005
- **Analysis:** Outliers in 'work_text_reviews_count' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### ratings_1
- **Bounds:** Lower Bound = -837.5, Upper Bound = 1918.5
- **Number of Outliers:** 1140
- **Analysis:** Outliers in 'ratings_1' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### ratings_2
- **Bounds:** Lower Bound = -1889.875, Upper Bound = 4899.125
- **Number of Outliers:** 1156
- **Analysis:** Outliers in 'ratings_2' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### ratings_3
- **Bounds:** Lower Bound = -6150.5, Upper Bound = 18549.5
- **Number of Outliers:** 1149
- **Analysis:** Outliers in 'ratings_3' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### ratings_4
- **Bounds:** Lower Bound = -10520.875, Upper Bound = 31950.125
- **Number of Outliers:** 1131
- **Analysis:** Outliers in 'ratings_4' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

### ratings_5
- **Bounds:** Lower Bound = -12621.75, Upper Bound = 35260.25
- **Number of Outliers:** 1158
- **Analysis:** Outliers in 'ratings_5' could indicate potential errors, unusual cases, or influential factors in the dataset. These could significantly affect statistical analyses like mean or regression results..

## Pair Plots

![Pair Plots](goodreads/pair_plots.png)

## Significant Findings

### t_test
Result: {'t_stat': np.float64(-69.43069249095024), 'p_value': np.float64(0.0)}

### regression
Result: {'slope': np.float64(302.1745629892938), 'intercept': np.float64(3753672.6109720366), 'r_value': np.float64(0.11515422507298714), 'p_value': np.float64(7.1762070591852e-31), 'std_err': np.float64(26.06890066657803)}

### pearson_corr
Result: {'correlation': np.float64(0.11515422507298706)}

### decision_tree
Result: {'mse': 0.0}

## Visualizations

### book_id
Histogram of book_id showing frequency distribution.

### goodreads_book_id
Histogram of goodreads_book_id showing frequency distribution.

### best_book_id
Histogram of best_book_id showing frequency distribution.

### work_id
Histogram of work_id showing frequency distribution.

### books_count
Histogram of books_count showing frequency distribution.

### isbn13
Histogram of isbn13 showing frequency distribution.

### original_publication_year
Histogram of original_publication_year showing frequency distribution.

### average_rating
Histogram of average_rating showing frequency distribution.

### ratings_count
Histogram of ratings_count showing frequency distribution.

### work_ratings_count
Histogram of work_ratings_count showing frequency distribution.

### work_text_reviews_count
Histogram of work_text_reviews_count showing frequency distribution.

### ratings_1
Histogram of ratings_1 showing frequency distribution.

### ratings_2
Histogram of ratings_2 showing frequency distribution.

### ratings_3
Histogram of ratings_3 showing frequency distribution.

### ratings_4
Histogram of ratings_4 showing frequency distribution.

### ratings_5
Histogram of ratings_5 showing frequency distribution.

### correlation_matrix
Correlation matrix showing relationships between numeric features.

## Summary

### Dataset Analysis: Overview and Insights

This dataset contains information about books, including identifiers, metadata, ratings, and author details. The following analysis breaks down the relevant features and provides insight into the underlying trends and characteristics inherent in the dataset.

#### Column Descriptions:
1. **Identifiers**:
   - `book_id`, `goodreads_book_id`, `best_book_id`, and `work_id`: Unique identifiers for books, linking to various platforms.

2. **Books Characteristics**:
   - `books_count`: Indicates the number of books in a series or by a particular author.
   - `isbn` and `isbn13`: International Standard Book Numbers, critical for unique identification.
   - `authors`: Contains the names of the authors, allowing analysis of author popularity and diversity.

3. **Publication Information**:
   - `original_publication_year`: Year the book was first published, which can be useful for analyzing trends over time.
   - `original_title` and `title`: Provide information on how books are marketed and potentially altered in different editions.

4. **Language and Availability**:
   - `language_code`: The language in which the book is published, which can impact readership and marketing strategies.

5. **Ratings and Reviews**:
   - `average_rating`: An important metric for assessing the overall reception of a book.
   - `ratings_count` and `work_ratings_count`: Indicate the popularity and engagement level of books, correlating to their sales and visibility.
   - `work_text_reviews_count`: Number of textual reviews provided, giving insight into customer engagement beyond numerical ratings.
   - `ratings_1` to `ratings_5`: Breakdown of rating distributions, useful for identifying books with polarized reviews.

6. **Images**:
   - `image_url` and `small_image_url`: Visual representations of the book which can impact reader interest and choice.

### Insights:

1. **Rating Analysis**:
   - The `average_rating` combined with the distribution metrics (ratings_1 to ratings_5) allows for the identification of books with strong positive reception versus those that are polarizing.
   - High `ratings_count` but low average ratings could indicate divisive opinion, reflective of niche genres or recent releases.

2. **Publication Trends**:
   - Analyzing the `original_publication_year` can reveal trends in publishing, such as a spike in publications in specific genres over time, or shifts in reader preferences.
   - Identifying the best-selling years or periods of increased activity may drive marketing strategies for publishers.

3. **Genre and Author Popularity**:
   - By cross-referencing the `authors` against the `average_rating` and `ratings_count`, one can gauge author popularity and the reception of their works.
   - Identifying authors with consistently high ratings could provide insights into what attributes (e.g., writing style, themes) resonate with readers.

4. **Impact of Reviews**:
   - Higher numbers in `work_text_reviews_count` correlate with reader engagement and can be indicative of a community’s investment in a book. A deeper text review analysis could uncover recurring themes or sentiments.

5. **Diversity of Titles**:
   - The `books_count` metric may provide insight into series versus standalone titles, indicating potential reader preferences for ongoing narratives versus one-time reads.
   - Diverse `language_code` entries imply potential global engagement, which would necessitate different marketing strategies based on locality.

### Potential Implications:

- **Targeted Marketing**: Understanding the characteristics of high-rated books can guide marketing efforts, suggesting which genres or author types to highlight based on historical data.
- **Publisher Strategy**: Recognizing trends in publication years could inform publishers about whether to invest in certain genres or reprints, especially if recent spikes in interest are noted.
- **Author Engagement**: Successful authors may be leveraged for book tours or promotional campaigns based on their high engagement metrics.
- **Reader Community Building**: Engaging with the community around highly reviewed books could foster loyalty and drive further sales.

Overall, insights derived from this dataset can directly inform publishing strategies, marketing plans, and engagement efforts while understanding reader preferences and behavior in the literary landscape.

## Conclusion

The dataset analysis provides a comprehensive overview of a collection of books, highlighting key metrics such as ratings, reviews, and publication details. Notably, the analysis revealed significant outliers across various metrics, particularly in the fields of book IDs and original publication years, indicating the presence of data entries that may require further scrutiny to ensure data quality. The correlation analysis showed a weak positive relationship between average ratings and ratings count, suggesting that higher-rated books tend to attract more ratings, albeit with a small effect size. The findings from the regression analysis indicate a potential relationship between some variables, though the low r-value suggests a limited explanatory power. Moreover, with a substantial portion of the dataset's variables still containing missing values, particularly in the parameters related to book identification numbers and authorship, there exists an opportunity for data cleaning and imputation. Consequently, while the dataset offers a rich source of information for exploring book ratings and trends, addressing the identified outliers and missing values is crucial for enhancing its reliability and validity for future analyses.

