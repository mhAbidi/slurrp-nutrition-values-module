import csv
import elasticsearch

client = elasticsearch.Elasticsearch()

with open("./unique_ingredients.csv", "r", encoding='utf-8') as items:
    csv_reader = csv.reader(items)
    total = 0
    skipped = 0
    for row in csv_reader:
        ing = row[0]
        query = {
                "title": ing.strip()
            }
        try:
                client.index(index="nin_v3", doc_type="sample", body=query, ignore=400)
                total = total + 1
                print(total)
        except elasticsearch.ElasticsearchException as es1:
                print(es1)
                skipped = skipped + 1
print("total indexed:", total)
print("total skipped", skipped)
