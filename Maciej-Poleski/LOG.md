7-8.11.2015:
- Imported data to SQL database
- First computations (number of registered users, all users, ...) (and data sets miss only ~10k users at all)
- A few views with (maybe) useful data based on datasets

18.11.2015:
- Updated database schema
- Collecting evidence for each user (to be used by estimation engine)

24.11.2015
- Updated database schema
- Exported sample data (group of ~150000 users - users who commited any transaction)
- Commited two simples linear regression tools on them (in model/)
- Comments written in model/README.md

01.12.2015
- Updated database schema
- Exported new samples
- Prepared normalized set (divide time intervals by 1M to decrease its weight)
- Results improved slightly
- Working with Decision Trees (surprisingly weak results here!)
- 3 new features (based on views)
- Worsen linear regression results (a bit)
- Improve Decision Trees regression results (noticeably)
