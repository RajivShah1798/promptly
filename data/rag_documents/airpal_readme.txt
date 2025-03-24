# Airpal

Airpal is a web-based, query execution tool which leverages Facebook's [PrestoDB](http://prestodb.io)
to make authoring queries and retrieving results simple for users.
Airpal provides the ability to find tables, see metadata, browse sample rows,
write and edit queries, then submit queries all in a web interface. Once
queries are running, users can track query progress and when finished,
get the results back through the browser as a CSV (download it or share it
with friends). The results of a query can be used to generate a new Hive table
for subsequent analysis, and Airpal maintains a searchable history of all
queries run within the tool.

* [Features](#features)
* [Requirements](#requirements)
* [Launching](#steps-to-launch)
* [Presto Compatibility Chart](#compatibility-chart)

![Airpal UI](screenshots/demo.gif)

## Features

* Optional [Access Control](docs/USER_ACCOUNTS.md)
* Syntax highlighting
* Results exported to a CSV for download or a Hive table
* Query history for self and others
* Saved queries
* Table finder to search for appropriate tables
* Table explorer to visualize schema of table and first 1000 rows

## Requirements

* Java 7 or higher
* MySQL database
* [Presto](http://prestodb.io) 0.77 or higher
* S3 bucket (to store CSVs)
* Gradle 2.2 or higher


## Steps to launch

1. Build Airpal

    We'll be using [Gradle](https://www.gradle.org/) to build the back-end Java code
    and a [Node.js](http://nodejs.org/)-based build pipeline ([Browserify](http://browserify.org/)
    and [Gulp](http://gulpjs.com/)) to build the front-end Javascript code.

    If you have `node` and `npm` installed locally, and wish to use
    them, simply run:

    ```
    ./gradlew clean shadowJar -Dairpal.useLocalNode
    ```

    Otherwise, `node` and `npm` will be automatically downloaded for you
    by running:

    ```
    ./gradlew clean shadowJar
    ```

    Specify Presto version by `-Dairpal.prestoVersion`:

    ```
    ./gradlew -Dairpal.prestoVersion=0.145 clean shadowJar
    ```

1. Create a MySQL database for Airpal. We recommend you call it `airpal` and will assume that for future steps.

1. Create a `reference.yml` file to store your configuration options.

    Start by copying over the example configuration, `reference.example.yml`.

    ```
    cp reference.example.yml reference.yml
    ```
    Then edit it to specify your MySQL credentials, and your S3 credentials if
    using S3 as a storage layer (Airpal defaults to local file storage, for
    demonstration purposes).

1. Migrate your database.

    ```
    java -Duser.timezone=UTC \
         -cp build/libs/airpal-*-all.jar com.airbnb.airpal.AirpalApplication db migrate reference.yml
    ```

1. Run Airpal.

    ```
    java -server \
         -Duser.timezone=UTC \
         -cp build/libs/airpal-*-all.jar com.airbnb.airpal.AirpalApplication server reference.yml
    ```

1. Visit Airpal.
    Assuming you used the default settings in `reference.yml` you can
    now open http://localhost:8081 to use Airpal. Note that you might
    have to change the host, depending on where you deployed it.

*Note:* To override the configuration specified in `reference.yml`, you may
specify certain settings on the command line in [the traditional Dropwizard
fashion](https://dropwizard.github.io/dropwizard/manual/core.html#configuration),
like so:

```
java -Ddw.prestoCoordinator=http://presto-coordinator-url.com \
     -Ddw.s3AccessKey=$ACCESS_KEY \
     -Ddw.s3SecretKey=$SECRET_KEY \
     -Ddw.s3Bucket=airpal \
     -Ddw.dataSourceFactory.url=jdbc:mysql://127.0.0.1:3306/airpal \
     -Ddw.dataSourceFactory.user=airpal \
     -Ddw.dataSourceFactory.password=$YOUR_PASSWORD \
     -Duser.timezone=UTC \
     -cp build/libs/airpal-*-all.jar db migrate reference.yml
```


## Compatibility Chart

Airpal Version | Presto Versions Tested
---------------|-----------------------
0.1            | 0.77, 0.87, 0.145

## In the Wild
Organizations and projects using `airpal` can list themselves [here](INTHEWILD.md).

## Contributors

- Andy Kramolisch [@andykram](https://github.com/andykram)
- Harry Shoff [@hshoff](https://github.com/hshoff)
- Josh Perez [@goatslacker](https://github.com/goatslacker)
- Spike Brehm [@spikebrehm](https://github.com/spikebrehm)
- Stefan Vermaas [@stefanvermaas](https://github.com/stefanvermaas)
Please use [pull requests](https://github.com/airbnb/airpal/pull/new/master) to add your organization and/or project to this document!

Organizations
----------
 - [Airbnb](https://github.com/airbnb)
 - [Nasdaq](https://github.com/nasdaq)
 - [PubNative](https://github.com/pubnative)

Projects
----------
# Airpal is an OPEN Open Source Project

(borrowed from the excellent [node-levelup CONTRIBUTING.md](https://github.com/rvagg/node-levelup/blob/master/CONTRIBUTING.md)

-----------------------------------------

## What?

Individuals making significant and valuable contributions are given commit-access to the project to contribute as they see fit. This project is more like an open wiki than a standard guarded open source project.

## Rules

There are a few basic ground-rules for contributors:

1. **No `--force` pushes** or modifying the Git history in any way.
1. **Non-master branches** ought to be used for ongoing work.
1. **External API changes and significant modifications** ought to be subject to an **internal pull-request** to solicit feedback from other contributors.
1. Internal pull-requests to solicit feedback are *encouraged* for any other non-trivial contribution but left to the discretion of the contributor.
1. Contributors should attempt to adhere to the prevailing code-style.

## Releases

Declaring formal releases remains the prerogative of the project maintainer.

## Changes to this arrangement

This is an experiment and feedback is welcome! This document may also be subject to pull-requests or changes by contributors where you believe you have something valuable to add or change.

# User Accounts

Airpal has the ability to restrict access to data based on the schema
and table it is in. These restrictions also support limiting access
to views, based on the view's fully qualified name.
This functionality is mostly provided by [Apache
Shiro](http://shiro.apache.org/), and is configured by specifying an INI
file in the Airpal configuration under [`shiro > iniConfigs`](https://github.com/airbnb/airpal/blob/master/reference.example.yml#L22).
The [Shiro docs](http://shiro.apache.org/reference.html) provide
information on configuring Shiro.

By default, Airpal is configured to use the provided
[allow all](https://github.com/airbnb/airpal/blob/master/src/main/resources/shiro_allow_all.ini)
configuration file. This configuration allows all users to have access
to all data available to Presto.

Airpal also ships with a provided config file with [statically
configured users](https://github.com/airbnb/airpal/blob/master/src/main/resources/shiro_static_users.ini).
This INI file establishes one user account with a static username and
password, and should not be used in a production setting. To enable this,
simply modify `reference.yml` to use `shiro_static_users.ini`.

Airpal can be configured to provide authentication and authorization via
any shiro supported realm or filter, however, the primary principle must
be an instance of one of the following:

* A class which implements [`com.airbnb.airpal.core.ToAirpalUser`](https://github.com/airbnb/airpal/blob/master/src/main/java/com/airbnb/airpal/core/ToAirpalUser.java)
* A class which is an [`com.airbnb.airpal.core.AirpalUser`](https://github.com/airbnb/airpal/blob/master/src/main/java/com/airbnb/airpal/core/AirpalUser.java)
* A string, denoting the user's name, in which case the user assumes
  default permissions and privileges

Internally, we have a custom realm and filter which will map a user from
our internal auth system to an `AirpalUser`.

Note that there are very likely better ways of making this more general,
and PRs are welcome.

# JavaScript

## Gulp
The frontend application uses Gulp for automation of some frontend stuff like
compiling the browserify code and for reloading the browser while developing.

To run the default configuration/tasks of gulp, just run `gulp` and you'll be
fine. If you want to build the JavaScript, just run simply `gulp build` (this
is also what the `pom.xml` does when running `mvn clean package`).

## Adding new gulp tasks
If you want to add more tasks, add them to the `gulp/tasks` folder and
don't forget to add the configuration in the `gulp/config.js` file.

More information about this gulp setup: [Gulp starter](https://github.com/greypants/gulp-starter).

# Stylesheet
The CSS files are following the CSS guidelines of Harry Roberts and can be
found at: http://cssguidelin.es

## Theming
It's possible to add your own theme (which probably will be based on bootstrap,
since it's used in the project).

It's recommended to use pure CSS instead of SASS, because it's very low level
and understood by everyone. But at the end: it's your own choice while
developing your own theme for Airpal.

To keep your code clean it's recommended to add your theme to the `stylesheets/
themes/` folder, but feel free to change it for your own needs.
