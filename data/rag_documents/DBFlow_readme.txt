# README

![Image](https://github.com/agrosner/DBFlow/blob/develop/dbflow_banner.png?raw=true)

[![JitPack.io](https://img.shields.io/badge/JitPack.io-5.0.0alpha1-red.svg?style=flat)](https://jitpack.io/#Raizlabs/DBFlow) [![Android Weekly](http://img.shields.io/badge/Android%20Weekly-%23129-2CB3E5.svg?style=flat)](http://androidweekly.net/issues/issue-129) [![Android Arsenal](https://img.shields.io/badge/Android%20Arsenal-DBFlow-brightgreen.svg?style=flat)](https://android-arsenal.com/details/1/1134)

DBFlow is fast, efficient, and feature-rich Kotlin database library built on SQLite for Android. DBFlow utilizes annotation processing to generate SQLite boilerplate for you and provides a powerful SQLite query language that makes using SQLite a joy.

DBFlow is built from a collection of some of the best features of many database libraries. Don't let an ORM or library get in your way, let the code you write in your applications be the best as possible.

Supports:

**Kotlin:** Built using the language, the library is super-concise, null-safe and efficient.

**Coroutines:** Adds coroutine support for queries.

**RX Java:** Enable applications to be reactive by listening to DB changes and ensuring your subscribers are up-to-date.

**Paging:** Android architecture component paging library support for queries via `QueryDataSource`.

**SQLCipher:** Easy database encryption support in this library.

**SQLite Query Language:** Enabling autocompletion on sqlite queries combined with Kotlin language features means SQLite-like syntax.

## Changelog

Changes exist in the [releases tab](https://github.com/Raizlabs/DBFlow/releases).

## Usage Docs

For more detailed usage, check out it out [here](https://agrosner.gitbooks.io/dbflow/content/)

## Including in your project

Add jitpack.io to your project's repositories:

```groovy
allProjects {
  repositories {
    google() 
    // required to find the project's artifacts
    // place last
    maven { url "https://www.jitpack.io" }
  }
}
```

Add artifacts to your project:

```groovy
  apply plugin: 'kotlin-kapt' // only required for kotlin consumers.

  def dbflow_version = "5.0.0-alpha1"
  // or 10-digit short-hash of a specific commit. (Useful for bugs fixed in develop, but not in a release yet)

  dependencies {

    // Use if Kotlin user.
    kapt "com.github.agrosner.dbflow:processor:${dbflow_version}"

    // Annotation Processor
    // if only using Java, use this. If using Kotlin do NOT use this.
    annotationProcessor "com.github.agrosner.dbflow:processor:${dbflow_version}"


    // core set of libraries
    implementation "com.github.agrosner.dbflow:core:${dbflow_version}"
    implementation "com.github.agrosner.dbflow:lib:${dbflow_version}"

    // sql-cipher database encryption (optional)
    implementation "com.github.agrosner.dbflow:sqlcipher:${dbflow_version}"
    implementation "net.zetetic:android-database-sqlcipher:${sqlcipher_version}@aar"

    // RXJava 2 support
    implementation "com.github.agrosner.dbflow:reactive-streams:${dbflow_version}"

    // Kotlin Coroutines
    implementation "com.github.agrosner.dbflow:coroutines:${dbflow_version}"

    // Android Architecture Components Paging Library Support
    implementation "com.github.agrosner.dbflow:paging:${dbflow_version}"

    // adds generated content provider annotations + support.
    implementation "com.github.agrosner.dbflow:contentprovider:${dbflow_version}"

  }
```

## Pull Requests

I welcome and encourage all pull requests. Here are some basic rules to follow to ensure timely addition of your request: 1. Match coding style \(braces, spacing, etc.\) This is best achieved using **Reformat Code** shortcut, command+option+L on Mac and Ctrl+Alt+L on Windows, with Android Studio defaults. 2. If its a feature, bugfix, or anything please only change code to what you specify. 3. Please keep PR titles easy to read and descriptive of changes, this will make them easier to merge :\) 4. Pull requests _must_ be made against `develop` branch. Any other branch \(unless specified by the maintainers\) will get **rejected**. 5. Have fun!

## Maintainer

Originally created by [Raizlabs](https://www.raizlabs.com), a [Rightpoint](https://www.rightpoint.com) company

Maintained by [agrosner](https://github.com/agrosner) \([@agrosner](https://www.twitter.com/agrosner)\)

# Table of contents

* [README](README.md)
* [GettingStarted](gettingstarted.md)
* [Usage Docs](usage2/README.md)
  * [Including In Project](usage2/including-in-project.md)
  * [Proguard](usage2/proguard.md)
  * [Main Usage](usage2/usage/README.md)
    * [Databases](usage2/usage/databases.md)
    * [Models](usage2/usage/models.md)
    * [Migrations](usage2/usage/migrations.md)
    * [Views](usage2/usage/modelviews.md)
    * [Relationships](usage2/usage/relationships.md)
    * [Storing Data](usage2/usage/storingdata.md)
    * [Retrieval](usage2/usage/retrieval.md)
    * [SQLite Query Language](usage2/usage/sqlitewrapperlanguage.md)
    * [TypeConverters](usage2/usage/typeconverters.md)
    * [Observability](usage2/usage/observability.md)
  * [RXJavaSupport](usage2/rxjavasupport.md)
  * [Advanced Usage](usage2/advanced-usage/README.md)
    * [Caching](usage2/advanced-usage/caching.md)
    * [ListBasedQueries](usage2/advanced-usage/listbasedqueries.md)
    * [MultipleModules](usage2/advanced-usage/multiplemodules.md)
    * [QueryModels](usage2/advanced-usage/querymodels.md)
    * [Indexing](usage2/advanced-usage/indexing.md)
    * [SQLCipher](usage2/advanced-usage/sqlciphersupport.md)
  * [ContentProviderGeneration](usage2/contentprovidergeneration.md)
  * [Migration4Guide](usage2/migration4guide.md)
* [ISSUE\_TEMPLATE](issue_template.md)
* [.github](.github/README.md)
  * [CONTRIBUTING](.github/contributing.md)

# GettingStarted

This section describes how Models and tables are constructed via DBFlow. first let's describe how to get a database up and running.

## Creating a Database

In DBFlow, creating a database is as simple as only a few lines of code. DBFlow supports any number of databases, however individual tables and other related files can only be associated with one database.

```kotlin
@Database(version = 1)
abstract class AppDatabase : DBFlowDatabase()
```

```java
@Database(version = 1)
public abstract class AppDatabase extends DBFlowDatabase {
}
```

The name of the database by default is the class name. To change it, read [here](usage2/usage/databases.md).

Writing this file generates \(by default\) a `AppDatabaseAppDatabase_Database.java` file, which contains tables, views, and more all tied to a specific database. This class is automatically placed into the main `GeneratedDatabaseHolder`, which holds potentially many databases. The name, `AppDatabaseAppDatabase_Database.java`, is generated via {DatabaseClassName}{DatabaseFileName}\_Database

To learn more about what you can configure in a database, read [here](usage2/usage/databases.md)

## Initialize FlowManager

DBFlow needs an instance of `Context` in order to use it for a few features such as reading from assets, content observing, and generating `ContentProvider`.

Initialize in your `Application` subclass. You can also initialize it from other `Context` but we always grab the `Application` `Context` \(this is done only once\).

```kotlin
class ExampleApplication : Application {

  override fun onCreate() {
    super.onCreate()
    FlowManager.init(this)
  }
}
```

```java
public class ExampleApplication extends Application {

    @Override
    public void onCreate() {
        super.onCreate();
        FlowManager.init(this);
    }
}
```

By default without passing in a `DatabaseConfig`, we construct an `AndroidSQLiteOpenHelper` database instance. To learn more about what you can configure in a database, read [here](usage2/usage/databases.md), including providing own database instances.

Finally, add the custom `Application` definition to the manifest \(with the name that you chose for the class\):

```markup
<application
  android:name="{packageName}.ExampleApplication"
  ...>
</application>
```

A database within DBFlow is only initialized once you call `database<SomeDatabase>()`. If you don't want this behavior or prefer it to happen immediately, modify your `FlowConfig`:

```kotlin
override fun onCreate() {
    super.onCreate()
    FlowManager.init(FlowConfig.builder(this)
        .openDatabasesOnInit(true)
        .build())
}
```

```java
@Override
public void onCreate() {
    super.onCreate();
    FlowManager.init(FlowConfig.builder(this)
        .openDatabasesOnInit(true)
        .build());
}
```

If you do not like the built-in `DefaultTransactionManager`, or just want to roll your own existing system:

```kotlin
FlowManager.init(FlowConfig.builder(this)
    .database(DatabaseConfig.builder(AppDatabase::class)
            .transactionManager(CustomTransactionManager())
          .build()))
```

You can define different kinds for each database. To read more on transactions and subclassing `BaseTransactionManager` go [here](usage2/usage/storingdata.md)

## Create Models

Creating models are as simple as defining the model class, and adding the `@Table` annotation. To read more on this, read [here](usage2/usage/models.md).

**For now**: Models must provide a default, parameterless constructor. An example:

```kotlin
@Table(database = TestDatabase::class)
    class Currency(@PrimaryKey(autoincrement = true) var id: Long = 0,
                   @Column @Unique var symbol: String? = null,
                   @Column var shortName: String? = null,
                   @Column @Unique var name: String = "") // nullability of fields are respected. We will not assign a null value to this field.
```

or with Java:

```java
@Table(database = TestDatabase.class)
public class Currency {

    @PrimaryKey(autoincrement = true)
    long id; // package-private recommended, not required

    @Column
    @Unique
    String symbol;

    @Column
    String shortName;

    @Column
    @Unique
    private String name; // private with getters and setters

    public String getName() {
      return name;
    }

    public void setName(String name) {
      this.name = name;
    }
}
```

## Perform Some Queries

DBFlow uses expressive builders to represent and translate to the SQLite language.

A simple query in SQLite:

```text
SELECT * FROM Currency WHERE symbol='$';
```

DBFlow Kotlin \(by using our `dbflow-coroutines` module\):

```kotlin
async {
  database<AppDatabase>{
    val list = awaitTransact(
      select from Currency::class
      where (symbol eq "$")) { list }

    // use the objects here
  }
}
```

or in Java with fluent syntax

```java
SQLite.select(FlowManager.getDatabase(AppDatabase.class))
  .from(Currency.class)
  .where(Currency_Table.symbol.eq("$"));
```

We support many kinds of complex and complicated queries using the builder language. To read more about this, see [the wrapper language docs](usage2/usage/sqlitewrapperlanguage.md)

There is much more you can do in DBFlow. Read through the other docs to get a sense of the library.

# ISSUE\_TEMPLATE

DBFlow Version:

Bug or Feature Request:

Description:

The MIT License (MIT)

Copyright (c) 2014 Raizlabs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# CONTRIBUTING

## Contributing Guidelines

This document provides general guidelines about how to contribute to the project. Keep in mind these important things before you start contributing.

## Reporting issues

* Use [github issues](https://github.com/agrosner/DBFlow/issues) to report a bug.
* Before creating a new issue:
  * Make sure you are using the [latest release](https://github.com/agrosner/DBFlow/releases).
  * Check if the issue was [already reported or fixed](https://github.com/agrosner/DBFlow/issues?utf8=✓&q=is%3Aissue). Notice that it may not be released yet.
  * If you found a match add the github "+1" reaction brief comment. This helps prioritize the issues addressing the most common and critical ones first. If possible, add additional information to help us reproduce, and find the issue. Please use your best judgement.    
* Reporting issues:
  * Please include the following information to help maintainers to fix the problem faster:
    * Android version you are targeting.
    * Full console output of stack trace or code compilation error.
    * Any other additional detail you think it would be useful to understand and solve the problem.

## Pull requests

I welcome and encourage all pull requests. It usually will take me within 24-48 hours to respond to any issue or request. Here are some basic rules to follow to ensure timely addition of your request: 1. Match coding style \(braces, spacing, etc.\) This is best achieved using CMD+Option+L \(Reformat code\) on Mac \(not sure for Windows\) with Android Studio defaults. 2. If its a feature, bugfix, or anything please only change code to what you specify. 3. Please keep PR titles easy to read and descriptive of changes, this will make them easier to merge :\) 4. Pull requests _must_ be made against `develop` branch. Any other branch \(unless specified by the maintainers\) will get rejected.

### Suggested git workflow to contribute

1. Fork the repository.
2. Clone your forked project into your developer machine: `git clone git@github.com:<your-github-username>/DBFlow.git`
3. Add the original project repo as upstream repository in your forked project: `git remote add upstream git@github.com:DBFlow/DBFlow.git`
4. Before starting a new feature make sure your forked develop branch is synchronized upstream master branch. Considering you do not mere your pull request into develop you can run: `git checkout master` and then `git pull upstream develop`. Optionally `git push origin develop`.
5. Create a new branch. Note that the starting point is the upstream develop branch HEAD. `git checkout -b my-feature-name`
6. Stage all your changes `git add .` and commit them `git commit -m "Your commit message"`
7. Make sure your branch is up to date with upstream develop, `git pull --rebase upstream develop`, resolve conflicts if necessary. This will move your commit to the top of git stack.
8. Squash your commits into one commit. `git rebase -i HEAD~6` considering you did 6 commits.
9. Push your branch into your forked remote repository.
10. Create a new pull request adding any useful comment.

### Feature proposal

We would love to hear your ideas and make discussions about it.

* Use github issues to make feature proposals.
* We use `type: feature request` label to mark all [feature request issues](https://github.com/agrosner/DBFlow/labels/type%3A%20feature%20request).
* Before submitting your proposal make sure there is no similar feature request. If you find a match, feel free to join the discussion or just or just act with a reaction if you think the feature is worth implementing.
* Be as specific as possible providing a precise explanation of the feature so anyone can understand the problem and the benefits of solving it.

# RXJavaSupport

RXJava support in DBFlow is an _incubating_ feature and likely to change over time. We support both RX1 and RX2 and have made the extensions + DBFlow compatibility almost identical - save for the changes and where it makes sense in each version.

Currently it supports 1. `Insert`, `Update`, `Delete`, `Set`, `Join`, and all wrapper query mechanisms by wrapping them in `rx()` 2. Single + `List` model `save()`, `insert()`, `update()`, and `delete()`. 3. Streaming a set of results from a query 4. Observing on table changes for specific `ModelQueriable` and providing ability to query from that set repeatedly as needed. 5. Kotlin extension methods in a separate artifact that enhance the conversion.

## Getting Started

Add the separate packages to your project:

```groovy
dependencies {
  // RXJava1
  compile "com.github.agrosner.dbflow:rx:${dbflow_version}"

  // RXJava2
  compile "com.github.agrosner.dbflow:rx2:${dbflow_version}"

}
```

## Wrapper Language

Using the classes is as easy as wrapping all SQL wrapper calls with `RXSQLite.rx()` \(Kotlin we supply extension method\):

Before:

```java
List<MyTable> list = SQLite.select()
  .from(MyTable.class)
  .queryList();
```

After:

```java
RXSQLite.rx(
  SQLite.select().from(MyTable.class))
  .queryList()
  .subscribe((list) -> {

  });
```

or with Kotlin + extension methods:

```kotlin
  select.from(MyTable::class.java)
  .rx()
  .list { list ->

  }
```

## Model operations

To make the transition as smoothest as possible, we've provided a `BaseRXModel` which replaces `BaseModel` for convenience in the RX space.

```kotlin
class Person(@PrimaryKey var id: Int = 0, @Column var name: String? = "") : BaseRXModel
```

Operations are as easy as:

```java
new Person(5, "Andrew Grosner")
  .insert()
  .subscribe((rowId) -> {

  });
```

or with Kotlin+extensions:

```kotlin
Person(5, "Andrew Grosner")
  .insert { rowId ->

  }
```

## Query Stream

We can use RX to stream the result set, one at a time from the `ModelQueriable` using the method `queryStreamResults()`:

```java
RXSQLite.rx(
    SQLite.select()
    .from(TestModel1.class))
   .queryStreamResults()
   .subscribe((model) -> {

   });
```

## Kotlin Support

Most of the support mirrors [kotlin support]() with a few minor changes.

Extension properties/methods include: 1. `rx()` extension method making it super easy to integrate RX. 2. `RXModelQueriable.streamResults` - stream results one at time to a `Subscription` 3. `list`, `result`,`streamResults`, `cursorResult`,`statement`, `hasData`, `cursor`, and `count` all provide a method lambda that is called within a `Subscription`.

```kotlin
select from MyTable::class
  where (MyTable.name `is` "Good")
  list { list -> //

  }
```

which is the same with RX as:

```kotlin
(select.from(MyTable::class.java)
  .where(MyTable.name `is` "Good"))
  .rx()
  .list { list ->

  }
```

Or if we want to get pretty with `BaseRXModel` + extensions:

```kotlin
Person("Somebody").save { success ->
  // do something
}

Person("Somebody").update { success ->
  // do something
}

Person("Somebody").insert { rowId ->
  // do something
}

Person("Somebody").delete { success ->
  // do something
}
```

# Usage Docs

DBFlow is a Kotlin SQLite library for Android that makes it ridiculously easy to interact and use databases. Built with Annotation Processing, code use within a DB is fast, efficient, and type-safe. It removes the tedious \(and tough-to-maintain\) database interaction code, while providing a very SQLite-like query syntax.

Creating a database is as easy as a few lines of code:

```kotlin
@Database(version = AppDatabase.VERSION)
object AppDatabase {
    const val VERSION = 1
}
```

The `@Database` annotation generates a `DatabaseDefinition` which now references your SQLite Database on disk in the file named "AppDatabase.db". You can reference it in code as:

```java
val db: DatabaseDefinition = database<AppDatabase>();
```

To ensure generated code in DBFlow is found by the library, initialize the library in your `Application` class:

```kotlin
class MyApp : Application {

  override fun onCreate() {
    super.onCreate()
    FlowManager.init(this)
  }
}
```

By default, DBFlow generates the `GeneratedDatabaseHolder` class, which is instantiated once by reflection, only once in memory.

Creating a table is also very simple:

```kotlin
@Table(database = AppDatabase::class, name = "User2")
class User(@PrimaryKey var id: Int = 0,
           @Column var firstName: String? = null,
           @Column var lastName: String? = null,
           @Column var email: String? = null)
```

Then to create, read, update, and delete the model:

```kotlin
val user = User(id = UUID.randomUUID(),
                name = "Andrew Grosner",
                age = 27)

val db = databaseForTable<User>()
user.insert(db)

user.name = "Not Andrew Grosner";
user.update(db)

user.delete(db)

// Db optional on extension method
user.insert()
user.update()
user.delete()
user.save()

// find adult users
val users = database<AppDatabase>()
              .(select from User::class
                       where (User_Table.age greaterThan 18))
              .list

// or asynchronous retrieval
database<AppDatabase>().executeTransactionAsync(
{ (select from User::class where User_Table.age.greaterThan(18)).list },
success = { transaction, result ->
  // use result here
},
error = { transaction, error ->
  // handle any errors
})

// use coroutines!
async {
  database.awaitTransact(
       delete<SimpleModel>() where SimpleModel_Table.name.eq("5")) { executeUpdateDelete(database)
  }
}
```

# Migration4Guide

In 4.0, DBFlow has greatly improved its internals and flexibility in this release. We have removed the `Model` restriction, rewritten the annotation processor completely in Kotlin, and more awesome improvements.

_Major Changes In this release_

1. `PrimaryKey` can have `TypeConverters`, be table-based objects, and all kinds of objects. No real restrictions.
2. `ForeignKey` have been revamped to allow `stubbedRelationship`. This replaces `ForeignKeyContainer`.
3. `Model` interface now includes `load()` to enabled reloading very easily when fields change.
4. All `ModelContainer` implementation + support has been removed. A few reasons pushed the removal, including implementation. Since removing support, the annotation processor is cleaner, easier to maintain, and more streamlined. Also the support for it was not up to par, and by removing it, we can focus on improving the quality of the other features.
5. The annotation processor has been rewritten in Kotlin! By doing so, we reduced the code by ~13%.
6. Removed the `Model` restriction on tables. If you leave out extending `BaseModel`, you _must_ interact with the `ModelAdapter`.
7. We generate much less less code than 3.0. Combined the `_Table` + `_Adapter` into the singular `_Table` class, which contains both `Property` + all of the regular `ModelAdapter` methods. To ease the transition to 4.0, it is named `_Table` but extends `ModelAdapter`. So most use cases / interactions will not break.
8. `Condition` are now `Operator`, this includes `SQLCondition` -&gt; `SQLOperator`, `ConditionGroup` -&gt; `OperatorGroup`. `Operator` are now typed and safer to use. 1. `Operator` now also have `div`, `times`, `rem`, `plus` and `minus` methods.
9. Property class changes: 1. All primitive `Property` classes have been removed. We already boxed the values internally anyways so removing them cut down on method count and maintenance. 2. `BaseProperty` no longer needs to exist, so all of it's methods now exist in `Property` 3. `mod` method is now `rem` \(remainder\) method to match Kotlin 1.1's changes. 4. `dividedBy` is now `div` to match Kotlin operators. 5. `multipliedBy` is now `times` to match Kotlin operators.
10. Rewrote all Unit tests to be more concise, better tested, and cleaner.
11. A lot of bug fixes
12. Kotlin: 1. Added more Kotlin extensions. 2. Most importantly you don't need to use `BaseModel`/`Model` at all anymore if you so choose. There are `Model`-like extension methods that supply the `Model` methods. 3. Updated to version 1.1.1
13. RXJava1 and RXJava2 support! Can now write queries that return `Observable` and more.

# ContentProviderGeneration

This library includes a very fast, easy way to use `ContentProvider`! Using annotations, you can generate `ContentProvider` with ease.

## Getting Started

This feature is largely based off of [schematic](https://github.com/SimonVT/schematic), while leveraging DBFlow's power.

### Placeholder ContentProvider

In order to define a `ContentProvider`, you must define it in a placeholder class:

```java
@ContentProvider(authority = TestContentProvider.AUTHORITY,
        database = TestDatabase.class,
        baseContentUri = TestContentProvider.BASE_CONTENT_URI)
public class TestContentProvider {

    public static final String AUTHORITY = "com.dbflow5.test.provider";

    public static final String BASE_CONTENT_URI = "content://";

}
```

or you can use the annotation in any class you wish. The recommended place would be in a `@Database` placeholder class. This is to simplify some of the declarations and keep it all in one place.

```java
@ContentProvider(authority = TestDatabase.AUTHORITY,
        database = TestDatabase.class,
        baseContentUri = TestDatabase.BASE_CONTENT_URI)
@Database(name = TestDatabase.NAME, version = TestDatabase.VERSION)
public class TestDatabase {

    public static final String NAME = "TestDatabase";

    public static final int VERSION = "1";

    public static final String AUTHORITY = "com.dbflow5.test.provider";

    public static final String BASE_CONTENT_URI = "content://";

}
```

### Adding To Manifest

In other applications or your current's `AndroidManifest.xml` add the **generated $Provider** class:

```markup
<provider
            android:authorities="com.dbflow5.test.provider"
            android:exported="true|false"
            android:name=".provider.TestContentProvider_Provider"/>
```

`android:exported`: setting this to true, enables other applications to make use of it.

**True** is recommended for outside application access.

**Note you must have at least one** `@TableEndpoint` **for it to compile/pass error checking**

### Adding endpoints into the data

There are two ways of defining `@TableEndpoint`: 1. Create an inner class within the `@ContentProvider` annotation. 2. Or Add the annotation to a `@Table` and specify the content provider class name \(ex. TestContentProvider\)

`@TableEndpoint`: links up a query, insert, delete, and update to a specific table in the `ContentProvider` local database.

Some recommendations: 1. \(if inside a `@ContentProvider` class\) Name the inner class same as the table it's referencing 2. Create a `public static final String ENDPOINT = "{tableName}"` field for reusability 3. Create `buildUri()` method \(see below\) to aid in creating other ones.

To define one:

```java
@TableEndpoint(ContentProviderModel.ENDPOINT)
public static class ContentProviderModel {

    public static final String ENDPOINT = "ContentProviderModel";

    private static Uri buildUri(String... paths) {
        Uri.Builder builder = Uri.parse(BASE_CONTENT_URI + AUTHORITY).buildUpon();
        for (String path : paths) {
            builder.appendPath(path);
        }
        return builder.build();
    }

    @ContentUri(path = ContentProviderModel.ENDPOINT,
            type = ContentUri.ContentType.VND_MULTIPLE + ENDPOINT)
    public static Uri CONTENT_URI = buildUri(ENDPOINT);

}
```

or via the table it belongs to

```java
@TableEndpoint(name = ContentProviderModel.NAME, contentProvider = ContentDatabase.class)
@Table(database = ContentDatabase.class, tableName = ContentProviderModel.NAME)
public class ContentProviderModel extends BaseProviderModel<ContentProviderModel> {

    public static final String NAME = "ContentProviderModel";

    @ContentUri(path = NAME, type = ContentUri.ContentType.VND_MULTIPLE + NAME)
    public static final Uri CONTENT_URI = ContentUtils.buildUriWithAuthority(ContentDatabase.AUTHORITY);

    @PrimaryKey(autoincrement = true)
    long id;

    @Column
    String notes;

    @Column
    String title;

    @Override
    public Uri getDeleteUri() {
        return TestContentProvider.ContentProviderModel.CONTENT_URI;
    }

    @Override
    public Uri getInsertUri() {
        return TestContentProvider.ContentProviderModel.CONTENT_URI;
    }

    @Override
    public Uri getUpdateUri() {
        return TestContentProvider.ContentProviderModel.CONTENT_URI;
    }

    @Override
    public Uri getQueryUri() {
        return TestContentProvider.ContentProviderModel.CONTENT_URI;
    }
}
```

There are much more detailed usages of the `@ContentUri` annotation. Those will be in a later section.

### Connect Model operations to the newly created ContentProvider

There are two kinds of `Model` that connect your application to a ContentProvider that was defined in your app, or another app. Extend these for convenience, however they are not required.

`BaseProviderModel`: Overrides all `Model` methods and performs them on the `ContentProvider`

`BaseSyncableProviderModel`: same as above, except it will synchronize the data changes with the local app database as well!

#### Interacting with the Content Provider

You can use the `ContentUtils` methods:

```java
ContentProviderModel contentProviderModel = ...; // some instance

int count = ContentUtils.update(getContentResolver(), ContentProviderModel.CONTENT_URI, contentProviderModel);

Uri uri = ContentUtils.insert(getContentResolver(), ContentProviderModel.CONTENT_URI, contentProviderModel);

int count = ContentUtils.delete(getContentResolver(), someContentUri, contentProviderModel);
```

**Recommended** usage is extending `BaseSyncableProviderModel` \(for inter-app usage\) so the local database contains the same data. Otherwise `BaseProviderModel` works just as well.

```java
MyModel model = new MyModel();
model.id = 5;
model.load(); // queries the content provider

model.someProp = "Hello"
model.update(false); // runs an update on the CP

model.insert(false); // inserts the data into the CP
```

## Advanced Usage

### Notify Methods

You can define `@Notify` method to specify a custom interaction with the `ContentProvider` and return a custom `Uri[]` that notifies the contained `ContentResolver`. These methods can have any valid parameter from the `ContentProvider` methods.

Supported kinds include: 1. Update 2. Insert 3. Delete

#### Example

```java
@Notify(method = Notify.Method.UPDATE,
paths = {}) // specify paths that will call this method when specified.
public static Uri[] onUpdate(Context context, Uri uri) {

  return new Uri[] {
    // return custom uris here
  };
}
```

### ContentUri Advanced

#### Path Segments

Path segments enable you to "filter" the uri query, update, insert, and deletion by a specific column and a value define by '\#'.

To specify one, this is an example `path`

```java
path = "Friends/#/#"
```

then match up the segments as:

```java
segments = {@PathSegment(segment = 1, column = "id"),
    @PathSegment(segment = 2, column = "name")}
```

And to put it all together:

```java
@ContentUri(type = ContentType.VND_MULTIPLE,
path = "Friends/#/#",
segments = {@PathSegment(segment = 1, column = "id"),
    @PathSegment(segment = 2, column = "name")})
public static Uri withIdAndName(int id, String name) {
  return buildUri(id, name);
}
```

# Proguard

Since DBFlow uses annotation processing, which is run pre-proguard phase, the configuration is highly minimal. Also since we combine all generated files into the `GeneratedDatabaseHolder`, any other class generated can be obfuscated.

```text
-keep class * extends com.dbflow5.config.DatabaseHolder { *; }
```

This also works on modules from other library projects that use DBFlow.

# Including In Project

DBFlow has a number of artifacts that you can include in the project.

**Annotation Processor**: Generates the necessary code that you don't need to write.

**Core:** Contains the main annotations and misc classes that are shared across all of DBFlow.

**DBFlow:** The main library artifact used in conjunction with the previous two artifacts.

**Coroutines:** Adds coroutine support for queries.

**RX Java:** Enable applications to be reactive by listening to DB changes and ensuring your subscribers are up-to-date.

**Paging:** Android architecture component paging library support for queries via `QueryDataSource`.

**SQLCipher:** Easy database encryption support in this library.

## Add the jitpack.io repository

This repo is used to publish the artifacts. It also enables [dynamic builds](https://jitpack.io/docs/), allowing you to specify specific branches or commit hashes of the project to include outside of normal releases.

```groovy
allProjects {
  repositories {
    google()
    // required to find the project's artifacts
    // place last
    maven { url "https://www.jitpack.io" }
  }
}
```

Add artifacts to your project:

```groovy
  apply plugin: 'kotlin-kapt' // only required for kotlin consumers.

  def dbflow_version = "5.0.0-alpha1"
  // or 10-digit short-hash of a specific commit. (Useful for bugs fixed in develop, but not in a release yet)

  dependencies {

    // Use if Kotlin user.
    kapt "com.github.agrosner.dbflow:processor:${dbflow_version}"

    // Annotation Processor
    // if only using Java, use this. If using Kotlin do NOT use this.
    annotationProcessor "com.github.agrosner.dbflow:processor:${dbflow_version}"

    // core set of libraries
    implementation "com.github.agrosner.dbflow:core:${dbflow_version}"
    implementation "com.github.agrosner.dbflow:lib:${dbflow_version}"

    // sql-cipher database encryption (optional)
    implementation "com.github.agrosner.dbflow:sqlcipher:${dbflow_version}"
    implementation "net.zetetic:android-database-sqlcipher:${sqlcipher_version}@aar"

    // RXJava 2 support
    implementation "com.github.agrosner.dbflow:reactive-streams:${dbflow_version}"

    // Kotlin Coroutines
    implementation "com.github.agrosner.dbflow:coroutines:${dbflow_version}"

    // Android Architecture Components Paging Library Support
    implementation "com.github.agrosner.dbflow:paging:${dbflow_version}"

    // adds generated content provider annotations + support.
    implementation "com.github.agrosner.dbflow:contentprovider:${dbflow_version}"

  }
```
# SQLite Query Language

DBFlow's SQLite wrapper language attempts to make it as easy as possible to write queries, execute statements, and more.

We will attempt to make this doc comprehensive, but reference the SQLite language for how to formulate queries, as DBFlow follows it as much as possible.

## SELECT

The way to query data, `SELECT` are started by:

```kotlin
select from SomeTable::class
```

### Projections

By default if no parameters are specified in the `select()` query, we use the `*` wildcard qualifier, meaning all columns are returned in the results.

To specify individual columns, you _must_ use `Property` variables. These get generated when you annotate your `Model` with columns, or created manually.

```kotlin
select(Player_Table.name, Player_Table.position)
   from Player::class
```

To specify methods such as `COUNT()` or `SUM()` \(static import on `Method`\):

```kotlin
select(count(Employee_Table.name), sum(Employee_Table.salary))
    from Employee::class
```

Translates to:

```text
SELECT COUNT(`name`), SUM(`salary`) FROM `Employee`;
```

There are more handy methods in `Method`.

### Operators

DBFlow supports many kinds of operations. They are formulated into a `OperatorGroup`, which represent a set of `SQLOperator` subclasses combined into a SQLite conditional piece. `Property` translate themselves into `SQLOperator` via their conditional methods such as `eq()`, `lessThan()`, `greaterThan()`, `between()`, `in()`, etc.

They make it very easy to construct concise and meaningful queries:

```kotlin
val taxBracketCount = (select(count(Employee_Table.name))
    from Employee::class
    where Employee_Table.salary.lessThan(150000)
    and Employee_Table.salary.greaterThan(80000))
    .count(database)
```

Translates to:

```text
SELECT COUNT(`name`) FROM `Employee` WHERE `salary`<150000 AND `salary`>80000;
```

DBFlow supports `IN`/`NOT IN` and `BETWEEN` as well.

A more comprehensive list of operations DBFlow supports and what they translate to:

1. is\(\), eq\(\) -&gt; =
2. isNot\(\), notEq\(\) -&gt; !=
3. isNull\(\) -&gt; IS NULL / isNotNull\(\) -&gt; IS NOT NULL
4. like\(\), glob\(\)
5. greaterThan\(\), greaterThanOrEqual\(\), lessThan\(\), lessThanOrEqual\(\)
6. between\(\) -&gt; BETWEEN
7. in\(\), notIn\(\)

#### Nested Conditions

To create nested conditions \(in parenthesis more often than not\), just include an `OperatorGroup` as a `SQLOperator` in a query:

```kotlin
(select from Location::class
  where Location_Table.latitude.eq(home.latitude)
  and (Location_Table.latitude
         - home.latitude) eq 1000L
 )
```

Translates to:

```text
SELECT * FROM `Location` WHERE `latitude`=45.05 AND (`latitude` - 45.05) = 1000
```

#### Nested Queries

To create a nested query simply include a query as a `Property` via `(query).property`:

```kotlin
.where((select from(...) where(...)).property)
```

This appends a `WHERE (SELECT * FROM {table} )` to the query.

### JOINS

For reference, \([JOIN examples](http://www.tutorialspoint.com/sqlite/sqlite_using_joins.htm)\).

`JOIN` statements are great for combining many-to-many relationships. If your query returns non-table fields and cannot map to an existing object, see about [query models](../advanced-usage/querymodels.md)

For example we have a table named `Customer` and another named `Reservations`.

```sql
SELECT FROM `Customer` AS `C` INNER JOIN `Reservations` AS `R` ON `C`.`customerId`=`R`.`customerId`
```

```kotlin
// use the different QueryModel (instead of Table) if the result cannot be applied to existing Model classes.
val customers = (select from Customer::class).as("C")   
  innerJoin<Reservations.class>().as("R")    
   on(Customer_Table.customerId
      .withTable("C".nameAlias)
     eq Reservations_Table.customerId.withTable("R"))
    .customList<CustomTable>());
```

The `IProperty.withTable()` method will prepend a `NameAlias` or the `Table` alias to the `IProperty` in the query, convenient for JOIN queries:

```text
SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT
      ON COMPANY.ID = DEPARTMENT.EMP_ID
```

in DBFlow:

```kotlin
(select(Company_Table.EMP_ID, Company_Table.DEPT)
  from Company::class
  leftOuterJoin<Department>()
  .on(Company_Table.ID.withTable().eq(Department_Table.EMP_ID.withTable()))
)
```

### Order By

```kotlin
// true for 'ASC', false for 'DESC'. ASC is default.
(select from table
  orderBy(Customer_Table.customer_id)

  (select from table
    orderBy(Customer_Table.customer_id, ascending = true)
    orderBy(Customer_Table.name, ascending = false))
```

### Group By

```kotlin
(select from table)
  .groupBy(Customer_Table.customer_id, Customer_Table.customer_name)
```

### HAVING

```kotlin
(select from table)
  .groupBy(Customer_Table.customer_id, Customer_Table.customer_name))
  .having(Customer_Table.customer_id.greaterThan(2))
```

### LIMIT + OFFSET

```kotlin
SQLite.select()
  .from(table)
  .limit(3)
  .offset(2)
```

## UPDATE

DBFlow supports two kind of UPDATE: 1. `Model.update()` 2. `SQLite.update()`

For simple `UPDATE` for a single or few, concrete set of `Model` stick with \(1\). For powerful multiple `Model` update that can span many rows, use \(2\). In this section we speak on \(2\). **Note:** if using model caching, you'll need to clear it out post an operation from \(2\).

```sql
UPDATE Ant SET type = 'other' WHERE male = 1 AND type = 'worker';
```

Using DBFlow:

```kotlin
// Native SQL wrapper
database.beginTransactionAsync { db -> (update<Ant>()
   set Ant_Table.type.eq("other")
   where Ant_Table.type.is("worker")
   and Ant_Table.isMale.is(true))
   .executeUpdateDelete(db)
  }.execute { _, count -> }; // non-UI blocking
```

The `Set` part of the `Update` supports different kinds of values: 1. `ContentValues` -&gt; converts to key/value as a `SQLOperator` of `is()`/`eq()` 2. `SQLOperator`, which are grouped together as part of the `SET` statement.

## DELETE

`DELETE` queries in DBFlow are similiar to `Update` in that we have two kinds:

1. `Model.delete()`
2. `SQLite.delete()`

For simple `DELETE` for a single or few, concrete set of `Model` stick with \(1\). For powerful multiple `Model` deletion that can span many rows, use \(2\). In this section we speak on \(2\). **Note:** if using model caching, you'll need to clear it out post an operation from \(2\).

```kotlin
// Delete a whole table
delete<MyTable>().execute(database)

// Delete using query
database.beginTransactionAsync { db -> delete<MyTable>()
   where DeviceObject_Table.carrier.is("T-MOBILE")
   and DeviceObject_Table.device.is("Samsung-Galaxy-S5"))
   .executeUpdateDelete(db)
 }.execute { _, count -> };
```

## INSERT

`INSERT` queries in DBFlow are also similiar to `Update` and `Delete` in that we have two kinds:

1. `Model.insert()`
2. `SQLite.insert()`

For simple `INSERT` for a single or few, concrete set of `Model` stick with \(1\). For powerful multiple `Model` insertion that can span many rows, use \(2\). In this section we speak on \(2\). **Note:** using model caching, you'll need to clear it out post an operation from \(2\).

```kotlin
// columns + values via pairs
database.beginTransactionAsync { db ->
   (insert<SomeTable>(SomeTable_Table.name to "Default",
    MSomeTable_Table.phoneNumber to "5555555")
    .executeInsert(db)
}.execute()

// or combine into Operators
database.beginTransactionAsync { db ->
   (insert<SomeTable>(SomeTable_Table.name eq "Default",
    MSomeTable_Table.phoneNumber eq "5555555")
    .executeInsert(db)
}.execute()
```

`INSERT` supports inserting multiple rows as well.

```kotlin
// columns + values separately
database.beginTransactionAsync { db ->
  (insert<SomeTable>(SomeTable_Table.name, SomeTable_Table.phoneNumber)
  .values("Default1", "5555555")
  .values("Default2", "6666666"))
  .executeInsert(db)
}.execute()

// or combine into Operators
database.beginTransactionAsync { db ->
  (insert<SomeTable>(SomeTable_Table.name.eq("Default1"),
     SomeTable_Table.phoneNumber.eq("5555555"))
    .columnValues(SomeTable_Table.name.eq("Default2"),
     SomeTable_Table.phoneNumber.eq("6666666")))
     .executeInsert(db)
   }.execute()
```

## Trigger

Triggers enable SQLite-level listener operations that perform some operation, modification, or action to run when a specific database event occurs. [See](https://www.sqlite.org/lang_createtrigger.html) for more documentation on its usage.

```kotlin
*createTrigger("SomeTrigger")
    .after() insertOn<ConditionModel>())
    .begin(update<TestUpdateModel>()
            .set(TestUpdateModel_Table.value.is("Fired"))))
            .enable(); // enables the trigger if it does not exist, so subsequent calls are OK
```

## Case

The SQLite `CASE` operator is very useful to evaluate a set of conditions and "map" them to a certain value that returns in a SELECT query.

We have two kinds of case: 1. Simple 2. Searched

The simple CASE query in DBFlow:

```kotlin
select(CaseModel_Table.customerId,
        CaseModel_Table.firstName,
        CaseModel_Table.lastName,
        (case(CaseModel_Table.country)
                 whenever "USA"
                 then "Domestic"
                 `else` "Foreign")
                .end("CustomerGroup"))
  from<CaseModel>()
```

The CASE is returned as `CustomerGroup` with the valyes of "Domestic" if the country is from the 'USA' otherwise we mark the value as "Foreign". These appear alongside the results set from the SELECT.

The search CASE is a little more complicated in that each `when()` statement represents a `SQLOperator`, which return a `boolean` expression:

```kotlin
select(CaseModel_Table.customerId,
    CaseModel_Table.firstName,
    CaseModel_Table.lastName,
    caseWhen(CaseModel_Table.country.eq("USA"))
             then "Domestic"
             `else` "Foreign")
     .end("CustomerGroup"))
 from<CaseModel>()
```

# Observability

## Observability

DBFlow provides a flexible way to observe changes on models and tables in this library.

By default, DBFlow utilizes the [`ContentResolver`](https://developer.android.com/reference/android/content/ContentResolver.html) to send changes through the android system. We then can utilize [`ContentObserver`](http://developer.android.com/reference/android/database/ContentObserver.html) to listen for these changes via the `FlowContentObserver`.

Also, DBFlow also supports direct [model notification](observability.md#direct-changes) via a custom `ModelNotifier`.

### FlowContentObserver

The content observer converts each model passed to it into `Uri` format that describes the `Action`, primary keys, and table of the class that changed.

A model:

```kotlin
@Table(database = AppDatabase.class)
class User(@PrimaryKey var id: Int = 0, @Column var name: String = "")
```

with data:

```kotlin
User(55, "Andrew Grosner").delete()
```

converts to:

```text
dbflow://%60User%60?%2560id%2560=55#DELETE
```

Then after we register a `FlowContentObserver`:

```java
FlowContentObserver observer = new FlowContentObserver();

observer.registerForContentChanges(context, User.class);

// do something here
// unregister when done
observer.unregisterForContentChanges(context);
```

### Model Changes

It will now receive the `Uri` for that table. Once we have that, we can register for model changes on that content:

```java
observer.addModelChangeListener(new OnModelStateChangedListener() {
  @Override
  public void onModelStateChanged(@Nullable Class<? extends Model> table, BaseModel.Action action, @NonNull SQLOperator[] primaryKeyValues) {
    // do something here
  }
});
```

The method will return the `Action` which is one of: 1. `SAVE` \(will call `INSERT` or `UPDATE` as well if that operation was used\) 2. `INSERT` 3. `UPDATE` 4. `DELETE`

The `SQLOperator[]` passed back specify the primary column and value pairs that were changed for the model.

If we want to get less granular and just get notifications when generally a table changes, read on.

### Register for Table Changes

Table change events are similar to `OnModelStateChangedListener`, except that they only specify the table and action taken. These get called for any action on a table, including granular model changes. We recommend batching those events together, which we describe in the next section.

```java
addOnTableChangedListener(new OnTableChangedListener() {
    @Override
    public void onTableChanged(@Nullable Class<? extends Model> tableChanged, BaseModel.Action action) {
        // perform an action. May get called many times! Use batch transactions to combine them.
    }
});
```

### Batch Up Many Events

Sometimes we're modifying tens or hundreds of items at the same time and we do not wish to get notified for _every_ one but only once for each _kind_ of change that occurs.

To batch up the notifications so that they fire all at once, we use batch transactions:

```java
FlowContentObserver observer = new FlowContentObserver();

observer.beginTransaction();

// save, modify models here
for(User user: users) {
  users.save();
}

observer.endTransactionAndNotify(); // callback batched
```

Batch interactions will store up all unique `Uri` for each action \(these include `@Primary` key of the `Model` changed\). When `endTransactionAndNotify()` is called, all those `Uri` are called in the `onChange()` method from the `FlowContentObserver` as expected.

If we are using `OnTableChangedListener` callbacks, then by default we will receive one callback per `Action` per table. If we wish to only receive a single callback, set `setNotifyAllUris(false)`, which will make the `Uri` all only specify `CHANGE`.

## Direct Changes

DBFlow also supports direct observability on model changes rather than convert those models into `Uri` and have to decipher what has changed.

To set up direct changes we override the default `ModelNotifier`:

```java
FlowManager.init(FlowConfig.Builder(context)
            .database(DatabaseConfig.Builder(TestDatabase.class)
                .modelNotifier(DirectModelNotifier.get())
                .build()).build());
```

We must use the shared instance of the `DirectModelNotifier` since if we do not, your listeners will not receive callbacks.

Next register for changes on the `DirectModelNotifier`:

```java
DirectModelNotifier.get().registerForModelChanges(User.class, new ModelChangedListener<User>() {
            @Override
            public void onModelChanged(User model, BaseModel.Action action) {
                // react to model changes
            }

            @Override
            public void onTableChanged(BaseModel.Action action) {
              // react to table changes.
            }
        };)
```

Then unregister your model change listener when you don't need it anymore \(to prevent memory leaks\):

```java
DirectModelNotifier.get().unregisterForModelChanges(Userr.class, modelChangedListener);
```

# Main Usage

DBFlow supports a number of database features that will enhance and decrease time you need to spend coding with databases. We support multiple databases at the same time \(and in separate modules\) as long as there's no shared models.

What is covered in these docs are not all inclusive, but should give you an idea of how to operate with DBFlow on databases.

There are a few concepts to familiarize yourself with. We will go more in depth in other sections in this doc.

**SQLite Wrapper Language:** DBFlow provides a number of convenience methods, extensions, and generated helpers that produce a concise, flowable query syntax. A few examples below:

```text
List<User> users = SQLite.select()
  .from(User.class)
  .where(name.is("Andrew Grosner"))
  .queryList();

SQLite.update(User.class)
  .set(name.eq("Andrew Grosner"))
  .where(name.eq("Andy Grosner"))
  .executeUpdateDelete()

FlowManager.getDatabase(AppDatabase.class).beginTransactionAsync((DatabaseWrapper wrapper) -> {
  // wraps in a SQLite transaction, do something on BG thread.
});

CursorResult<User> results = SQLite.select().from(User.class).queryResults();
try {
  for (User user: results) { // memory efficient iterator

  }
} finally {
  results.close()
}
```

Or in Kotlin:

```text
val users = (select from User::class where (name `is` "Andrew Grosner")).list

(update<User>() set (name eq "Andrew Grosner") where (name eq "Andy Grosner")).executeUpdateDelete()

database<AppDatabase>().beginTransactionAsync {

}

(select from User::class).queryResults().use { results ->
  for (user in results) { 

  }
}
```

**Caching:** DBFlow supports caching in models. Caching them greatly increases speed, but cache carefully as it can lead to problems such as stale data.

```text
@Table(cachingEnabled = true)
public class User
```

**Migrations:** Migrations are made very simple in DBFlow. We only support the kinds that [SQLite provide](https://sqlite.org/lang_altertable.html), but also allow you to modify the data within the DB in a structured way during these. They are also run whenever the `SQLiteOpenHelper` detects a version change in the order of version they specify.

**Multiple Modules:** DBFlow can be used in library projects, in any number of inner-project modules simultaneously. However these models must reside in separate databases.

**Relationships:** Not the human kind. We support `@ForeignKey` including multiple foreign keys for 1-1. `@OneToMany` is a manual relationship generated by the compiler between two tables to manage data.`@ManyToMany` generates a join table between two tables for many to many relationships.

**Views:** Declared like tables, Views \(Virtual Tables\) are supported.

**Query Models:** Query models have no SQLite connection, but are extremely useful for custom queries or join queries that return a result set not mappable to any model you currently use for tables.

**Encrypted Databases:** DBFlow supports database encryption for security using SQLCipher through a separate, easy-to-integrate artifact.

**Indexes:** A SQLite feature that drastically improves query performance on large datasets. Dead-easy to implement.

**Reactive:** Easily listen to changes in database data via `ModelNotifier` system.

**Transaction Management:** Place all transactions and retrievals on same background thread for maximum efficiency and to prevent UI-hiccups.

**Type Converters**: Have custom data? Define a `TypeConverter` to map it to SQLite data types.

# TypeConverters

When building out `Model` classes, you may wish to provide a different type of `@Column` that from the standard supported column types. To recap the standard column types include: 1. `String`, `char`, `Character` 2. All numbers types \(primitive + boxed\) 3. `byte[]`/`Byte` 4. `Blob` \(DBFlow's version\) 5. `Date`/`java.sql.Date` 6. Bools 7. `Model` as `@ForeignKey` 8. `Calendar` 9. `BigDecimal` 10. `UUID`

`TypeConverter` do _not_ support: 1. Any Parameterized fields. 2. `List<T>`, `Map<T>`, etc. Best way to fix this is to create a separate table [relationship](relationships.md) 3. Conversion from one type-converter to another \(i.e `JSONObject` to `Date`\). The first parameter of `TypeConverter` is the value of the type as if it was a primitive/boxed type. 4. Conversion from custom type to `Model`, or `Model` to a supported type. 5. The custom class _must_ map to a non-complex field such as `String`, numbers, `char`/`Character` or `Blob`

## Define a TypeConverter

Defining a `TypeConverter` is quick and easy.

This example creates a `TypeConverter` for a field that is `JSONObject` and converts it to a `String` representation:

```java
@com.dbflow5.annotation.TypeConverter
public class JSONConverter extends TypeConverter<String, JSONObject> {

    @Override
    public String getDBValue(JSONObject model) {
        return model == null ? null : model.toString();
    }

    @Override
    public JSONObject getModelValue(String data) {
        JSONObject jsonObject = null;
        try {
            jsonObject = new JSONObject(data);
        } catch (JSONException e) {
          // you should consider logging or throwing exception.
        }
        return jsonObject;
    }
}
```

Once this is defined, by using the annotation `@TypeConverter`, it is registered automatically accross all databases.

There are cases where you wish to provide multiple `TypeConverter` for same kind of field \(i.e. `Date` with different date formats stored in a DB\).

## TypeConverter for specific `@Column`

In DBFlow, specifying a `TypeConverter` for a `@Column` is as easy as `@Column(typeConverter = JSONConverter.class)`. What it will do is create the converter once for use only when that column is used.

# Storing Data

DBFlow provide a few mechanisms by which we store data to the database. The difference of options should not provide confusion but rather allow flexibility in what you decide is the best way to store information.

## Synchronous Storage

While generally saving data synchronous should be avoided, for small amounts of data it has little effect.

```kotlin
model.save()
model.insert()
model.update()
```

Avoid saving large amounts of models outside of a transaction:

```kotlin
// AVOID
models.forEach { it.save() }
```

Doing operations on the main thread can block it if you read and write to the DB on a different thread while accessing DB on the main. Instead, use Async Transactions.

### Async Transactions

## Transactions

Transactions are ACID in SQLite, meaning they either occur completely or not at all. Using transactions significantly speed up the time it takes to store. So recommendation you should use transactions whenever you can.

Async is the preferred method. Transactions, using the `DefaultTransactionManager`, occur on one thread per-database \(to prevent flooding from other DB in your app\) and receive callbacks on the UI. You can override this behavior and roll your own or hook into an existing system, read [here](storingdata.md#custom-transactionmanager).

Also to use the legacy, priority-based system, read [here](storingdata.md#priority-queue).

A basic transaction:

```kotlin
 val transaction = database<AppDatabase>().beginTransactionAsync { db ->
    // handle to DB
    // return a result, or execute a method that returns a result
  }.build()
transaction.execute(
   error = { transaction, error -> // handle any exceptions here },
   completion = { transaction -> // called when transaction completes success or fail }
  ) { transaction, result ->
  // utilize the result returned

transaction.cancel();
 // attempt to cancel before its run. If it's already ran, this call has no effect.
```

The `Success` callback runs post-transaction on the UI thread. The `Error` callback is called on the UI thread if and only if it is specified and an exception occurs, otherwise it is thrown in the `Transaction` as a `RuntimeException`. **Note**: all exceptions are caught when specifying the callback. Ensure you handle all errors, otherwise you might miss some problems.

### ProcessModelTransaction

`ProcessModelTransaction` allows for more flexibility and for you to easily operate on a set of `Model` in a `Transaction` easily. It holds a list of `Model` by which you provide the modification method in the `Builder`. You can listen for when each are processed inside a normal `Transaction`.

It is a convenient way to operate on them:

```kotlin
database.beginTransactionAsync(items.processTransaction { model, db ->
      // call some operation on model here
      model.save()
      model.insert() // or
      model.delete() // or
    }
    .processListener { current, total, modifiedModel ->
        // for every model looped through and completes
        modelProcessedCount.incrementAndGet();
     }
    .build())
    .execute()
```

You can listen to when operations complete for each model via the `OnModelProcessListener`. These callbacks occur on the UI thread. If you wish to run them on same thread \(great for tests\), set `runProcessListenerOnSameThread()` to `true`.

### FastStoreModelTransaction

The `FastStoreModelTransaction` is the quickest, lightest way to store a `List` of `Model` into the database through a `Transaction`. It comes with some restrictions when compared to `ProcessModelTransaction`: 1. All `Model` must be from same Table/Model Class. 2. No progress listening 3. Can only `save`, `insert`, or `update` the whole list entirely.

```kotlin
database.beginTransactionAsync(list.fastSave().build())
  .execute()
database.beginTransactionAsync(list.fastInsert().build())
  .execute()
database.beginTransactionAsync(list.fastUpdate().build())
  .execute()
```

What it provides: 1. Reuses `ContentValues`, `DatabaseStatement`, and other classes where possible. 2. Opens and closes own `DatabaseStatement` per total execution. 3. Significant speed bump over `ProcessModelTransaction` at the expense of flexibility.

### Custom TransactionManager

If you prefer to roll your own thread-management system or have an existing system you can override the default system included.

To begin you must implement a `ITransactionQueue`:

```kotlin
class CustomQueue : ITransactionQueue {
  override fun add(transaction: Transaction<out Any?>) {

  }

  override fun cancel(transaction: Transaction<out Any?>) {

  }

  override fun startIfNotAlive() {
  }

  override fun cancel(name: String) {

  }

  override fun quit() {

  }
}
```

You must provide ways to `add()`, `cancel(Transaction)`, and `startIfNotAlive()`. The other two methods are optional, but recommended.

`startIfNotAlive()` in the `DefaultTransactionQueue` will start itself \(since it's a thread\).

Next you can override the `BaseTransactionManager` \(not required, see later\):

```kotlin
class CustomTransactionManager(databaseDefinition: DBFlowDatabase)
    : BaseTransactionManager(CustomTransactionQueue(), databaseDefinition)
```

To register it with DBFlow, in your `FlowConfig`, you must:

```kotlin
FlowManager.init(FlowConfig.Builder(DemoApp.context)
  .database(DatabaseConfig(
    databaseClass = AppDatabase::class.java,
    transactionManagerCreator = { databaseDefinition ->
        CustomTransactionManager(databaseDefinition)
    })
  .build())
.build())
```

### Priority Queue

In versions pre-3.0, DBFlow utilized a `PriorityBlockingQueue` to manage the asynchronous dispatch of `Transaction`. As of 3.0, it has switched to simply a FIFO queue. To keep the legacy way, a `PriorityTransactionQueue` was created.

As seen in [Custom Transaction Managers](storingdata.md#custom-transactionmanager), we provide a custom instance of the `DefaultTransactionManager` with the `PriorityTransactionQueue` specified:

```kotlin
FlowManager.init(FlowConfig.builder(context)
  .database(DatabaseConfig.Builder(AppDatabase::class.java)
          .transactionManagerCreator { db ->
              // this will be called once database modules are loaded and created.
              DefaultTransactionManager(
                      PriorityTransactionQueue("DBFlow Priority Queue"),
                      db)
          }
          .build())
  .build())
```

What this does is for the specified database \(in this case `AppDatabase`\), now require each `ITransaction` specified for the database should wrap itself around the `PriorityTransactionWrapper`. Otherwise an the `PriorityTransactionQueue` wraps the existing `Transaction` in a `PriorityTransactionWrapper` with normal priority.

To specify a priority, wrap your original `ITransaction` with a `PriorityTransactionWrapper`:

```kotlin
database<AppDatabase>()
    .beginTransactionAsync(PriorityTransactionWrapper.Builder(myTransaction)
        .priority(PriorityTransactionWrapper.PRIORITY_HIGH).build())
    .execute();
```

# Databases

This section describes how databases are created in DBFlow and some more advanced features.

## Creating a Database

In DBFlow, creating a database is as simple as only a few lines of code. DBFlow supports any number of databases, however individual tables and other related files can only be associated with one database. **Note**: Starting with DBFlow 5.0, databases are required to extend `DBFlowDatabase`.

```kotlin
@Database(version = 1)
abstract class AppDatabase : DBFlowDatabase()
```

or in Java:

```java
@Database(version = 1)
public abstract class AppDatabase extends DBFlowDatabase() {
}
```

## Initialization

To specify a custom **name** to the database, in previous versions of DBFlow \(&lt; 4.1.0\), you had to specify it in the `@Database` annotation. As of 5.0 now you pass it in the initialization of the `FlowManager`:

```kotlin
FlowManager.init(FlowConfig.builder()
    .database(DatabaseConfig.builder(AppDatabase::class)
      .databaseName("AppDatabase")
      .build())
    .build())
```

To dynamically change the database name, call:

```kotlin
database<AppDatabase>()
  .reopen(DatabaseConfig.builder(AppDatabase::class)
    .databaseName("AppDatabase-2")
    .build())
```

or in Java:

```java
FlowManager.getDatabase(AppDatabase.class)
  .reopen(DatabaseConfig.builder(AppDatabase.class)
    .databaseName("AppDatabase-2")
    .build())
```

This will close the open DB, reopen the DB, and replace previous `DatabaseConfig` with this new one. Ensure that you persist the changes to the `DatabaseConfig` somewhere as next time app is launched and DBFlow is initialized, the new config would get overwritten.

### In Memory Databases

As with **name**, in previous versions of DBFlow \(&lt; 5.0\), you specified `inMemory` in the `@Database` annotation. Starting with 5.0 that is replaced with:

```kotlin
FlowManager.init(FlowConfig.builder()
    .database(DatabaseConfig.inMemoryBuilder(AppDatabase::class.java)
      .databaseName("AppDatabase")
      .build())
    .build())
```

```java
FlowManager.init(FlowConfig.builder()
    .database(DatabaseConfig.inMemoryBuilder(AppDatabase::class)
      .databaseName("AppDatabase")
      .build())
    .build())
```

This will allow you to use in-memory databases in your tests, while writing to disk in your apps. Also if your device the app is running on is low on memory, you could also swap the DB into memory by calling `reopen(DatabaseConfig)` as explained above.

## Database Migrations

Database migrations are run when upon open of the database connection, the version number increases on an existing database.

It is preferred that `Migration` files go in the same file as the database, for organizational purposes. An example migration:

```kotlin
@Database(version = 2)
abstract class AppDatabase : DBFlowDatabase() {

  @Migration(version = 2, database = MigrationDatabase::class)
  class AddEmailToUserMigration : AlterTableMigration<User>(User::class.java) {

    override fun onPreMigrate() {
        addColumn(SQLiteType.TEXT, "email")
    }
  }
}
```

```java
@Database(version = 2)
public abstract class AppDatabase extends DBFlowDatabase {

  @Migration(version = 2, database = MigrationDatabase.class)
  public static class AddEmailToUserMigration extends AlterTableMigration<User> {

    public AddEmailToUserMigration(Class<User> table) {
        super(table);
    }

    @Override
    public void onPreMigrate() {
        addColumn(SQLiteType.TEXT, "email");
    }
  }
}
```

This simple example adds a column to the `User` table named "email". In code, just add the column to the `Model` class and this migration runs only on existing dbs. To read more on migrations and more examples of different kinds, visit the [page](migrations.md).

## Advanced Database features

This section goes through features that are for more advanced use of a database, and may be very useful.

### Prepackaged Databases

To include a prepackaged database for your application, simply include the ".db" file in `src/main/assets/{databaseName}.db`. On creation of the database, we copy over the file into the application for usage. Since this is prepackaged within the APK, we cannot delete it once it's copied over, which can bulk up your raw APK size. _Note_ this is only copied over on initial creation of the database for the app.

### Global Conflict Handling

In DBFlow when an INSERT or UPDATE are performed, by default, we use `NONE`. If you wish to configure this globally, you can define it to apply for all tables from a given database:

```kotlin
@Database(version = 2, insertConflict = ConflictAction.IGNORE, updateConflict= ConflictAction.REPLACE)
abstract class AppDatabase : DBFlowDatabase()
```

```java
@Database(version = 2, insertConflict = ConflictAction.IGNORE, updateConflict= ConflictAction.REPLACE)
public abstract class AppDatabase extends DBFlowDatabase {
}
```

These follow the SQLite standard [here](https://www.sqlite.org/conflict.html).

### Integrity Checking

Databases can get corrupted or in an invalid state at some point. If you specify `consistencyChecksEnabled=true` It runs a `PRAGMA quick_check(1)` whenever the database is opened. If it fails, you should provide a backup database that it will copy over. If not, **we wipe the internal database**. Note that during this time in case of failure we create a **third copy of the database** in case transfer fails.

### Custom FlowSQLiteOpenHelper

For variety of reasons, you may want to provide your own `FlowSQLiteOpenHelper` to manage database interactions. To do so, you must implement `OpenHelper`, but for convenience you should extend `AndroidSQLiteOpenHelper` \(for Android databases\), or `SQLCipherOpenHelper` for SQLCipher. Read more [here](../advanced-usage/sqlciphersupport.md)

```kotlin
class CustomFlowSQliteOpenHelper(context: Contect, databaseDefinition: DatabaseDefinition, listener: DatabaseHelperListener) : FlowSQLiteOpenHelper(context, databaseDefinition, listener)
```

```java
public class CustomFlowSQliteOpenHelper extends FlowSQLiteOpenHelper {

    public CustomFlowSQliteOpenHelper(Context context, BaseDatabaseDefinition databaseDefinition, @Nullable DatabaseCallback callback) {
        super(context, databaseDefinition, callback);
    }
}
```

Then in your `DatabaseConfig`:

```kotlin
FlowManager.init(FlowConfig.builder(context)
  .database(DatabaseConfig.Builder(CipherDatabase::class.java)
      .openHelper(::CustomFlowSQliteOpenHelper)
      .build())
  .build())
```

```java
FlowManager.init(FlowConfig.builder(context)
  .database(
      DatabaseConfig.builder(CipherDatabase.class)
          .openHelper(new DatabaseConfig.OpenHelperCreator() {
              @Override
              public OpenHelper createHelper(@NonNull DatabaseDefinition databaseDefinition, @Nullable DatabaseCallback callback) {
                  return new CustomFlowSQliteOpenHelper(context, databaseDefinition, callback);
              }
          })
      .build())
  .build());
```

# Views

A `ModelView` is a SQLite representation of a `VIEW`. Read official SQLite docs [here](https://www.sqlite.org/lang_createview.html) for more information.

As with SQLite a `ModelView` cannot insert, update, or delete itself as it's read-only. It is a virtual "view" placed on top of a regular table as a prepackaged `Select` statement. In DBFlow using a `ModelView` should feel familiar and be very simple.

```java
@ModelView(database = TestDatabase.class)
public class TestModelView {

    @ModelViewQuery
    public static final Query QUERY = SQLite.select().from(TestModel2.class)
            .where(TestModel2_Table.model_order.greaterThan(5));

    @Column
    long model_order;
}
```

```kotlin
@ModelView(database = TestDatabase::class)
class TestModelView(@Column modelOrder: Long = 0L) {

  companion object {
    @ModelViewQuery @JvmField
    val query = (select from TestModel2::class where TestModel2_Table.model_order.greaterThan(5))
  }
}
```

To specify the query that a `ModelView` creates itself with, we _must_ define a public static final field annotated with `@ModelViewQuery`. This tells DBFlow what field is the query. This query is used only once when the database is created \(or updated\) to create the view.

The full list of limitations/supported types are: 1. Only `@Column`/`@ColumnMap` are allowed 2. No `@PrimaryKey` or `@ForeignKey` 3. Supports all fields, and accessibility modifiers that `Model` support 4. Does not support `@InheritedField`, `@InheritedPrimaryKey` 5. Basic, type-converted, non-model `@Column`. 6. **Cannot**: update, insert, or delete

`ModelView` are used identical to `Model` when retrieving from the database:

```java
SQLite.select()
  .from(TestModelView.class)
  .where(...) // ETC
```

```kotlin
(select from TestModelView::class where (...))
```

# Migrations

In this section we will discuss how migrations work, how each of the provided migration classes work, and how to create your own custom one.

There are two kinds of migrations that DBFlow supports: Script-based SQL files and class annotation-based migrations.

## How Migrations Work

In SQL databases, migrations are used to modify or change existing database schema to adapt to changing format or nature of stored data. In SQLite we have a limited ability compared to SQL to modify tables and columns of an existing database. There are only two kinds of modifications that exist: rename table and add a new column.

In DBFlow migrations are not only used to modify the _structure_ of the database, but also other operations such as insert data into a database \(for prepopulate\), or add an index on a specific table.

Migrations are only run on an existing database _except_ for the "0th" migration. Read [initial database setup](migrations.md#initial-database-setup)

### Migration Classes

We recommend placing any `Migration` inside an associated `@Database` class so it's apparent the migration is tied to it. An example migration class:

```java
@Database(version = 2)
public class AppDatabase {

    @Migration(version = 2, database = AppDatabase.class)
    public static class Migration2 extends BaseMigration {

        @Override
        public void migrate(DatabaseWrapper database) {
          // run some code here
          SQLite.update(Employee.class)
            .set(Employee_Table.status.eq("Invalid"))
            .where(Employee_Table.job.eq("Laid Off"))
            .execute(database); // required inside a migration to pass the wrapper
        }
    }
}
```

```kotlin
@Database(version = 2)
object AppDatabase {

    @Migration(version = 2, database = AppDatabase.class)
    class Migration2 : BaseMigration() {

        override fun migrate(database: DatabaseWrapper) {
          // run some code here
          (update<Employee>()
            set Employee_Table.status.eq("Invalid")
            where Employee_Table.job.eq("Laid Off"))
            .execute(database) // required to pass wrapper in migration
        }
    }
}
```

The classes provide the ability to set a `priority` on the `Migration` so that an order is established. The higher the priority, that one will execute first.

`Migration` have three methods: 1. `onPreMigrate()` - called first, do setup, and construction here. 2. `migrate()` -&gt; called with the `DatabaseWrapper` specified, this is where the actual migration code should execute. 3. `onPostMigrate()` -&gt; perform some cleanup, or any notifications that it was executed.

### Migration files

DBFlow also supports `.sql` migration files. The rules on these follows must be followed: 1. Place them in `assets/migrations/{DATABASE_NAME}/{versionNumber}.sql`. So that an example `AppDatabase` migration for version 2 resides in `assets/migrations/AppDatabase/2.sql` 2. The file can contain any number of SQL statements - they are executed in order. Each statement must be on a single line or multiline and must end with `;` 3. Comments are allowed as long as they appear on an individual file with standard SQLite comment syntax `--`

### Prevent Recursive Access to the DB

Since `Migration` occur when the database is opening, we cannot recursively access the database object in our models, SQLite wrapper statements, and other classes in DBFlow that are inside a `Migration`.

To remedy that, DBFlow comes with support to pass the `DatabaseWrapper` into almost all places that require it: 1. All query language `BaseQueriable` objects such as `Select`, `Insert`, `Update`, `Delete`, etc have methods that take in the `DatabaseWrapper` 2. Any subclass of `BaseModel` \(`Model` does not provide the methods for simplicity\)

### Initial Database Setup

DBFlow supports `Migration` that run on version "0" of a database. When Android opens a `SQLiteDatabase` object, if the database is created, DBFlow calls on a `Migration` of -1 to 0th version. In this case, any `Migration` run at `version = 0` will get called. Once a database is created, this migration will not run again. So if you had an existent database at version 1, and changed version to 2, the "0th" `Migration` is not run because the old version the database would have been 1.

## Provided Migration Classes

In DBFlow we provide a few helper `Migration` subclasses to provide default and easier implementation: 1. `AlterTableMigration` 2. `IndexMigration/IndexPropertyMigration` 3. `UpdateTableMigration`

### AlterTableMigration

The _structural_ modification of a table is brought to a handy `Migration` subclass.

It performs both of SQLite supported operations: 1. Rename tables 2. Add columns.

For renaming tables, you should rename the `Model` class' `@Table(name = "{newName}")` before running this `Migration`. The reason is that DBFlow will know the new name only and the existing database will get caught up on it through this migration. Any new database created on a device will automatically have the new table name.

For adding columns, we only support `SQLiteType` \(all supported ones [here](https://www.sqlite.org/datatype3.html)\) operations to add or remove columns. This is to enforce that the columns are created properly. If a column needs to be a `TypeConverter` column, use the database value from it. We map the associated type of the database field to a `SQLiteType` in [SQLiteType.kt](https://github.com/agrosner/DBFlow/tree/fb3739caa4c894d50fd0d7873c70a33416c145e6/dbflow/src/main/java/com/dbflow5/sql/SQLiteType.kt). So if you have a `DateConverter` that specifies a `Date` column converted to `Long`, then you should look up `Long` in the `Map`. In this case `Long` converts to `INTEGER`.

```java
@Migration(version = 2, database = AppDatabase.class)
public class Migration2 extends AlterTableMigration<AModel> {

    public Migration2(Class<AModel> table) {
        super(table);
    }

    @Override
    public void onPreMigrate() {
        addColumn(SQLiteType.TEXT, "myColumn");
        addColumn(SQLiteType.REAL, "anotherColumn");
    }
}
```

```kotlin
@Migration(version = 2, database = AppDatabase.class)
class Migration2 : AlterTableMigration<AModel>(AModel::class.java) {

    override fun onPreMigrate() {
        addColumn(SQLiteType.TEXT, "myColumn")
        addColumn(SQLiteType.REAL, "anotherColumn")
    }
}
```

### Index Migrations

An `IndexMigration` \(and `IndexPropertyMigration`\) is used to structurally activate an `Index` on the database at a specific version. See [here](../advanced-usage/indexing.md) for information on creating them.

`IndexMigration` does not require an `IndexProperty` to run, while `IndexPropertyMigration` makes use of the property to run.

An `IndexMigration`:

```java
@Migration(version = 2, priority = 0, database = MigrationDatabase.class)
public static class IndexMigration2 extends IndexMigration<MigrationModel> {

  public IndexMigration2(@NonNull Class<MigrationModel> onTable) {
      super(onTable);
  }

  @NonNull
  @Override
  public String getName() {
      return "TestIndex";
  }
}
```

```kotlin
@Migration(version = 2, priority = 0, database = MigrationDatabase::class)
class IndexMigration2 : IndexMigration<MigrationModel>(MigrationModel::class.java) {

    override fun getName() = "TestIndex"
}
```

An `IndexPropertyMigration`:

```java
@Migration(version = 2, priority = 1, database = MigrationDatabase.class)
public static class IndexPropertyMigration2 extends IndexPropertyMigration {

   @NonNull
   @Override
   public IndexProperty getIndexProperty() {
       return IndexModel_Table.index_customIndex;
   }
}
```

```kotlin
@Migration(version = 2, priority = 1, database = MigrationDatabase.class)
class IndexPropertyMigration2 : IndexPropertyMigration {

   override fun getIndexProperty() = IndexModel_Table.index_customIndex
}
```

### Update Table Migration

A simple wrapper around `Update`, provides simply a default way to update data during a migration.

```java
@Migration(version = 2, priority = 2, database = MigrationDatabase.class)
public static class UpdateMigration2 extends UpdateTableMigration<MigrationModel> {

   /**
    * Creates an update migration.
    *
    * @param table The table to update
    */
   public UpdateMigration2(Class<MigrationModel> table) {
       super(table);
       set(MigrationModel_Table.name.eq("New Name"));
   }

}
```

# Retrieval

DBFlow provides a few ways to retrieve information from the database. Through the `Model` classes we can map this information to easy-to-use objects.

DBFlow provides a few different ways to retrieve information from the database. We can retrieve synchronously or asynchronous \(preferred\).

We can also use `ModelView` \([read here](modelviews.md)\) and `@Index` \([read here](../advanced-usage/indexing.md)\) to perform faster retrieval on a set of data constantly queried.

## Synchronous Retrieval

Using the [SQLite query language](sqlitewrapperlanguage.md) we can retrieve data easily and expressively. To perform it synchronously:

```kotlin
// list
val employees = (select from Employee:class).list

// single result, we apply a limit(1) automatically to get the result even faster.
val employee: Employee? = (select from Employee::class
                        where Employee_Table.name.eq("Andrew Grosner")).result

// can require result to get non-null if you know it exists
// throws a SQLiteException if missing
val employee: Employee? = (select from Employee::class
                        where Employee_Table.name.eq("Andrew Grosner")).requireResult

// get a custom list
val employees = (select from Employee::class)
                .customList<AnotherTable>(database)

// custom object
val anotherObject = (select from Employee::class
                        where(Employee_Table.name.eq("Andrew Grosner")))
                        .customSingle<AnotherTable>();
```

To query custom objects or lists, see how to do so in [QueryModel](../advanced-usage/querymodels.md).

Also you can query a `FlowCursorList`/`FlowTableList` from a query easily via `queryCursorList()` and the `queryTableList()` methods. To see more on these, go to [Flow Lists](../advanced-usage/listbasedqueries.md).

## Asynchronous Retrieval

DBFlow provides the very-handy `Transaction` system that allows you to place all calls to the DB in a background queue. Using this system, we recommend placing retrieval queries on this queue to help prevent locking and threading issues when using a database.

We wrap our queries in a `beginTransactionAsync` block, executing and providing call backs to the method as follows:

```java
database.beginTransactionAsync { db ->
  (select from TestModel1::class
    where TestModel1_Table.name.is("Async")).querySingle(db)
  }
    .execute(
     success = { transaction, r ->   }, // if successful
     error  = { transaction, throwable ->  }, // any exception thrown is put here
     completion = { transaction -> }) // always called success or failure
```

A `ITransaction<R>` simply returns a result, `R` , which could be a query, or a result from multiple queries combined into one result.

By default the library uses an ordered queue that executes FIFO \(first-in-first-out\) and blocks itself until new `Transaction` are added. Each subsequent call to the `database.beginTransactionAsync` places a new transaction on this queue.

If you wish to customize and provide a different queue \(or map it to an existing system\), read up on [Transactions](storingdata.md). We also provide constructs such as coroutines and RX `Observables` to map to your team's needs.

# Relationships

We can link `@Table` in DBFlow via 1-1, 1-many, or many-to-many. For 1-1 we use `@PrimaryKey`, for 1-many we use `@OneToMany`, and for many-to-many we use the `@ManyToMany` annotation.

## One To One

DBFlow supports multiple `@ForeignKey` right out of the box as well \(and for the most part, they can also be `@PrimaryKey`\).

```kotlin
@Table(database = AppDatabase::class)
class Dog(@PrimaryKey var name: String,
          @ForeignKey(tableClass = Breed::class)
          @PrimaryKey var breed: String,
          @ForeignKey var owner: Owner? = null)
```

`@ForeignKey` can only be a subset of types: 1. `Model` 2. Any field not requiring a `TypeConverter`. If not a `Model` or a table class, you _must_ specify the `tableClass` it points to. 3. Cannot inherit `@ForeignKey` from non-model classes \(see [Inherited Columns](models.md#inherited-columns)\)

If you create a circular reference \(i.e. two tables with strong references to `Model` as `@ForeignKey` to each other\), read on.

## Stubbed Relationships

For efficiency reasons we recommend specifying `@ForeignKey(stubbedRelationship = true)`. What this will do is only _preset_ the primary key references into a table object.

All other fields will not be set. If you need to access the full object, you will have to call `load()` for `Model`, or use the `ModelAdapter` to load the object from the DB.

From our previous example of `Dog`, instead of using a `String` field for **breed** we recommended by using a `Breed`. It is nearly identical, but the difference being we would then only need to call `load()` on the reference and it would query the `Breed` table for a row with the `breed` id. This also makes it easier if the table you reference has multiple primary keys, since DBFlow will handle the work for you.

Multiple calls to `load()` will query the DB every time, so call when needed. Also if you don't specify `@Database(foreignKeyConstraintsEnforced = true)`, calling `load()` may not have any effect. Essentially without enforcing `@ForeignKey` at a SQLite level, you can end up with floating key references that do not exist in the referenced table.

In normal circumstances, for every load of a `Dog` object from the database, we would also do a load of related `Owner`. This means that even if multiple `Dog` say \(50\) all point to same owner we end up doing 2x retrievals for every load of `Dog`. Replacing that model field of `Owner` with a stubbed relationship prevents the extra N lookup time, leading to much faster loads of `Dog`.

**Note**: using stubbed relationships also helps to prevent circular references that can get you in a `StackOverFlowError` if two tables strongly reference each other in `@ForeignKey`.

Our modified example now looks like this:

```kotlin
@Table(database = AppDatabase::class)
class Dog(@PrimaryKey var name: String,
          @ForeignKey(stubbedRelationship = true)
          @PrimaryKey var breed: Breed? = null,
          @ForeignKey(stubbedRelationship = true)
          var owner: Owner? = null)
```

## One To Many

In DBFlow, `@OneToMany` is an annotation that you provide to a method in your `Model` class that will allow management of those objects during CRUD operations. This can allow you to combine a relationship of objects to a single `Model` to happen together on load, save, insert, update, and deletion.

```kotlin
@Table(database = ColonyDatabase::class)
class Queen(@PrimaryKey(autoincrement = true)
            var id: Long = 0,
            var name: String? = null,
            @ForeignKey(saveForeignKeyModel = false)
            var colony: Colony? = null) : BaseModel() {

    @get:OneToMany
    val ants: List<Ant>? by oneToMany { select from Ant::class where Ant_Table.queen_id.eq(id) }

}
```

### Efficient Methods

When using `@ManyToMany`, by default we skip the `Model` methods in each retrieved `Ant` \(in this example\). If you have nested `@ManyToMany` \(which should strongly be avoided\), you can turn off the efficient operations. Call `@OneToMany(efficientMethods = false)` and it will instead loop through each model and perform `save()`, `delete()`, etc when the parent model is called.

### Custom ForeignKeyReferences

When simple `@ForeignKey` annotation is not enough, you can manually specify references for your table:

```kotlin
@ForeignKey(saveForeignKeyModel = false,
references = {ForeignKeyReference(columnName = "colony", foreignKeyColumnName = "id")})
var colony: Colony? = null;
```

By default not specifying references will take each field and append "${foreignKeyFieldName}\_${ForeignKeyReferenceColumnName}" to make the reference column name. So by default the previous example would use `colony_id` without references. With references it becomes `colony`.

## Many To Many

In DBFlow many to many is done via source-gen. A simple table:

```kotlin
@Table(database = AppDatabase::class)
@ManyToMany(referencedTable = Follower::class)
class User(@PrimaryKey var id: Int = 0, @PrimaryKey var name: String = "")
```

Generates a `@Table` class named `User_Follower`, which DBFlow treats as if you coded the class yourself!:

```java
@Table(
    database = TestDatabase.class
)
public final class User_Follower extends BaseModel {
  @PrimaryKey(
      autoincrement = true
  )
  long _id;

  @ForeignKey(
      saveForeignKeyModel = false
  )
  Follower follower;

  @ForeignKey(
      saveForeignKeyModel = false
  )
  User user;

  public final long getId() {
    return _id;
  }

  public final Followers getFollower() {
    return follower;
  }

  public final void setFollower(Follower param) {
    follower = param;
  }

  public final Users getUser() {
    return user;
  }

  public final void setUser(User param) {
    user = param;
  }
}
```

This annotation makes it very easy to generate "join" tables for you to use in the app for a ManyToMany relationship. It only generates the table you need. To use it you must reference it in code as normal.

_Note_: This annotation is only a helper to generate tables that otherwise you would have to write yourself. It is expected that management still is done by you, the developer.

### Custom Column Names

You can change the name of the columns that are generated. By default they are simply lower case first letter version of the table name.

`referencedTableColumnName` -&gt; Refers to the referenced table. `thisTableColumnName` -&gt; Refers to the table that is creating the reference.

### Multiple ManyToMany

You can also specify `@MultipleManyToMany` which enables you to define more than a single `@ManyToMany` relationship on the table.

A class can use both:

```kotlin
@Table(database = TestDatabase::class)
@ManyToMany(referencedTable = TestModel1::class)
@MultipleManyToMany({@ManyToMany(referencedTable = TestModel2::class),
    @ManyToMany(referencedTable = TestModel3::class)})
class ManyToManyModel(
  @PrimaryKey var name: String = "",
  @PrimaryKey var id: Int = 0,
  @PrimaryKey var anotherColumn: Char? = null)
```

# Models

In DBFlow we dont have any restrictions on what your table class is. We do, however if you use Java, we recommend you subclass `BaseModel` on your highest-order base-class, which provides a default implementation for you. Otherwise utilize a kotlin extension method on `Any`.

```kotlin
myTableObject.save()
```

## Columns

By default, DBFlow inclusdes all properties as columns. For other kinds of fields, they must contain either `@PrimaryKey` or `@ForeignKey` to be used in tables. However this still requires you to specify at least one `@PrimaryKey` field. You can then explicitly ignore fields via the `@ColumnIgnore` annotation if necessary. You can turn off all fields and make it explicit using `@Table(allFields = false)`

In Kotlin, Column properties must be public and `var` for now. In future versions, we hope to support Kotlin constructors without default arguments. For now, all must be `var` and provide a default constructor. We respect nullability of the properties and won't assign `null` to them if they're not nullable.

In Java, Columns can be `public`, package-private, or `private`. `private` fields **must** come with `public` java-bean-style getters and setters. Package private used in other packages generate a `_Helper` class which exposes a method to call these fields in an accessible way. This has some overhead, so consider making them with `public` get/set or public.

Here is an example of a "nice" `Table`:

```kotlin
@Table(database = AppDatabase.class)
public class Dog(@PrimaryKey var id: Int = 0, var name: String? = null)
```

Columns have a wide-range of supported types in the `Model` classes: **Supported Types**:

   1. all primitives including `Char`,`Byte`, `Short`, and `Boolean`.
   2. All Kotlin nullable primitives (java boxed).
   3. String, Date, java.sql.Date, Calendar, Blob, Boolean
   4. Custom data types via a [TypeConverter](typeconverters.md)
   5. `Model` as fields, but only as `@PrimaryKey` and/or `@ForeignKey`
   6. `@ColumnMap` objects that flatten an object into the current table. Just like a `@ForeignKey`, but without requiring a separate table. \(4.1.0+\). Avoid nesting more than one object, as the column count could get out of control.

**Unsupported Types**:

  1. `List<T>` : List columns are not supported and not generally proper for a relational database. However, you can get away with a non-generic `List` column via a `TypeConverter`. But again, avoid this if you can.
  2. Anything that is generically typed \(even with an associated `TypeConverter`\). If you need to include the field, subclass the generic object and provide a `TypeConverter`.

## Inherited Columns

Since we don't require extension on `BaseModel` directly, tables can extend non-model classes and inherit their fields directly \(given proper accessibility\) via the `@InheritedColumn` annotation \(or `@InheritedPrimaryKey` for primary keys\):

```java
@Table(database = AppDatabase.class,
        inheritedColumns = {@InheritedColumn(column = @Column, fieldName = "name"),
                @InheritedColumn(column = @Column, fieldName = "number")},
        inheritedPrimaryKeys = {@InheritedPrimaryKey(column = @Column,
                primaryKey = @PrimaryKey,
                fieldName = "inherited_primary_key")})
public class InheritorModel extends InheritedModel implements Model {
```

Generally, this should be avoided and if you control the source, just place your model objects / db objects in same module as a `db` module.

## Primary Keys

DBFlow supports multiple primary keys, right out of the box. Simply create a table with multiple `@PrimaryKey`:

```kotlin
@Table(database = AppDatabase::class)
class Dog(@PrimaryKey var name: String = "", @PrimaryKey var breed: String = "")
```

If we want an auto-incrementing key, you specify `@PrimaryKey(autoincrement = true)`, but only one of these kind can exist in a table and you cannot mix with regular primary keys.

## Unique Columns

DBFlow has support for SQLite `UNIQUE` constraint \(here for documentation\)\[[http://www.tutorialspoint.com/sqlite/sqlite\_constraints.htm](http://www.tutorialspoint.com/sqlite/sqlite_constraints.htm)\].

Add `@Unique` annotation to your existing `@Column` and DBFlow adds it as a constraint when the database table is first created. This means that once it is created you should not change or modify this.

We can _also_ support multiple unique clauses in order to ensure any combination of fields are unique. For example:

To generate this in the creation query:

```text
UNIQUE('name', 'number') ON CONFLICT FAIL, UNIQUE('name', 'address') ON CONFLICT ROLLBACK
```

We declare the annotations as such:

```kotlin
@Table(database = AppDatabase::class,
  uniqueColumnGroups = {@UniqueGroup(groupNumber = 1, uniqueConflict = ConflictAction.FAIL),
                        @UniqueGroup(groupNumber = 2, uniqueConflict = ConflictAction.ROLLBACK))
class UniqueModel(
  @PrimaryKey @Unique(unique = false, uniqueGroups = {1,2})
  var name: String = "",
  @Column @Unique(unique = false, uniqueGroups = 1)
  var number: String = "",
  @Column @Unique(unique = false, uniqueGroups = 2)
  var address: String = "")
```

The `groupNumber` within each defined `uniqueColumnGroups` with an associated `@Unique` column. We need to specify `unique=false` for any column used in a group so we expect the column to be part of a group. If true as well, the column will _also_ alone be unique.

## Default Values
**Not to be confused with Kotlin default values** This only applies when fields are marked as `nullable`. When fields are non null in kotlin, we utilize the default constructor value when it is set, so when the column data is `null` from a `Cursor`, we do not override the initial assignment.

DBFlow supports default values in a slighty different way that SQLite does. Since we do not know exactly the intention of missing data when saving a `Model`, since we group all fields, `defaultValue` specifies a value that we replace when saving to the database when the value of the field is `null`.

This feature only works on Boxed primitive and the `DataClass` equivalent of objects \(such as from TypeConverter\), such as String, Integer, Long, Double, etc. **Note**: If the `DataClass` is a `Blob`, unfortunately this will not work. For `Boolean` classes, use "1" for true, "0" for false.

```java
@Column(defaultValue = "55")
Integer count;

@Column(defaultValue = "\"this is\"")
String test;

@Column(defaultValue = "1000L")
Date date;

@Column(defaultValue = "1")
Boolean aBoolean;
```

DBFlow inserts it's literal value into the `ModelAdapter` for the table so any `String` must be escaped.
# SQLCipher

As of 3.0.0-beta2+, DBFlow now supports [SQLCipher](https://www.zetetic.net/sqlcipher/) fairly easily.

To add the library add the library to your `build.gradle` with same version you are using with the rest of the library.

```groovy
dependencies {
  implementation "com.dbflow5:sqlcipher:${version}"
  implementation "net.zetetic:android-database-sqlcipher:${sqlcipher_version}@aar"
}
```

You also need to add the Proguard rule:

```text
-keep class net.sqlcipher.** { *; }
-dontwarn net.sqlcipher.**
```

Next, you need to subclass the provided `SQLCipherOpenHelper` \(taken from test files\):

```kotlin
class SQLCipherOpenHelperImpl(context: Context,
                              databaseDefinition: DBFlowDatabase,
                              callback: DatabaseCallback?)
    : SQLCipherOpenHelper(context, databaseDefinition, callback) {
    override val cipherSecret get() = "dbflow-rules"
}
```

_Note:_ that the constructor with `DatabaseDefinition` and `DatabaseHelperListener` is required.

Then in your application class when initializing DBFlow:

```kotlin
FlowManager.init(FlowConfig.Builder(this)
  .database(
      DatabaseConfig.Builder(CipherDatabase::class) { db, callback -> SQLCipherHelperImpl(databaseDefinition, callback))
      .build())
  .build())
```

And that's it. You're all set to start using SQLCipher!

# Advanced Usage

This section details the more advanced usages of DBFlow.

# QueryModels

A `QueryModel` is purely an ORM object that maps rows from a `Cursor` into a `Model` such that when loading from the DB, we can easily use the data from it.

We use a different annotation, `@QueryModel`, to define it separately. These do not allow for modifications in the DB, rather act as a marshal agent out of the DB.

## Define a QueryModel

For this example, we have a list of employees that we want to gather the average salary for each position in each department from our company.

We defined an `Employee` table:

```java
@Table(database = AppDatabase.class)
public class EmployeeModel {

    @PrimaryKey
    String uid;

    @Column
    long salary;

    @Column
    String name;

    @Column
    String title;

    @Column
    String department;
}
```

We need someway to retrieve the results of this query, since we want to avoid dealing with the `Cursor` directly. We can use a SQLite query with our existing models, but we have no way to map it currently to our tables, since the query returns new Columns that do not represent any existing table:

```java
SQLite.select(EmployeeModel_Table.department,
                Method.avg(EmployeeModel_Table.salary.as("average_salary")),
                EmployeeModel_Table.title)
      .from(EmployeeModel.class)
      .groupBy(EmployeeModel_Table.department, EmployeeModel_Table.title);
```

So we must define a `QueryModel`, representing the results of the query:

```java
@QueryModel(database = AppDatabase.class)
public class AverageSalary {

    @Column
    String title;

    @Column
    long average_salary;

    @Column
    String department;
}
```

And adjust our query to handle the new output:

```java
SQLite.select(EmployeeModel_Table.department,
                Method.avg(EmployeeModel_Table.salary.as("average_salary")),
                EmployeeModel_Table.title)
      .from(EmployeeModel.class)
      .groupBy(EmployeeModel_Table.department, EmployeeModel_Table.title)
      .async()
      .queryResultCallback(new QueryTransaction.QueryResultCallback<EmployeeModel>() {
          @Override
          public void onQueryResult(QueryTransaction transaction, @NonNull CursorResult<EmployeeModel> tResult) {
              List<AverageSalary> queryModels = tResult.toCustomListClose(AverageSalary.class);

            // do something with the result
          }
      }).execute();
```

## Query Model Support

`QueryModel` support only a limited subset of `Model` features.

If you use the optional base class of `BaseQueryModel`, Modifications such as `insert()`, `update()`, `save()`, and `delete()` will throw an `InvalidSqlViewOperationException`. Otherwise, `RetrievalAdapter` do not contain modification methods.

They support `allFields` and inheritance and visibility modifiers as defined by [Models](../usage/models.md).

`QueryModel` **do not** support: 1. `InheritedField`/`InheritedPrimaryKey` 2. `@PrimaryKey`/`@ForeignKey` 3. caching 4. changing "useBooleanGetterSetters" for private boolean fields.

# ListBasedQueries

When we have large datasets from the database in our application, we wish to display them in a `ListView`, `RecyclerView` or some other component that recycles it's views. Instead of running a potentially very large query on the database, converting it to a `List` and then keeping that chunk of memory active, we can lazy-load each row from the query/table.

DBFlow makes it easy using the `FlowCursorList`, for simple `BaseAdapter`-like methods, or the `FlowQueryList`, which implements the `List` interface.

Getting one of these lists is as simple as:

```java
FlowQueryList<MyTable> list = SQLite.select()
    .from(MyTable.class)
    .where(...) // some conditions
    .flowQueryList();
FlowCursorList<MyTable> list = SQLite.select()
    .from(MyTable.class)
    .where(...) // some conditions
    .cursorList();

    list.close(); // ensure you close these, as they utilize active cursors :)
```

```kotlin
val list = (select from MyTable::class where (...)).cursorList
val list = (select from MyTable::class where (...)).flowQueryList
list.close()
```

Any query method allows you to retrieve a default implementation of each. You can also manually instantiate them:

```java
FlowQueryList<MyTable> list = new FlowQueryList.Builder<>(SQLite.select().from(MyTable.class))
  .cachingEnabled(false) // caching enabled by default
  .build();

FlowCursorList<MyTable> list = new FlowCursorList.Builder<>(SQLite.select().from(MyTable.class))
  .cachingEnabled(true)
  .modelCache(cache) // provide custom cache for this list
  .build();
```

## Caching

Both of these classes come with the ability to cache `Model` used in it's queries so that loading only happens once and performance can remain high once loaded. The default caching mechanism is a `ModelLruCache`, which provides an `LruCache` to manage loading `Model`.

They are done in almost the same way:

```java
FlowCursorList<MyTable> list = new FlowCursorList.Builder<>(SQLite.select().from(MyTable.class))
  .modelCache(cache) // provide custom cache for this list
  .build();
FlowQueryList<MyTable> list = new FlowQueryList.Builder<>(SQLite.select().from(MyTable.class))
  .modelCache(cache)
  .build();
```

## FlowCursorList

The `FlowCursorList` is simply a wrapper around a standard `Cursor`, giving it the ability to cache `Model`, load items at specific position with conversion, and refresh it's content easily.

The `FlowCursorList` by default caches its results, for fast usage. The cache size is determined by the `ModelCache` you're using. Read on [here](caching.md).

The `FlowCursorList` provides these methods:

1. `getItem(position)` - loads item from `Cursor` at specified position, caching and loading from cache \(if enabled\)
2. `refresh()` - re-queries the underlying `Cursor`, clears out the cache, and reconstructs it. Use a `OnCursorRefreshListener` to get callbacks when this occurs.
3. `getAll()` - returns a `List` of all items from the `Cursor`, no caching used
4. `getCount()` - returns count of `Cursor` or 0 if `Cursor` is `null`
5. `isEmpty()` - returns if count == 0
6. `clearCache()` - manually clears cache

## Flow Query List

This class is a much more powerful version of the `FlowCursorList`. It contains a `FlowCursorList`, which backs it's retrieval operations.

This class acts as `List` and can be used almost wherever a `List` is used. Also, it is a `FlowContentObserver` see [Observability](../usage/observability.md), meaning other classes can listen for its specific changes and it can auto-refresh itself when content changes.

Feature rundown: 1. `List` implementation of a Query 2. `FlowContentObserver`, only for the table that it corresponds to in its initial `ModelQueriable` query statement. Mostly used for self refreshes. 3. Transact changes to the query asynchronously \(note that this refreshes itself every callback unless in a transaction state\) 5. Caching \(almost same implementation as `FlowCursorList`\)

### List Implementation

The `List` implementation is mostly for convenience. Please note that most of the modification methods \(`add`, `addAll` etc.\) may not affect the query that you expect it to, unless the object you pass objects that are valid for the query and you enable self refreshes.

The retrieval methods are where the query works as you would expect. `get()` calls `getItem()` on the internal `FlowCursorList`, `isEmpty()`, `getCount()`, etc all correspond to the `Cursor` underneath.

Both `FlowQueryList` and `FlowTableList` support `Iterator` and provide a very efficient class: `FlowCursorIterator` that iterates through each row in a `Cursor` and provides efficient operations.

**Note**: any retrieval operation that turns it into another object \(i.e. `subList()`, `toArray`, etc\) retrieves all objects contained in the query into memory, and then converts it using the associated method on that returned `List`.

### FlowContentObserver Implementation

Using the `FlowContentObserver`, we can enable self-refreshes whenever a model changes for the table this query points to. See [Observability](../usage/observability.md).

To turn on self-refreshes, call `registerForContentChanges(context)`, which requeries the data whenever it changes.

We recommend placing this within a transaction on the `FlowQueryList`, so we only refresh content the minimal amount of times:

```java
flowQueryList.beginTransaction();

// perform a bunch of modifications

flowQueryList.endTransactionAndNotify();
```

To listen for `Cursor` refreshes register a `OnCursorRefreshListener`:

```java
modelList
  .addOnCursorRefreshListener(new FlowCursorList.OnCursorRefreshListener<ListModel>() {
      @Override
      public void onCursorRefreshed(FlowCursorList<ListModel> cursorList) {

      }
  });
```

### Transact Changes Asynchronously

If you want to pass or modify the `FlowQueryList` asynchronously, set `setTransact(true)`. This will run all modifications in a `Transaction` and when completed, a `Cursor` refresh occurs.

You can also register `Transaction.Error` and `Transaction.Success` callbacks for these modifications on the `FlowQueryList` to handle when these `Transaction` finish.

# MultipleModules

In apps that want to share DBFlow across multiple modules or when developing a library module that uses DBFlow, we have to provide a little extra configuration to properly ensure that all database classes are accounted for.

It's directly related to the fact that annotation processors are isolated between projects and are not shared.

In order to add support for multiple modules, in each and every library/subproject that uses a DBFlow instance, you must add an APT argument \(using the [android-apt plugin](https://bitbucket.org/hvisser/android-apt)\) to its `build.gradle`:

```java
apt {
    arguments {
        targetModuleName 'SomeUniqueModuleName'
    }
}
```

or for if you use Kotlin, KAPT:

```java
kapt {
    generateStubs = true
    arguments {
        arg("targetModuleName", "SomeUniqueModuleName")
    }
}
```

By passing the targetModuleName, we append that to the `GeneratedDatabaseHolder` class name to create the `{targetModuleName}GeneratedDatabaseHolder` module. **Note**: Specifying this in code means you need to specify the module when initializing DBFlow:

From previous sample code, we recommend initializing the specific module inside your library, to prevent developer error. **Note**: Multiple calls to `FlowManager` will not adversely affect DBFlow. If DBFlow is already initialized, we append the module to DBFlow if and only if it does not already exist.

```java
public void initialize(Context context) {
  FlowManager.init(FlowConfig.builder(context)
    .addDatabaseHolder(SomeUniqueModuleNameGeneratedDatabaseHolder.class)
    .build());
}
```

# Indexing

In SQLite, an `Index` is a pointer to specific columns in a table that enable super-fast retrieval.

**Note**: The database size can increase significantly, however if performance is more important, the tradeoff is worth it.

Indexes are defined using the `indexGroups()` property of the `@Table` annotation. These operate similar to how `UniqueGroup` work: 1. specify an `@IndexGroup` 2. Add the `@Index` 3. Build and an `IndexProperty` gets generated. This allows super-easy access to the index so you can enable/disable it with ease.

**Note**: `Index` are not explicitly enabled unless coupled with an `IndexMigration`. \([read here](../usage/migrations.md#index-migrations)\).

You can define as many `@IndexGroup` you want within a `@Table` as long as one field references the group. Also individual `@Column` can belong to any number of groups:

```java
@Table(database = TestDatabase.class,
       indexGroups = [
               @IndexGroup(number = 1, name = "firstIndex"),
               @IndexGroup(number = 2, name = "secondIndex"),
               @IndexGroup(number = 3, name = "thirdIndex")
       ])
public class IndexModel2 {

   @Index(indexGroups = {1, 2, 3})
   @PrimaryKey
   int id;

   @Index(indexGroups = 1)
   @Column
   String first_name;

   @Index(indexGroups = 2)
   @Column
   String last_name;

   @Index(indexGroups = {1, 3})
   @Column
   Date created_date;

   @Index(indexGroups = {2, 3})
   @Column
   boolean isPro;
}
```

By defining the index this way, we generate an `IndexProperty`, which makes it very easy to enable, disable, and use it within queries:

```java
IndexModel2_Table.firstIndex.createIfNotExists();

SQLite.select()
  .from(IndexModel2.class)
  .indexedBy(IndexModel2_Table.firstIndex)
  .where(...); // do a query here.

IndexModel2_Table.firstIndex.drop(); // turn it off when no longer needed.
```

```kotlin
IndexModel2_Table.firstIndex.createIfNotExists()

(select from IndexModel2::class indexedBy IndexModel2_Table.firstIndex where (...))

IndexModel2_Table.firstIndex.drop() // turn it off when no longer needed.
```

## SQLite Index Wrapper

For flexibility, we also support the SQLite `Index` wrapper object, in which the `IndexProperty` uses underneath.

```java
Index<SomeTable> index = SQLite.index("MyIndex")
    .on(SomeTable.class, SomeTable_Table.name, SomeTable_Table.othercolumn);
index.enable();

// do some operations

index.disable(); // disable when no longer needed
```

```kotlin
val index = indexOn<SomeTable>("MyIndex", SomeTable_Table.name, SomeTable_Table.othercolumn)
index.enable()

index.disable()
```

# Caching

DBFlow provides powerful caching mechanisms to speed up retrieval from the database to enable high performance in our applications.

Caching is not enabled by default, but it is very easy to enable.

## When to Use Caching

1. retrieve the near-same list of objects from the DB when data does not change frequently.
2. Need to load large, full objects from the DB repeatedly in different places in the app.

## When Not To Use Caching

Do not use caching when: 1. you need a subset of columns from the DB. i.e. \(`select(name, age, firstName)`\) 2. The data is expected to change frequently as any operation on the DB we do that is not tied to model instances will invalidate our cache anyways. 3. You load data from `@OneToMany`, or have nested `@OneToMany` fields within inner objects.

**Note**: DBFlow is fast and efficient. Caching may not be required at all, except in very particular use-cases. Do not abuse. You can call `disableCaching()` on a query to ensure it's a fresh dataset.

## How Caching Works

Caching under the hood is done by storing an instance of each `Model` returned from a query on a specific table into memory. 1. Developer enables caching on Table A 2. Query from Table A 3. When receiving the `Cursor`, we read the primary key values from it and look them up from `ModelCache`. If the `Model` exists, return it from cache; otherwise create new instance, read in values, and store in cache. 4. That instance remains in memory such on next query, we return that instance instead of recreating one from a `Cursor`. 5. When we call `ModelAdapter.save()`, `insert()`, `update()`, or `delete()`, we update model in the cache so that on next retrieval, the model with proper values is returned. 6. When wrapper operations are performed on tables with caching, caches are not modified. When doing such a call, please call `TableA_Table.cacheAdapter.clearCache()`

### Supported Backing Objects

Caching is supported under the hood for: 1. `SparseArray` via `SparseArrayBasedCache` \(platform SparseArray\) 2. `Map` via `SimpleMapCache` 3. `LruCache` via `ModelLruCache` \(copy of `LruCache`, so dependency avoided\) 4. Custom Caching classes that implement `ModelCache`

Cache sizes are not supported for `SimpleMapCache`. This is because `Map` can hold arbitrary size of contents.

### Enable Caching

To enable caching on a single-primary key table, simply specify that it is enabled:

```kotlin
@Table(database = AppDatabase.class, cachingEnabled = true)
class CacheableModel {

    @PrimaryKey(autoincrement = true)
    var id: Long = 0L

    @Column
    var name: String? = null
}
```

or in Java:

```java
@Table(database = AppDatabase.class, cachingEnabled = true)
public class CacheableModel {

    @PrimaryKey(autoincrement = true)
    long id;

    @Column
    String name;
}
```

to use caching on a table that uses multiple primary keys, [see](caching.md#multiple-primary-key-caching).

By default we use a `SimpleMapCache`, which loads `Model` into a `Map`. The key is either the primary key of the object or a combination of the two, but it should have an associated `HashCode` and `equals()` value.

## Modifying Cache Objects

Any time a field on these objects are modified, you _should_ immediately save those since we have a direct reference to the object from the cache. Otherwise, the DB and cache could get into an inconsistent state.

```kotlin
database<AppDatabase> {
  (select from MyModel::class where (...)).result?.let { result ->
    result.name = "Name"
    result.save()
  }
}
```

```java
MyModel model = SQLite.select(db).from(MyModel.class).where(...).querySingle();
model.setName("Name");
model.save(); // save it to DB post any modifications to this object.
```

## Disable Caching For Some Queries

To disable caching on certain queries as you might want to project on only a few columns, rather than the full dataset. Just call `disableCaching()`:

```kotlin
database<AppDatabase> {
  select(My_Table.column, My_Table.column2)
    .from(My::class)
    .disableCaching()
    .list
}
```

or in Java:

```java
select(db, My_Table.column, My_Table.column2)
  .from(My.class)
  .disableCaching()
  .queryList();
```

## Advanced

### Specifying cache Size

To specify cache size, set `@Table(cacheSize = {size})`. Please note that not all caches support sizing. It's up to each cache.

### Custom Caches

To specify a custom cache for a table, please define a `@JvmField` field:

```kotlin
companion object {

  @JvmField @ModelCacheField
  val modelCache = SimpleMapCache<CacheableModel3, Any>()
}
```

or in Java using `public static final`:

```java
@ModelCacheField
public static ModelCache<CacheableModel3, ?> modelCache = new SimpleMapCache<>(); // replace with any cache you want.
```

### Multiple Primary Key Caching

This allows for tables that have multiple primary keys be used in caching. To use, add a `@MultiCacheField` `@JvmField` field. for example we have a `Coordinate` class:

```kotlin
@Table(database = AppDatabase.class, cachingEnabled = true)
class Coordinate(@PrimaryKey latitude: Double = 0.0,
                 @PrimaryKey longitude: Double = 0.0) {

    companion object {
      @JvmField
      @MultiCacheField
      val cacheConverter = IMultiKeyCacheConverter { values -> "${values[0]},${values[1]}" }
    }
}
```

or in Java:

```java
@Table(database = AppDatabase.class, cachingEnabled = true)
public class Coordinate {

    @MultiCacheField
    public static final IMultiKeyCacheConverter<String> multiKeyCacheModel = new IMultiKeyCacheConverter<String>() {

        @Override
        @NonNull
        public String getCachingKey(@NonNull Object[] values) {
            return "(" + values[0] + "," + values[1] + ")";
        }
    };

    @PrimaryKey
    double latitude;

    @PrimaryKey
    double longitude;
```

In this case we use the `IMultiKeyCacheConverter` class, which specifies a key type that the object returns. The `getCachingKey` method returns an ordered set of `@PrimaryKey` columns in declaration order. Also the value that is returned should have an `equals()` or `hashcode()` specified \(use a `data class`\) especially when used in the `SimpleMapCache`.

