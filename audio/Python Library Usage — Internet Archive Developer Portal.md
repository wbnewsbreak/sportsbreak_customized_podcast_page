Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

# Python Library Usage 

Print to PDF 

## On this page 

Quick Start 

- Simple Functional Interface 

- Using Sessions 

- Working with Items 

- Searching for Items 

- Common Patterns 

- Configuration 

- Next Steps 

The `internetarchive` Python library provides two main ways to interact with archive.org: 

1. Simple functional interface via **<u>`internetarchive.api`</u>** - Easy to use for common tasks 

2. Flexible object-oriented interface via **<u>`ArchiveSession`</u>** - More control for complex applications 

## Quick Start 

The easiest way to get started is with the **<u>`internetarchive.api`</u>** module, which provides simple functions for common operations: 

```
from internetarchive importdownload,upload,search_items,get_item
```

```
# Download files from an item
download('TripDown1905',glob_pattern='*.mp4')
# Search for items
search=search_items('collection:opensource')
forresultinsearch:
print(result['identifier'])
# Get an item and work with it
item=get_item('TripDown1905')
print(item.metadata['title'])
```

For more control and to persist configuration across operations, use a **<u>`ArchiveSession`</u>** : 

https://archive.org/developers/internetarchive/python-lib.html 

1/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

```
from internetarchive importget_session
```

```
# Create a session with your configuration
session=get_session(config_file='~/.config/internetarchive/ia.ini')
# Use the session for all operations
item=session.get_item('TripDown1905')
item.download()
search=session.search_items('subject:science')
```

####  Note 

Downloads send `cnt=0` by default and do not count toward archive.org view counts. To count a download as a view, pass `count_views=True` to **`internetarchive.download()`** , **`Item.download()`** , or **`File.download()`** . 

## Simple Functional Interface 

The **<u>`internetarchive.api`</u>** module provides these convenient functions for common tasks: 

### internetarchive.api 

This module implements the Internetarchive API. 

copyright: C. 2012-2024 by Internet Archive. license: AGPL 3, see LICENSE for more details. 

```
delete(identifier: str,files: File| list[File] | None=None, formats: str|
list[str] | None=None, glob_pattern: str| list[str] | None=None,
cascade_delete: bool=False, access_key: str| None=None, secret_key: str|
None=None, verbose: bool=False, debug: bool=False, **kwargs) →
list[Request| Response][source]
```

```
[source]
```

Delete files from an item. Note: Some system files, such as <itemname>_meta.xml, cannot be deleted. 

#### Parameters: 

identifier – The globally unique Archive.org identifier for a given item. 

files – Only return files matching the given filenames. 

formats – Only return files matching the given formats. 

https://archive.org/developers/internetarchive/python-lib.html 

2/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

- glob_pattern – Only return files matching the given glob pattern. Multiple patterns can be separated by `|` , passed as a list, or a mix of both. 

- cascade_delete – Delete all files associated with the specified file, including upstream derivatives and the original. 

- access_key – IA-S3 access_key to use when making the given request. 

- secret_key – IA-S3 secret_key to use when making the given request. 

- verbose – Print actions to stdout. 

- debug – Set to True to print headers to stdout and exit exit without sending the delete request. 

#### Returns: 

- A list Requests if debug else a list of Responses 

```
download(identifier: str,files: File| list[File] | None=None, formats: str|
list[str] | None=None, glob_pattern: str| list[str] | None=None, dry_run:
bool=False, verbose: bool=False, ignore_existing: bool=False, checksum:
bool=False, checksum_archive: bool=False, destdir: str| None=None,
no_directory: bool=False, retries: int| None=None, item_index: int| None=
None, ignore_errors: bool=False, on_the_fly: bool=False, return_responses:
bool=False, no_change_timestamp: bool=False, timeout: float| tuple[int,
float] | None=None, count_views: bool=False, headers: Mapping| None=None,
**get_item_kwargs) → list[Request| Response][source]
```

```
[source]
```

Download files from an item. 

#### Parameters: 

- identifier – The globally unique Archive.org identifier for a given item. 

- files – Only return files matching the given file names. 

- formats – Only return files matching the given formats. 

- glob_pattern – Only return files matching the given glob pattern. Multiple patterns can be separated by `|` , passed as a list, or a mix of both. 

- dry_run – Print URLs to files to stdout rather than downloading them. 

- verbose – Turn on verbose output. 

- ignore_existing – Skip files that already exist locally. 

- checksum – Skip downloading file based on checksum. 

- checksum_archive – Skip downloading file based on checksum, and skip checksum 

- validation if it already succeeded (will create and use _checksum_archive.txt). 

- destdir – The directory to download files to. 

- no_directory – Download files to current working directory rather than creating an item directory. 

https://archive.org/developers/internetarchive/python-lib.html 

3/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

- retries – The number of times to retry on failed requests. 

- item_index – The index of the item for displaying progress in bulk downloads. 

- ignore_errors – Donʼt fail if a single file fails to download, continue to download other files. 

- on_the_fly – Download on-the-fly files (i.e. derivative EPUB, MOBI, DAISY files). 

- return_responses – Rather than downloading files to disk, return a list of response objects. 

- count_views – If True, omit the default `cnt=0` parameter so downloads count toward archive.org view counts. 

- headers – Extra HTTP headers to send with each download request. Supplying a `Range` header (e.g. `{'Range': 'bytes=0-1023'}` ) performs an intentional partial fetch, skipping resume and full-file checksum validation. 

- **kwargs – Optional arguments that `get_item` takes. 

#### Returns: 

A list Requests if debug else a list of Responses. 

```
get_files(identifier: str,files: File| list[File] | None=None, formats: str
| list[str] | None=None, glob_pattern: str| list[str] | None=None,
exclude_pattern: str| list[str] | None=None, on_the_fly: bool=False,
```

```
**get_item_kwargs) → list[File]
```

```
[source]
```

Get **`File`** objects from an item. 

#### Parameters: 

identifier – The globally unique Archive.org identifier for a given item. 

- files – Only return files matching the given filenames. 

- formats – Only return files matching the given formats. 

- glob_pattern – Only return files matching the given glob pattern. Multiple patterns can be separated by `|` , passed as a list, or a mix of both. 

- exclude_pattern – Exclude files matching the given glob pattern. Multiple patterns can be separated by `|` , passed as a list, or a mix of both. 

- on_the_fly – Include on-the-fly files (i.e. derivative EPUB, MOBI, DAISY files). 

- **get_item_kwargs – Arguments that `get_item()` takes. 

#### Returns: 

Files from an item. 

#### Usage: 

```
>>> from internetarchive importget_files
```

```
>>> fnames=[f.nameforfinget_files('nasa',glob_pattern='*xml')]
>>> print(fnames)
```

```
['nasa_reviews.xml', 'nasa_meta.xml', 'nasa_files.xml']
```

https://archive.org/developers/internetarchive/python-lib.html 

4/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

```
get_item(identifier: str,config: Mapping| None=None, config_file: str| None
=None, archive_session: ArchiveSession| None=None, debug: bool=False,
http_adapter_kwargs: MutableMapping| None=None, request_kwargs: MutableMapping
| None=None) → Item[source]
```

```
[source]
```

Get an **`Item`** object. 

#### Parameters: 

identifier – The globally unique Archive.org item identifier. 

- config – A dictionary used to configure your session. 

- config_file – A path to a config file used to configure your session. 

- archive_session – An **`ArchiveSession`** object can be provided via the `archive_session` parameter. 

- debug – To be passed on to get_session(). 

- http_adapter_kwargs – Keyword arguments that **<u>`requests.adapters.HTTPAdapter`</u>** takes. request_kwargs – Keyword arguments that **<u>`requests.Request`</u>** takes. 

#### Returns: 

The Item that fits the criteria. 

#### Usage: 

```
>>> from internetarchive importget_item
>>> item=get_item('nasa')
>>> item.item_size
121084
```

```
get_session(config: Mapping| None=None, config_file: str| None=None,
debug: bool=False, http_adapter_kwargs: MutableMapping| None=None) →
ArchiveSession
```

```
[source]
```

Return a new **`ArchiveSession`** object. The **`ArchiveSession`** object is the main interface to the 

`internetarchive` lib. It allows you to persist certain parameters across tasks. 

#### Parameters: 

#### config – 

- A dictionary used to configure your session. Supports the following keys in the `general` section: 

   - `user_agent_suffix` : Custom string to append to the default User-Agent. The default 

   - (including access key) is always sent. 

   - `secure` : Use HTTPS (default: True). 

   - `host` : Host to connect to (default: archive.org). 

5/17 

https://archive.org/developers/internetarchive/python-lib.html 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

- config_file – A path to a config file used to configure your session. 

- debug – To be passed on to this sessionʼs method calls. 

- http_adapter_kwargs – Keyword arguments that **<u>`requests.adapters.HTTPAdapter`</u>** takes. 

#### Returns: 

To persist certain parameters across tasks. 

#### Usage: 

```
>>> from internetarchive importget_session
>>> config={'s3':{'access':'foo','secret':'bar'}}
>>> s=get_session(config)
>>> s.access_key
'foo'
```

Append a custom User-Agent suffix: 

```
>>> config={'general':{'user_agent_suffix':'MyApp/1.0'}}
>>> s=get_session(config)
>>> s.headers['User-Agent']
'internetarchive/5.7.2 (Darwin x86_64; N; en; ACCESS_KEY) Python/3.9.0 MyApp/1.0'
```

From the session object, you can access all of the functionality of the `internetarchive` lib: 

```
>>> item=s.get_item('nasa')
>>> item.download()
nasa: ddddddd - success
>>> s.get_tasks(task_ids=31643513)[0].server
'ia311234'
```

```
get_tasks(identifier: str='', params: dict| None=None, config: Mapping|
None=None, config_file: str| None=None, archive_session: ArchiveSession|
None=None, http_adapter_kwargs: MutableMapping| None=None, request_kwargs:
MutableMapping| None=None) → set[CatalogTask][source]
```

Get tasks from the Archive.org catalog. 

#### Parameters: 

identifier – The Archive.org identifier for which to retrieve tasks for. 

params – The URL parameters to send with each request sent to the Archive.org catalog API. 

https://archive.org/developers/internetarchive/python-lib.html 

6/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

- config – A dictionary used to configure your session. 

- config_file – A path to a config file used to configure your session. 

- archive_session – An **`ArchiveSession`** object to use for requests. 

- http_adapter_kwargs – Keyword arguments that **<u>`requests.adapters.HTTPAdapter`</u>** takes. request_kwargs – Keyword arguments that **<u>`requests.Request`</u>** takes. 

#### Returns: 

A set of **`CatalogTask`** objects. 

```
modify_metadata(identifier: str,metadata: Mapping,target: str| None=None,
append: bool=False, append_list: bool=False, priority: int=0, access_key:
str| None=None, secret_key: str| None=None, debug: bool=False,
request_kwargs: Mapping| None=None, **get_item_kwargs) → Request| Response
```

Modify the metadata of an existing item on Archive.org. 

```
[source]
```

#### Parameters: 

- identifier – The globally unique Archive.org identifier for a given item. 

- metadata – Metadata used to update the item. 

- target – The metadata target to update. Defaults to metadata. 

- append – set to True to append metadata values to current values rather than replacing. Defaults to `False` . 

- append_list – Append values to an existing multi-value metadata field. No duplicate values will be added. 

- priority – Set task priority. 

- access_key – IA-S3 access_key to use when making the given request. 

- secret_key – IA-S3 secret_key to use when making the given request. 

- debug – set to True to return a **`requests.Request`** object instead of sending request. Defaults to `False` . 

- **get_item_kwargs – Arguments that `get_item` takes. 

#### Returns: 

- A Request if debug else a Response. 

```
search_items(query: str,fields: Iterable| None=None, sorts=None, params:
Mapping| None=None, full_text_search: bool=False, dsl_fts: bool=False,
archive_session: ArchiveSession| None=None, config: Mapping| None=None,
config_file: str| None=None, http_adapter_kwargs: MutableMapping| None=
None, request_kwargs: Mapping| None=None, max_retries: int| Retry | None=
None) → Search[source]
```

```
[source]
```

https://archive.org/developers/internetarchive/python-lib.html 

7/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

Search for items on Archive.org. 

#### Parameters: 

- query – The Archive.org search query to yield results for. Refer to 

- <u>https://archive.org/advancedsearch.php#raw</u> for help formatting your query. 

- fields – The metadata fields to return in the search results. 

- params – The URL parameters to send with each request sent to the Archive.org Advancedsearch Api. 

- full_text_search – Beta support for querying the archive.org Full Text Search API [default: False]. 

- dsl_fts – Beta support for querying the archive.org Full Text Search API in dsl (i.e. do not prepend `!L `` to the ``full_text_search` query [default: False]. 

- archive_session – An **`ArchiveSession`** object to use for requests. 

- config – A dictionary used to configure your session. 

- config_file – A path to a config file used to configure your session. 

- http_adapter_kwargs – Keyword arguments that **<u>`requests.adapters.HTTPAdapter`</u>** takes. 

- request_kwargs – Keyword arguments that **<u>`requests.Request`</u>** takes. 

- max_retries – 

- The number of times to retry a failed request. This can also be an urllib3.Retry object. If you need more control (e.g. status_forcelist), use a ArchiveSession object, and mount your own adapter after the session object has been initialized. For example: 

```
>>> s=get_session()
>>> s.mount_http_adapter()
>>> search_results=s.search_items('nasa')
```

- See **`ArchiveSession.mount_http_adapter()`** for more details. 

#### Returns: 

- A **`Search`** object, yielding search results. 

```
upload(identifier: str,files, metadata: Mapping| None=None, headers: dict|
None=None, access_key: str| None=None, secret_key: str| None=None,
queue_derive=None, verbose: bool=False, verify: bool=False, checksum: bool=
False, delete: bool=False, retries: int| None=None, retries_sleep: int|
None=None, debug: bool=False, validate_identifier: bool=False,
request_kwargs: dict| None=None, **get_item_kwargs) → list[Request|
Response][source]
```

```
[source]
```

Upload files to an item. The item will be created if it does not exist. 

https://archive.org/developers/internetarchive/python-lib.html 

8/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

#### Parameters: 

- identifier – The globally unique Archive.org identifier for a given item. 

- files – The filepaths or file-like objects to upload. This value can be an iterable or a single file-like object or string. 

- metadata – Metadata used to create a new item. If the item already exists, the metadata will not be updated – use `modify_metadata` . 

- headers – Add additional HTTP headers to the request. 

- access_key – IA-S3 access_key to use when making the given request. 

- secret_key – IA-S3 secret_key to use when making the given request. 

- queue_derive – Set to False to prevent an item from being derived after upload. 

- verbose – Display upload progress. 

- verify – Verify local MD5 checksum matches the MD5 checksum of the file received by IAS3. 

- checksum – Skip uploading files based on checksum. 

- delete – Delete local file after the upload has been successfully verified. 

- retries – Number of times to retry the given request if S3 returns a 503 SlowDown error. 

- retries_sleep – Amount of time to sleep between `retries` . 

- debug – Set to True to print headers to stdout, and exit without sending the upload request. 

- validate_identifier – Set to True to validate the identifier before uploading the file. 

- **kwargs – Optional arguments that `get_item` takes. 

#### Returns: 

A list Requests if debug else a list of Responses. 

These functions are great for scripts and simple applications. They automatically create a session in the background for you. For complete documentation including all parameters, see <u>internetarchive.api module</u> in the reference. 

## Using Sessions 

For more complex applications or when you need to perform multiple operations, use the **<u>`ArchiveSession`</u>** class: 

**_`class`_** **`ArchiveSession(`** **_`config: Mapping | None`_** _`= None`_ **`,`** **_`config_file: str`_** _`= ''`_ **`,`** **_`debug: bool`_** _`= False`_ **`,`** **_`http_adapter_kwargs: MutableMapping | None`_** _`= None`_ **`)`** **<u>`[source]`</u>** The **<u>`ArchiveSession`</u>** object collects together useful functionality from internetarchive as well as important data such as configuration information and credentials. It is subclassed from 

**<u>`requests.Session`</u>** . 

https://archive.org/developers/internetarchive/python-lib.html 

9/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

Usage: 

```
>>> from internetarchive importArchiveSession
>>> s=ArchiveSession()
>>> item=s.get_item('nasa')
Collection(identifier='nasa', exists=True)
```

**`follow_task_log(`** **_`task_id: str | int`_** **<u>`,`</u>** _`*`_ **`,`** **_`lines: int | None`_** _`= None`_ **`,`** **_`params:`_** **_<u>`Mapping`</u>_** **_`| None`_** _`= None`_ **`,`** **_`request_kwargs: Mapping | None`_** _`= None`_ **`) → Iterator[str]`** **<u>`[source]`</u>** Follow a task log as it grows, `tail -f` style. 

Yields newly appended text as it appears, stopping when the task finishes. Transient request failures are retried for several consecutive polls before the error is raised. 

#### Parameters: 

- task_id – The task id to follow. 

- lines – How much existing backlog to emit before following, using Tasks API `lines` semantics: `None` = the whole log, negative `N` = the last `N` lines, `0` = none. A positive value (the head of the log) cannot be followed and is rejected. 

- params – Extra URL parameters forwarded to every task-log request (do not pass the Tasks API `lines` parameter here; use the `lines` argument instead). 

- request_kwargs – Keyword arguments that **<u>`requests.Request`</u>** takes. 

#### Returns: 

An iterator of newly appended log text. 

#### Raises: 



```
get_connection_info() → dict
```

```
[source]
```

Get connection info for the current thread. 

Returns diagnostic information about the most recent socket connection made by this thread, useful for debugging connection issues. 

#### Returns: 

A dict containing connection details: - `src` : Source IP:port string - `dst` : Destination IP:port string - `src_ip` : Source IP address - `src_port` : Source port number - `dst_ip` : Destination IP address - `dst_port` : Destination port number 

Returns an empty dict if no connection info is available. 

https://archive.org/developers/internetarchive/python-lib.html 

10/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

```
get_item(identifier: str,item_metadata: Mapping| None=None,
```

```
[source]
```

```
request_kwargs: MutableMapping| None=None)
```

A method for creating **`internetarchive.Item`** and **`internetarchive.Collection`** objects. 

#### Parameters: 

- identifier – A globally unique Archive.org identifier. 

- item_metadata – A metadata dict used to initialize the Item or Collection object. Metadata will automatically be retrieved from Archive.org if nothing is provided. 

- request_kwargs – Keyword arguments to be used in 

- **`requests.sessions.Session.get()`** request. 

**`get_metadata(`** **_`identifier: str`_** **<u>`,`</u>** **_`request_kwargs: MutableMapping | None`_** _`= None`_ **`)`** Get an itemʼs metadata from the <u>Metadata API</u> **<u>`[source]`</u>** 

#### Parameters: 

identifier – Globally unique Archive.org identifier. 

Returns: 

Metadata API response. 

```
get_my_catalog(params: dict| None=None, request_kwargs: Mapping| None=
None) → set[CatalogTask][source]
```

```
[source]
```

Get all queued or running tasks. 

#### Parameters: 

- params – Query parameters, refer to <u>Tasks API</u> for available parameters. 

- request_kwargs – Keyword arguments to be used in **`requests.sessions.Session.get()`** request. 

#### Returns: 

A set of all queued or running tasks. 

```
get_task_log(task_id: str| int,*, params: Mapping| None=None,
request_kwargs: Mapping| None=None) → str
```

```
[source]
```

Get a task log. 

#### Parameters: 



https://archive.org/developers/internetarchive/python-lib.html 

11/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

params – URL parameters to send with the request (e.g. `{'lines': 100}` to fetch a truncated log). 

request_kwargs – Keyword arguments that **<u>`requests.Request`</u>** takes. 

#### Returns: 

The task log as a string. 

```
get_tasks(identifier: str='', params: dict| None=None, request_kwargs:
Mapping| None=None) → set[CatalogTask][source]
```

Get a list of all tasks meeting all criteria. The list is ordered by submission time. 

#### Parameters: 

identifier – The item identifier, if provided will return tasks for only this item filtered by other criteria provided in params. 

params – 

Query parameters, refer to <u>Tasks API</u> for available parameters. 

request_kwargs – Keyword arguments to be used in 

**`requests.sessions.Session.get()`** request. 

#### Returns: 

A set of all tasks meeting all criteria. 

```
get_tasks_summary(identifier: str='', params: dict| None=None,
```

```
request_kwargs: Mapping| None=None) → dict
```

```
[source]
```

Get the total counts of catalog tasks meeting all criteria, organized by run status (queued, running, error, and paused). 

#### Parameters: 

identifier – Item identifier. 

#### params – 

Query parameters, refer to <u>Tasks API</u> for available parameters. 

- request_kwargs – Keyword arguments to be used in 

**`requests.sessions.Session.get()`** request. 

#### Returns: 

Counts of catalog tasks meeting all criteria. 

```
iter_catalog(identifier: str| None=None, params: dict| None=None,
request_kwargs: Mapping| None=None) → Iterable[CatalogTask]
```

```
[source]
```

https://archive.org/developers/internetarchive/python-lib.html 

12/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

A generator that returns queued or running tasks. 

#### Parameters: 

identifier – Item identifier. 

#### params – 

Query parameters, refer to <u>Tasks API</u> for available parameters. 

request_kwargs – Keyword arguments to be used in **`requests.sessions.Session.get()`** request. 

#### Returns: 

An iterable of queued or running CatalogTasks. 

```
iter_history(identifier: str| None,params: dict| None=None,
request_kwargs: Mapping| None=None) → Iterable[CatalogTask]
```

```
[source]
```

A generator that returns completed tasks. 

#### Parameters: 

identifier – Item identifier. 

params – 

Query parameters, refer to <u>Tasks API</u> for available parameters. request_kwargs – Keyword arguments to be used in 

**`requests.sessions.Session.get()`** request. 

#### Returns: 

An iterable of completed CatalogTasks. 

```
search_items(query: str,fields: Iterable[str] | None=None, sorts:
Iterable[str] | None=None, params: Mapping| None=None, full_text_search:
bool=False, dsl_fts: bool=False, request_kwargs: Mapping| None=None,
max_retries: int| Retry | None=None) → Search[source]
```

```
[source]
```

Search for items on Archive.org. 

#### Parameters: 

query – The Archive.org search query to yield results for. Refer to <u>https://archive.org/advancedsearch.php#raw</u> for help formatting your query. 

fields – The metadata fields to return in the search results. 

- params – The URL parameters to send with each request sent to the Archive.org Advancedsearch Api. 

https://archive.org/developers/internetarchive/python-lib.html 

13/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

- full_text_search – Beta support for querying the archive.org Full Text Search API [default: False]. 

- dsl_fts – Beta support for querying the archive.org Full Text Search API in dsl (i.e. do not prepend `!L `` to the ``full_text_search` query [default: False]. 

#### Returns: 

- A **`Search`** object, yielding search results. 

```
submit_task(identifier: str,cmd: str,comment: str='', priority: int=
0, data: dict| None=None, headers: dict| None=None, reduced_priority:
bool=False, request_kwargs: Mapping| None=None) → Response[source]
```

Submit an archive.org task. 

#### Parameters: 

identifier – Item identifier. 

- cmd – Task command to submit, see <u>supported task commands.</u> 

- comment – A reasonable explanation for why the task is being submitted. 

- priority – Task priority from 10 to -10 (default: 0). 

- data – Extra POST data to submit with the request. Refer to <u>Tasks API Request Entity.</u> 

- headers – Add additional headers to request. 

- reduced_priority – Submit your derive at a lower priority. This option is helpful to get around rate-limiting. Your task will more likely be accepted, but it might not run for a long time. Note that you still may be subject to rate-limiting. This is different than `priority` in that it will allow you to possibly avoid rate-limiting. 

- request_kwargs – Keyword arguments to be used in 

- **`requests.sessions.Session.post()`** request. 

#### Returns: 

```
requests.Response
```

```
whoami() → str
```

```
[source]
```

Return the logged-in user email address. 

#### Returns: 

The logged-in user email address. 

Creating a session: 

https://archive.org/developers/internetarchive/python-lib.html 

14/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

```
from internetarchive importget_session
# From config file
session=get_session(config_file='~/.config/internetarchive/ia.ini')
# From dictionary
config={
's3':{
'access':'your_access_key',
'secret':'your_secret_key'
}
}
session=get_session(config=config)
```

For complete session documentation, see <u>internetarchive.session module.</u> 

## Working with Items 

Once you have an item (from **<u>`get_item()`</u>** or **`get_item()`** ), you can: 

```
item=get_item('TripDown1905')
# Access metadata
print(item.metadata['title'])
print(item.metadata['creator'])
# Download files
item.download(glob_pattern='*.mp4')
# Upload new files
item.upload(['file1.txt','file2.jpg'],
metadata={'title':'My New Files'})
# Modify metadata
item.modify_metadata({'subject':['history','film']})
# List files
forfileinitem.files:
print(file.name,file.format)
```

For complete item documentation, see <u>internetarchive.item module.</u> 

15/17 

https://archive.org/developers/internetarchive/python-lib.html 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

## Searching for Items 

```
from internetarchive importsearch_items
```

```
# Basic search
search=search_items('collection:opensource movies')
# Iterate through results
forresultinsearch:
print(f"{result['identifier']}: {result.get('title', 'No title')}")
# Get specific fields
search=search_items('subject:science',
fields=['identifier','title','date'])
forresultinsearch:
print(result)
```

For complete search documentation, see <u>internetarchive.search module.</u> 

## Common Patterns 

Download all files from multiple items: 

```
from internetarchive importget_item
identifiers=['TripDown1905','goodytwoshoes00newyiala']
foridentifierinidentifiers:
item=get_item(identifier)
item.download()
```

Upload with custom metadata: 

```
from internetarchive importupload
upload(
'my-new-item-001',
files=['document.pdf','cover.jpg'],
metadata={
'title':'My Document',
'mediatype':'texts',
'collection':'opensource',
'subject':['documentation','tutorial']
}
)
```

Search and process results: 

https://archive.org/developers/internetarchive/python-lib.html 

16/17 

Python Library Usage — Internet Archive Developer Portal 

10/23/26, 4:43 PM 

```
from internetarchive importsearch_items
# Search with pagination
search=search_items(
'collection:prelinger',
params={'rows':50,'page':1}
)
# Collect identifiers
identifiers=[result['identifier']forresultinsearch]
# Process in batches
foridentifierinidentifiers[:10]:# First 10 items
print(f"Processing {identifier}")
```

## Configuration 

The library needs your archive.org credentials for certain operations (uploading, modifying metadata, etc.). You can configure it in several ways: 

1. Config file (recommended): Use `ia configure` from the CLI or **<u>`configure()`</u>** from Python 

2. Environment variables: Set `IA_ACCESS_KEY_ID` and `IA_SECRET_ACCESS_KEY` 

3. Python dictionary: Pass credentials directly when creating a session 

See <u>Configuration</u> for complete configuration details. 

## Next Steps 

For complete documentation of all modules, classes, and methods, see <u>Module Documentation.</u> 

For troubleshooting and advanced usage, check the examples in the <u>GitHub repository.</u> 

https://archive.org/developers/internetarchive/python-lib.html 

17/17 

