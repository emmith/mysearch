from elasticsearch_dsl import Search, connections

client  = connections.create_connection(hosts=['localhost:9200'], timeout=60)

def dsl_demo():
    s = Search(using=client, index="videodata") \
        .query("match", area="大陆") \
        .exclude("match", year=2018)

    response = s.params(size=100).execute()

    for hit in response:
        print(hit.meta.score, hit.name,hit.year)

if __name__ == '__main__':
    dsl_demo()