import os
import institutions_service
import html_reports


curr_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

#a = institutions_service.OrgManager()
#a.create_db()

a = institutions_service.OrgListManager()
a.load()
countries = a.get_countries_orgnames()

print(__file__)
print(curr_path)
path = curr_path + '/../../aff'

print(path)
if not os.path.isdir(path):
    os.makedirs(path)

if os.path.isdir(path):
    links = []
    labels = ['name', 'city', 'state']
    for country in sorted(countries.keys()):
        name, code = country.split(' - ')
        print(country)
        links.append(html_reports.link('./' + code + '.html', country))

        rows = []
        for items in countries[country]:
            print(items)
            org, city, state = items.split('\t')
            tr = {}
            tr['name'] = org
            tr['city'] = city
            tr['state'] = state
            rows.append(tr)
        content = html_reports.sheet(labels, None, rows)
        print(path + '/' + code + '.html')
        html_reports.save(path + '/' + code + '.html', country, content)

    content = html_reports.format_list('', 'ol', links)
    print(path + '/aff.html')
    html_reports.save(path + '/aff.html', 'Affiliations', content)
