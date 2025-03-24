Android testing samples
===================================

A collection of samples demonstrating different frameworks and techniques for automated testing.

### Espresso Samples

**[BasicSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/BasicSample)** - Basic Espresso sample

**[CustomMatcherSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/CustomMatcherSample)** - Shows how to extend Espresso to match the *hint* property of an EditText

**[DataAdapterSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/DataAdapterSample)** - Showcases the `onData()` entry point for Espresso, for lists and AdapterViews

**[FragmentScenarioSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/FragmentScenarioSample)** - Basic usage of `FragmentScenario` with Espresso. 

**[IdlingResourceSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/IdlingResourceSample)** - Synchronization with background jobs

**[IntentsBasicSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/IntentsBasicSample)** - Basic usage of `intended()` and `intending()`

**[IntentsAdvancedSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/IntentsAdvancedSample)** - Simulates a user fetching a bitmap using the camera

**[MultiWindowSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/MultiWindowSample)** - Shows how to point Espresso to different windows

**[RecyclerViewSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/RecyclerViewSample)** - RecyclerView actions for Espresso

**[WebBasicSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/WebBasicSample)** - Use Espresso-web to interact with WebViews

**[BasicSampleBundled](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/BasicSampleBundled)** - Basic sample for Eclipse and other IDEs

**[MultiProcessSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/MultiProcessSample)** - Showcases how to use multiprocess Espresso.
### UiAutomator Sample

**[BasicSample](https://github.com/googlesamples/android-testing/tree/master/ui/uiautomator/BasicSample)** - Basic UI Automator sample

### AndroidJUnitRunner Sample

**[AndroidJunitRunnerSample](https://github.com/googlesamples/android-testing/tree/master/runner/AndroidJunitRunnerSample)** - Showcases test annotations, parameterized tests and testsuite creation

### JUnit4 Rules Sample

**All previous samples use ActivityTestRule or IntentsTestRule but there's one specific to ServiceTestRule:

**[BasicSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/BasicSample)** - Simple usage of `ActivityTestRule`

**[IntentsBasicSample](https://github.com/googlesamples/android-testing/blob/master/ui/espresso/IntentsBasicSample)** - Simple usage of `IntentsTestRule`

**[ServiceTestRuleSample](https://github.com/googlesamples/android-testing/tree/master/integration/ServiceTestRuleSample)** - Simple usage of `ServiceTestRule`

Prerequisites
--------------

- Android SDK v28
- Android Build Tools v28.03

Getting Started
---------------

These samples use the Gradle build system. To build a project, enter the project directory and use the `./gradlew assemble` command or use "Import Project" in Android Studio.

- Use `./gradlew connectedAndroidTest` to run the tests on a connected emulator or device.
- Use `./gradlew test` to run the unit test on your local host.

There is a top-level `build.gradle` file if you want to build and test all samples from the root directory. This is mostly helpful to build on a CI (Continuous Integration) server.

AndroidX Test Library
---------------
Many of these samples use the AndroidX Test Library. Visit the [Testing site on developer.android.com](https://developer.android.com/training/testing) for more information.

Experimental Bazel Support
--------------------------

[![Build status](https://badge.buildkite.com/18dda320b265e9a8f20cb6141b1e80ca58fb62bdb443e527be.svg)](https://buildkite.com/bazel/android-testing)

Some of these samples can be tested with [Bazel](https://bazel.build) on Linux. These samples contain a `BUILD.bazel` file, which is similar to a `build.gradle` file. The external dependencies are defined in the top level `WORKSPACE` file.

This is __experimental__ feature. To run the tests, please install the latest version of Bazel (0.12.0 or later) by following the [instructions on the Bazel website](https://docs.bazel.build/versions/master/install-ubuntu.html).

### Bazel commands

```
# Clone the repository if you haven't.
$ git clone https://github.com/google/android-testing
$ cd android-testing

# Edit the path to your local SDK at the top of the WORKSPACE file
$ $EDITOR WORKSPACE

# Test everything in a headless mode (no graphical display)
$ bazel test //... --config=headless

# Test a single test, e.g. ui/espresso/BasicSample/BUILD.bazel
$ bazel test //ui/uiautomator/BasicSample:BasicSampleInstrumentationTest_21_x86 --config=headless

# Query for all android_instrumentation_test targets
$ bazel query 'kind(android_instrumentation_test, //...)'
//ui/uiautomator/BasicSample:BasicSampleInstrumentationTest_23_x86
//ui/uiautomator/BasicSample:BasicSampleInstrumentationTest_22_x86
//ui/uiautomator/BasicSample:BasicSampleInstrumentationTest_21_x86
//ui/uiautomator/BasicSample:BasicSampleInstrumentationTest_19_x86
//ui/espresso/RecyclerViewSample:RecyclerViewSampleInstrumentationTest_23_x86
//ui/espresso/RecyclerViewSample:RecyclerViewSampleInstrumentationTest_22_x86
//ui/espresso/RecyclerViewSample:RecyclerViewSampleInstrumentationTest_21_x86
//ui/espresso/RecyclerViewSample:RecyclerViewSampleInstrumentationTest_19_x86
//ui/espresso/MultiWindowSample:MultiWindowSampleInstrumentationTest_23_x86
//ui/espresso/MultiWindowSample:MultiWindowSampleInstrumentationTest_22_x86
...

# Test everything with GUI enabled
$ bazel test //... --config=gui

# Test with a local device or emulator. Ensure that `adb devices` lists the device.
$ bazel test //... --config=local_device

# If multiple devices are connected, add --device_serial_number=$identifier where $identifier is the name of the device in `adb devices`
$ bazel test //... --config=local_device --test_arg=--device_serial_number=$identifier
```

For more information, check out the documentation for [Android Instrumentation Tests in Bazel](https://docs.bazel.build/versions/master/android-instrumentation-test.html). You may also want to check out [Building an Android App with Bazel](https://docs.bazel.build/versions/master/tutorial/android-app.html), and the list of [Android Rules](https://docs.bazel.build/versions/master/be/android.html) in the Bazel Build Encyclopedia.

Known issues:

* Building of APKs is supported on Linux, Mac and Windows, but testing is only supported on Linux.
* `android_instrumentation_test.target_device` attribute still needs to be specified even if `--config=local_device` is used.
* If using a local device or emulator, the APKs are not uninstalled automatically after the test. Use this command to
remove the packages:
    * `adb shell pm list packages com.example.android.testing | cut -d ':' -f 2 | tr -d '\r' | xargs -L1 -t adb uninstall`
    
Please file Bazel related issues against the [Bazel](https://github.com/bazelbuild/bazel) repository instead of this repository.

Support
-------

- Google+ Community: https://plus.google.com/communities/105153134372062985968
- Stack Overflow: http://stackoverflow.com/questions/tagged/android-testing

If you've found an error in this sample, please file an issue:
https://github.com/googlesamples/android-testing

Patches are encouraged, and may be submitted by forking this project and
submitting a pull request through GitHub. Please see CONTRIBUTING.md for more details.

License
-------

Copyright 2015 The Android Open Source Project, Inc.

Licensed to the Apache Software Foundation (ASF) under one or more contributor
license agreements.  See the NOTICE file distributed with this work for
additional information regarding copyright ownership.  The ASF licenses this
file to you under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License.  You may obtain a copy of
the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
License for the specific language governing permissions and limitations under
the License.
# How to become a contributor and submit your own code

To contribute with a small fix, simply create a pull request. If you want to add a new sample or plan to request a big change, [contact us](https://groups.google.com/forum/#!forum/android-testing-support-library) first.

## Contributing new samples

If you want to contribute full samples, we'd love to review and accept them. In case you need ideas, these are some samples on the roadmap:

* Advanced Idling Resource 
* RecyclerView actions
* Sharding 
* RunListener 
* Rules
 
You can also contribute to this list if you have a sample request.

## Code style and structure

Please check out the [Code Style for Contributors](https://source.android.com/source/code-style.html) section in AOSP. Also, check out the rest of the samples and maintain as much consistency with them as possible.

## Contributor License Agreements

We'd love to accept your sample apps and patches! Before we can take them, we
have to jump a couple of legal hurdles.

Please fill out either the individual or corporate Contributor License Agreement (CLA).

  * If you are an individual writing original source code and you're sure you
    own the intellectual property, then you'll need to sign an [individual CLA]
    (https://cla.developers.google.com).
  * If you work for a company that wants to allow you to contribute your work,
    then you'll need to sign a [corporate CLA]
    (https://cla.developers.google.com).
  * Please make sure you sign both, Android and Google CLA

Follow either of the two links above to access the appropriate CLA and
instructions for how to sign and return it. Once we receive it, we'll be able to
accept your pull requests.

## Contributing A Patch

1. Submit an issue describing your proposed change to the repo in question.
1. The repo owner will respond to your issue promptly.
1. If your proposed change is accepted, and you haven't already done so, sign a
   Contributor License Agreement (see details above).
1. Fork the desired repo, develop and test your code changes.
1. Ensure that your code adheres to the existing style in the sample to which
   you are contributing. Refer to the
   [Android Code Style Guide]
   (https://source.android.com/source/code-style.html) for the
   recommended coding standards for this organization.
1. Ensure that your code has an appropriate set of unit tests which all pass.
1. Submit a pull request.

# Custom matchers sample for Espresso

*Extending Espresso is easy! This sample shows how to match the "hint" property of an EditText.*

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio is recommended.

1. Download the project code, preferably using `git clone`.
1. Open the Android SDK Manager (*Tools* Menu | *Android*) and make sure you have installed the *Android testing support library Repository* under *Extras*.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Tests are in `src/androidTest/java`
1. Create the test configuration with a custom runner: `androidx.test.runner.AndroidJUnitRunner`
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Tests* configuration
    * Choose a module
    * Add a *Specific instrumentation runner*: `androidx.test.runner.AndroidJUnitRunner`
1. Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
1. Run the newly created configuration

The application will be started on the device/emulator and a series of actions will be performed automatically.

If you are using Android Studio, the *Run* window will show the test results.

# Basic sample for Espresso Web

Espresso Web is an API that can be used to write automated tests for hybrid applications which
contain one or more WebViews. Similar to onData, WebView interactions are actually composed of
several ViewActions, however ViewActions in Espresso Web are composed of Web Driver Atoms.
Espresso Web takes care of synchronization and tries to minimize boilerplate to a bare minimum,
while still giving you an Espresso-like feel to interacting with WebViews.

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio is recommended.

1. Download the project code, preferably using `git clone`.
1. Open the Android SDK Manager (*Tools* Menu | *Android*) and make sure you have installed the *Android Support Repository* under *Extras*. (For more Information click [here](http://developer.android.com/tools/testing-support-library/index.html#setup))
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Tests are in `src/androidTest/java`
1. Create the test configuration with a custom runner: `androidx.test.runner.AndroidJUnitRunner`
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Tests* configuration
    * Choose a module
    * Add a *Specific instrumentation runner*: `androidx.test.runner.AndroidJUnitRunner`
1. Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
1. Run the newly created configuration

The application will be started on the device/emulator and a series of actions will be performed automatically.

If you are using Android Studio, the *Run* window will show the test results.
# Advanced sample for Espresso Intents

Espresso Intents is a great way to do hermetic inter app testing. It works essentially like mockito and allows for Intent
verification and stubbing. This sample shows how to stub an Intent and simulate that a picture is fetched
from the camera without leaving the main app.

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio is recommended.

1. Download the project code, preferably using `git clone`.
1. Open the Android SDK Manager (*Tools* Menu | *Android*) and make sure you have installed the *Android testing support library Repository* under *Extras*.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Tests are in `src/androidTest/java`
1. Create the test configuration with a custom runner: `androidx.test.runner.AndroidJUnitRunner`
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Tests* configuration
    * Choose a module
    * Add a *Specific instrumentation runner*: `androidx.test.runner.AndroidJUnitRunner`
1. Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
1. Run the newly created configuration

The application will be started on the device/emulator and a series of actions will be performed automatically.

If you are using Android Studio, the *Run* window will show the test results.
# Sample for FragmentScenario with Espresso

*A simple example that shows use of FragmentScenario with Espresso.*

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio 3.4 is recommended.

1. Download the project code, preferably using `git clone`.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * The test source is located in `src/sharedTest/java`. There is a single set of test source that can be executed
    either on local host using Robolectric or on emulator/device.
1. Create and run the Android Instrumented Test configuration
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Instrumented Tests* configuration
    * Choose the `app` module
    * Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
    * Run the newly created configuration
1. Create and run the local Test configuration
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android JUnit* configuration
    * Set `Use classpath of module` to `app`
    * Set `Class` to FragmentScenarioTest
    * Run the configuration

If you are using Android Studio, the *Run* window will show the test results.
# Basic Idling Resource sample for Espresso

The centerpiece of Espresso is its ability to seamlessly synchronize all test operations with the application under test. By default, Espresso waits for UI events in the current message queue to be processed and default AsyncTasks* to complete before it moves on to the next test operation. This should address the majority of application/test synchronization in your application.

However, there are instances where applications perform background operations (such as communicating with web services) via non-standard means; for example: direct creation and management of threads.

This sample showcases how to implement a very simple IdlingResource interface and expose it to a test. The application shows a message to the user after a delay that is executed on a different thread.

Consider using the CountingIdlingResource class from the espresso-contrib package. It's a very easy to use Idling Resource implementation that can handle multiple parallel operations keeping track of the number of pending operations.

Note that the `espresso-idling-resource` dependency is added into the `implementation` scope.

This sample use AndroidX:

```
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.1.1'
    implementation 'androidx.test.espresso:espresso-idling-resource:3.1.1'
```

If you haven't yet migrated to AndroidX:

```
	androidTestImplementation 'com.android.support.test.espresso:espresso-core:3.0.2'
	implementation 'com.android.support.test.espresso:espresso-idling-resource:3.0.2'
```


This dependency and its implementation are added to the app under test but are not needed in production. This bloats the released app but it's kept this way to simplify the sample. You can:
 * ProGuard/shrink your release build to minimize impact
 * Use a build type or product flavor for tests and remove the Idling Resource classes in the production/release variant.
 * Add the dependency to `androidTestCompile` and inject an IdlingResource-aware MessageDelayer from the test.
 * Keep them, since the added methods and size are insignificant.


# Multi-window sample for Espresso

Android's Window system allows multiple view hierarchies to layer on top of each other.

A real world analogy would be an overhead projector with multiple transparencies placed
on top of each other. Each Window is a transparency, and what is drawn on top of this
transparency is the view hierarchy.

By default Espresso uses a heuristic to guess which Window you intend to interact with.
This heuristic is normally 'good enough' however if you want to interact with a Window
that it does not select then you'll have to swap in your own root window matcher.
Initially there's only one window, but typing into the auto-complete text view creates another
window that will be layered on top of the screen. Espresso ignores this layer because it is
not connected to the keyboard/ime.

Espresso provides the ability to switch the default window matcher used in both onView and onData
interactions.

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio is recommended.

1. Download the project code, preferably using `git clone`.
1. Open the Android SDK Manager (*Tools* Menu | *Android*) and make sure you have installed the *Android testing support library Repository* under *Extras*.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Tests are in `src/androidTest/java`
1. Create the test configuration with a custom runner: `androidx.test.runner.AndroidJUnitRunner`
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Tests* configuration
    * Choose a module
    * Add a *Specific instrumentation runner*: `androidx.test.runner.AndroidJUnitRunner`
1. Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
1. Run the newly created configuration

The application will be started on the device/emulator and a series of actions will be performed automatically.

If you are using Android Studio, the *Run* window will show the test results.
# Basic sample for Espresso Intents

Espresso Intents is a great way to do hermetic inter app testing. It works essentially like mockito and allows for Intent
verification and stubbing.

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio 3.4 is recommended.

1. Download the project code, preferably using `git clone`.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Instrumentation Tests are in `src/androidTest/java`
    * Local Tests are in `src/test/java` 
1. Create and run the Instrumented test configuration
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Instrumented Tests* configuration
    * Choose the `app` module
    * Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
    * Run the newly created configuration
    * The application will be started on the device/emulator and a series of actions will be performed automatically.
1. Create and run the local Test configuration
    * Open Run menu | Edit Configurations
    * Add a new *Android JUnit * configuration
    * Set `Use classpath of module` to `app`
    * Set `Class` to `DialerActivityTest`
    * Run the configuration    
    * The test will run on local host

If you are using Android Studio, the *Run* window will show the test results.

# Data Adapter sample for Espresso

An AdapterView (like ListView, GridView, etc.) is a view bound to an Adapter that determines the
view's children. In Espresso, you can match these children views using the onData() method instead of
onView() as you would do normally. Instead of matching views, onData() matches the data that is
bound to each view item.

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio is recommended.

1. Download the project code, preferably using `git clone`.
1. Open the Android SDK Manager (*Tools* Menu | *Android*) and make sure you have installed the *Android testing support library Repository* under *Extras*.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Tests are in `src/androidTest/java`
1. Create the test configuration with a custom runner: `androidx.test.runner.AndroidJUnitRunner`
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Tests* configuration
    * Choose a module
    * Add a *Specific instrumentation runner*: `androidx.test.runner.AndroidJUnitRunner`
1. Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
1. Run the newly created configuration

The application will be started on the device/emulator and a series of actions will be performed automatically.

If you are using Android Studio, the *Run* window will show the test results.
# Basic sample for Espresso

*If you are new to Espresso, try this sample first.*

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio 3.4 is recommended.

1. Download the project code, preferably using `git clone`.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Instrumentation Tests are in `src/androidTest/java`
    * Local Tests are in `src/test/java` 
1. Create and run the Instrumented test configuration
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Instrumented Tests* configuration
    * Choose the `app` module
    * Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
    * Run the newly created configuration
    * The application will be started on the device/emulator and a series of actions will be performed automatically.
1. Create and run the local Test configuration
    * Open Run menu | Edit Configurations
    * Add a new *Android JUnit * configuration
    * Set `Use classpath of module` to `app`
    * Set `Class` to `ChangeTextBehaviorLocalTest`
    * Run the configuration    
    * The test will run on local host

If you are using Android Studio, the *Run* window will show the test results.
# Basic sample for Espresso

*If you are new to Espresso, try this sample first.*

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio 3.4 is recommended.

1. Download the project code, preferably using `git clone`.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Instrumentation Tests are in `src/androidTest/java`
    * Local Tests are in `src/test/java` 
1. Create and run the Instrumented test configuration
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Instrumented Tests* configuration
    * Choose the `app` module
    * Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
    * Run the newly created configuration
    * The application will be started on the device/emulator and a series of actions will be performed automatically.
1. Create and run the local Test configuration
    * Open Run menu | Edit Configurations
    * Add a new *Android JUnit * configuration
    * Set `Use classpath of module` to `app`
    * Set `Class` to `ChangeTextBehaviorLocalTest`
    * Run the configuration    
    * The test will run on local host

If you are using Android Studio, the *Run* window will show the test results.
# Multiprocess Espresso Sample

To test app components in a non-default processes, you can use the functionality of Multiprocess Espresso. This tool, available on Android O (API level 26) and higher, allows you to seamlessly test your app's UI interactions that cross your app's process boundaries while maintaining Espresso's synchronization guarantees.

1. Download the project code, preferably using `git clone`.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Tests are in `src/androidTest/java`
1. Create the test configuration:
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Tests* configuration
    * Choose a module
1. Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
1. Run the newly created configuration

The application will be started on the device/emulator and a series of actions will be performed automatically.

If you are using Android Studio, the *Run* window will show the test results.
# Basic sample for Espresso using static JAR files

*If you are using Espresso with Eclipse, try this sample first.*

This project uses Eclipse and ADT to build and run the tests.

1. Download the project code, preferably using `git clone`.
1. Check out the static JAR files required to run the Espresso tests in the libs/ folder of the project
1. Run the ./remove_license.sh script to remove duplicated LICENSE.txt files. This step is required because some of the test dependencies contain LICENSE.txt files which result in this build error:
"Error generating final archive: Found duplicate file for APK: LICENSE.txt".
The problem is that the same LICENSE.TXT file is found multiple times and AAPT does not know how to resolve this conflict.
1. Check out the relevant code:
    * The application under test is located in `src/`
    * Tests are in `tests/`
1. Create the test configuration with a custom runner: `androidx.test.runner.AndroidJUnitRunner`
    * Open *Run* menu | *Run Configurations*
    * Click on Android JUnit Test
    * Add a new configuration by pressing the "new launch configuration" button
    * Select your project by clicking the "Browse" button
    * Add a *Specific instrumentation runner*: `androidx.test.runner.AndroidJUnitRunner`
1. Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
1. Run the newly created configuration

The application will be started on the device/emulator and a series of actions will be performed automatically.
zip -d libs/hamcrest-core-1.3.jar LICENSE.txt
zip -d libs/hamcrest-library-1.3.jar LICENSE.txt
zip -d libs/hamcrest-integration-1.3.jar LICENSE.txt

# To enable ProGuard in your project, edit project.properties
# to define the proguard.config property as described in that file.
#
# Add project specific ProGuard rules here.
# By default, the flags in this file are appended to flags specified
# in ${sdk.dir}/tools/proguard/proguard-android.txt
# You can edit the include path and order by changing the ProGuard
# include property in project.properties.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# Add any project specific keep options here:

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}
# RecyclerView sample for Espresso

Espresso has a special entry point to interact with AdapterViews, `onData()`, however, RecyclerViews work differently than AdapterViews.

In order to interact with RecyclerViews using Espresso, the `espresso-contrib` package has a collection of `RecyclerViewActions` that can be used to scroll to positions or perform actions on items.

In this example you'll find a basic Activity that shows a list and an example of how to scroll through it, perform some ViewActions and check ViewAssertions using Espresso.
# Basic sample for UiAutomator

*If you are new to UiAutomator, try this sample first.*

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio is recommended.

1. Download the project code, preferably using `git clone`.
1. Open the Android SDK Manager (*Tools* Menu | *Android*) and make sure you have installed the *Android testing support library Repository* under *Extras*.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Tests are in `src/androidTest/java`
1. Create the test configuration with a custom runner: `androidx.test.runner.AndroidJUnitRunner`
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Tests* configuration
    * Choose a module
    * Add a *Specific instrumentation runner*: `androidx.test.runner.AndroidJUnitRunner`
1. Run the newly created configuration

The application will be started on the device/emulator and a series of actions will be performed automatically.

If you are using Android Studio, the *Run* window will show the test results.
# Basic sample (in Kotlin) for writing unit tests that mocks the Android framework

*If you are new to unit testing on Android, try this sample first.*

This project uses the Gradle build system and the Android gradle plugin support for unit testing.
You can either benefit from IDEs integration such as Android studio or run the tests on the command
line.

Unit tests run on a local JVM on your development machine. The Android Gradle plugin will compile
your app's source code and execute it using gradle test task. Tests are executed against a modified
version of android.jar where all final modifiers have been stripped off. This lets you use popular
mocking libraries, like Mockito.

For more information see http://tools.android.com/tech-docs/unit-testing-support

## Setup the project in Android studio and run tests.

1. Download the project code, preferably using `git clone`.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Make sure you select "Unit Tests" as the test artifact in the "Build Variants" panel in Android Studio. 
1. Check out the relevant code:
    * The application code is located in `src/main/java`
    * Unit Tests are in `src/test/java`
1. Create a test configuration with the JUnit4 runner: `org.junit.runners.JUnit4`
    * Open *Run* menu | *Edit Configurations*
    * Add a new *JUnit* configuration
    * Choose module *app*
    * Select the class to run by using the *...* button
1. Run the newly created configuration

The unit test will be ran automatically.

## Use Gradle on the command line.

After downloading the projects code using `git clone` you'll be able to run the
unit tests using the command line:

    ./gradlew test

If all the unit tests have been successful you will get a `BUILD SUCCESSFUL`
message.

## See the report.

A report in HTML format is generated in `app/build/reports/tests`
# Basic sample for unit testing on device or emulator

An *Unit Android Test* is a test that needs an Android device or emulator but it's different
from a UI test because it doesn't start any activities.

In this sample the test can't run without the Android Framework because the Parcel class is used in
one of the methods of the Parcelable interface and the way data is written into a Parcel and read
from it is not trivial enough to be stubbed.

Note that the unit test is placed in `/androidTest/` instead of `/test/`.

This project uses the Gradle build system. You can either benefit from IDEs
integration such as Android studio or run the tests on the command line.

## Setup the project in Android studio and run the tests.

1. Download the project code, preferably using `git clone`.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * `LogHistory.java` is the class under test. It implements Parcelable.
    * `LogHistoryAndroidUnitTest` is the Android unit test
    * `MainActivity.java` shows the Parcelable in action but note that the test is not showing any
activities on the device or emulator.
1. Create the test configuration with a custom runner: `androidx.test.runner.AndroidJUnitRunner`
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Tests* configuration
    * Choose a module
    * Add a *Specific instrumentation runner*: `androidx.test.runner.AndroidJUnitRunner`
1. Connect a device or start an emulator
1. Run the newly created configuration

The unit test will be ran automatically.

## Use Gradle on the command line.

After downloading the projects code using `git clone` you'll be able to run the
unit tests using the command line:

    ./gradlew connectedCheck

If all the unit tests have been successful you will get a `BUILD SUCCESSFUL`
message.

## See the report.

A report in HTML format is generated in `app/build/outputs/reports/androidTests/connected`
# Basic sample for writing unit tests that mocks the Android framework

*If you are new to unit testing on Android, try this sample first.*

This project uses the Gradle build system and the Android gradle plugin support for unit testing.
You can either benefit from IDEs integration such as Android studio or run the tests on the command
line.

Unit tests run on a local JVM on your development machine. The Android Gradle plugin will compile
your app's source code and execute it using gradle test task. Tests are executed against a modified
version of android.jar where all final modifiers have been stripped off. This lets you use popular
mocking libraries, like Mockito.

For more information see http://tools.android.com/tech-docs/unit-testing-support

## Setup the project in Android studio and run tests.

1. Download the project code, preferably using `git clone`.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Make sure you select "Unit Tests" as the test artifact in the "Build Variants" panel in Android Studio. 
1. Check out the relevant code:
    * The application code is located in `src/main/java`
    * Unit Tests are in `src/test/java`
1. Create a test configuration with the JUnit4 runner: `org.junit.runners.JUnit4`
    * Open *Run* menu | *Edit Configurations*
    * Add a new *JUnit* configuration
    * Choose module *app*
    * Select the class to run by using the *...* button
1. Run the newly created configuration

The unit test will be ran automatically.

## Use Gradle on the command line.

After downloading the projects code using `git clone` you'll be able to run the
unit tests using the command line:

    ./gradlew test

If all the unit tests have been successful you will get a `BUILD SUCCESSFUL`
message.

## See the report.

A report in HTML format is generated in `app/build/reports/tests`
# AndroidTestOrchestrator sample

The Android Test Orchestrator allows you to run each of your app's tests in isolation, enabling greater relability.
See https://developer.android.com/training/testing/junit-runner#using-android-test-orchestrator for more background.

This sample is a subset of the AndroidJUnitRunner sample, but it
ilustrates how to enable the Android Test Orchestrator in the app/build.gradle file.

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio is recommended.

1. Download the project code, preferably using `git clone`.
1. Open the Android SDK Manager (*Tools* Menu | *Android*).
1. In Android Studio, select *File* | *Open...* and point to the top-level `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Tests are in `src/androidTest/java`
1. Create the test configuration with a custom runner: `androidx.test.runner.AndroidJUnitRunner`
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Tests* configuration
    * Choose a module
    * Add a *Specific instrumentation runner*: `androidx.test.runner.AndroidJUnitRunner`
1. Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
1. Run the newly created configuration

The application will be started on the device/emulator and a series of actions will be performed automatically.

If you are using Android Studio, the *Run* window will show the test results.
# AndroidJUnitRunner sample

The new android test runner brings Junit4 support to android testing. This samples gives a quick
overview of some of the new features like test annotations, parameterized tests and test suite
creation.

1. CalculatorTest.java contains JUnit4 style unit tests for the calculator logic.
1. CalculatorAddParameterizedTest.java contains JUnit4 style tests and uses the @Parameters annotation
   to parameterize a single test with different values.
1. CalculatorInstrumentationTest.java uses JUnit4 style tests to test the Ui of the CalculatorActivity
1. OperationHintInstrumentationTest.java uses JUnit3 style tests to test the Ui of the CalculatorActivity

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio is recommended.

1. Download the project code, preferably using `git clone`.
1. Open the Android SDK Manager (*Tools* Menu | *Android*) and make sure you have installed the *Android Support Repository* under *Extras*.
1. In Android Studio, select *File* | *Open...* and point to the top-level `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Tests are in `src/androidTest/java`
1. Create the test configuration with a custom runner: `androidx.test.runner.AndroidJUnitRunner`
    * Open *Run* menu | *Edit Configurations*
    * Add a new *Android Tests* configuration
    * Choose a module
    * Choose which tests to run. Click on Test: class and select one of the TestSuites
    (AndroidTestSuite, UnitTestSuite, InstrumentationTestSuite)
    * Add a *Specific instrumentation runner*: `androidx.test.runner.AndroidJUnitRunner`
1. Connect a device or start an emulator
    * Turn animations off.
    (On your device, under Settings->Developer options disable the following 3 settings: "Window animation scale", "Transition animation scale" and "Animator duration scale")
1. Run the newly created configuration

The application will be started on the device/emulator and a series of actions will be performed automatically.

If you are using Android Studio, the *Run* window will show the test results.
# Basic sample for ServiceTestRule

This rule provides a simplified mechanism to start and shutdown your service before and after
the duration of your test. It also guarantees that the service is successfully connected when starting
(or binding to) a service. The service can be started (or bound) using one of the helper methods.
It will automatically be stopped (or unbound) after the test completes and any methods annotated with @After are finished.

Note: This rule doesn't support `IntentService` because it's automatically destroyed when
`IntentService#onHandleIntent(android.content.Intent)`
 finishes all outstanding commands. So there is no guarantee to establish a successful connection in a timely manner.

This project uses the Gradle build system. You don't need an IDE to build and execute it but Android Studio is recommended.

1. Download the project code, preferably using `git clone`.
1. Open the Android SDK Manager (*Tools* Menu | *Android*) and make sure you have installed the *Support Repository* under *Extras*.
1. In Android Studio, select *File* | *Open...* and point to the `./build.gradle` file.
1. Check out the relevant code:
    * The application under test is located in `src/main/java`
    * Tests are in `src/androidTest/java`
1. Connect a device or start an emulator
1. Run the newly created configuration

The application will be started on the device/emulator and a series of actions will be performed automatically.

If you are using Android Studio, the *Run* window will show the test results.
