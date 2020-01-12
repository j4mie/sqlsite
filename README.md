# SQLSite

A tool for serving simple websites and JSON APIs directly from a [SQLite](https://sqlite.org/) database.

## Why?

SQLite is a fantastic way of storing data in a safe, well-structured, uniform way and querying it quickly. This project helps you expose that data to the web.

SQLSite is inspired by [Datasette](https://datasette.readthedocs.io), but is much simpler. Unlike Datasette, SQLSite does not do anything automatically. It doesn't allow to you explore and visualize your data in nicely formatted tables and graphs. Instead, you must manually define how your data is exposed to the Web using SQL queries.

## Use Cases

* Building simple websites (SQLSite would work well where you might normally use a static site generator but prefer your data to be structured and queryable).
* Creating very quick and simple JSON APIs to expose data in a SQLite database to the web.
* Serving static files directly from a [SQLite Archive](#sqlite-archives).

## Prerequisite concepts

The first thing to note is that SQLSite is **designed for building _read only_ web applications**. It does not allow you to build applications that modify the underlying SQLite database in any way. Use some other tool (like the `sqlite3` command line tool, or [sqlite-utils](https://sqlite-utils.readthedocs.io/), or a SQLite GUI) to create and edit your database. 

The second concept you'll need to know about is [SQLite Archives](https://sqlite.org/sqlar.html). This is a file container format similar to a ZIP archive or Tarball but based on an SQLite database. This allows websites served by SQLSite to be completely self-contained. **The HTML templates and static files needed by the web application are stored alongside its relational data in the same file**. See [below](#sqlite-archives) for more information on this.

## How to use SQLSite

SQLSite allows you to create _routes_ that map incoming HTTP request URLs to configurable _handlers_. Handlers are like "views" (if you're accustomed to Django, Flask etc).

In most web frameworks, the routing of incoming URLs to views is configured in code (Django's `URLConf`, Flask's `@app.route` decorator, etc). In SQLSite, the routing is configured _in the SQLite database itself_.

Here's the schema for the `route` table. To use a SQLite database with SQLSite, this table must exist:

```sql
CREATE TABLE route (
    pattern TEXT PRIMARY KEY NOT NULL,
    handler TEXT NOT NULL,
    config TEXT NOT NULL,
    exists_query TEXT
);
```

The columns of this table are:

### `pattern`

This is a regular expression that defines the URL that will be matched by the route. It is identical to Django's "old fashioned" (pre-`path`) regex-based URL routing syntax. You can use named capturing groups to extract values from the path. Some examples:

* `^$` - matches the root (`/`)
* `^blog/$` - matches `/blog/`
* `^blog/(?P<slug>[-a-zA-Z0-9_]+)/$` - matches `/blog/<slug>/`, where `<slug>` is any lowercase or uppercase letter, digit, `-` or `_`

### `handler`

This is the name of the handler that should respond to HTTP requests whose path matches the given `pattern`. Valid handlers are `template`, `json` and `static`. See [below](#handlers) for details of each handler.

### `config`

Configuration for the handler. The meaning of this field is different for each handler. See [below](#handlers) for details.

### `exists_query`

This column is optional. If it is used, it should contain an SQL query that will be executed before your handler runs, and should return a single boolean value. If the value is `0`, the handler will not run and instead `404 Not Found` will be returned. The SQL query can contain [named parameters](https://sqlite.org/lang_expr.html#varparam) which will be populated with captured values from the route's URL pattern.

This allows you to check whether a row in the database exists before attempting to render it. An example value for the `exists_query` column might be:

`SELECT EXISTS(SELECT 1 FROM blogpost WHERE slug=:slug)`

## Handlers

### `template` handler

This handler is used to respond to requests by rendering HTML pages. It uses [Jinja](https://jinja.palletsprojects.com/) and can build HTML dynamically by running database queries.

If you use the `template` handler, the `config` field for the route should be set to the name of the template you wish to use. However, **SQLSite does not use templates stored in the filesystem, like you would normally use with Jinja2**. Instead, SQLSite stores the templates _inside the database_ using [SQLite's "Archive" feature](https://sqlite.org/sqlar.html). See [below](#sqlite-archives) for details of how to use this.

Note that template paths start at the root of the archive, so if your template is in a "directory" (`templates/`) you should provide the full path (`templates/index.html`). If you use Jinja's template inheritance functionality, you should also fully-qualify template names, for example: `{% extends "templates/base.html" %}`

#### Running SQL in templates

Your Jinja template will be rendered with a special function included in its context called `sql`. This allows you to run any database query and generate HTML dynamically using the results. For example, to build a blog index page you may use a template like this:

```html
<html>
  <head><title>Blog!</title></head>
  <body>
    <h1>My blog!</h1>
    <ul>
    {% for post in sql("SELECT * FROM blogpost") %}
      <li><a href="/posts/{{ post.slug }}/">{{ post.title }}</a></li>
    {% endfor %}
    </ul>
  </body>
</html>
```

Queries run using the `sql` function can contain [named parameters](https://sqlite.org/lang_expr.html#varparam). The optional second argument to `sql` is a dictionary of parameter values. The context for your template contains a variable called `url`, which is a dictionary containing all values captured from the URL pattern.

For example, given the route pattern `^blog/(?P<slug>[-a-zA-Z0-9_]+)/$`, your template may contain the following on the blog post detail page:

```html
{% with post = sql("SELECT title, content FROM blogpost WHERE slug=:slug", {"slug": url.slug})[0] %}
<h2>{{ post.title }}</h2>
{% endwith %}
```

#### Rendering Markdown

SQLSite has support for rendering Markdown in your templates using the [Misaka](https://misaka.61924.nl/) library. If Misaka is installed (`pip install misaka`) then a `markdown` filter becomes available in your templates:

```
{{ post.content | markdown }}
```

### `static` handler

This handler serves static files. **It does not serve files stored in the filesystem, but instead serves them directly from the SQLite Archive inside the database**. See [below](#sqlite-archives) for details of this.

If you use the `static` handler, the `config` field for the route should be set to the path prefix ("directory") inside the archive from which to serve files. For example, to serve files that are prefixed with `static`, you should set the value of the `config` column to `static`.

The `pattern` for the route _must_ include a named capturing group called `name`, which should capture the rest of the filename after the prefix you supplied in `config`.

For example, to serve static files under the URL prefix `media`, using the path prefix `static`, you should set `pattern` to `^media/(?P<name>.+)$`, `handler` to `static` and `config` to `static`. There is no need to set the `exists_query` column: the handler will automatically return 404 if the file does not exist inside the archive.

### `json` handler

This handler takes the results of a query and serializes it into a list of JSON objects. The `config` field should be the query to execute.

## SQLite Archives

SQLSite stores the HTML templates and static files needed to build your website _inside the SQLite database itself_. To do this, it uses the [SQLite Archive](https://sqlite.org/sqlar.html) format. Please read the SQLite documentation for full details of this feature, but a quick primer is below.

A SQLite Archive is just an ordinary SQLite database with an ordinary table inside it with a particular name and schema. The `sqlite3` command line tool comes with a few commands to work with files stored in this table.

First, you need to create the special `sqlar` table in your database with the following command:

`sqlite3 db.sqlite -Ac`

Then, given the following folder structure on disk:

```
db.sqlite
static/
  cat.gif
templates/
  index.html
```

You can copy this data into the archive as follows:

`sqlite3 db.sqlite -Au static/* templates/*`

To list the files stored in your database:

`sqlite3 db.sqlite -At`

This should return:

```
static/cat.gif
templates/index.html
```

## Installing SQLSite

You can install SQLSite with `pip install sqlsite`. It requires Python 3.7+.

## Configuration

The only configuration option available is the name of the SQLite database file to use. By default, SQLSite uses a database called `db.sqlite`. To change this, set the environment variable `SQLSITE_DATABASE` to the name of your database file.

## Running and deploying SQLSite

SQLSite is implemented as a [WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) application. WSGI is a Python standard for interfacing between a web application and a web server. SQLSite itself does not come with a web server, so you will have to install your own.

[Gunicorn](https://gunicorn.org) is a widely used Python web application server. Read its [documentation](http://docs.gunicorn.org/en/stable/) carefully. An example command for local development might be:

```
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 sqlsite:app
```
