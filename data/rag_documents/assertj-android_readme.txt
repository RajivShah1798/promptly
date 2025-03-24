AssertJ Android
===============

A set of AssertJ assertions geared toward testing Android.

## Deprecated

The support libraries and play services are developing at a rate which this library cannot sustain. Additionally, we no longer think AssertJ's model for supporting alternate assertions is a good practice.

We recommend using [Truth](https://github.com/google/truth) which has vastly superior extensibility model which, when coupled with things like Kotlin's `apply` method create a really nice assertion experience.

---

Writing tests is not the most glamorous part of developing an Android
application but it is an invaluable one. Using libraries like JUnit and AssertJ
provide a great starting point for writing tests.

This library is an extension of [AssertJ][1] which aims to make it even easier to test
Android.



Examples
--------

 *  AssertJ Android:

    ```java
    assertThat(view).isGone();
    ```

 *  Regular JUnit:

    ```java
    assertEquals(View.GONE, view.getVisibility());
    ```

 *  Regular AssertJ:

    ```java
    assertThat(view.getVisibility()).isEqualTo(View.GONE);
    ```

When failing, the _AssertJ Android_ assertion produces an output which allows you
to immediately recognize the problem:
`Expected visibility <gone> but was <invisible>`.

Compare that to the output of regular _AssertJ_ `Expected:<[8]> but was:<[4]>` and
regular _JUnit_ `Expected: <8> but was: <4>` and you should immediately see the
advantage.


Because _AssertJ Android_ offers assertions directly on objects rather than
properties they can be chained together.

 *  AssertJ Android:

    ```java
    assertThat(layout).isVisible()
        .isVertical()
        .hasChildCount(4)
        .hasShowDividers(SHOW_DIVIDERS_MIDDLE);
    ```

 *  Regular JUnit:

    ```java
    assertEquals(View.VISIBLE, layout.getVisibility());
    assertEquals(VERTICAL, layout.getOrientation());
    assertEquals(4, layout.getChildCount());
    assertEquals(SHOW_DIVIDERS_MIDDLE, layout.getShowDividers());
    ```

 *  Regular AssertJ:

    ```java
    assertThat(layout.getVisibility()).isEqualTo(View.VISIBLE);
    assertThat(layout.getOrientation()).isEqualTo(VERTICAL);
    assertThat(layout.getChildCount()).isEqualTo(4);
    assertThat(layout.getShowDividers()).isEqualTo(SHOW_DIVIDERS_MIDDLE);
    ```

Assertions exist for nearly every object that you would ever want to test, from
`LinearLayout` to `ActionBar` to `Fragment` to `MenuItem`. Everything in the
support library is included too.

To get started writing tests add the following import:

```java
import static org.assertj.android.api.Assertions.assertThat;
```



Add-On Modules
--------------

Modules are also provided for the add-on Android libraries. Add the dependency
(listed below) and use the following imports:

 * support-v4: `import static org.assertj.android.support.v4.api.Assertions.assertThat;`
 * play-services: `import static org.assertj.android.playservices.api.Assertions.assertThat;`
 * appcompat-v7: `import static org.assertj.android.appcompat.v7.api.Assertions.assertThat;`
 * mediarouter-v7: `import static org.assertj.android.mediarouter.v7.api.Assertions.assertThat;`
 * gridlayout-v7: `import static org.assertj.android.gridlayout.v7.api.Assertions.assertThat;`
 * cardview-v7: `import static org.assertj.android.cardview.v7.api.Assertions.assertThat;`
 * recyclerview-v7: `import static org.assertj.android.recyclerview.v7.api.Assertions.assertThat;`
 * palette-v7: `import static org.assertj.android.palette.v7.api.Assertions.assertThat;`



Extending
---------

The provided assertions have also been designed to be extended for any custom
controls you have developed.

```java
public class CustomLayout extends LinearLayout {
  public int getBehavior() {
    /* ... */
  }
}
```

Use the following pattern to set up your assertions.

```java
public class CustomLayoutAssert extends AbstractLinearLayoutAssert<CustomLayoutAssert, CustomLayout> {
  public static CustomLayoutAssert assertThat(CustomLayout actual) {
    return new CustomLayoutAssert(actual);
  }

  public CustomLayoutAssert(CustomLayout actual) {
    super(actual, CustomLayoutAssert.class);
  }

  public CustomLayoutAssert hasSomeBehavior() {
    isNotNull();
    assertThat(actual.getBehavior())
        .overridingErrorMessage("Expected some behavior but was doing other behavior.")
        .isEqualTo(42)
    return this;
  }
}
```

Now static import `CustomLayoutAssert.assertThat` in your test classes.

For more information about writing custom assertions see the [official documentation][2].



Download
--------

Android module:
```groovy
androidTestCompile 'com.squareup.assertj:assertj-android:1.2.0'
```

support-v4 module:
```groovy
androidTestCompile 'com.squareup.assertj:assertj-android-support-v4:1.2.0'
```

Google Play Services module:
```groovy
androidTestCompile 'com.squareup.assertj:assertj-android-play-services:1.2.0'
```

appcompat-v7 module:
```groovy
androidTestCompile 'com.squareup.assertj:assertj-android-appcompat-v7:1.2.0'
```

Design library module:
```groovy
androidTestCompile 'com.squareup.assertj:assertj-android-design:1.2.0'
```

mediarouter-v7 module:
```groovy
androidTestCompile 'com.squareup.assertj:assertj-android-mediarouter-v7:1.2.0'
```

gridlayout-v7 module:
```groovy
androidTestCompile 'com.squareup.assertj:assertj-android-gridlayout-v7:1.2.0'
```

cardview-v7 module:
```groovy
androidTestCompile 'com.squareup.assertj:assertj-android-cardview-v7:1.2.0'
```

recyclerview-v7 module:
```groovy
androidTestCompile 'com.squareup.assertj:assertj-android-recyclerview-v7:1.2.0'
```

palette-v7 module:
```groovy
androidTestCompile 'com.squareup.assertj:assertj-android-palette-v7:1.2.0'
```

Snapshots of the development version are available in [Sonatype's `snapshots` repository][snap].



License
-------

    Copyright 2013 Square, Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.




 [1]: http://joel-costigliola.github.io/assertj/
 [2]: http://joel-costigliola.github.io/assertj/assertj-core-custom-assertions.html
 [snap]: https://oss.sonatype.org/content/repositories/snapshots/
Contributing
============

If you would like to contribute code you can do so through GitHub by forking
the repository and sending a pull request.

When submitting code, please make every effort to follow existing conventions
and style in order to keep the code as readable as possible. Please also make
sure your code compiles by running `./gradlew clean build`. Checkstyle failures
during compilation indicate errors in your style and can be viewed in files
located at `*/build/report/checkstyle` directories.

Before your code can be accepted into the project you must also sign the
[Individual Contributor License Agreement (CLA)][1].


 [1]: https://spreadsheets.google.com/spreadsheet/viewform?formkey=dDViT2xzUHAwRkI3X3k5Z0lQM091OGc6MQ&ndplr=1
Change Log
==========

Version 1.2.0 *(2017-08-26)*
----------------------------

 * Support libraries updated to 26.
 * New assertions!
   * `android.support.design.widget.TextInputLayout`
   * `android.support.v4.media.MediaMetadataCompat`
 * New: `ViewAssert` gains assertions for `elevation`, `z`, and `translationZ`.
 * New: `TimePickerAssert` gains assertions for `hour` and `minute`.
 * New: `IntentAssert` gains assertions for `pacakge`.
 * Fix: `ViewAssert.hasTag` now checks based on equality, not identity.
 * Fix: `BluetoothClassAssert.doesNotHave` to correctly assert negatively.
 * Fix: `BluetoothGattCharacteristicAssert.hasUuid` to assert against actual value.
 * Fix: `BluetoothGattDescriptorAssert.hasUuid` to assert against actual value.
 * Fix: `BluetoothGattServiceAssert.hasUuid` to assert against actual value.
 * Fix: `ViewAssert.canResolveTextAlignment` and `canNotResolveTextAlignment` to check the correct property.
 * Fix: `DisplayAssert.hasDisplayId` to assert against actual value.
 * Fix: `ToastAssert.hasGravity` to assert against actual value.
 * Fix: `AnimationAssert.hasStartTime` to assert against actual value.
 * Fix: `RecyclerViewLayoutManagerAssert.hasMinimumWidth` and `hasMinimumHeight` to assert against actual value.
 * Fix: `MediaRouteDiscoveryRequestAssert` now assert against actual values.


Version 1.1.1 *(2015-10-17)*
----------------------------

 * Add assertion for `Uri`.
 * New: Overload for `IntentAssert.hasExtra` which takes a value to compare.
 * Fix: `NotificationAssert.hasFlags` now checks to see if the specified flags are set while allowing
   unspecified flags to also be set. Use `hasOnlyFlags` to check for an exact match.
 * Fix: `TabLayoutAssert.hasTabMode` now correctly compares against the tab mode instead of count.


Version 1.1.0 *(2015-08-15)*
----------------------------

 * New: Design library add-on module! Includes assertions for `NavigationView`, `Snackbar`,
   `TabLayout`, and `TabLayout.Tab`.
 * Fix: Correct `minSdkVersion` declared in Card View, Palette, and Recycler View modules.


Version 1.0.1 *(2015-07-23)*
----------------------------

 * Add assertions for `CameraPosition`, `GoogleMap`, `Marker`, and `UiSettings` to Play Services.
 * Change methods taking a `boolean` to have individual "enabled" and "disabled" assertions in
   Play Services.
 * Add string conversions for `Activity`, `Display`, `TextView` and `View` flag assertions messages.
 * Moved assertions from `ListViewAssert` to `AbstractListViewAssert`.
 * Fix: Use correct value from view for `NumberPickerAssert.hasValue`.
 * Fix: Correct `Intent.hasFlags` assert and update its known flags.
 * Fix: Update AppCompat's `SearchView` assertion to reflect it extending from `LinearLayout`.


Version 1.0.0 *(2014-08-27)*
----------------------------

Convert project from 'fest-android' to 'assertj-android'.

 * New: Add-on modules!
   * Support library (v4)
   * Google Play Services
   * AppCompat (v7)
   * Media Router (v7)
   * Grid Layout (v7)
   * Recycler View (v7)
   * Card View (v7)
   * Pallete (v7)


----

NOTE: The following change log is from the 'fest-android' releases which remain
a part of this repository history.

Version 1.0.8 *(2014-04-05)*
----------------------------

 * New assertions:
   * `android.content.SharedPreferences`
 * Added `hasItem` and `doesNotHaveItem` check to `Adapter`.
 * Added `hasRequestedOrientation` check to `Activity`.
 * Fix: `TextView`'s `endsWith` now properly matches the end of text instead of start.


Version 1.0.7 *(2013-09-11)*
----------------------------

 * Added check for input method target for `TextView`.
 * Fix: `TextView` empty check uses empty `String` instead of empty `CharSequence`.
 * Fix: Correct missing format arguments on some error strings.


Version 1.0.6 *(2013-08-17)*
----------------------------

 * Added checks for the absence of fragments by ID or tag on `FragmentManager`.
 * Added component name and data check for `Intent`.
 * Fix: Correct missing format arguments on some error strings.


Version 1.0.5 *(2013-06-06)*
----------------------------

 * Added bitmap and paint check to `BitmapDrawble`.
 * Added map-liked assertions for `ContentValues`.


Version 1.0.4 *(2013-04-04)*
----------------------------

 * Added custom view check for `ActionBar`.
 * Added flag assert for `Intent`.
 * Added regex 'matches' and 'does not match' for `TextView`.


Version 1.0.3 *(2013-02-27)*
----------------------------

 * Update to FEST 2.0M10 which resolves a potential Android incompatibility.


Version 1.0.2 *(2013-02-26)*
----------------------------

 * New assertions:
   * `android.content.ContentValues`
 * Added negative assertions to `CursorLoader`.
 * Added `String` text assertion to `TextView`.
 * Generation script now supports Python 3.


Version 1.0.1 *(2013-02-05)*
----------------------------

 * New assertions:
   * `android.app.Instrumentation.ActivityMonitor`
   * `android.app.Instrumentation.ActivityResult`
   * `android.app.ListActivity`
   * `android.preference.CheckBoxPreference`
   * `android.preference.DialogPreference`
   * `android.preference.EditTextPreference`
   * `android.preference.ListPreference`
   * `android.preference.MultiSelectListPreference`
   * `android.preference.PreferenceActivity`
   * `android.preference.Preference`
   * `android.preference.PreferenceGroup`
   * `android.preference.PreferenceScreen`
   * `android.preference.RingtonePreference`
   * `android.preference.SwitchPreference`
   * `android.preference.TwoStatePreference`
   * `android.util.AttributeSet`
   * `android.util.Pair`
 * Added convenience methods for orientations to `Display`, `LinearLayout`, and
   `GridLayout`.
 * Added error and ellipsis checks for `TextView`.
 * Added column name checks for `Cursor`.
 * `LinearLayout` and `AdapterView` assertions now correctly extend from `ViewGroup` assertions.
 * Added `TextView` text assertions for empty, contains, starts with, and ends with.
 * Added general `hasVisibility(int)` assertion for `View`.
 * Correct spelling of `isNotInvisible` assertions for `View`.
 * Support for generics by assertions classes (e.g., `LruCacheAssert<K, V>`).
 * Support using string resource ID for most text assertions.


Version 1.0.0 *(2013-01-17)*
----------------------------

Initial release.

Releasing
========

 1. Change the version in `gradle.properties` to a non-SNAPSHOT version.
 2. Update the `CHANGELOG.md` for the impending release.
 3. Update the `README.md` with the new version.
 4. `git commit -am "Prepare for release X.Y.Z."` (where X.Y.Z is the new version)
 5. `git tag -a X.Y.X -m "Version X.Y.Z"` (where X.Y.Z is the new version)
 6. `./gradlew clean uploadArchives`
 7. Update the `gradle.properties` to the next SNAPSHOT version.
 8. `git commit -am "Prepare next development version."`
 9. `git push && git push --tags`
 10. Visit [Sonatype Nexus](https://oss.sonatype.org/) and promote the artifact.
