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


                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright 2013-present, Airbnb, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

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
