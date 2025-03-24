# Contributors

Caffe is developed by a core set of BAIR members and the open-source community.

We thank all of our [contributors](https://github.com/BVLC/caffe/graphs/contributors)!

**For the detailed history of contributions** of a given file, try

    git blame file

to see line-by-line credits and

    git log --follow file

to see the change log even across renames and rewrites.

Please refer to the [acknowledgements](http://caffe.berkeleyvision.org/#acknowledgements) on the Caffe site for further details.

**Copyright** is held by the original contributor according to the versioning history; see LICENSE.
# Caffe

[![License](https://img.shields.io/badge/license-BSD-blue.svg)](LICENSE)

Caffe is a deep learning framework made with expression, speed, and modularity in mind.
It is developed by Berkeley AI Research ([BAIR](http://bair.berkeley.edu))/The Berkeley Vision and Learning Center (BVLC) and community contributors.

Check out the [project site](http://caffe.berkeleyvision.org) for all the details like

- [DIY Deep Learning for Vision with Caffe](https://docs.google.com/presentation/d/1UeKXVgRvvxg9OUdh_UiC5G71UMscNPlvArsWER41PsU/edit#slide=id.p)
- [Tutorial Documentation](http://caffe.berkeleyvision.org/tutorial/)
- [BAIR reference models](http://caffe.berkeleyvision.org/model_zoo.html) and the [community model zoo](https://github.com/BVLC/caffe/wiki/Model-Zoo)
- [Installation instructions](http://caffe.berkeleyvision.org/installation.html)

and step-by-step examples.

## Windows Setup
**Requirements**: Visual Studio 2015, CUDA 9.0, third party libraries: [Baidu Yun](https://pan.baidu.com/s/1ZTp8iWszMPrZ718w_UCZ5Q) or [Google Drive](https://drive.google.com/file/d/13dbvXmMosxozWbSgJdDdxH62YWqXLjoJ/view?usp=sharing). Please extract the archive into `./windows/thirdparty/`. Then, add the folder `./windows/thirdparty/bins` to the environment variable `PATH`.

### Pre-Build Steps
Copy `.\windows\CommonSettings.props.example` to `.\windows\CommonSettings.props`

By defaults Windows build requires `CUDA` and `cuDNN` libraries.
Both can be disabled by adjusting build variables in `.\windows\CommonSettings.props`.
Python support is disabled by default, but can be enabled via `.\windows\CommonSettings.props` as well.

### CUDA
Download `CUDA Toolkit 8.0` [from nVidia website](https://developer.nvidia.com/cuda-toolkit).
If you don't have CUDA installed, you can experiment with CPU_ONLY build.
In `.\windows\CommonSettings.props` set `CpuOnlyBuild` to `true` and set `UseCuDNN` & `UseNCCL` to `false`.

### cuDNN
Download `cuDNN v5` [from nVidia website](https://developer.nvidia.com/cudnn).
Unpack downloaded zip to %CUDA_PATH% (environment variable set by CUDA installer).
Alternatively, you can unpack zip to any location and set `CuDnnPath` to point to this location in `.\windows\CommonSettings.props`.
`CuDnnPath` defined in `.\windows\CommonSettings.props`.
Also, you can disable cuDNN by setting `UseCuDNN` to `false` in the property file.

### Python
To build Caffe Python wrapper set `PythonSupport` to `true` in `.\windows\CommonSettings.props`.
Download Miniconda 2.7 64-bit Windows installer [from Miniconda website] (http://conda.pydata.org/miniconda.html).
Install for all users and add Python to PATH (through installer).

Run the following commands from elevated command prompt:

```
conda install --yes numpy scipy matplotlib scikit-image pip
pip install protobuf
```

#### Remark
After you have built solution with Python support, in order to use it you have to either:  
* set `PythonPath` environment variable to point to `<caffe_root>\Build\x64\Release\pycaffe`, or
* copy folder `<caffe_root>\Build\x64\Release\pycaffe\caffe` under `<python_root>\lib\site-packages`.

### Matlab
To build Caffe Matlab wrapper set `MatlabSupport` to `true` and `MatlabDir` to the root of your Matlab installation in `.\windows\CommonSettings.props`.

#### Remark
After you have built solution with Matlab support, in order to use it you have to add the `./matlab` folder to Matlab search path.

### Build
Now, you should be able to build `.\windows\Caffe.sln`

## License and Citation

Caffe is released under the [BSD 2-Clause license](https://github.com/BVLC/caffe/blob/master/LICENSE).
The BAIR/BVLC reference models are released for unrestricted use.

Please cite Caffe in your publications if it helps your research:

    @article{jia2014caffe,
      Author = {Jia, Yangqing and Shelhamer, Evan and Donahue, Jeff and Karayev, Sergey and Long, Jonathan and Girshick, Ross and Guadarrama, Sergio and Darrell, Trevor},
      Journal = {arXiv preprint arXiv:1408.5093},
      Title = {Caffe: Convolutional Architecture for Fast Feature Embedding},
      Year = {2014}
    }
FAQ for caffe-windows
================

 - How to use the static library `caffelib.lib` in my own project?
 
   Directly link the `caffelib.lib` may lead the compiler ignore the layer and solver register macros. When loading a layer or solver,
   similar error will be reported:
   ```
   check failed: registry.count(type)==1(0 vs 1)unknown layer type:convolution
   ```
   There are two ways to solve this problem. One is to add the caffelib project to your own solution, and open the property window of
   your project set
   `Common Property` - `Reference` - `caffelib` - `Project Reference Property` - `Library Dependency Link`: True .
   
   Another method is to add `layer_factory.cpp` and `force_link.cpp` to your own project, to let the compiler know the existence of
   the layers and solvers. However, when using this method, the layers will be registered twice and you will get an error in `include/caffe/layer_factory.hpp` line `68`. To fix this error, you can just remove line `68-69` or use `if(registry.count(type) > 0) continue;` to replace the `CHECK` statement.
   
   If you came across similar error when using `caffe.exe`, I guess you may have modified the `.vcxproj` files manually by yourself. VS lost some configurations during your modification. Never mind, you can still follow the above instructions to fix it.
   
 - How to compile the codes in Debug mode?
   
  There is a [3rdparty library archive file](http://pan.baidu.com/s/1qW88MTY) provided by a friend of me. However, I haven't tested it.

  You can compile your own third party libraries from https://github.com/willyd/caffe-windows-dependencies . This way is the most recommended, because you can better understand Visual Studio during configuring so much applications.
  
  In addition, you can still debug the codes in Release mode, by following the instructions here https://msdn.microsoft.com/en-us/library/fsk896zz.aspx .

 - How can I create other tools, such as `extract_features.cpp` and `cpp_classification.cpp`?
  
  I have only created projects which is used most frequently in my eyes. If you want to compile other tools, there is no need to create a new project. You can just copy and rename `./build/MSVC` folder to another one, and add the new project to the VS solution. Remove `caffe.cpp` and add your target cpp file. Compile it, then you will get a corresponding exe file in `./bin`.

 - Why can't my VS open the projects?
  
  This is mainly because your CUDA version is different from mine, CUDA 7.0. You can modify the CUDA configurations in the `.vcxproj` file manually by open each `.vcxproj` with notepad or other text processor. 

  However, manually modifying the project file may destroy some of the configurations. Someone reported that the reference relationship between the projects was lost after they modified the project files. You may refer to the second question to solve this problem.
cmake_minimum_required(VERSION 2.8.7)
if(POLICY CMP0046)
  cmake_policy(SET CMP0046 NEW)
endif()
if(POLICY CMP0054)
  cmake_policy(SET CMP0054 NEW)
endif()

# ---[ Caffe project
project(Caffe C CXX)

# ---[ Caffe version
set(CAFFE_TARGET_VERSION "1.0.0" CACHE STRING "Caffe logical version")
set(CAFFE_TARGET_SOVERSION "1.0.0" CACHE STRING "Caffe soname version")
add_definitions(-DCAFFE_VERSION=${CAFFE_TARGET_VERSION})

# ---[ Using cmake scripts and modules
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/Modules)

include(ExternalProject)
include(GNUInstallDirs)

include(cmake/Utils.cmake)
include(cmake/Targets.cmake)
include(cmake/Misc.cmake)
include(cmake/Summary.cmake)
include(cmake/ConfigGen.cmake)

# ---[ Options
caffe_option(CPU_ONLY  "Build Caffe without CUDA support" OFF) # TODO: rename to USE_CUDA
caffe_option(USE_CUDNN "Build Caffe with cuDNN library support" ON IF NOT CPU_ONLY)
caffe_option(USE_NCCL "Build Caffe with NCCL library support" OFF)
caffe_option(BUILD_SHARED_LIBS "Build shared libraries" ON)
caffe_option(BUILD_python "Build Python wrapper" ON)
set(python_version "2" CACHE STRING "Specify which Python version to use")
caffe_option(BUILD_matlab "Build Matlab wrapper" OFF IF UNIX OR APPLE)
caffe_option(BUILD_docs   "Build documentation" ON IF UNIX OR APPLE)
caffe_option(BUILD_python_layer "Build the Caffe Python layer" ON)
caffe_option(USE_OPENCV "Build with OpenCV support" ON)
caffe_option(USE_LEVELDB "Build with levelDB" ON)
caffe_option(USE_LMDB "Build with lmdb" ON)
caffe_option(ALLOW_LMDB_NOLOCK "Allow MDB_NOLOCK when reading LMDB files (only if necessary)" OFF)
caffe_option(USE_OPENMP "Link with OpenMP (when your BLAS wants OpenMP and you get linker errors)" OFF)

# ---[ Dependencies
include(cmake/Dependencies.cmake)

# ---[ Flags
if(UNIX OR APPLE)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -Wall")
endif()

caffe_set_caffe_link()

if(USE_libstdcpp)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libstdc++")
  message("-- Warning: forcing libstdc++ (controlled by USE_libstdcpp option in cmake)")
endif()

# ---[ Warnings
caffe_warnings_disable(CMAKE_CXX_FLAGS -Wno-sign-compare -Wno-uninitialized)

# ---[ Config generation
configure_file(cmake/Templates/caffe_config.h.in "${PROJECT_BINARY_DIR}/caffe_config.h")

# ---[ Includes
set(Caffe_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/include)
set(Caffe_SRC_DIR ${PROJECT_SOURCE_DIR}/src)
include_directories(${PROJECT_BINARY_DIR})

# ---[ Includes & defines for CUDA

# cuda_compile() does not have per-call dependencies or include pathes
# (cuda_compile() has per-call flags, but we set them here too for clarity)
#
# list(REMOVE_ITEM ...) invocations remove PRIVATE and PUBLIC keywords from collected definitions and include pathes
if(HAVE_CUDA)
  # pass include pathes to cuda_include_directories()
  list(APPEND Caffe_INCLUDE_DIRS PRIVATE ${PROJECT_SOURCE_DIR}/3rdparty)
  set(Caffe_ALL_INCLUDE_DIRS ${Caffe_INCLUDE_DIRS})
  list(REMOVE_ITEM Caffe_ALL_INCLUDE_DIRS PRIVATE PUBLIC)
  cuda_include_directories(${Caffe_INCLUDE_DIR} ${Caffe_SRC_DIR} ${Caffe_ALL_INCLUDE_DIRS})

  # add definitions to nvcc flags directly
  set(Caffe_ALL_DEFINITIONS ${Caffe_DEFINITIONS})
  list(REMOVE_ITEM Caffe_ALL_DEFINITIONS PRIVATE PUBLIC)
  list(APPEND CUDA_NVCC_FLAGS ${Caffe_ALL_DEFINITIONS})
endif()

if(NOT MSVC)
  cmake_minimum_required(VERSION 3.3)
  include(CheckCXXCompilerFlag)
  check_cxx_compiler_flag("-std=c++11"   SUPPORT_CXX11)
  if(SUPPORT_CXX11)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
  else(SUPPORT_CXX11)
    message(ERROR "I write lots of c++11 codes. Please update your gcc to version 4.8 or higher.")
  endif()
endif()

# ---[ Subdirectories
add_subdirectory(src/gtest)
add_subdirectory(src/caffe)
add_subdirectory(tools)
add_subdirectory(examples)
add_subdirectory(python)
add_subdirectory(matlab)
add_subdirectory(docs)

# ---[ Linter target
add_custom_target(lint COMMAND ${CMAKE_COMMAND} -P ${PROJECT_SOURCE_DIR}/cmake/lint.cmake)

# ---[ pytest target
if(BUILD_python)
  add_custom_target(pytest COMMAND python${python_version} -m unittest discover -s caffe/test WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/python )
  add_dependencies(pytest pycaffe)
endif()

# ---[ uninstall target
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/Uninstall.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/cmake/Uninstall.cmake
    IMMEDIATE @ONLY)

add_custom_target(uninstall
    COMMAND ${CMAKE_COMMAND} -P
    ${CMAKE_CURRENT_BINARY_DIR}/cmake/Uninstall.cmake)

# ---[ Configuration summary
caffe_print_configuration_summary()

# ---[ Export configs generation
caffe_generate_export_configs()

# Installation

See http://caffe.berkeleyvision.org/installation.html for the latest
installation instructions.

Check the users group in case you need help:
https://groups.google.com/forum/#!forum/caffe-users
# Contributing

## Issues

Specific Caffe design and development issues, bugs, and feature requests are maintained by GitHub Issues.

_Please do not post usage, installation, or modeling questions, or other requests for help to Issues._
Use the [caffe-users list](https://groups.google.com/forum/#!forum/caffe-users) instead. This helps developers maintain a clear, uncluttered, and efficient view of the state of Caffe.

When reporting a bug, it's most helpful to provide the following information, where applicable:

* What steps reproduce the bug?
* Can you reproduce the bug using the latest [master](https://github.com/BVLC/caffe/tree/master), compiled with the `DEBUG` make option?
* What hardware and operating system/distribution are you running?
* If the bug is a crash, provide the backtrace (usually printed by Caffe; always obtainable with `gdb`).

Try to give your issue a title that is succinct and specific. The devs will rename issues as needed to keep track of them.

## Pull Requests

Caffe welcomes all contributions.

See the [contributing guide](http://caffe.berkeleyvision.org/development.html) for details.

Briefly: read commit by commit, a PR should tell a clean, compelling story of _one_ improvement to Caffe. In particular:

* A PR should do one clear thing that obviously improves Caffe, and nothing more. Making many smaller PRs is better than making one large PR; review effort is superlinear in the amount of code involved.
* Similarly, each commit should be a small, atomic change representing one step in development. PRs should be made of many commits where appropriate.
* Please do rewrite PR history to be clean rather than chronological. Within-PR bugfixes, style cleanups, reversions, etc. should be squashed and should not appear in merged PR history.
* Anything nonobvious from the code should be explained in comments, commit messages, or the PR description, as appropriate.
COPYRIGHT

All contributions by the University of California:
Copyright (c) 2014-2017 The Regents of the University of California (Regents)
All rights reserved.

All other contributions:
Copyright (c) 2014-2017, the respective contributors
All rights reserved.

Caffe uses a shared copyright model: each contributor holds copyright over
their contributions to Caffe. The project versioning records all such
contribution and copyright details. If a contributor wants to further mark
their specific copyright on a particular contribution, they should indicate
their copyright solely in the commit message of the change when it is
committed.

LICENSE

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

CONTRIBUTION AGREEMENT

By contributing to the BVLC/caffe repository through pull-request, comment,
or otherwise, the contributor releases their content to the
license and copyright terms herein.
# Collect source files
file(GLOB_RECURSE srcs ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp)

# Build each source file independently
foreach(source ${srcs})
  get_filename_component(name ${source} NAME_WE)

  # caffe target already exits
  if(name MATCHES "caffe")
    set(name ${name}.bin)
  endif()

  # target
  add_executable(${name} ${source})
  target_link_libraries(${name} ${Caffe_LINK})
  caffe_default_properties(${name})

  # set back RUNTIME_OUTPUT_DIRECTORY
  caffe_set_runtime_directory(${name} "${PROJECT_BINARY_DIR}/tools")
  caffe_set_solution_folder(${name} tools)

  # restore output name without suffix
  if(name MATCHES "caffe.bin")
    set_target_properties(${name} PROPERTIES OUTPUT_NAME caffe)
  endif()

  # Install
  install(TARGETS ${name} DESTINATION ${CMAKE_INSTALL_BINDIR})

endforeach(source)
---
name: BAIR/BVLC Reference RCNN ILSVRC13 Model
caffemodel: bvlc_reference_rcnn_ilsvrc13.caffemodel
caffemodel_url: http://dl.caffe.berkeleyvision.org/bvlc_reference_rcnn_ilsvrc13.caffemodel
license: unrestricted
sha1: bdd8abb885819cba5e2fe1eb36235f2319477e64
caffe_commit: a7e397abbda52c0b90323c23ab95bdeabee90a98
---

The pure Caffe instantiation of the [R-CNN](https://github.com/rbgirshick/rcnn) model for ILSVRC13 detection.
This model was made by transplanting the R-CNN SVM classifiers into a `fc-rcnn` classification layer, provided here as an off-the-shelf Caffe detector.
Try the [detection example](http://nbviewer.ipython.org/github/BVLC/caffe/blob/master/examples/detection.ipynb) to see it in action.

*N.B. For research purposes, make use of the official R-CNN package and not this example.*

This model was trained by Ross Girshick @rbgirshick

## License

This model is released for unrestricted use.
---
name: BAIR/BVLC CaffeNet Model
caffemodel: bvlc_reference_caffenet.caffemodel
caffemodel_url: http://dl.caffe.berkeleyvision.org/bvlc_reference_caffenet.caffemodel
license: unrestricted
sha1: 4c8d77deb20ea792f84eb5e6d0a11ca0a8660a46
caffe_commit: 709dc15af4a06bebda027c1eb2b3f3e3375d5077
---

This model is the result of following the Caffe [ImageNet model training instructions](http://caffe.berkeleyvision.org/gathered/examples/imagenet.html).
It is a replication of the model described in the [AlexNet](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks) publication with some differences:

- not training with the relighting data-augmentation;
- the order of pooling and normalization layers is switched (in CaffeNet, pooling is done before normalization).

This model is snapshot of iteration 310,000.
The best validation performance during training was iteration 313,000 with validation accuracy 57.412% and loss 1.82328.
This model obtains a top-1 accuracy 57.4% and a top-5 accuracy 80.4% on the validation set, using just the center crop.
(Using the average of 10 crops, (4 + 1 center) * 2 mirror, should obtain a bit higher accuracy still.)

This model was trained by Jeff Donahue @jeffdonahue

## License

This model is released for unrestricted use.
---
name: BAIR/BVLC GoogleNet Model
caffemodel: bvlc_googlenet.caffemodel
caffemodel_url: http://dl.caffe.berkeleyvision.org/bvlc_googlenet.caffemodel
license: unrestricted
sha1: 405fc5acd08a3bb12de8ee5e23a96bec22f08204
caffe_commit: bc614d1bd91896e3faceaf40b23b72dab47d44f5
---

This model is a replication of the model described in the [GoogleNet](http://arxiv.org/abs/1409.4842) publication. We would like to thank Christian Szegedy for all his help in the replication of GoogleNet model.

Differences:
- not training with the relighting data-augmentation;
- not training with the scale or aspect-ratio data-augmentation;
- uses "xavier" to initialize the weights instead of "gaussian";
- quick_solver.prototxt uses a different learning rate decay policy than the original solver.prototxt, that allows a much faster training (60 epochs vs 250 epochs);

The bundled model is the iteration 2,400,000 snapshot (60 epochs) using quick_solver.prototxt

This bundled model obtains a top-1 accuracy 68.7% (31.3% error) and a top-5 accuracy 88.9% (11.1% error) on the validation set, using just the center crop.
(Using the average of 10 crops, (4 + 1 center) * 2 mirror, should obtain a bit higher accuracy.)

Timings for bvlc_googlenet with cuDNN using batch_size:128 on a K40c:
 - Average Forward pass: 562.841 ms.
 - Average Backward pass: 1123.84 ms.
 - Average Forward-Backward: 1688.8 ms.

This model was trained by Sergio Guadarrama @sguada

## License

This model is released for unrestricted use.
---
name: Finetuning CaffeNet on Flickr Style
caffemodel: finetune_flickr_style.caffemodel
caffemodel_url: http://dl.caffe.berkeleyvision.org/finetune_flickr_style.caffemodel
license: non-commercial
sha1: b61b5cef7d771b53b0c488e78d35ccadc073e9cf
caffe_commit: 737ea5e936821b5c69f9c3952d72693ae5843370
gist_id: 034c6ac3865563b69e60
---

This model is trained exactly as described in `docs/finetune_flickr_style/readme.md`, using all 80000 images.
The final performance:

    I1017 07:36:17.370688 31333 solver.cpp:228] Iteration 100000, loss = 0.757952
    I1017 07:36:17.370730 31333 solver.cpp:247] Iteration 100000, Testing net (#0)
    I1017 07:36:34.248730 31333 solver.cpp:298]     Test net output #0: accuracy = 0.3916

This model was trained by Sergey Karayev @sergeyk

## License

The Flickr Style dataset contains only URLs to images.
Some of the images may have copyright.
Training a category-recognition model for research/non-commercial use may constitute fair use of this data, but the result should not be used for commercial purposes.
---
name: BAIR/BVLC AlexNet Model
caffemodel: bvlc_alexnet.caffemodel
caffemodel_url: http://dl.caffe.berkeleyvision.org/bvlc_alexnet.caffemodel
license: unrestricted
sha1: 9116a64c0fbe4459d18f4bb6b56d647b63920377
caffe_commit: 709dc15af4a06bebda027c1eb2b3f3e3375d5077
---

This model is a replication of the model described in the [AlexNet](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks) publication.

Differences:
- not training with the relighting data-augmentation;
- initializing non-zero biases to 0.1 instead of 1 (found necessary for training, as initialization to 1 gave flat loss).

The bundled model is the iteration 360,000 snapshot.
The best validation performance during training was iteration 358,000 with validation accuracy 57.258% and loss 1.83948.
This model obtains a top-1 accuracy 57.1% and a top-5 accuracy 80.2% on the validation set, using just the center crop.
(Using the average of 10 crops, (4 + 1 center) * 2 mirror, should obtain a bit higher accuracy.)

This model was trained by Evan Shelhamer @shelhamer

## License

This model is released for unrestricted use.
# Builds Matlab (or Octave) interface. In case of Matlab caffe must be
# compield as shared library. Octave can link static or shared caffe library
# To install octave run: sudo apt-get install liboctave-dev

if(NOT BUILD_matlab)
  return()
endif()

if(HAVE_MATLAB AND Octave_compiler)
  set(build_using ${Matlab_build_mex_using})
elseif(HAVE_MATLAB AND NOT Octave_compiler)
  set(build_using "Matlab")
elseif(NOT HAVE_MATLAB AND Octave_compiler)
  set(build_using "Octave")
else()
  return()
endif()

if(NOT BUILD_SHARED_LIBS AND build_using MATCHES Matlab)
  message(FATAL_ERROR "Matlab MEX interface (with default mex options file) can only be built if caffe is compiled as shared library. Please enable 'BUILD_SHARED_LIBS' in CMake. Aternativelly you can switch to Octave compiler.")
endif()

# helper function to set proper mex file extension
function(caffe_fetch_and_set_proper_mexext mexfile_variable)
  execute_process(COMMAND ${Matlab_mexext} OUTPUT_STRIP_TRAILING_WHITESPACE RESULT_VARIABLE res OUTPUT_VARIABLE ext)
  if(res MATCHES 0)
    get_filename_component(folder  ${${mexfile_variable}} PATH)
    get_filename_component(name_we ${${mexfile_variable}} NAME_WE)
    set(${mexfile_variable} ${folder}/${name_we}.${ext} PARENT_SCOPE)
  endif()
endfunction()

# global settings
file(GLOB Matlab_srcs +caffe/private/caffe_.cpp)
set(Matlab_caffe_mex ${PROJECT_SOURCE_DIR}/matlab/+caffe/private/caffe_.mex)

caffe_get_current_cflags(cflags)
caffe_parse_linker_libs(Caffe_LINKER_LIBS folders libflags macos_frameworks)
set(folders $<TARGET_LINKER_FILE_DIR:caffe> ${folders})

# prepare linker flag lists
string(REPLACE ";" ";-L" link_folders "-L${folders}")
string(REPLACE ";" ":"  rpath_folders   "${folders}")

if(build_using MATCHES "Matlab")
  set(libflags -lcaffe${CAffe_POSTFIX} ${libflags}) # Matlab R2014a complans for -Wl,--whole-archive

  caffe_fetch_and_set_proper_mexext(Matlab_caffe_mex)
  add_custom_command(OUTPUT ${Matlab_caffe_mex} COMMAND ${Matlab_mex}
      ARGS -output ${Matlab_caffe_mex} ${Matlab_srcs} ${cflags} ${link_folders} ${libflags}
      DEPENDS caffe COMMENT "Building Matlab interface: ${Matlab_caffe_mex}" VERBATIM)
  add_custom_target(matlab ALL DEPENDS ${Matlab_caffe_mex} SOURCES ${Matlab_srcs})

elseif(build_using MATCHES "Octave")

  if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
    set(libflags -Wl,-force_load,$<TARGET_LINKER_FILE:caffe> ${libflags})
  elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
    set(libflags -Wl,--whole-archive -lcaffe${CAffe_POSTFIX} -Wl,--no-whole-archive ${libflags})
  endif()

  add_custom_command(OUTPUT ${Matlab_caffe_mex} COMMAND ${Octave_compiler}
      ARGS --mex -o ${Matlab_caffe_mex} ${Matlab_srcs} ${cflags} ${link_folders} ${libflags} -Wl,-rpath,${rpath_folders}
      DEPENDS caffe COMMENT "Building Octave interface: ${Matlab_caffe_mex}" VERBATIM)

  add_custom_target(octave ALL DEPENDS ${Matlab_caffe_mex} SOURCES ${Matlab_srcs})
endif()

# ---[ Install
file(GLOB mfiles caffe/*.m)
install(FILES ${mfiles} ${Matlab_caffe_mex} DESTINATION matlab)

### Running an official image

You can run one of the automatic [builds](https://hub.docker.com/r/bvlc/caffe). E.g. for the CPU version:

`docker run -ti bvlc/caffe:cpu caffe --version`

or for GPU support (You need a CUDA 8.0 capable driver and
[nvidia-docker](https://github.com/NVIDIA/nvidia-docker)):

`nvidia-docker run -ti bvlc/caffe:gpu caffe --version`

You might see an error about libdc1394, ignore it.

### Docker run options

By default caffe runs as root, thus any output files, e.g. snapshots, will be owned
by root. It also runs by default in a container-private folder.

You can change this using flags, like user (-u), current directory, and volumes (-w and -v).
E.g. this behaves like the usual caffe executable:

`docker run --rm -u $(id -u):$(id -g) -v $(pwd):$(pwd) -w $(pwd) bvlc/caffe:cpu caffe train --solver=example_solver.prototxt`

Containers can also be used interactively, specifying e.g. `bash` or `ipython`
instead of `caffe`.

```
docker run -ti bvlc/caffe:cpu ipython
import caffe
...
```

The caffe build requirements are included in the container, so this can be used to
build and run custom versions of caffe. Also, `caffe/python` is in PATH, so python
utilities can be used directly, e.g. `draw_net.py`, `classify.py`, or `detect.py`.

### Building images yourself

Examples:

`docker build -t caffe:cpu cpu`

`docker build -t caffe:gpu gpu`

You can also build Caffe and run the tests in the image:

`docker run -ti caffe:cpu bash -c "cd /opt/caffe/build; make runtest"`
---
title: "Installation: RHEL / Fedora / CentOS"
---

# RHEL / Fedora / CentOS Installation

**General dependencies**

    sudo yum install protobuf-devel leveldb-devel snappy-devel opencv-devel boost-devel hdf5-devel

**Remaining dependencies, recent OS**

    sudo yum install gflags-devel glog-devel lmdb-devel

**Remaining dependencies, if not found**

    # glog
    wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/google-glog/glog-0.3.3.tar.gz
    tar zxvf glog-0.3.3.tar.gz
    cd glog-0.3.3
    ./configure
    make && make install
    # gflags
    wget https://github.com/schuhschuh/gflags/archive/master.zip
    unzip master.zip
    cd gflags-master
    mkdir build && cd build
    export CXXFLAGS="-fPIC" && cmake .. && make VERBOSE=1
    make && make install
    # lmdb
    git clone https://github.com/LMDB/lmdb
    cd lmdb/libraries/liblmdb
    make && make install

Note that glog does not compile with the most recent gflags version (2.1), so before that is resolved you will need to build with glog first.

**CUDA**: Install via the NVIDIA package instead of `yum` to be certain of the library and driver versions.
Install the library and latest driver separately; the driver bundled with the library is usually out-of-date.
    + CentOS/RHEL/Fedora:

**BLAS**: install ATLAS by `sudo yum install atlas-devel` or install OpenBLAS or MKL for better CPU performance. For the Makefile build, uncomment and set `BLAS_LIB` accordingly as ATLAS is usually installed under `/usr/lib[64]/atlas`).

**Python** (optional): if you use the default Python you will need to `sudo yum install` the `python-devel` package to have the Python headers for building the pycaffe wrapper.

Continue with [compilation](installation.html#compilation).
# Caffe Documentation

To generate the documentation, run `$CAFFE_ROOT/scripts/build_docs.sh`.

To push your changes to the documentation to the gh-pages branch of your or the BVLC repo, run `$CAFFE_ROOT/scripts/deploy_docs.sh <repo_name>`.
---
title: "Installation: Debian"
---

# Debian Installation

Caffe packages are available for several Debian versions, as shown in the
following chart:

```
Your Distro     |  CPU_ONLY  |  CUDA  | Codename
----------------+------------+--------+-------------------
Debian/oldstable|     ✘      |   ✘    | Jessie (8.0)
Debian/stable   |     ✔      |   ✔    | Stretch (9.0)
Debian/testing  |     ✔      |   ✔    | Buster
Debian/unstable |     ✔      |   ✔    | Buster
```

* `✘ ` You should take a look at [Ubuntu installation instruction](install_apt.html).

* `✔ ` You can install caffe with a single command line following this guide.

* [Package status of CPU-only version](https://tracker.debian.org/pkg/caffe)

* [Package status of CUDA version](https://tracker.debian.org/pkg/caffe-contrib)

Last update: 2017-07-08

## Binary installation with APT

Apart from the installation methods based on source, Debian users can install
pre-compiled Caffe packages from the official archive with APT.

Make sure that your `/etc/apt/sources.list` contains `contrib` and `non-free`
sections if you want to install the CUDA version, for instance:

```
deb http://ftp2.cn.debian.org/debian sid main contrib non-free
```

Then we update APT cache and directly install Caffe. Note, the cpu version and
the cuda version cannot coexist.

```
$ sudo apt update
$ sudo apt install [ caffe-cpu | caffe-cuda ]
$ caffe                                              # command line interface working
$ python3 -c 'import caffe; print(caffe.__path__)'   # python3 interface working
```

These Caffe packages should work for you out of box. However, the CUDA version
may break if your NVIDIA driver and CUDA toolkit are not installed with APT.

#### Customizing caffe packages

Some users may need to customize the Caffe package. The way to customize
the package is beyond this guide. Here is only a brief guide of producing
the customized `.deb` packages. 

Make sure that there is a `dec-src` source in your `/etc/apt/sources.list`,
for instance:

```
deb http://ftp2.cn.debian.org/debian sid main contrib non-free
deb-src http://ftp2.cn.debian.org/debian sid main contrib non-free
```

Then we build caffe deb files with the following commands:

```
$ sudo apt update
$ sudo apt install build-essential debhelper devscripts  # standard package building tools
$ sudo apt build-dep [ caffe-cpu | caffe-cuda ]          # the most elegant way to pull caffe build dependencies
$ apt source [ caffe-cpu | caffe-cuda ]                  # download the source tarball and extract
$ cd caffe-XXXX
[ ... optional, customizing caffe code/build ... ]
$ dch --local "Modified XXX"                             # bump package version and write changelog
$ debuild -B -j4                                         # build caffe with 4 parallel jobs (similar to make -j4)
[ ... building ...]
$ debc                                                   # optional, if you want to check the package contents
$ sudo debi                                              # optional, install the generated packages
$ ls ../                                                 # optional, you will see the resulting packages
```

It is a BUG if the package failed to build without any change.
The changelog will be installed at e.g. `/usr/share/doc/caffe-cpu/changelog.Debian.gz`.

## Source installation

Source installation under Debian/unstable and Debian/testing is similar to that of Ubuntu, but
here is a more elegant way to pull caffe build dependencies:

```
$ sudo apt build-dep [ caffe-cpu | caffe-cuda ]
```

Note, this requires a `deb-src` entry in your `/etc/apt/sources.list`.

#### Compiler Combinations

Some users may find their favorate compiler doesn't work with CUDA.

```
CXX compiler |  CUDA 7.5  |  CUDA 8.0  |  CUDA 9.0  |
-------------+------------+------------+------------+
GCC-8        |     ?      |     ?      |     ?      |
GCC-7        |     ?      |     ?      |     ?      |
GCC-6        |     ✘      |     ✘      |     ✔      |
GCC-5        |     ✔ [1]  |     ✔      |     ✔      |
-------------+------------+------------+------------+
CLANG-4.0    |     ?      |     ?      |     ?      |
CLANG-3.9    |     ✘      |     ✘      |     ✔      |
CLANG-3.8    |     ?      |     ✔      |     ✔      |
```

`[1]` CUDA 7.5 's `host_config.h` must be patched before working with GCC-5.

`[2]` CUDA 9.0: https://devblogs.nvidia.com/parallelforall/cuda-9-features-revealed/

BTW, please forget the GCC-4.X series, since its `libstdc++` ABI is not compatible with GCC-5's.
You may encounter failure linking GCC-4.X object files against GCC-5 libraries.
(See https://wiki.debian.org/GCC5 )

## Notes

* Consider re-compiling OpenBLAS locally with optimization flags for sake of
performance. This is highly recommended for any kind of production use, including
academic research.

* If you are installing `caffe-cuda`, APT will automatically pull some of the
CUDA packages and the nvidia driver packages. Please be careful if you have
manually installed or hacked nvidia driver or CUDA toolkit or any other
related stuff, because in this case APT may fail.

* Additionally, a manpage (`man caffe`) and a bash complementation script
(`caffe <TAB><TAB>`, `caffe train <TAB><TAB>`) are provided.
Both of the two files are still not merged into caffe master.

* The python interface is Python 3 version: `python3-caffe-{cpu,cuda}`.
No plan to support python2.

* If you encountered any problem related to the packaging system (e.g. failed to install `caffe-*`),
please report bug to Debian via Debian's bug tracking system. See https://www.debian.org/Bugs/ .
Patches and suggestions are also welcome.

## FAQ

* where is caffe-cudnn?

CUDNN library seems not redistributable currently. If you really want the
caffe-cudnn deb packages, the workaround is to install cudnn by yourself,
and hack the packaging scripts, then build your customized package.

* I installed the CPU version. How can I switch to the CUDA version?

`sudo apt install caffe-cuda`, apt's dependency resolver is smart enough to deal with this.

* Where are the examples, the models and other documentation stuff?

```
$ sudo apt install caffe-doc
$ dpkg -L caffe-doc
```
# Building docs script
# Requirements:
#   sudo apt-get install doxygen texlive ruby-dev
#   sudo gem install jekyll execjs therubyracer

if(NOT BUILD_docs OR NOT DOXYGEN_FOUND)
  return()
endif()

#################################################################################################
# Gather docs from <root>/examples/**/readme.md
function(gather_readmes_as_prebuild_cmd target gathered_dir root)
  set(full_gathered_dir ${root}/${gathered_dir})

  file(GLOB_RECURSE readmes ${root}/examples/readme.md ${root}/examples/README.md)
  foreach(file ${readmes})
    # Only use file if it is to be included in docs.
    file(STRINGS ${file} file_lines REGEX "include_in_docs: true")

    if(file_lines)
      # Since everything is called readme.md, rename it by its dirname.
      file(RELATIVE_PATH file ${root} ${file})
      get_filename_component(folder ${file} PATH)
      set(new_filename ${full_gathered_dir}/${folder}.md)

      # folder value might be like <subfolder>/readme.md. That's why make directory.
      get_filename_component(new_folder ${new_filename} PATH)
      add_custom_command(TARGET ${target} PRE_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory ${new_folder}
        COMMAND ln -sf ${root}/${file} ${new_filename}
        COMMENT "Creating symlink ${new_filename} -> ${root}/${file}"
        WORKING_DIRECTORY ${root} VERBATIM)
    endif()
  endforeach()
endfunction()

################################################################################################
# Gather docs from examples/*.ipynb and add YAML front-matter.
function(gather_notebooks_as_prebuild_cmd target gathered_dir root)
  set(full_gathered_dir ${root}/${gathered_dir})

  if(NOT PYTHON_EXECUTABLE)
    message(STATUS "Python interpeter is not found. Can't include *.ipynb files in docs. Skipping...")
    return()
  endif()

  file(GLOB_RECURSE notebooks ${root}/examples/*.ipynb)
  foreach(file ${notebooks})
    file(RELATIVE_PATH file ${root} ${file})
    set(new_filename ${full_gathered_dir}/${file})

    get_filename_component(new_folder ${new_filename} PATH)
    add_custom_command(TARGET ${target} PRE_BUILD
      COMMAND ${CMAKE_COMMAND} -E make_directory ${new_folder}
      COMMAND ${PYTHON_EXECUTABLE} scripts/copy_notebook.py ${file} ${new_filename}
      COMMENT "Copying notebook ${file} to ${new_filename}"
      WORKING_DIRECTORY ${root} VERBATIM)
  endforeach()

  set(${outputs_var} ${outputs} PARENT_SCOPE)
endfunction()

################################################################################################
########################## [ Non macro part ] ##################################################

# Gathering is done at each 'make doc'
file(REMOVE_RECURSE ${PROJECT_SOURCE_DIR}/docs/gathered)

# Doxygen config file path
set(DOXYGEN_config_file ${PROJECT_SOURCE_DIR}/.Doxyfile CACHE FILEPATH "Doxygen config file")

# Adding docs target
add_custom_target(docs COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_config_file}
                       WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
                       COMMENT "Launching doxygen..." VERBATIM)

# Gathering examples into docs subfolder
gather_notebooks_as_prebuild_cmd(docs docs/gathered ${PROJECT_SOURCE_DIR})
gather_readmes_as_prebuild_cmd(docs docs/gathered  ${PROJECT_SOURCE_DIR})

# Auto detect output directory
file(STRINGS ${DOXYGEN_config_file} config_line REGEX "OUTPUT_DIRECTORY[ \t]+=[^=].*")
if(config_line)
  string(REGEX MATCH "OUTPUT_DIRECTORY[ \t]+=([^=].*)" __ver_check "${config_line}")
  string(STRIP ${CMAKE_MATCH_1} output_dir)
  message(STATUS "Detected Doxygen OUTPUT_DIRECTORY: ${output_dir}")
else()
  set(output_dir ./doxygen/)
  message(STATUS "Can't find OUTPUT_DIRECTORY in doxygen config file. Try to use default: ${output_dir}")
endif()

if(NOT IS_ABSOLUTE ${output_dir})
  set(output_dir ${PROJECT_SOURCE_DIR}/${output_dir})
  get_filename_component(output_dir ${output_dir} ABSOLUTE)
endif()

# creates symlink in docs subfolder to code documentation built by doxygen
add_custom_command(TARGET docs POST_BUILD VERBATIM
                   COMMAND ln -sfn "${output_dir}/html" doxygen
                   WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/docs
                   COMMENT "Creating symlink ${PROJECT_SOURCE_DIR}/docs/doxygen -> ${output_dir}/html")

# for quick launch of jekyll
add_custom_target(jekyll COMMAND jekyll serve -w -s . -d _site --port=4000
                         WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/docs
                         COMMENT "Launching jekyll..." VERBATIM)
---
title: Installation
---

# Installation

Prior to installing, have a glance through this guide and take note of the details for your platform.
We install and run Caffe on Ubuntu 16.04–12.04, OS X 10.11–10.8, and through Docker and AWS.
The official Makefile and `Makefile.config` build are complemented by a [community CMake build](#cmake-build).

**Step-by-step Instructions**:

- [Docker setup](https://github.com/BVLC/caffe/tree/master/docker) *out-of-the-box brewing*
- [Ubuntu installation](install_apt.html) *the standard platform*
- [Debian installation](install_apt_debian.html) *install caffe with a single command*
- [OS X installation](install_osx.html)
- [RHEL / CentOS / Fedora installation](install_yum.html)
- [Windows](https://github.com/BVLC/caffe/tree/windows) *see the Windows branch led by Guillaume Dumont*
- [OpenCL](https://github.com/BVLC/caffe/tree/opencl) *see the OpenCL branch led by Fabian Tschopp*
- [AWS AMI](https://github.com/bitfusionio/amis/tree/master/awsmrkt-bfboost-ubuntu14-cuda75-caffe) *pre-configured for AWS*

**Overview**:

- [Prerequisites](#prerequisites)
- [Compilation](#compilation)
- [Hardware](#hardware)

When updating Caffe, it's best to `make clean` before re-compiling.

## Prerequisites

Caffe has several dependencies:

* [CUDA](https://developer.nvidia.com/cuda-zone) is required for GPU mode.
    * library version 7+ and the latest driver version are recommended, but 6.* is fine too
    * 5.5, and 5.0 are compatible but considered legacy
* [BLAS](http://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms) via ATLAS, MKL, or OpenBLAS.
* [Boost](http://www.boost.org/) >= 1.55
* `protobuf`, `glog`, `gflags`, `hdf5`

Optional dependencies:

* [OpenCV](http://opencv.org/) >= 2.4 including 3.0
* IO libraries: `lmdb`, `leveldb` (note: leveldb requires `snappy`)
* cuDNN for GPU acceleration (v6)

Pycaffe and Matcaffe interfaces have their own natural needs.

* For Python Caffe:  `Python 2.7` or `Python 3.3+`, `numpy (>= 1.7)`, boost-provided `boost.python`
* For MATLAB Caffe: MATLAB with the `mex` compiler.

**cuDNN Caffe**: for fastest operation Caffe is accelerated by drop-in integration of [NVIDIA cuDNN](https://developer.nvidia.com/cudnn). To speed up your Caffe models, install cuDNN then uncomment the `USE_CUDNN := 1` flag in `Makefile.config` when installing Caffe. Acceleration is automatic. The current version is cuDNN v6; older versions are supported in older Caffe.

**CPU-only Caffe**: for cold-brewed CPU-only Caffe uncomment the `CPU_ONLY := 1` flag in `Makefile.config` to configure and build Caffe without CUDA. This is helpful for cloud or cluster deployment.

### CUDA and BLAS

Caffe requires the CUDA `nvcc` compiler to compile its GPU code and CUDA driver for GPU operation.
To install CUDA, go to the [NVIDIA CUDA website](https://developer.nvidia.com/cuda-downloads) and follow installation instructions there. Install the library and the latest standalone driver separately; the driver bundled with the library is usually out-of-date. **Warning!** The 331.* CUDA driver series has a critical performance issue: do not use it.

For best performance, Caffe can be accelerated by [NVIDIA cuDNN](https://developer.nvidia.com/cudnn). Register for free at the cuDNN site, install it, then continue with these installation instructions. To compile with cuDNN set the `USE_CUDNN := 1` flag set in your `Makefile.config`.

Caffe requires BLAS as the backend of its matrix and vector computations.
There are several implementations of this library. The choice is yours:

* [ATLAS](http://math-atlas.sourceforge.net/): free, open source, and so the default for Caffe.
* [Intel MKL](http://software.intel.com/en-us/intel-mkl): commercial and optimized for Intel CPUs, with [free](https://registrationcenter.intel.com/en/forms/?productid=2558) licenses.
    1. Install MKL.
    2. Set up MKL environment (Details: [Linux](https://software.intel.com/en-us/node/528499), [OS X](https://software.intel.com/en-us/node/528659)). Example: *source /opt/intel/mkl/bin/mklvars.sh intel64*
    3. Set `BLAS := mkl` in `Makefile.config`
* [OpenBLAS](http://www.openblas.net/): free and open source; this optimized and parallel BLAS could require more effort to install, although it might offer a speedup.
    1. Install OpenBLAS
    2. Set `BLAS := open` in `Makefile.config`

### Python and/or MATLAB Caffe (optional)

#### Python

The main requirements are `numpy` and `boost.python` (provided by boost). `pandas` is useful too and needed for some examples.

You can install the dependencies with

    for req in $(cat requirements.txt); do pip install $req; done

but we suggest first installing the [Anaconda](https://store.continuum.io/cshop/anaconda/) Python distribution, which provides most of the necessary packages, as well as the `hdf5` library dependency.

To import the `caffe` Python module after completing the installation, add the module directory to your `$PYTHONPATH` by `export PYTHONPATH=/path/to/caffe/python:$PYTHONPATH` or the like. You should not import the module in the `caffe/python/caffe` directory!

*Caffe's Python interface works with Python 2.7. Python 3.3+ should work out of the box without protobuf support. For protobuf support please install protobuf 3.0 alpha (https://developers.google.com/protocol-buffers/). Earlier Pythons are your own adventure.*

#### MATLAB

Install MATLAB, and make sure that its `mex` is in your `$PATH`.

*Caffe's MATLAB interface works with versions 2015a, 2014a/b, 2013a/b, and 2012b.*

## Compilation

Caffe can be compiled with either Make or CMake. Make is officially supported while CMake is supported by the community.

### Compilation with Make

Configure the build by copying and modifying the example `Makefile.config` for your setup. The defaults should work, but uncomment the relevant lines if using Anaconda Python.

    cp Makefile.config.example Makefile.config
    # Adjust Makefile.config (for example, if using Anaconda Python, or if cuDNN is desired)
    make all
    make test
    make runtest

- For CPU & GPU accelerated Caffe, no changes are needed.
- For cuDNN acceleration using NVIDIA's proprietary cuDNN software, uncomment the `USE_CUDNN := 1` switch in `Makefile.config`. cuDNN is sometimes but not always faster than Caffe's GPU acceleration.
- For CPU-only Caffe, uncomment `CPU_ONLY := 1` in `Makefile.config`.

To compile the Python and MATLAB wrappers do `make pycaffe` and `make matcaffe` respectively.
Be sure to set your MATLAB and Python paths in `Makefile.config` first!

**Distribution**: run `make distribute` to create a `distribute` directory with all the Caffe headers, compiled libraries, binaries, etc. needed for distribution to other machines.

**Speed**: for a faster build, compile in parallel by doing `make all -j8` where 8 is the number of parallel threads for compilation (a good choice for the number of threads is the number of cores in your machine).

Now that you have installed Caffe, check out the [MNIST tutorial](gathered/examples/mnist.html) and the [reference ImageNet model tutorial](gathered/examples/imagenet.html).

### CMake Build

In lieu of manually editing `Makefile.config` to configure the build, Caffe offers an unofficial CMake build thanks to @Nerei, @akosiorek, and other members of the community. It requires CMake version >= 2.8.7.
The basic steps are as follows:

    mkdir build
    cd build
    cmake ..
    make all
    make install
    make runtest

See [PR #1667](https://github.com/BVLC/caffe/pull/1667) for options and details.

## Hardware

**Laboratory Tested Hardware**: Berkeley Vision runs Caffe with Titan Xs, K80s, GTX 980s, K40s, K20s, Titans, and GTX 770s including models at ImageNet/ILSVRC scale. We have not encountered any trouble in-house with devices with CUDA capability >= 3.0. All reported hardware issues thus-far have been due to GPU configuration, overheating, and the like.

**CUDA compute capability**: devices with compute capability <= 2.0 may have to reduce CUDA thread numbers and batch sizes due to hardware constraints. Brew with caution; we recommend compute capability >= 3.0.

Once installed, check your times against our [reference performance numbers](performance_hardware.html) to make sure everything is configured properly.

Ask hardware questions on the [caffe-users group](https://groups.google.com/forum/#!forum/caffe-users).
---
title: Developing and Contributing
---
# Development and Contributing

Caffe is developed with active participation of the community.<br>
The [BAIR](http://bair.berkeley.edu/)/BVLC brewers welcome all contributions!

The exact details of contributions are recorded by versioning and cited in our [acknowledgements](http://caffe.berkeleyvision.org/#acknowledgements).
This method is impartial and always up-to-date.

## License

Caffe is licensed under the terms in [LICENSE](https://github.com/BVLC/caffe/blob/master/LICENSE). By contributing to the project, you agree to the license and copyright terms therein and release your contribution under these terms.

## Copyright

Caffe uses a shared copyright model: each contributor holds copyright over their contributions to Caffe. The project versioning records all such contribution and copyright details.

If a contributor wants to further mark their specific copyright on a particular contribution, they should indicate their copyright solely in the commit message of the change when it is committed. Do not include copyright notices in files for this purpose.

### Documentation

This website, written with [Jekyll](http://jekyllrb.com/), acts as the official Caffe documentation -- simply run `scripts/build_docs.sh` and view the website at `http://0.0.0.0:4000`.

We prefer tutorials and examples to be documented close to where they live, in `readme.md` files.
The `build_docs.sh` script gathers all `examples/**/readme.md` and `examples/*.ipynb` files, and makes a table of contents.
To be included in the docs, the readme files must be annotated with [YAML front-matter](http://jekyllrb.com/docs/frontmatter/), including the flag `include_in_docs: true`.
Similarly for IPython notebooks: simply include `"include_in_docs": true` in the `"metadata"` JSON field.

Other docs, such as installation guides, are written in the `docs` directory and manually linked to from the `index.md` page.

We strive to provide lots of usage examples, and to document all code in docstrings.
We absolutely appreciate any contribution to this effort!

### Versioning

The `master` branch receives all new development including community contributions.
We try to keep it in a reliable state, but it is the bleeding edge, and things do get broken every now and then.
BAIR maintainers will periodically make releases by marking stable checkpoints as tags and maintenance branches. [Past releases](https://github.com/BVLC/caffe/releases) are catalogued online.

#### Issues & Pull Request Protocol

Post [Issues](https://github.com/BVLC/caffe/issues) to propose features, report [bugs], and discuss framework code.
Large-scale development work is guided by [milestones], which are sets of Issues selected for bundling as releases.

Please note that since the core developers are largely researchers, we may work on a feature in isolation for some time before releasing it to the community, so as to claim honest academic contribution.
We do release things as soon as a reasonable technical report may be written, and we still aim to inform the community of ongoing development through Github Issues.

**When you are ready to develop a feature or fixing a bug, follow this protocol**:

- Develop in [feature branches] with descriptive names. Branch off of the latest `master`.
- Bring your work up-to-date by [rebasing] onto the latest `master` when done.
(Groom your changes by [interactive rebase], if you'd like.)
- [Pull request] your contribution to `BVLC/caffe`'s `master` branch for discussion and review.
  - Make PRs *as soon as development begins*, to let discussion guide development.
  - A PR is only ready for merge review when it is a fast-forward merge, and all code is documented, linted, and tested -- that means your PR must include tests!
- When the PR satisfies the above properties, use comments to request maintainer review.

The following is a poetic presentation of the protocol in code form.

#### [Shelhamer's](https://github.com/shelhamer) “life of a branch in four acts”

Make the `feature` branch off of the latest `bvlc/master`

    git checkout master
    git pull upstream master
    git checkout -b feature
    # do your work, make commits

Prepare to merge by rebasing your branch on the latest `bvlc/master`

    # make sure master is fresh
    git checkout master
    git pull upstream master
    # rebase your branch on the tip of master
    git checkout feature
    git rebase master

Push your branch to pull request it into `BVLC/caffe:master`

    git push origin feature
    # ...make pull request to master...

Now make a pull request! You can do this from the command line (`git pull-request -b master`) if you install [hub](https://github.com/github/hub). Hub has many other magical uses.

The pull request of `feature` into `master` will be a clean merge. Applause.

[bugs]: https://github.com/BVLC/caffe/issues?labels=bug&page=1&state=open
[milestones]: https://github.com/BVLC/caffe/issues?milestone=1
[Pull request]: https://help.github.com/articles/using-pull-requests
[interactive rebase]: https://help.github.com/articles/interactive-rebase
[rebasing]: http://git-scm.com/book/en/Git-Branching-Rebasing
[feature branches]: https://www.atlassian.com/git/workflows#!workflow-feature-branch

**Historical note**: Caffe once relied on a two branch `master` and `dev` workflow.
PRs from this time are still open but these will be merged into `master` or closed.

### Testing

Run `make runtest` to check the project tests. New code requires new tests. Pull requests that fail tests will not be accepted.

The `gtest` framework we use provides many additional options, which you can access by running the test binaries directly. One of the more useful options is `--gtest_filter`, which allows you to filter tests by name:

    # run all tests with CPU in the name
    build/test/test_all.testbin --gtest_filter='*CPU*'

    # run all tests without GPU in the name (note the leading minus sign)
    build/test/test_all.testbin --gtest_filter=-'*GPU*'

To get a list of all options `googletest` provides, simply pass the `--help` flag:

    build/test/test_all.testbin --help

### Style

- **Run `make lint` to check C++ code.**
- Wrap lines at 80 chars.
- Follow [Google C++ style](http://google-styleguide.googlecode.com/svn/trunk/cppguide.xml) and [Google python style](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html) + [PEP 8](http://legacy.python.org/dev/peps/pep-0008/).
- Remember that “a foolish consistency is the hobgoblin of little minds,” so use your best judgement to write the clearest code for your particular case.
---
title: Multi-GPU Usage, Hardware Configuration Assumptions, and Performance
---

# Multi-GPU Usage

Currently Multi-GPU is only supported via the C/C++ paths and only for training.

The GPUs to be used for training can be set with the "-gpu" flag on the command line to the 'caffe' tool.  e.g. "build/tools/caffe train --solver=models/bvlc_alexnet/solver.prototxt --gpu=0,1" will train on GPUs 0 and 1.

**NOTE**: each GPU runs the batchsize specified in your train_val.prototxt.  So if you go from 1 GPU to 2 GPU, your effective batchsize will double.  e.g. if your train_val.prototxt specified a batchsize of 256, if you run 2 GPUs your effective batch size is now 512.  So you need to adjust the batchsize when running multiple GPUs and/or adjust your solver params, specifically learning rate.

# Hardware Configuration Assumptions

The current implementation uses a tree reduction strategy.  e.g. if there are 4 GPUs in the system, 0:1, 2:3 will exchange gradients, then 0:2 (top of the tree) will exchange gradients, 0 will calculate
updated model, 0\-\>2, and then 0\-\>1, 2\-\>3.

For best performance, P2P DMA access between devices is needed. Without P2P access, for example crossing PCIe root complex, data is copied through host and effective exchange bandwidth is greatly reduced.

Current implementation has a "soft" assumption that the devices being used are homogeneous.  In practice, any devices of the same general class should work together, but performance and total size is limited by the smallest device being used.  e.g. if you combine a TitanX and a GTX980, performance will be limited by the 980.  Mixing vastly different levels of boards, e.g. Kepler and Fermi, is not supported.

"nvidia-smi topo -m" will show you the connectivity matrix.  You can do P2P through PCIe bridges, but not across socket level links at this time, e.g. across CPU sockets on a multi-socket motherboard.

# Scaling Performance

Performance is **heavily** dependent on the PCIe topology of the system, the configuration of the neural network you are training, and the speed of each of the layers.  Systems like the DIGITS DevBox have an optimized PCIe topology (X99-E WS chipset).  In general, scaling on 2 GPUs tends to be ~1.8X on average for networks like AlexNet, CaffeNet, VGG, GoogleNet.  4 GPUs begins to have falloff in scaling.  Generally with "weak scaling" where the batchsize increases with the number of GPUs you will see 3.5x scaling or so.  With "strong scaling", the system can become communication bound, especially with layer performance optimizations like those in [cuDNNv3](http://nvidia.com/cudnn), and you will likely see closer to mid 2.x scaling in performance.  Networks that have heavy computation compared to the number of parameters tend to have the best scaling performance.
---
title: Deep Learning Framework
---

# Caffe

Caffe is a deep learning framework made with expression, speed, and modularity in mind.
It is developed by Berkeley AI Research ([BAIR](http://bair.berkeley.edu)) and by community contributors.
[Yangqing Jia](http://daggerfs.com) created the project during his PhD at UC Berkeley.
Caffe is released under the [BSD 2-Clause license](https://github.com/BVLC/caffe/blob/master/LICENSE).

Check out our web image classification [demo](http://demo.caffe.berkeleyvision.org)!

## Why Caffe?

**Expressive architecture** encourages application and innovation.
Models and optimization are defined by configuration without hard-coding.
Switch between CPU and GPU by setting a single flag to train on a GPU machine then deploy to commodity clusters or mobile devices.

**Extensible code** fosters active development.
In Caffe's first year, it has been forked by over 1,000 developers and had many significant changes contributed back.
Thanks to these contributors the framework tracks the state-of-the-art in both code and models.

**Speed** makes Caffe perfect for research experiments and industry deployment.
Caffe can process **over 60M images per day** with a single NVIDIA K40 GPU\*.
That's 1 ms/image for inference and 4 ms/image for learning and more recent library versions and hardware are faster still.
We believe that Caffe is among the fastest convnet implementations available.

**Community**: Caffe already powers academic research projects, startup prototypes, and even large-scale industrial applications in vision, speech, and multimedia.
Join our community of brewers on the [caffe-users group](https://groups.google.com/forum/#!forum/caffe-users) and [Github](https://github.com/BVLC/caffe/).

<p class="footnote" markdown="1">
\* With the ILSVRC2012-winning [SuperVision](http://www.image-net.org/challenges/LSVRC/2012/supervision.pdf) model and prefetching IO.
</p>

## Documentation

- [DIY Deep Learning for Vision with Caffe](https://docs.google.com/presentation/d/1UeKXVgRvvxg9OUdh_UiC5G71UMscNPlvArsWER41PsU/edit#slide=id.p) and [Caffe in a Day](https://docs.google.com/presentation/d/1HxGdeq8MPktHaPb-rlmYYQ723iWzq9ur6Gjo71YiG0Y/edit#slide=id.gc2fcdcce7_216_0)<br>
Tutorial presentation of the framework and a full-day crash course.
- [Tutorial Documentation](/tutorial)<br>
Practical guide and framework reference.
- [arXiv / ACM MM '14 paper](http://arxiv.org/abs/1408.5093)<br>
A 4-page report for the ACM Multimedia Open Source competition (arXiv:1408.5093v1).
- [Installation instructions](/installation.html)<br>
Tested on Ubuntu, Red Hat, OS X.
* [Model Zoo](/model_zoo.html)<br>
BAIR suggests a standard distribution format for Caffe models, and provides trained models.
* [Developing & Contributing](/development.html)<br>
Guidelines for development and contributing to Caffe.
* [API Documentation](/doxygen/annotated.html)<br>
Developer documentation automagically generated from code comments.
* [Benchmarking](https://docs.google.com/spreadsheets/d/1Yp4rqHpT7mKxOPbpzYeUfEFLnELDAgxSSBQKp5uKDGQ/edit#gid=0)<br>
Comparison of inference and learning for different networks and GPUs.

### Notebook Examples

{% assign notebooks = site.pages | where:'category','notebook' | sort: 'priority' %}
{% for page in notebooks %}
- <div><a href="http://nbviewer.ipython.org/github/BVLC/caffe/blob/master/{{page.original_path}}">{{page.title}}</a><br>{{page.description}}</div>
{% endfor %}

### Command Line Examples

{% assign examples = site.pages | where:'category','example' | sort: 'priority' %}
{% for page in examples %}
- <div><a href="{{page.url}}">{{page.title}}</a><br>{{page.description}}</div>
{% endfor %}

## Citing Caffe

Please cite Caffe in your publications if it helps your research:

    @article{jia2014caffe,
      Author = {Jia, Yangqing and Shelhamer, Evan and Donahue, Jeff and Karayev, Sergey and Long, Jonathan and Girshick, Ross and Guadarrama, Sergio and Darrell, Trevor},
      Journal = {arXiv preprint arXiv:1408.5093},
      Title = {Caffe: Convolutional Architecture for Fast Feature Embedding},
      Year = {2014}
    }

If you do publish a paper where Caffe helped your research, we encourage you to cite the framework for tracking by [Google Scholar](https://scholar.google.com/citations?view_op=view_citation&hl=en&citation_for_view=-ltRSM0AAAAJ:u5HHmVD_uO8C).

## Contacting Us

Join the [caffe-users group](https://groups.google.com/forum/#!forum/caffe-users) to ask questions and discuss methods and models. This is where we talk about usage, installation, and applications.

Framework development discussions and thorough bug reports are collected on [Issues](https://github.com/BVLC/caffe/issues).

## Acknowledgements

The BAIR Caffe developers would like to thank NVIDIA for GPU donation, A9 and Amazon Web Services for a research grant in support of Caffe development and reproducible research in deep learning, and BAIR PI [Trevor Darrell](http://www.eecs.berkeley.edu/~trevor/) for guidance.

The BAIR members who have contributed to Caffe are (alphabetical by first name):
[Carl Doersch](http://www.carldoersch.com/), [Eric Tzeng](https://github.com/erictzeng), [Evan Shelhamer](http://imaginarynumber.net/), [Jeff Donahue](http://jeffdonahue.com/), [Jon Long](https://github.com/longjon), [Philipp Krähenbühl](http://www.philkr.net/), [Ronghang Hu](http://ronghanghu.com/), [Ross Girshick](http://www.cs.berkeley.edu/~rbg/), [Sergey Karayev](http://sergeykarayev.com/), [Sergio Guadarrama](http://www.eecs.berkeley.edu/~sguada/), [Takuya Narihira](https://github.com/tnarihi), and [Yangqing Jia](http://daggerfs.com/).

The open-source community plays an important and growing role in Caffe's development.
Check out the Github [project pulse](https://github.com/BVLC/caffe/pulse) for recent activity and the [contributors](https://github.com/BVLC/caffe/graphs/contributors) for the full list.

We sincerely appreciate your interest and contributions!
If you'd like to contribute, please read the [developing & contributing](development.html) guide.

Yangqing would like to give a personal thanks to the NVIDIA Academic program for providing GPUs, [Oriol Vinyals](http://www1.icsi.berkeley.edu/~vinyals/) for discussions along the journey, and BAIR PI [Trevor Darrell](http://www.eecs.berkeley.edu/~trevor/) for advice.
---
title: "Installation: OS X"
---

# OS X Installation

We highly recommend using the [Homebrew](http://brew.sh/) package manager.
Ideally you could start from a clean `/usr/local` to avoid conflicts.
In the following, we assume that you're using Anaconda Python and Homebrew.

**CUDA**: Install via the NVIDIA package that includes both CUDA and the bundled driver. **CUDA 7 is strongly suggested.** Older CUDA require `libstdc++` while clang++ is the default compiler and `libc++` the default standard library on OS X 10.9+. This disagreement makes it necessary to change the compilation settings for each of the dependencies. This is prone to error.

**Library Path**: We find that everything compiles successfully if `$LD_LIBRARY_PATH` is not set at all, and `$DYLD_FALLBACK_LIBRARY_PATH` is set to provide CUDA, Python, and other relevant libraries (e.g. `/usr/local/cuda/lib:$HOME/anaconda/lib:/usr/local/lib:/usr/lib`).
In other `ENV` settings, things may not work as expected.

**General dependencies**

    brew install -vd snappy leveldb gflags glog szip lmdb
    # need the homebrew science source for OpenCV and hdf5
    brew tap homebrew/science
    brew install hdf5 opencv

If using Anaconda Python, a modification to the OpenCV formula might be needed
Do `brew edit opencv` and change the lines that look like the two lines below to exactly the two lines below.

      -DPYTHON_LIBRARY=#{py_prefix}/lib/libpython2.7.dylib
      -DPYTHON_INCLUDE_DIR=#{py_prefix}/include/python2.7

If using Anaconda Python, HDF5 is bundled and the `hdf5` formula can be skipped.

**Remaining dependencies, with / without Python**

    # with Python pycaffe needs dependencies built from source
    brew install --build-from-source --with-python -vd protobuf
    brew install --build-from-source -vd boost boost-python
    # without Python the usual installation suffices
    brew install protobuf boost

**BLAS**: already installed as the [Accelerate / vecLib Framework](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man7/Accelerate.7.html). OpenBLAS and MKL are alternatives for faster CPU computation.

**Python** (optional): Anaconda is the preferred Python.
If you decide against it, please use Homebrew.
Check that Caffe and dependencies are linking against the same, desired Python.

Continue with [compilation](installation.html#compilation).

## libstdc++ installation

This route is not for the faint of heart.
For OS X 10.10 and 10.9 you should install CUDA 7 and follow the instructions above.
If that is not an option, take a deep breath and carry on.

In OS X 10.9+, clang++ is the default C++ compiler and uses `libc++` as the standard library.
However, NVIDIA CUDA (even version 6.0) currently links only with `libstdc++`.
This makes it necessary to change the compilation settings for each of the dependencies.

We do this by modifying the Homebrew formulae before installing any packages.
Make sure that Homebrew doesn't install any software dependencies in the background; all packages must be linked to `libstdc++`.

The prerequisite Homebrew formulae are

    boost snappy leveldb protobuf gflags glog szip lmdb homebrew/science/opencv

For each of these formulas, `brew edit FORMULA`, and add the ENV definitions as shown:

      def install
          # ADD THE FOLLOWING:
          ENV.append "CXXFLAGS", "-stdlib=libstdc++"
          ENV.append "CFLAGS", "-stdlib=libstdc++"
          ENV.append "LDFLAGS", "-stdlib=libstdc++ -lstdc++"
          # The following is necessary because libtool likes to strip LDFLAGS:
          ENV["CXX"] = "/usr/bin/clang++ -stdlib=libstdc++"
          ...

To edit the formulae in turn, run

    for x in snappy leveldb protobuf gflags glog szip boost boost-python lmdb homebrew/science/opencv; do brew edit $x; done

After this, run

    for x in snappy leveldb gflags glog szip lmdb homebrew/science/opencv; do brew uninstall $x; brew install --build-from-source -vd $x; done
    brew uninstall protobuf; brew install --build-from-source --with-python -vd protobuf
    brew install --build-from-source -vd boost boost-python

If this is not done exactly right then linking errors will trouble you.

**Homebrew versioning** that Homebrew maintains itself as a separate git repository and making the above `brew edit FORMULA` changes will change files in your local copy of homebrew's master branch. By default, this will prevent you from updating Homebrew using `brew update`, as you will get an error message like the following:

    $ brew update
    error: Your local changes to the following files would be overwritten by merge:
      Library/Formula/lmdb.rb
    Please, commit your changes or stash them before you can merge.
    Aborting
    Error: Failure while executing: git pull -q origin refs/heads/master:refs/remotes/origin/master

One solution is to commit your changes to a separate Homebrew branch, run `brew update`, and rebase your changes onto the updated master. You'll have to do this both for the main Homebrew repository in `/usr/local/` and the Homebrew science repository that contains OpenCV in  `/usr/local/Library/Taps/homebrew/homebrew-science`, as follows:

    cd /usr/local
    git checkout -b caffe
    git add .
    git commit -m "Update Caffe dependencies to use libstdc++"
    cd /usr/local/Library/Taps/homebrew/homebrew-science
    git checkout -b caffe
    git add .
    git commit -m "Update Caffe dependencies"

Then, whenever you want to update homebrew, switch back to the master branches, do the update, rebase the caffe branches onto master and fix any conflicts:

    # Switch batch to homebrew master branches
    cd /usr/local
    git checkout master
    cd /usr/local/Library/Taps/homebrew/homebrew-science
    git checkout master

    # Update homebrew; hopefully this works without errors!
    brew update

    # Switch back to the caffe branches with the formulae that you modified earlier
    cd /usr/local
    git rebase master caffe
    # Fix any merge conflicts and commit to caffe branch
    cd /usr/local/Library/Taps/homebrew/homebrew-science
    git rebase master caffe
    # Fix any merge conflicts and commit to caffe branch

    # Done!

At this point, you should be running the latest Homebrew packages and your Caffe-related modifications will remain in place.
---
title: "Installation: Ubuntu"
---

# Ubuntu Installation

### For Ubuntu (>= 17.04)

**Installing pre-compiled Caffe**

Everything including caffe itself is packaged in 17.04 and higher versions.
To install pre-compiled Caffe package, just do it by

    sudo apt install caffe-cpu

for CPU-only version, or

    sudo apt install caffe-cuda

for CUDA version. Note, the cuda version may break if your NVIDIA driver
and CUDA toolkit are not installed by APT.

[Package status of CPU-only version](https://launchpad.net/ubuntu/+source/caffe)

[Package status of CUDA version](https://launchpad.net/ubuntu/+source/caffe-contrib)

**Installing Caffe from source**

We may install the dependencies by merely one line

    sudo apt build-dep caffe-cpu        # dependencies for CPU-only version
    sudo apt build-dep caffe-cuda       # dependencies for CUDA version

It requires a `deb-src` line in your `sources.list`.
Continue with [compilation](installation.html#compilation).

### For Ubuntu (\< 17.04)

**General dependencies**

    sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
    sudo apt-get install --no-install-recommends libboost-all-dev

**CUDA**: Install by `apt-get` or the NVIDIA `.run` package.
The NVIDIA package tends to follow more recent library and driver versions, but the installation is more manual.
If installing from packages, install the library and latest driver separately; the driver bundled with the library is usually out-of-date.
This can be skipped for CPU-only installation.

**BLAS**: install ATLAS by `sudo apt-get install libatlas-base-dev` or install OpenBLAS by `sudo apt-get install libopenblas-dev` or MKL for better CPU performance.

**Python** (optional): if you use the default Python you will need to `sudo apt-get install` the `python-dev` package to have the Python headers for building the pycaffe interface.

**Compatibility notes, 16.04**

CUDA 8 is required on Ubuntu 16.04.

**Remaining dependencies, 14.04**

Everything is packaged in 14.04.

    sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev

**Remaining dependencies, 12.04**

These dependencies need manual installation in 12.04.

    # glog
    wget https://github.com/google/glog/archive/v0.3.3.tar.gz
    tar zxvf v0.3.3.tar.gz
    cd glog-0.3.3
    ./configure
    make && make install
    # gflags
    wget https://github.com/schuhschuh/gflags/archive/master.zip
    unzip master.zip
    cd gflags-master
    mkdir build && cd build
    export CXXFLAGS="-fPIC" && cmake .. && make VERBOSE=1
    make && make install
    # lmdb
    git clone https://github.com/LMDB/lmdb
    cd lmdb/libraries/liblmdb
    make && make install

Note that glog does not compile with the most recent gflags version (2.1), so before that is resolved you will need to build with glog first.

Continue with [compilation](installation.html#compilation).
---
title: Model Zoo
---
# Caffe Model Zoo

Lots of researchers and engineers have made Caffe models for different tasks with all kinds of architectures and data: check out the [model zoo](https://github.com/BVLC/caffe/wiki/Model-Zoo)!
These models are learned and applied for problems ranging from simple regression, to large-scale visual classification, to Siamese networks for image similarity, to speech and robotics applications.

To help share these models, we introduce the model zoo framework:

- A standard format for packaging Caffe model info.
- Tools to upload/download model info to/from Github Gists, and to download trained `.caffemodel` binaries.
- A central wiki page for sharing model info Gists.

## Where to get trained models

First of all, we bundle BAIR-trained models for unrestricted, out of the box use.
<br>
See the [BAIR model license](#bair-model-license) for details.
Each one of these can be downloaded by running `scripts/download_model_binary.py <dirname>` where `<dirname>` is specified below:

- **BAIR Reference CaffeNet** in `models/bvlc_reference_caffenet`: AlexNet trained on ILSVRC 2012, with a minor variation from the version as described in [ImageNet classification with deep convolutional neural networks](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks) by Krizhevsky et al. in NIPS 2012. (Trained by Jeff Donahue @jeffdonahue)
- **BAIR AlexNet** in `models/bvlc_alexnet`: AlexNet trained on ILSVRC 2012, almost exactly as described in [ImageNet classification with deep convolutional neural networks](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks) by Krizhevsky et al. in NIPS 2012. (Trained by Evan Shelhamer @shelhamer)
- **BAIR Reference R-CNN ILSVRC-2013** in `models/bvlc_reference_rcnn_ilsvrc13`: pure Caffe implementation of [R-CNN](https://github.com/rbgirshick/rcnn) as described by Girshick et al. in CVPR 2014. (Trained by Ross Girshick @rbgirshick)
- **BAIR GoogLeNet** in `models/bvlc_googlenet`: GoogLeNet trained on ILSVRC 2012, almost exactly as described in [Going Deeper with Convolutions](http://arxiv.org/abs/1409.4842) by Szegedy et al. in ILSVRC 2014. (Trained by Sergio Guadarrama @sguada)

**Community models** made by Caffe users are posted to a publicly editable [model zoo wiki page](https://github.com/BVLC/caffe/wiki/Model-Zoo).
These models are subject to conditions of their respective authors such as citation and license.
Thank you for sharing your models!

## Model info format

A caffe model is distributed as a directory containing:

- Solver/model prototxt(s)
- `readme.md` containing
    - YAML frontmatter
        - Caffe version used to train this model (tagged release or commit hash).
        - [optional] file URL and SHA1 of the trained `.caffemodel`.
        - [optional] github gist id.
    - Information about what data the model was trained on, modeling choices, etc.
    - License information.
- [optional] Other helpful scripts.

This simple format can be handled through bundled scripts or manually if need be.

### Hosting model info

Github Gist is a good format for model info distribution because it can contain multiple files, is versionable, and has in-browser syntax highlighting and markdown rendering.

`scripts/upload_model_to_gist.sh <dirname>` uploads non-binary files in the model directory as a Github Gist and prints the Gist ID. If `gist_id` is already part of the `<dirname>/readme.md` frontmatter, then updates existing Gist.

Try doing `scripts/upload_model_to_gist.sh models/bvlc_alexnet` to test the uploading (don't forget to delete the uploaded gist afterward).

Downloading model info is done just as easily with `scripts/download_model_from_gist.sh <gist_id> <dirname>`.

### Hosting trained models

It is up to the user where to host the `.caffemodel` file.
We host our BAIR-provided models on our own server.
Dropbox also works fine (tip: make sure that `?dl=1` is appended to the end of the URL).

`scripts/download_model_binary.py <dirname>` downloads the `.caffemodel` from the URL specified in the `<dirname>/readme.md` frontmatter and confirms SHA1.

## BAIR model license

The Caffe models bundled by the BAIR are released for unrestricted use.

These models are trained on data from the [ImageNet project](http://www.image-net.org/) and training data includes internet photos that may be subject to copyright.

Our present understanding as researchers is that there is no restriction placed on the open release of these learned model weights, since none of the original images are distributed in whole or in part.
To the extent that the interpretation arises that weights are derivative works of the original copyright holder and they assert such a copyright, UC Berkeley makes no representations as to what use is allowed other than to consider our present release in the spirit of fair use in the academic mission of the university to disseminate knowledge and tools as broadly as possible without restriction.
---
title: Forward and Backward for Inference and Learning
---
# Forward and Backward

The forward and backward passes are the essential computations of a [Net](net_layer_blob.html).

<img src="fig/forward_backward.png" alt="Forward and Backward" width="480">

Let's consider a simple logistic regression classifier.

The **forward** pass computes the output given the input for inference.
In forward Caffe composes the computation of each layer to compute the "function" represented by the model.
This pass goes from bottom to top.

<img src="fig/forward.jpg" alt="Forward pass" width="320">

The data $$x$$ is passed through an inner product layer for $$g(x)$$ then through a softmax for $$h(g(x))$$ and softmax loss to give $$f_W(x)$$.

The **backward** pass computes the gradient given the loss for learning.
In backward Caffe reverse-composes the gradient of each layer to compute the gradient of the whole model by automatic differentiation.
This is back-propagation.
This pass goes from top to bottom.

<img src="fig/backward.jpg" alt="Backward pass" width="320">

The backward pass begins with the loss and computes the gradient with respect to the output $$\frac{\partial f_W}{\partial h}$$. The gradient with respect to the rest of the model is computed layer-by-layer through the chain rule. Layers with parameters, like the `INNER_PRODUCT` layer, compute the gradient with respect to their parameters $$\frac{\partial f_W}{\partial W_{\text{ip}}}$$ during the backward step.

These computations follow immediately from defining the model: Caffe plans and carries out the forward and backward passes for you.

- The `Net::Forward()` and `Net::Backward()` methods carry out the respective passes while `Layer::Forward()` and `Layer::Backward()` compute each step.
- Every layer type has `forward_{cpu,gpu}()` and `backward_{cpu,gpu}()` methods to compute its steps according to the mode of computation. A layer may only implement CPU or GPU mode due to constraints or convenience.

The [Solver](solver.html) optimizes a model by first calling forward to yield the output and loss, then calling backward to generate the gradient of the model, and then incorporating the gradient into a weight update that attempts to minimize the loss. Division of labor between the Solver, Net, and Layer keep Caffe modular and open to development.

For the details of the forward and backward steps of Caffe's layer types, refer to the [layer catalogue](layers.html).

---
title: Solver / Model Optimization
---
# Solver

The solver orchestrates model optimization by coordinating the network's forward inference and backward gradients to form parameter updates that attempt to improve the loss.
The responsibilities of learning are divided between the Solver for overseeing the optimization and generating parameter updates and the Net for yielding loss and gradients.

The Caffe solvers are:

- Stochastic Gradient Descent (`type: "SGD"`),
- AdaDelta (`type: "AdaDelta"`),
- Adaptive Gradient (`type: "AdaGrad"`),
- Adam (`type: "Adam"`),
- Nesterov's Accelerated Gradient (`type: "Nesterov"`) and
- RMSprop (`type: "RMSProp"`)

The solver

1. scaffolds the optimization bookkeeping and creates the training network for learning and test network(s) for evaluation.
2. iteratively optimizes by calling forward / backward and updating parameters
3. (periodically) evaluates the test networks
4. snapshots the model and solver state throughout the optimization

where each iteration

1. calls network forward to compute the output and loss
2. calls network backward to compute the gradients
3. incorporates the gradients into parameter updates according to the solver method
4. updates the solver state according to learning rate, history, and method

to take the weights all the way from initialization to learned model.

Like Caffe models, Caffe solvers run in CPU / GPU modes.

## Methods

The solver methods address the general optimization problem of loss minimization.
For dataset $$D$$, the optimization objective is the average loss over all $$|D|$$ data instances throughout the dataset

$$L(W) = \frac{1}{|D|} \sum_i^{|D|} f_W\left(X^{(i)}\right) + \lambda r(W)$$

where $$f_W\left(X^{(i)}\right)$$ is the loss on data instance $$X^{(i)}$$ and $$r(W)$$ is a regularization term with weight $$\lambda$$.
$$|D|$$ can be very large, so in practice, in each solver iteration we use a stochastic approximation of this objective, drawing a mini-batch of $$N << |D|$$ instances:

$$L(W) \approx \frac{1}{N} \sum_i^N f_W\left(X^{(i)}\right) + \lambda r(W)$$

The model computes $$f_W$$ in the forward pass and the gradient $$\nabla f_W$$ in the backward pass.

The parameter update $$\Delta W$$ is formed by the solver from the error gradient $$\nabla f_W$$, the regularization gradient $$\nabla r(W)$$, and other particulars to each method.

### SGD

**Stochastic gradient descent** (`type: "SGD"`) updates the weights $$ W $$ by a linear combination of the negative gradient $$ \nabla L(W) $$ and the previous weight update $$ V_t $$.
The **learning rate** $$ \alpha $$ is the weight of the negative gradient.
The **momentum** $$ \mu $$ is the weight of the previous update.

Formally, we have the following formulas to compute the update value $$ V_{t+1} $$ and the updated weights $$ W_{t+1} $$ at iteration $$ t+1 $$, given the previous weight update $$ V_t $$ and current weights $$ W_t $$:

$$
V_{t+1} = \mu V_t - \alpha \nabla L(W_t)
$$

$$
W_{t+1} = W_t + V_{t+1}
$$

The learning "hyperparameters" ($$\alpha$$ and $$\mu$$) might require a bit of tuning for best results.
If you're not sure where to start, take a look at the "Rules of thumb" below, and for further information you might refer to Leon Bottou's [Stochastic Gradient Descent Tricks](http://research.microsoft.com/pubs/192769/tricks-2012.pdf) [1].

[1] L. Bottou.
    [Stochastic Gradient Descent Tricks](http://research.microsoft.com/pubs/192769/tricks-2012.pdf).
    *Neural Networks: Tricks of the Trade*: Springer, 2012.

#### Rules of thumb for setting the learning rate $$ \alpha $$ and momentum $$ \mu $$

A good strategy for deep learning with SGD is to initialize the learning rate $$ \alpha $$ to a value around $$ \alpha \approx 0.01 = 10^{-2} $$, and dropping it by a constant factor (e.g., 10) throughout training when the loss begins to reach an apparent "plateau", repeating this several times.
Generally, you probably want to use a momentum $$ \mu = 0.9 $$ or similar value.
By smoothing the weight updates across iterations, momentum tends to make deep learning with SGD both stabler and faster.

This was the strategy used by Krizhevsky et al. [1] in their famously winning CNN entry to the ILSVRC-2012 competition, and Caffe makes this strategy easy to implement in a `SolverParameter`, as in our reproduction of [1] at `./examples/imagenet/alexnet_solver.prototxt`.

To use a learning rate policy like this, you can put the following lines somewhere in your solver prototxt file:

    base_lr: 0.01     # begin training at a learning rate of 0.01 = 1e-2

    lr_policy: "step" # learning rate policy: drop the learning rate in "steps"
                      # by a factor of gamma every stepsize iterations

    gamma: 0.1        # drop the learning rate by a factor of 10
                      # (i.e., multiply it by a factor of gamma = 0.1)

    stepsize: 100000  # drop the learning rate every 100K iterations

    max_iter: 350000  # train for 350K iterations total

    momentum: 0.9

Under the above settings, we'll always use `momentum` $$ \mu = 0.9 $$.
We'll begin training at a `base_lr` of $$ \alpha = 0.01 = 10^{-2} $$ for the first 100,000 iterations, then multiply the learning rate by `gamma` ($$ \gamma $$) and train at $$ \alpha' = \alpha \gamma = (0.01) (0.1) = 0.001 = 10^{-3} $$ for iterations 100K-200K, then at $$ \alpha'' = 10^{-4} $$ for iterations 200K-300K, and finally train until iteration 350K (since we have `max_iter: 350000`) at $$ \alpha''' = 10^{-5} $$.

Note that the momentum setting $$ \mu $$ effectively multiplies the size of your updates by a factor of $$ \frac{1}{1 - \mu} $$ after many iterations of training, so if you increase $$ \mu $$, it may be a good idea to **decrease** $$ \alpha $$ accordingly (and vice versa).

For example, with $$ \mu = 0.9 $$, we have an effective update size multiplier of $$ \frac{1}{1 - 0.9} = 10 $$.
If we increased the momentum to $$ \mu = 0.99 $$, we've increased our update size multiplier to 100, so we should drop $$ \alpha $$ (`base_lr`) by a factor of 10.

Note also that the above settings are merely guidelines, and they're definitely not guaranteed to be optimal (or even work at all!) in every situation.
If learning diverges (e.g., you start to see very large or `NaN` or `inf` loss values or outputs), try dropping the `base_lr` (e.g., `base_lr: 0.001`) and re-training, repeating this until you find a `base_lr` value that works.

[1] A. Krizhevsky, I. Sutskever, and G. Hinton.
    [ImageNet Classification with Deep Convolutional Neural Networks](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf).
    *Advances in Neural Information Processing Systems*, 2012.

### AdaDelta

The **AdaDelta** (`type: "AdaDelta"`) method (M. Zeiler [1]) is a "robust learning rate method". It is a gradient-based optimization method (like SGD). The update formulas are

$$
\begin{align}
(v_t)_i &= \frac{\operatorname{RMS}((v_{t-1})_i)}{\operatorname{RMS}\left( \nabla L(W_t) \right)_{i}} \left( \nabla L(W_{t'}) \right)_i
\\
\operatorname{RMS}\left( \nabla L(W_t) \right)_{i} &= \sqrt{E[g^2] + \varepsilon}
\\
E[g^2]_t &= \delta{E[g^2]_{t-1} } + (1-\delta)g_{t}^2
\end{align}
$$

and

$$
(W_{t+1})_i =
(W_t)_i - \alpha
(v_t)_i.
$$

[1] M. Zeiler
    [ADADELTA: AN ADAPTIVE LEARNING RATE METHOD](http://arxiv.org/pdf/1212.5701.pdf).
    *arXiv preprint*, 2012.

### AdaGrad

The **adaptive gradient** (`type: "AdaGrad"`) method (Duchi et al. [1]) is a gradient-based optimization method (like SGD) that attempts to "find needles in haystacks in the form of very predictive but rarely seen features," in Duchi et al.'s words.
Given the update information from all previous iterations $$ \left( \nabla L(W) \right)_{t'} $$ for $$ t' \in \{1, 2, ..., t\} $$,
the update formulas proposed by [1] are as follows, specified for each component $$i$$ of the weights $$W$$:

$$
(W_{t+1})_i =
(W_t)_i - \alpha
\frac{\left( \nabla L(W_t) \right)_{i}}{
    \sqrt{\sum_{t'=1}^{t} \left( \nabla L(W_{t'}) \right)_i^2}
}
$$

Note that in practice, for weights $$ W \in \mathcal{R}^d $$, AdaGrad implementations (including the one in Caffe) use only $$ \mathcal{O}(d) $$ extra storage for the historical gradient information (rather than the $$ \mathcal{O}(dt) $$ storage that would be necessary to store each historical gradient individually).

[1] J. Duchi, E. Hazan, and Y. Singer.
    [Adaptive Subgradient Methods for Online Learning and Stochastic Optimization](http://www.magicbroom.info/Papers/DuchiHaSi10.pdf).
    *The Journal of Machine Learning Research*, 2011.

### Adam

The **Adam** (`type: "Adam"`), proposed in Kingma et al. [1], is a gradient-based optimization method (like SGD). This includes an "adaptive moment estimation" ($$m_t, v_t$$) and can be regarded as a generalization of AdaGrad. The update formulas are

$$
(m_t)_i = \beta_1 (m_{t-1})_i + (1-\beta_1)(\nabla L(W_t))_i,\\
(v_t)_i = \beta_2 (v_{t-1})_i + (1-\beta_2)(\nabla L(W_t))_i^2
$$

and

$$
(W_{t+1})_i =
(W_t)_i - \alpha \frac{\sqrt{1-(\beta_2)_i^t}}{1-(\beta_1)_i^t}\frac{(m_t)_i}{\sqrt{(v_t)_i}+\varepsilon}.
$$

Kingma et al. [1] proposed to use $$\beta_1 = 0.9, \beta_2 = 0.999, \varepsilon = 10^{-8}$$ as default values. Caffe uses the values of `momemtum, momentum2, delta` for $$\beta_1, \beta_2, \varepsilon$$, respectively.

[1] D. Kingma, J. Ba.
    [Adam: A Method for Stochastic Optimization](http://arxiv.org/abs/1412.6980).
    *International Conference for Learning Representations*, 2015.

### NAG

**Nesterov's accelerated gradient** (`type: "Nesterov"`) was proposed by Nesterov [1] as an "optimal" method of convex optimization, achieving a convergence rate of $$ \mathcal{O}(1/t^2) $$ rather than the $$ \mathcal{O}(1/t) $$.
Though the required assumptions to achieve the $$ \mathcal{O}(1/t^2) $$ convergence typically will not hold for deep networks trained with Caffe (e.g., due to non-smoothness and non-convexity), in practice NAG can be a very effective method for optimizing certain types of deep learning architectures, as demonstrated for deep MNIST autoencoders by Sutskever et al. [2].

The weight update formulas look very similar to the SGD updates given above:

$$
V_{t+1} = \mu V_t - \alpha \nabla L(W_t + \mu V_t)
$$

$$
W_{t+1} = W_t + V_{t+1}
$$

What distinguishes the method from SGD is the weight setting $$ W $$ on which we compute the error gradient $$ \nabla L(W) $$ -- in NAG we take the gradient on weights with added momentum $$ \nabla L(W_t + \mu V_t) $$; in SGD we simply take the gradient $$ \nabla L(W_t) $$ on the current weights themselves.

[1] Y. Nesterov.
    A Method of Solving a Convex Programming Problem with Convergence Rate $$\mathcal{O}(1/\sqrt{k})$$.
    *Soviet Mathematics Doklady*, 1983.

[2] I. Sutskever, J. Martens, G. Dahl, and G. Hinton.
    [On the Importance of Initialization and Momentum in Deep Learning](http://www.cs.toronto.edu/~fritz/absps/momentum.pdf).
    *Proceedings of the 30th International Conference on Machine Learning*, 2013.

### RMSprop

The **RMSprop** (`type: "RMSProp"`), suggested by Tieleman in a Coursera course lecture, is a gradient-based optimization method (like SGD). The update formulas are

$$
\operatorname{MS}((W_t)_i)= \delta\operatorname{MS}((W_{t-1})_i)+ (1-\delta)(\nabla L(W_t))_i^2 \\
(W_{t+1})_i= (W_{t})_i -\alpha\frac{(\nabla L(W_t))_i}{\sqrt{\operatorname{MS}((W_t)_i)}}
$$

The default value of $$\delta$$ (`rms_decay`) is set to $$\delta=0.99$$.

[1] T. Tieleman, and G. Hinton.
    [RMSProp: Divide the gradient by a running average of its recent magnitude](http://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf).
    *COURSERA: Neural Networks for Machine Learning.Technical report*, 2012.

## Scaffolding

The solver scaffolding prepares the optimization method and initializes the model to be learned in `Solver::Presolve()`.

    > caffe train -solver examples/mnist/lenet_solver.prototxt
    I0902 13:35:56.474978 16020 caffe.cpp:90] Starting Optimization
    I0902 13:35:56.475190 16020 solver.cpp:32] Initializing solver from parameters:
    test_iter: 100
    test_interval: 500
    base_lr: 0.01
    display: 100
    max_iter: 10000
    lr_policy: "inv"
    gamma: 0.0001
    power: 0.75
    momentum: 0.9
    weight_decay: 0.0005
    snapshot: 5000
    snapshot_prefix: "examples/mnist/lenet"
    solver_mode: GPU
    net: "examples/mnist/lenet_train_test.prototxt"

Net initialization

    I0902 13:35:56.655681 16020 solver.cpp:72] Creating training net from net file: examples/mnist/lenet_train_test.prototxt
    [...]
    I0902 13:35:56.656740 16020 net.cpp:56] Memory required for data: 0
    I0902 13:35:56.656791 16020 net.cpp:67] Creating Layer mnist
    I0902 13:35:56.656811 16020 net.cpp:356] mnist -> data
    I0902 13:35:56.656846 16020 net.cpp:356] mnist -> label
    I0902 13:35:56.656874 16020 net.cpp:96] Setting up mnist
    I0902 13:35:56.694052 16020 data_layer.cpp:135] Opening lmdb examples/mnist/mnist_train_lmdb
    I0902 13:35:56.701062 16020 data_layer.cpp:195] output data size: 64,1,28,28
    I0902 13:35:56.701146 16020 data_layer.cpp:236] Initializing prefetch
    I0902 13:35:56.701196 16020 data_layer.cpp:238] Prefetch initialized.
    I0902 13:35:56.701212 16020 net.cpp:103] Top shape: 64 1 28 28 (50176)
    I0902 13:35:56.701230 16020 net.cpp:103] Top shape: 64 1 1 1 (64)
    [...]
    I0902 13:35:56.703737 16020 net.cpp:67] Creating Layer ip1
    I0902 13:35:56.703753 16020 net.cpp:394] ip1 <- pool2
    I0902 13:35:56.703778 16020 net.cpp:356] ip1 -> ip1
    I0902 13:35:56.703797 16020 net.cpp:96] Setting up ip1
    I0902 13:35:56.728127 16020 net.cpp:103] Top shape: 64 500 1 1 (32000)
    I0902 13:35:56.728142 16020 net.cpp:113] Memory required for data: 5039360
    I0902 13:35:56.728175 16020 net.cpp:67] Creating Layer relu1
    I0902 13:35:56.728194 16020 net.cpp:394] relu1 <- ip1
    I0902 13:35:56.728219 16020 net.cpp:345] relu1 -> ip1 (in-place)
    I0902 13:35:56.728240 16020 net.cpp:96] Setting up relu1
    I0902 13:35:56.728256 16020 net.cpp:103] Top shape: 64 500 1 1 (32000)
    I0902 13:35:56.728270 16020 net.cpp:113] Memory required for data: 5167360
    I0902 13:35:56.728287 16020 net.cpp:67] Creating Layer ip2
    I0902 13:35:56.728304 16020 net.cpp:394] ip2 <- ip1
    I0902 13:35:56.728333 16020 net.cpp:356] ip2 -> ip2
    I0902 13:35:56.728356 16020 net.cpp:96] Setting up ip2
    I0902 13:35:56.728690 16020 net.cpp:103] Top shape: 64 10 1 1 (640)
    I0902 13:35:56.728705 16020 net.cpp:113] Memory required for data: 5169920
    I0902 13:35:56.728734 16020 net.cpp:67] Creating Layer loss
    I0902 13:35:56.728747 16020 net.cpp:394] loss <- ip2
    I0902 13:35:56.728767 16020 net.cpp:394] loss <- label
    I0902 13:35:56.728786 16020 net.cpp:356] loss -> loss
    I0902 13:35:56.728811 16020 net.cpp:96] Setting up loss
    I0902 13:35:56.728837 16020 net.cpp:103] Top shape: 1 1 1 1 (1)
    I0902 13:35:56.728849 16020 net.cpp:109]     with loss weight 1
    I0902 13:35:56.728878 16020 net.cpp:113] Memory required for data: 5169924

Loss

    I0902 13:35:56.728893 16020 net.cpp:170] loss needs backward computation.
    I0902 13:35:56.728909 16020 net.cpp:170] ip2 needs backward computation.
    I0902 13:35:56.728924 16020 net.cpp:170] relu1 needs backward computation.
    I0902 13:35:56.728938 16020 net.cpp:170] ip1 needs backward computation.
    I0902 13:35:56.728953 16020 net.cpp:170] pool2 needs backward computation.
    I0902 13:35:56.728970 16020 net.cpp:170] conv2 needs backward computation.
    I0902 13:35:56.728984 16020 net.cpp:170] pool1 needs backward computation.
    I0902 13:35:56.728998 16020 net.cpp:170] conv1 needs backward computation.
    I0902 13:35:56.729014 16020 net.cpp:172] mnist does not need backward computation.
    I0902 13:35:56.729027 16020 net.cpp:208] This network produces output loss
    I0902 13:35:56.729053 16020 net.cpp:467] Collecting Learning Rate and Weight Decay.
    I0902 13:35:56.729071 16020 net.cpp:219] Network initialization done.
    I0902 13:35:56.729085 16020 net.cpp:220] Memory required for data: 5169924
    I0902 13:35:56.729277 16020 solver.cpp:156] Creating test net (#0) specified by net file: examples/mnist/lenet_train_test.prototxt

Completion

    I0902 13:35:56.806970 16020 solver.cpp:46] Solver scaffolding done.
    I0902 13:35:56.806984 16020 solver.cpp:165] Solving LeNet


## Updating Parameters

The actual weight update is made by the solver then applied to the net parameters in `Solver::ComputeUpdateValue()`.
The `ComputeUpdateValue` method incorporates any weight decay $$ r(W) $$ into the weight gradients (which currently just contain the error gradients) to get the final gradient with respect to each network weight.
Then these gradients are scaled by the learning rate $$ \alpha $$ and the update to subtract is stored in each parameter Blob's `diff` field.
Finally, the `Blob::Update` method is called on each parameter blob, which performs the final update (subtracting the Blob's `diff` from its `data`).

## Snapshotting and Resuming

The solver snapshots the weights and its own state during training in `Solver::Snapshot()` and `Solver::SnapshotSolverState()`.
The weight snapshots export the learned model while the solver snapshots allow training to be resumed from a given point.
Training is resumed by `Solver::Restore()` and `Solver::RestoreSolverState()`.

Weights are saved without extension while solver states are saved with `.solverstate` extension.
Both files will have an `_iter_N` suffix for the snapshot iteration number.

Snapshotting is configured by:

    # The snapshot interval in iterations.
    snapshot: 5000
    # File path prefix for snapshotting model weights and solver state.
    # Note: this is relative to the invocation of the `caffe` utility, not the
    # solver definition file.
    snapshot_prefix: "/path/to/model"
    # Snapshot the diff along with the weights. This can help debugging training
    # but takes more storage.
    snapshot_diff: false
    # A final snapshot is saved at the end of training unless
    # this flag is set to false. The default is true.
    snapshot_after_train: true

in the solver definition prototxt.
---
title: Data
---
# Data: Ins and Outs

Data flows through Caffe as [Blobs](net_layer_blob.html#blob-storage-and-communication).
Data layers load input and save output by converting to and from Blob to other formats.
Common transformations like mean-subtraction and feature-scaling are done by data layer configuration.
New input types are supported by developing a new data layer -- the rest of the Net follows by the modularity of the Caffe layer catalogue.

This data layer definition

    layer {
      name: "mnist"
      # Data layer loads leveldb or lmdb storage DBs for high-throughput.
      type: "Data"
      # the 1st top is the data itself: the name is only convention
      top: "data"
      # the 2nd top is the ground truth: the name is only convention
      top: "label"
      # the Data layer configuration
      data_param {
        # path to the DB
        source: "examples/mnist/mnist_train_lmdb"
        # type of DB: LEVELDB or LMDB (LMDB supports concurrent reads)
        backend: LMDB
        # batch processing improves efficiency.
        batch_size: 64
      }
      # common data transformations
      transform_param {
        # feature scaling coefficient: this maps the [0, 255] MNIST data to [0, 1]
        scale: 0.00390625
      }
    }

loads the MNIST digits.

**Tops and Bottoms**: A data layer makes **top** blobs to output data to the model.
It does not have **bottom** blobs since it takes no input.

**Data and Label**: a data layer has at least one top canonically named **data**.
For ground truth a second top can be defined that is canonically named **label**.
Both tops simply produce blobs and there is nothing inherently special about these names.
The (data, label) pairing is a convenience for classification models.

**Transformations**: data preprocessing is parametrized by transformation messages within the data layer definition.

    layer {
      name: "data"
      type: "Data"
      [...]
      transform_param {
        scale: 0.1
        mean_file_size: mean.binaryproto
        # for images in particular horizontal mirroring and random cropping
        # can be done as simple data augmentations.
        mirror: 1  # 1 = on, 0 = off
        # crop a `crop_size` x `crop_size` patch:
        # - at random during training
        # - from the center during testing
        crop_size: 227
      }
    }

**Prefetching**: for throughput data layers fetch the next batch of data and prepare it in the background while the Net computes the current batch.

**Multiple Inputs**: a Net can have multiple inputs of any number and type. Define as many data layers as needed giving each a unique name and top. Multiple inputs are useful for non-trivial ground truth: one data layer loads the actual data and the other data layer loads the ground truth in lock-step. In this arrangement both data and label can be any 4D array. Further applications of multiple inputs are found in multi-modal and sequence models. In these cases you may need to implement your own data preparation routines or a special data layer.

*Improvements to data processing to add formats, generality, or helper utilities are welcome!*

## Formats

Refer to the layer catalogue of [data layers](layers.html#data-layers) for close-ups on each type of data Caffe understands.

## Deployment Input

For on-the-fly computation deployment Nets define their inputs by `input` fields: these Nets then accept direct assignment of data for online or interactive computation.
---
title: Blobs, Layers, and Nets
---
# Blobs, Layers, and Nets: anatomy of a Caffe model

Deep networks are compositional models that are naturally represented as a collection of inter-connected layers that work on chunks of data. Caffe defines a net layer-by-layer in its own model schema. The network defines the entire model bottom-to-top from input data to loss. As data and derivatives flow through the network in the [forward and backward passes](forward_backward.html) Caffe stores, communicates, and manipulates the information as *blobs*: the blob is the standard array and unified memory interface for the framework. The layer comes next as the foundation of both model and computation. The net follows as the collection and connection of layers. The details of blob describe how information is stored and communicated in and across layers and nets.

[Solving](solver.html) is configured separately to decouple modeling and optimization.

We will go over the details of these components in more detail.

## Blob storage and communication

A Blob is a wrapper over the actual data being processed and passed along by Caffe, and also under the hood provides synchronization capability between the CPU and the GPU. Mathematically, a blob is an N-dimensional array stored in a C-contiguous fashion.

Caffe stores and communicates data using blobs. Blobs provide a unified memory interface holding data; e.g., batches of images, model parameters, and derivatives for optimization.

Blobs conceal the computational and mental overhead of mixed CPU/GPU operation by synchronizing from the CPU host to the GPU device as needed. Memory on the host and device is allocated on demand (lazily) for efficient memory usage.

The conventional blob dimensions for batches of image data are number N x channel K x height H x width W. Blob memory is row-major in layout, so the last / rightmost dimension changes fastest. For example, in a 4D blob, the value at index (n, k, h, w) is physically located at index ((n * K + k) * H + h) * W + w.

- Number / N is the batch size of the data. Batch processing achieves better throughput for communication and device processing. For an ImageNet training batch of 256 images N = 256.
- Channel / K is the feature dimension e.g. for RGB images K = 3.

Note that although many blobs in Caffe examples are 4D with axes for image applications, it is totally valid to use blobs for non-image applications. For example, if you simply need fully-connected networks like the conventional multi-layer perceptron, use 2D blobs (shape (N, D)) and call the InnerProductLayer (which we will cover soon).

Parameter blob dimensions vary according to the type and configuration of the layer. For a convolution layer with 96 filters of 11 x 11 spatial dimension and 3 inputs the blob is 96 x 3 x 11 x 11. For an inner product / fully-connected layer with 1000 output channels and 1024 input channels the parameter blob is 1000 x 1024.

For custom data it may be necessary to hack your own input preparation tool or data layer. However once your data is in your job is done. The modularity of layers accomplishes the rest of the work for you.

### Implementation Details

As we are often interested in the values as well as the gradients of the blob, a Blob stores two chunks of memories, *data* and *diff*. The former is the normal data that we pass along, and the latter is the gradient computed by the network.

Further, as the actual values could be stored either on the CPU and on the GPU, there are two different ways to access them: the const way, which does not change the values, and the mutable way, which changes the values:

    const Dtype* cpu_data() const;
    Dtype* mutable_cpu_data();

(similarly for gpu and diff).

The reason for such design is that, a Blob uses a SyncedMem class to synchronize values between the CPU and GPU in order to hide the synchronization details and to minimize data transfer. A rule of thumb is, always use the const call if you do not want to change the values, and never store the pointers in your own object. Every time you work on a blob, call the functions to get the pointers, as the SyncedMem will need this to figure out when to copy data.

In practice when GPUs are present, one loads data from the disk to a blob in CPU code, calls a device kernel to do GPU computation, and ferries the blob off to the next layer, ignoring low-level details while maintaining a high level of performance. As long as all layers have GPU implementations, all the intermediate data and gradients will remain in the GPU.

If you want to check out when a Blob will copy data, here is an illustrative example:

    // Assuming that data are on the CPU initially, and we have a blob.
    const Dtype* foo;
    Dtype* bar;
    foo = blob.gpu_data(); // data copied cpu->gpu.
    foo = blob.cpu_data(); // no data copied since both have up-to-date contents.
    bar = blob.mutable_gpu_data(); // no data copied.
    // ... some operations ...
    bar = blob.mutable_gpu_data(); // no data copied when we are still on GPU.
    foo = blob.cpu_data(); // data copied gpu->cpu, since the gpu side has modified the data
    foo = blob.gpu_data(); // no data copied since both have up-to-date contents
    bar = blob.mutable_cpu_data(); // still no data copied.
    bar = blob.mutable_gpu_data(); // data copied cpu->gpu.
    bar = blob.mutable_cpu_data(); // data copied gpu->cpu.

## Layer computation and connections

The layer is the essence of a model and the fundamental unit of computation. Layers convolve filters, pool, take inner products, apply nonlinearities like rectified-linear and sigmoid and other elementwise transformations, normalize, load data, and compute losses like softmax and hinge. [See the layer catalogue](layers.html) for all operations. Most of the types needed for state-of-the-art deep learning tasks are there.

<img src="fig/layer.jpg" alt="A layer with bottom and top blob." width="256">

A layer takes input through *bottom* connections and makes output through *top* connections.

Each layer type defines three critical computations: *setup*, *forward*, and *backward*.

- Setup: initialize the layer and its connections once at model initialization.
- Forward: given input from bottom compute the output and send to the top.
- Backward: given the gradient w.r.t. the top output compute the gradient w.r.t. to the input and send to the bottom. A layer with parameters computes the gradient w.r.t. to its parameters and stores it internally.

More specifically, there will be two Forward and Backward functions implemented, one for CPU and one for GPU. If you do not implement a GPU version, the layer will fall back to the CPU functions as a backup option. This may come handy if you would like to do quick experiments, although it may come with additional data transfer cost (its inputs will be copied from GPU to CPU, and its outputs will be copied back from CPU to GPU).

Layers have two key responsibilities for the operation of the network as a whole: a *forward pass* that takes the inputs and produces the outputs, and a *backward pass* that takes the gradient with respect to the output, and computes the gradients with respect to the parameters and to the inputs, which are in turn back-propagated to earlier layers. These passes are simply the composition of each layer's forward and backward.

Developing custom layers requires minimal effort by the compositionality of the network and modularity of the code. Define the setup, forward, and backward for the layer and it is ready for inclusion in a net.

## Net definition and operation

The net jointly defines a function and its gradient by composition and auto-differentiation. The composition of every layer's output computes the function to do a given task, and the composition of every layer's backward computes the gradient from the loss to learn the task. Caffe models are end-to-end machine learning engines.

The net is a set of layers connected in a computation graph -- a directed acyclic graph (DAG) to be exact. Caffe does all the bookkeeping for any DAG of layers to ensure correctness of the forward and backward passes. A typical net begins with a data layer that loads from disk and ends with a loss layer that computes the objective for a task such as classification or reconstruction.

The net is defined as a set of layers and their connections in a plaintext modeling language.
A simple logistic regression classifier

<img src="fig/logreg.jpg" alt="Softmax Regression" width="256">

is defined by

    name: "LogReg"
    layer {
      name: "mnist"
      type: "Data"
      top: "data"
      top: "label"
      data_param {
        source: "input_leveldb"
        batch_size: 64
      }
    }
    layer {
      name: "ip"
      type: "InnerProduct"
      bottom: "data"
      top: "ip"
      inner_product_param {
        num_output: 2
      }
    }
    layer {
      name: "loss"
      type: "SoftmaxWithLoss"
      bottom: "ip"
      bottom: "label"
      top: "loss"
    }

Model initialization is handled by `Net::Init()`. The initialization mainly does two things: scaffolding the overall DAG by creating the blobs and layers (for C++ geeks: the network will retain ownership of the blobs and layers during its lifetime), and calls the layers' `SetUp()` function. It also does a set of other bookkeeping things, such as validating the correctness of the overall network architecture. Also, during initialization the Net explains its initialization by logging to INFO as it goes:

    I0902 22:52:17.931977 2079114000 net.cpp:39] Initializing net from parameters:
    name: "LogReg"
    [...model prototxt printout...]
    # construct the network layer-by-layer
    I0902 22:52:17.932152 2079114000 net.cpp:67] Creating Layer mnist
    I0902 22:52:17.932165 2079114000 net.cpp:356] mnist -> data
    I0902 22:52:17.932188 2079114000 net.cpp:356] mnist -> label
    I0902 22:52:17.932200 2079114000 net.cpp:96] Setting up mnist
    I0902 22:52:17.935807 2079114000 data_layer.cpp:135] Opening leveldb input_leveldb
    I0902 22:52:17.937155 2079114000 data_layer.cpp:195] output data size: 64,1,28,28
    I0902 22:52:17.938570 2079114000 net.cpp:103] Top shape: 64 1 28 28 (50176)
    I0902 22:52:17.938593 2079114000 net.cpp:103] Top shape: 64 (64)
    I0902 22:52:17.938611 2079114000 net.cpp:67] Creating Layer ip
    I0902 22:52:17.938617 2079114000 net.cpp:394] ip <- data
    I0902 22:52:17.939177 2079114000 net.cpp:356] ip -> ip
    I0902 22:52:17.939196 2079114000 net.cpp:96] Setting up ip
    I0902 22:52:17.940289 2079114000 net.cpp:103] Top shape: 64 2 (128)
    I0902 22:52:17.941270 2079114000 net.cpp:67] Creating Layer loss
    I0902 22:52:17.941305 2079114000 net.cpp:394] loss <- ip
    I0902 22:52:17.941314 2079114000 net.cpp:394] loss <- label
    I0902 22:52:17.941323 2079114000 net.cpp:356] loss -> loss
    # set up the loss and configure the backward pass
    I0902 22:52:17.941328 2079114000 net.cpp:96] Setting up loss
    I0902 22:52:17.941328 2079114000 net.cpp:103] Top shape: (1)
    I0902 22:52:17.941329 2079114000 net.cpp:109]     with loss weight 1
    I0902 22:52:17.941779 2079114000 net.cpp:170] loss needs backward computation.
    I0902 22:52:17.941787 2079114000 net.cpp:170] ip needs backward computation.
    I0902 22:52:17.941794 2079114000 net.cpp:172] mnist does not need backward computation.
    # determine outputs
    I0902 22:52:17.941800 2079114000 net.cpp:208] This network produces output loss
    # finish initialization and report memory usage
    I0902 22:52:17.941810 2079114000 net.cpp:467] Collecting Learning Rate and Weight Decay.
    I0902 22:52:17.941818 2079114000 net.cpp:219] Network initialization done.
    I0902 22:52:17.941824 2079114000 net.cpp:220] Memory required for data: 201476

Note that the construction of the network is device agnostic - recall our earlier explanation that blobs and layers hide implementation details from the model definition. After construction, the network is run on either CPU or GPU by setting a single switch defined in `Caffe::mode()` and set by `Caffe::set_mode()`. Layers come with corresponding CPU and GPU routines that produce identical results (up to numerical errors, and with tests to guard it). The CPU / GPU switch is seamless and independent of the model definition. For research and deployment alike it is best to divide model and implementation.

### Model format

The models are defined in plaintext protocol buffer schema (prototxt) while the learned models are serialized as binary protocol buffer (binaryproto) .caffemodel files.

The model format is defined by the protobuf schema in [caffe.proto](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto). The source file is mostly self-explanatory so one is encouraged to check it out.

Caffe speaks [Google Protocol Buffer](https://code.google.com/p/protobuf/) for the following strengths: minimal-size binary strings when serialized, efficient serialization, a human-readable text format compatible with the binary version, and efficient interface implementations in multiple languages, most notably C++ and Python. This all contributes to the flexibility and extensibility of modeling in Caffe.
---
title: Layer Catalogue
---

# Layers

To create a Caffe model you need to define the model architecture in a protocol buffer definition file (prototxt).

Caffe layers and their parameters are defined in the protocol buffer definitions for the project in [caffe.proto](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto).

## Data Layers

Data enters Caffe through data layers: they lie at the bottom of nets. Data can come from efficient databases (LevelDB or LMDB), directly from memory, or, when efficiency is not critical, from files on disk in HDF5 or common image formats.

Common input preprocessing (mean subtraction, scaling, random cropping, and mirroring) is available by specifying `TransformationParameter`s by some of the layers.
The [bias](layers/bias.html), [scale](layers/scale.html), and [crop](layers/crop.html) layers can be helpful with transforming the inputs, when `TransformationParameter` isn't available.

Layers:

* [Image Data](layers/imagedata.html) - read raw images.
* [Database](layers/data.html) - read data from LEVELDB or LMDB.
* [HDF5 Input](layers/hdf5data.html) - read HDF5 data, allows data of arbitrary dimensions.
* [HDF5 Output](layers/hdf5output.html) - write data as HDF5.
* [Input](layers/input.html) - typically used for networks that are being deployed.
* [Window Data](layers/windowdata.html) - read window data file.
* [Memory Data](layers/memorydata.html) - read data directly from memory.
* [Dummy Data](layers/dummydata.html) - for static data and debugging.

Note that the [Python](layers/python.html) Layer can be useful for create custom data layers.

## Vision Layers

Vision layers usually take *images* as input and produce other *images* as output, although they can take data of other types and dimensions.
A typical "image" in the real-world may have one color channel ($$c = 1$$), as in a grayscale image, or three color channels ($$c = 3$$) as in an RGB (red, green, blue) image.
But in this context, the distinguishing characteristic of an image is its spatial structure: usually an image has some non-trivial height $$h > 1$$ and width $$w > 1$$.
This 2D geometry naturally lends itself to certain decisions about how to process the input.
In particular, most of the vision layers work by applying a particular operation to some region of the input to produce a corresponding region of the output.
In contrast, other layers (with few exceptions) ignore the spatial structure of the input, effectively treating it as "one big vector" with dimension $$chw$$.

Layers:

* [Convolution Layer](layers/convolution.html) - convolves the input image with a set of learnable filters, each producing one feature map in the output image.
* [Pooling Layer](layers/pooling.html) - max, average, or stochastic pooling.
* [Spatial Pyramid Pooling (SPP)](layers/spp.html)
* [Crop](layers/crop.html) - perform cropping transformation.
* [Deconvolution Layer](layers/deconvolution.html) - transposed convolution.

* [Im2Col](layers/im2col.html) - relic helper layer that is not used much anymore.

## Recurrent Layers

Layers:

* [Recurrent](layers/recurrent.html)
* [RNN](layers/rnn.html)
* [Long-Short Term Memory (LSTM)](layers/lstm.html)

## Common Layers

Layers:

* [Inner Product](layers/innerproduct.html) - fully connected layer.
* [Dropout](layers/dropout.html)
* [Embed](layers/embed.html) - for learning embeddings of one-hot encoded vector (takes index as input).

## Normalization Layers

* [Local Response Normalization (LRN)](layers/lrn.html) - performs a kind of "lateral inhibition" by normalizing over local input regions.
* [Mean Variance Normalization (MVN)](layers/mvn.html) - performs contrast normalization / instance normalization.
* [Batch Normalization](layers/batchnorm.html) - performs normalization over mini-batches.

The [bias](layers/bias.html) and [scale](layers/scale.html) layers can be helpful in combination with normalization.

## Activation / Neuron Layers

In general, activation / Neuron layers are element-wise operators, taking one bottom blob and producing one top blob of the same size. In the layers below, we will ignore the input and out sizes as they are identical:

* Input
    - n * c * h * w
* Output
    - n * c * h * w

Layers:

* [ReLU / Rectified-Linear and Leaky-ReLU](layers/relu.html) - ReLU and Leaky-ReLU rectification.
* [PReLU](layers/prelu.html) - parametric ReLU.
* [ELU](layers/elu.html) - exponential linear rectification.
* [Sigmoid](layers/sigmoid.html)
* [TanH](layers/tanh.html)
* [Absolute Value](layers/abs.html)
* [Power](layers/power.html) - f(x) = (shift + scale * x) ^ power.
* [Exp](layers/exp.html) - f(x) = base ^ (shift + scale * x).
* [Log](layers/log.html) - f(x) = log(x).
* [BNLL](layers/bnll.html) - f(x) = log(1 + exp(x)).
* [Threshold](layers/threshold.html) - performs step function at user defined threshold.
* [Bias](layers/bias.html) - adds a bias to a blob that can either be learned or fixed.
* [Scale](layers/scale.html) - scales a blob by an amount that can either be learned or fixed.

## Utility Layers

Layers:

* [Flatten](layers/flatten.html)
* [Reshape](layers/reshape.html)
* [Batch Reindex](layers/batchreindex.html)

* [Split](layers/split.html)
* [Concat](layers/concat.html)
* [Slicing](layers/slice.html)
* [Eltwise](layers/eltwise.html) - element-wise operations such as product or sum between two blobs.
* [Filter / Mask](layers/filter.html) - mask or select output using last blob.
* [Parameter](layers/parameter.html) - enable parameters to be shared between layers.
* [Reduction](layers/reduction.html) - reduce input blob to scalar blob using operations such as sum or mean.
* [Silence](layers/silence.html) - prevent top-level blobs from being printed during training.

* [ArgMax](layers/argmax.html)
* [Softmax](layers/softmax.html)

* [Python](layers/python.html) - allows custom Python layers.

## Loss Layers

Loss drives learning by comparing an output to a target and assigning cost to minimize. The loss itself is computed by the forward pass and the gradient w.r.t. to the loss is computed by the backward pass.

Layers:

* [Multinomial Logistic Loss](layers/multinomiallogisticloss.html)
* [Infogain Loss](layers/infogainloss.html) - a generalization of MultinomialLogisticLossLayer.
* [Softmax with Loss](layers/softmaxwithloss.html) - computes the multinomial logistic loss of the softmax of its inputs. It's conceptually identical to a softmax layer followed by a multinomial logistic loss layer, but provides a more numerically stable gradient.
* [Sum-of-Squares / Euclidean](layers/euclideanloss.html) - computes the sum of squares of differences of its two inputs, $$\frac 1 {2N} \sum_{i=1}^N \| x^1_i - x^2_i \|_2^2$$.
* [Hinge / Margin](layers/hingeloss.html) - The hinge loss layer computes a one-vs-all hinge (L1) or squared hinge loss (L2).
* [Sigmoid Cross-Entropy Loss](layers/sigmoidcrossentropyloss.html) - computes the cross-entropy (logistic) loss, often used for predicting targets interpreted as probabilities.
* [Accuracy / Top-k layer](layers/accuracy.html) - scores the output as an accuracy with respect to target -- it is not actually a loss and has no backward step.
* [Contrastive Loss](layers/contrastiveloss.html)

---
title: Caffe Tutorial
---
# Caffe Tutorial

Caffe is a deep learning framework and this tutorial explains its philosophy, architecture, and usage.
This is a practical guide and framework introduction, so the full frontier, context, and history of deep learning cannot be covered here.
While explanations will be given where possible, a background in machine learning and neural networks is helpful.

## Philosophy

In one sip, Caffe is brewed for

- Expression: models and optimizations are defined as plaintext schemas instead of code.
- Speed: for research and industry alike speed is crucial for state-of-the-art models and massive data.
- Modularity: new tasks and settings require flexibility and extension.
- Openness: scientific and applied progress call for common code, reference models, and reproducibility.
- Community: academic research, startup prototypes, and industrial applications all share strength by joint discussion and development in a BSD-2 project.

and these principles direct the project.

## Tour

- [Nets, Layers, and Blobs](net_layer_blob.html): the anatomy of a Caffe model.
- [Forward / Backward](forward_backward.html): the essential computations of layered compositional models.
- [Loss](loss.html): the task to be learned is defined by the loss.
- [Solver](solver.html): the solver coordinates model optimization.
- [Layer Catalogue](layers.html): the layer is the fundamental unit of modeling and computation -- Caffe's catalogue includes layers for state-of-the-art models.
- [Interfaces](interfaces.html): command line, Python, and MATLAB Caffe.
- [Data](data.html): how to caffeinate data for model input.

For a closer look at a few details:

- [Caffeinated Convolution](convolution.html): how Caffe computes convolutions.

## Deeper Learning

There are helpful references freely online for deep learning that complement our hands-on tutorial.
These cover introductory and advanced material, background and history, and the latest advances.

The [Tutorial on Deep Learning for Vision](https://sites.google.com/site/deeplearningcvpr2014/) from CVPR '14 is a good companion tutorial for researchers.
Once you have the framework and practice foundations from the Caffe tutorial, explore the fundamental ideas and advanced research directions in the CVPR '14 tutorial.

A broad introduction is given in the free online draft of [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/index.html) by Michael Nielsen. In particular the chapters on using neural nets and how backpropagation works are helpful if you are new to the subject.

These recent academic tutorials cover deep learning for researchers in machine learning and vision:

- [Deep Learning Tutorial](http://www.cs.nyu.edu/~yann/talks/lecun-ranzato-icml2013.pdf) by Yann LeCun (NYU, Facebook) and Marc'Aurelio Ranzato (Facebook). ICML 2013 tutorial.
- [LISA Deep Learning Tutorial](http://deeplearning.net/tutorial/deeplearning.pdf) by the LISA Lab directed by Yoshua Bengio (U. Montréal).

For an exposition of neural networks in circuits and code, check out [Understanding Neural Networks from a Programmer's Perspective](http://karpathy.github.io/neuralnets/) by Andrej Karpathy (Stanford).
---
title: Loss
---
# Loss

In Caffe, as in most of machine learning, learning is driven by a **loss** function (also known as an **error**, **cost**, or **objective** function).
A loss function specifies the goal of learning by mapping parameter settings (i.e., the current network weights) to a scalar value specifying the  "badness" of these parameter settings.
Hence, the goal of learning is to find a setting of the weights that *minimizes* the loss function.

The loss in Caffe is computed by the Forward pass of the network.
Each layer takes a set of input (`bottom`) blobs and produces a set of output (`top`) blobs.
Some of these layers' outputs may be used in the loss function.
A typical choice of loss function for one-versus-all classification tasks is the `SoftmaxWithLoss` function, used in a network definition as follows, for example:

    layer {
      name: "loss"
      type: "SoftmaxWithLoss"
      bottom: "pred"
      bottom: "label"
      top: "loss"
    }

In a `SoftmaxWithLoss` function, the `top` blob is a scalar (empty shape) which averages the loss (computed from predicted labels `pred` and actuals labels `label`) over the entire mini-batch.

### Loss weights

For nets with multiple layers producing a loss (e.g., a network that both classifies the input using a `SoftmaxWithLoss` layer and reconstructs it using a `EuclideanLoss` layer), *loss weights* can be used to specify their relative importance.

By convention, Caffe layer types with the suffix `Loss` contribute to the loss function, but other layers are assumed to be purely used for intermediate computations.
However, any layer can be used as a loss by adding a field `loss_weight: <float>` to a layer definition for each `top` blob produced by the layer.
Layers with the suffix `Loss` have an implicit `loss_weight: 1` for the first `top` blob (and `loss_weight: 0` for any additional `top`s); other layers have an implicit `loss_weight: 0` for all `top`s.
So, the above `SoftmaxWithLoss` layer could be equivalently written as:

    layer {
      name: "loss"
      type: "SoftmaxWithLoss"
      bottom: "pred"
      bottom: "label"
      top: "loss"
      loss_weight: 1
    }

However, *any* layer able to backpropagate may be given a non-zero `loss_weight`, allowing one to, for example, regularize the activations produced by some intermediate layer(s) of the network if desired.
For non-singleton outputs with an associated non-zero loss, the loss is computed simply by summing over all entries of the blob.

The final loss in Caffe, then, is computed by summing the total weighted loss over the network, as in the following pseudo-code:

    loss := 0
    for layer in layers:
      for top, loss_weight in layer.tops, layer.loss_weights:
        loss += loss_weight * sum(top)
---
title: Interfaces
---
# Interfaces

Caffe has command line, Python, and MATLAB interfaces for day-to-day usage, interfacing with research code, and rapid prototyping. While Caffe is a C++ library at heart and it exposes a modular interface for development, not every occasion calls for custom compilation. The cmdcaffe, pycaffe, and matcaffe interfaces are here for you.

## Command Line

The command line interface -- cmdcaffe -- is the `caffe` tool for model training, scoring, and diagnostics. Run `caffe` without any arguments for help. This tool and others are found in caffe/build/tools. (The following example calls require completing the LeNet / MNIST example first.)

**Training**: `caffe train` learns models from scratch, resumes learning from saved snapshots, and fine-tunes models to new data and tasks:

* All training requires a solver configuration through the `-solver solver.prototxt` argument.
* Resuming requires the `-snapshot model_iter_1000.solverstate` argument to load the solver snapshot.
* Fine-tuning requires the `-weights model.caffemodel` argument for the model initialization.

For example, you can run:

    # train LeNet
    caffe train -solver examples/mnist/lenet_solver.prototxt
    # train on GPU 2
    caffe train -solver examples/mnist/lenet_solver.prototxt -gpu 2
    # resume training from the half-way point snapshot
    caffe train -solver examples/mnist/lenet_solver.prototxt -snapshot examples/mnist/lenet_iter_5000.solverstate

For a full example of fine-tuning, see examples/finetuning_on_flickr_style, but the training call alone is

    # fine-tune CaffeNet model weights for style recognition
    caffe train -solver examples/finetuning_on_flickr_style/solver.prototxt -weights models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel

**Testing**: `caffe test` scores models by running them in the test phase and reports the net output as its score. The net architecture must be properly defined to output an accuracy measure or loss as its output. The per-batch score is reported and then the grand average is reported last.

    # score the learned LeNet model on the validation set as defined in the
    # model architeture lenet_train_test.prototxt
    caffe test -model examples/mnist/lenet_train_test.prototxt -weights examples/mnist/lenet_iter_10000.caffemodel -gpu 0 -iterations 100

**Benchmarking**: `caffe time` benchmarks model execution layer-by-layer through timing and synchronization. This is useful to check system performance and measure relative execution times for models.

    # (These example calls require you complete the LeNet / MNIST example first.)
    # time LeNet training on CPU for 10 iterations
    caffe time -model examples/mnist/lenet_train_test.prototxt -iterations 10
    # time LeNet training on GPU for the default 50 iterations
    caffe time -model examples/mnist/lenet_train_test.prototxt -gpu 0
    # time a model architecture with the given weights on the first GPU for 10 iterations
    caffe time -model examples/mnist/lenet_train_test.prototxt -weights examples/mnist/lenet_iter_10000.caffemodel -gpu 0 -iterations 10

**Diagnostics**: `caffe device_query` reports GPU details for reference and checking device ordinals for running on a given device in multi-GPU machines.

    # query the first device
    caffe device_query -gpu 0

**Parallelism**: the `-gpu` flag to the `caffe` tool can take a comma separated list of IDs to run on multiple GPUs. A solver and net will be instantiated for each GPU so the batch size is effectively multiplied by the number of GPUs. To reproduce single GPU training, reduce the batch size in the network definition accordingly.

    # train on GPUs 0 & 1 (doubling the batch size)
    caffe train -solver examples/mnist/lenet_solver.prototxt -gpu 0,1
    # train on all GPUs (multiplying batch size by number of devices)
    caffe train -solver examples/mnist/lenet_solver.prototxt -gpu all

## Python

The Python interface -- pycaffe -- is the `caffe` module and its scripts in caffe/python. `import caffe` to load models, do forward and backward, handle IO, visualize networks, and even instrument model solving. All model data, derivatives, and parameters are exposed for reading and writing.

- `caffe.Net` is the central interface for loading, configuring, and running models. `caffe.Classifier` and `caffe.Detector` provide convenience interfaces for common tasks.
- `caffe.SGDSolver` exposes the solving interface.
- `caffe.io` handles input / output with preprocessing and protocol buffers.
- `caffe.draw` visualizes network architectures.
- Caffe blobs are exposed as numpy ndarrays for ease-of-use and efficiency.

Tutorial IPython notebooks are found in caffe/examples: do `ipython notebook caffe/examples` to try them. For developer reference docstrings can be found throughout the code.

Compile pycaffe by `make pycaffe`.
Add the module directory to your `$PYTHONPATH` by `export PYTHONPATH=/path/to/caffe/python:$PYTHONPATH` or the like for `import caffe`.

## MATLAB

The MATLAB interface -- matcaffe -- is the `caffe` package in caffe/matlab in which you can integrate Caffe in your Matlab code.

In MatCaffe, you can

* Creating multiple Nets in Matlab
* Do forward and backward computation
* Access any layer within a network, and any parameter blob in a layer
* Get and set data or diff to any blob within a network, not restricting to input blobs or output blobs
* Save a network's parameters to file, and load parameters from file
* Reshape a blob and reshape a network
* Edit network parameter and do network surgery
* Create multiple Solvers in Matlab for training
* Resume training from solver snapshots
* Access train net and test nets in a solver
* Run for a certain number of iterations and give back control to Matlab
* Intermingle arbitrary Matlab code with gradient steps

An ILSVRC image classification demo is in caffe/matlab/demo/classification_demo.m (you need to download BAIR CaffeNet from [Model Zoo](http://caffe.berkeleyvision.org/model_zoo.html) to run it).

### Build MatCaffe

Build MatCaffe with `make all matcaffe`. After that, you may test it using `make mattest`.

Common issue: if you run into error messages like `libstdc++.so.6:version 'GLIBCXX_3.4.15' not found` during `make mattest`, then it usually means that your Matlab's runtime libraries do not match your compile-time libraries. You may need to do the following before you start Matlab:

    export LD_LIBRARY_PATH=/opt/intel/mkl/lib/intel64:/usr/local/cuda/lib64
    export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6

Or the equivalent based on where things are installed on your system, and do `make mattest` again to see if the issue is fixed. Note: this issue is sometimes more complicated since during its startup Matlab may overwrite your `LD_LIBRARY_PATH` environment variable. You can run `!ldd ./matlab/+caffe/private/caffe_.mexa64` (the mex extension may differ on your system) in Matlab to see its runtime libraries, and preload your compile-time libraries by exporting them to your `LD_PRELOAD` environment variable.

After successful building and testing, add this package to Matlab search PATH by starting `matlab` from caffe root folder and running the following commands in Matlab command window.

    addpath ./matlab

You can save your Matlab search PATH by running `savepath` so that you don't have to run the command above again every time you use MatCaffe.

### Use MatCaffe

MatCaffe is very similar to PyCaffe in usage.

Examples below shows detailed usages and assumes you have downloaded BAIR CaffeNet from [Model Zoo](http://caffe.berkeleyvision.org/model_zoo.html) and started `matlab` from caffe root folder.

    model = './models/bvlc_reference_caffenet/deploy.prototxt';
    weights = './models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel';

#### Set mode and device

**Mode and device should always be set BEFORE you create a net or a solver.**

Use CPU:

    caffe.set_mode_cpu();

Use GPU and specify its gpu_id:

    caffe.set_mode_gpu();
    caffe.set_device(gpu_id);

#### Create a network and access its layers and blobs

Create a network:

    net = caffe.Net(model, weights, 'test'); % create net and load weights

Or

    net = caffe.Net(model, 'test'); % create net but not load weights
    net.copy_from(weights); % load weights

which creates `net` object as

      Net with properties:

               layer_vec: [1x23 caffe.Layer]
                blob_vec: [1x15 caffe.Blob]
                  inputs: {'data'}
                 outputs: {'prob'}
        name2layer_index: [23x1 containers.Map]
         name2blob_index: [15x1 containers.Map]
             layer_names: {23x1 cell}
              blob_names: {15x1 cell}

The two `containers.Map` objects are useful to find the index of a layer or a blob by its name.

You have access to every blob in this network. To fill blob 'data' with all ones:

    net.blobs('data').set_data(ones(net.blobs('data').shape));

To multiply all values in blob 'data' by 10:

    net.blobs('data').set_data(net.blobs('data').get_data() * 10);

**Be aware that since Matlab is 1-indexed and column-major, the usual 4 blob dimensions in Matlab are `[width, height, channels, num]`, and `width` is the fastest dimension. Also be aware that images are in BGR channels.** Also, Caffe uses single-precision float data. If your data is not single, `set_data` will automatically convert it to single.

You also have access to every layer, so you can do network surgery. For example, to multiply conv1 parameters by 10:

    net.params('conv1', 1).set_data(net.params('conv1', 1).get_data() * 10); % set weights
    net.params('conv1', 2).set_data(net.params('conv1', 2).get_data() * 10); % set bias

Alternatively, you can use

    net.layers('conv1').params(1).set_data(net.layers('conv1').params(1).get_data() * 10);
    net.layers('conv1').params(2).set_data(net.layers('conv1').params(2).get_data() * 10);

To save the network you just modified:

    net.save('my_net.caffemodel');

To get a layer's type (string):

    layer_type = net.layers('conv1').type;

#### Forward and backward

Forward pass can be done using `net.forward` or `net.forward_prefilled`. Function `net.forward` takes in a cell array of N-D arrays containing data of input blob(s) and outputs a cell array containing data from output blob(s). Function `net.forward_prefilled` uses existing data in input blob(s) during forward pass, takes no input and produces no output. After creating some data for input blobs like `data = rand(net.blobs('data').shape);` you can run

    res = net.forward({data});
    prob = res{1};

Or

    net.blobs('data').set_data(data);
    net.forward_prefilled();
    prob = net.blobs('prob').get_data();

Backward is similar using `net.backward` or `net.backward_prefilled` and replacing `get_data` and `set_data` with `get_diff` and `set_diff`. After creating some gradients for output blobs like `prob_diff = rand(net.blobs('prob').shape);` you can run

    res = net.backward({prob_diff});
    data_diff = res{1};

Or

    net.blobs('prob').set_diff(prob_diff);
    net.backward_prefilled();
    data_diff = net.blobs('data').get_diff();

**However, the backward computation above doesn't get correct results, because Caffe decides that the network does not need backward computation. To get correct backward results, you need to set `'force_backward: true'` in your network prototxt.**

After performing forward or backward pass, you can also get the data or diff in internal blobs. For example, to extract pool5 features after forward pass:

    pool5_feat = net.blobs('pool5').get_data();

#### Reshape

Assume you want to run 1 image at a time instead of 10:

    net.blobs('data').reshape([227 227 3 1]); % reshape blob 'data'
    net.reshape();

Then the whole network is reshaped, and now `net.blobs('prob').shape` should be `[1000 1]`;

#### Training

Assume you have created training and validation lmdbs following our [ImageNET Tutorial](http://caffe.berkeleyvision.org/gathered/examples/imagenet.html), to create a solver and train on ILSVRC 2012 classification dataset:

    solver = caffe.Solver('./models/bvlc_reference_caffenet/solver.prototxt');

which creates `solver` object as

      Solver with properties:

              net: [1x1 caffe.Net]
        test_nets: [1x1 caffe.Net]

To train:

    solver.solve();

Or train for only 1000 iterations (so that you can do something to its net before training more iterations)

    solver.step(1000);

To get iteration number:

    iter = solver.iter();

To get its network:

    train_net = solver.net;
    test_net = solver.test_nets(1);

To resume from a snapshot "your_snapshot.solverstate":

    solver.restore('your_snapshot.solverstate');

#### Input and output

`caffe.io` class provides basic input functions `load_image` and `read_mean`. For example, to read ILSVRC 2012 mean file (assume you have downloaded imagenet example auxiliary files by running `./data/ilsvrc12/get_ilsvrc_aux.sh`):

    mean_data = caffe.io.read_mean('./data/ilsvrc12/imagenet_mean.binaryproto');

To read Caffe's example image and resize to `[width, height]` and suppose we want `width = 256; height = 256;`

    im_data = caffe.io.load_image('./examples/images/cat.jpg');
    im_data = imresize(im_data, [width, height]); % resize using Matlab's imresize

**Keep in mind that `width` is the fastest dimension and channels are BGR, which is different from the usual way that Matlab stores an image.** If you don't want to use `caffe.io.load_image` and prefer to load an image by yourself, you can do

    im_data = imread('./examples/images/cat.jpg'); % read image
    im_data = im_data(:, :, [3, 2, 1]); % convert from RGB to BGR
    im_data = permute(im_data, [2, 1, 3]); % permute width and height
    im_data = single(im_data); % convert to single precision

Also, you may take a look at caffe/matlab/demo/classification_demo.m to see how to prepare input by taking crops from an image.

We show in caffe/matlab/hdf5creation how to read and write HDF5 data with Matlab. We do not provide extra functions for data output as Matlab itself is already quite powerful in output.

#### Clear nets and solvers

Call `caffe.reset_all()` to clear all solvers and stand-alone nets you have created.
---
title: Convolution
---
# Caffeinated Convolution

The Caffe strategy for convolution is to reduce the problem to matrix-matrix multiplication.
This linear algebra computation is highly-tuned in BLAS libraries and efficiently computed on GPU devices.

For more details read Yangqing's [Convolution in Caffe: a memo](https://github.com/Yangqing/caffe/wiki/Convolution-in-Caffe:-a-memo).

As it turns out, this same reduction was independently explored in the context of conv. nets by

> K. Chellapilla, S. Puri, P. Simard, et al. High performance convolutional neural networks for document processing. In Tenth International Workshop on Frontiers in Handwriting Recognition, 2006.
---
title: Dropout Layer
---

# Dropout Layer

* Layer type: `Dropout`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1DropoutLayer.html)
* Header: [`./include/caffe/layers/dropout_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/dropout_layer.hpp)
* CPU implementation: [`./src/caffe/layers/dropout_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/dropout_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/dropout_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/dropout_layer.cu)

## Parameters

* Parameters (`DropoutParameter dropout_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/DropoutParameter.txt %}
{% endhighlight %}
---
title: ELU Layer
---

# ELU Layer

* Layer type: `ELU`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ELULayer.html)
* Header: [`./include/caffe/layers/elu_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/elu_layer.hpp)
* CPU implementation: [`./src/caffe/layers/elu_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/elu_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/elu_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/elu_layer.cu)

## References

* Clevert, Djork-Arne, Thomas Unterthiner, and Sepp Hochreiter.
  "Fast and Accurate Deep Network Learning by Exponential Linear Units (ELUs)" [arXiv:1511.07289](https://arxiv.org/abs/1511.07289). (2015).

## Parameters

* Parameters (`ELUParameter elu_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/ELUParameter.txt %}
{% endhighlight %}
---
title: Mean-Variance Normalization (MVN) Layer
---

# Mean-Variance Normalization (MVN) Layer

* Layer type: `MVN`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1MVNLayer.html)
* Header: [`./include/caffe/layers/mvn_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/mvn_layer.hpp)
* CPU implementation: [`./src/caffe/layers/mvn_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/mvn_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/mvn_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/mvn_layer.cu)

## Parameters

* Parameters (`MVNParameter mvn_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/MVNParameter.txt %}
{% endhighlight %}
---
title: HDF5 Output Layer
---

# HDF5 Output Layer

* Layer type: `HDF5Output`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1HDF5OutputLayer.html)
* Header: [`./include/caffe/layers/hdf5_output_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/hdf5_output_layer.hpp)
* CPU implementation: [`./src/caffe/layers/hdf5_output_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/hdf5_output_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/hdf5_output_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/hdf5_output_layer.cu)

The HDF5 output layer performs the opposite function of the other layers in this section: it writes its input blobs to disk.

## Parameters

* Parameters (`HDF5OutputParameter hdf5_output_param`)
    - Required
        - `file_name`: name of file to write to

* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/HDF5OutputParameter.txt %}
{% endhighlight %}
---
title: Reduction Layer
---

# Reduction Layer

* Layer type: `Reduction`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ReductionLayer.html)
* Header: [`./include/caffe/layers/reduction_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/reduction_layer.hpp)
* CPU implementation: [`./src/caffe/layers/reduction_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/reduction_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/reduction_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/reduction_layer.cu)

## Parameters

* Parameters (`ReductionParameter reduction_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/ReductionParameter.txt %}
{% endhighlight %}
---
title: Input Layer
---

# Input Layer

* Layer type: `Input`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1InputLayer.html)
* Header: [`./include/caffe/layers/input_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/input_layer.hpp)
* CPU implementation: [`./src/caffe/layers/input_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/input_layer.cpp)

## Parameters

* Parameters (`InputParameter input_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/InputParameter.txt %}
{% endhighlight %}
---
title: Softmax with Loss Layer
---

# Softmax with Loss Layer

* Layer type: `SoftmaxWithLoss`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1SoftmaxWithLossLayer.html)
* Header: [`./include/caffe/layers/softmax_loss_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/softmax_loss_layer.hpp)
* CPU implementation: [`./src/caffe/layers/softmax_loss_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/softmax_loss_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/softmax_loss_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/softmax_loss_layer.cu)

The softmax loss layer computes the multinomial logistic loss of the softmax of its inputs. It's conceptually identical to a softmax layer followed by a multinomial logistic loss layer, but provides a more numerically stable gradient.

## Parameters

* Parameters (`SoftmaxParameter softmax_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/SoftmaxParameter.txt %}
{% endhighlight %}

* Parameters (`LossParameter loss_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/LossParameter.txt %}
{% endhighlight %}

## See also

* [Softmax layer](softmax.html)
---
title: ReLU / Rectified-Linear and Leaky-ReLU Layer
---

# ReLU / Rectified-Linear and Leaky-ReLU Layer

* Layer type: `ReLU`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ReLULayer.html)
* Header: [`./include/caffe/layers/relu_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/relu_layer.hpp)
* CPU implementation: [`./src/caffe/layers/relu_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/relu_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/relu_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/relu_layer.cu)
* Sample (as seen in [`./models/bvlc_reference_caffenet/train_val.prototxt`](https://github.com/BVLC/caffe/blob/master/models/bvlc_reference_caffenet/train_val.prototxt))

      layer {
        name: "relu1"
        type: "ReLU"
        bottom: "conv1"
        top: "conv1"
      }

Given an input value x, The `ReLU` layer computes the output as x if x > 0 and negative_slope * x if x <= 0. When the negative slope parameter is not set, it is equivalent to the standard ReLU function of taking max(x, 0). It also supports in-place computation, meaning that the bottom and the top blob could be the same to preserve memory consumption.

## Parameters

* Parameters (`ReLUParameter relu_param`)
    - Optional
        - `negative_slope` [default 0]: specifies whether to leak the negative part by multiplying it with the slope value rather than setting it to 0.
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/ReLUParameter.txt %}
{% endhighlight %}
---
title: Tile Layer
---

# Tile Layer

* Layer type: `Tile`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1TileLayer.html)
* Header: [`./include/caffe/layers/tile_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/tile_layer.hpp)
* CPU implementation: [`./src/caffe/layers/tile_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/tile_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/tile_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/tile_layer.cu)

## Parameters

* Parameters (`TileParameter tile_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/TileParameter.txt %}
{% endhighlight %}
---
title: RNN Layer
---

# RNN Layer

* Layer type: `RNN`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1RNNLayer.html)
* Header: [`./include/caffe/layers/rnn_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/rnn_layer.hpp)
* CPU implementation: [`./src/caffe/layers/rnn_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/rnn_layer.cpp)

## Parameters

* Parameters (`RecurrentParameter recurrent_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/RecurrentParameter.txt %}
{% endhighlight %}
---
title: Bias Layer
---

# Bias Layer

* Layer type: `Bias`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1BiasLayer.html)
* Header: [`./include/caffe/layers/bias_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/bias_layer.hpp)
* CPU implementation: [`./src/caffe/layers/bias_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/bias_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/bias_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/bias_layer.cu)

## Parameters
* Parameters (`BiasParameter bias_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/BiasParameter.txt %}
{% endhighlight %}
---
title: Softmax Layer
---

# Softmax Layer

* Layer type: `Softmax`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1SoftmaxLayer.html)
* Header: [`./include/caffe/layers/softmax_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/softmax_layer.hpp)
* CPU implementation: [`./src/caffe/layers/softmax_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/softmax_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/softmax_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/softmax_layer.cu)

## Parameters

* Parameters (`SoftmaxParameter softmax_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/SoftmaxParameter.txt %}
{% endhighlight %}

## See also

* [Softmax loss layer](softmaxwithloss.html)
---
title: Split Layer
---

# Split Layer

* Layer type: `Split`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1SplitLayer.html)
* Header: [`./include/caffe/layers/split_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/split_layer.hpp)
* CPU implementation: [`./src/caffe/layers/split_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/split_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/split_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/split_layer.cu)

The `Split` layer is a utility layer that splits an input blob to multiple output blobs. This is used when a blob is fed into multiple output layers.

## Parameters

Does not take any parameters.
---
title: Memory Data Layer
---

# Memory Data Layer

* Layer type: `MemoryData`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1MemoryDataLayer.html)
* Header: [`./include/caffe/layers/memory_data_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/memory_data_layer.hpp)
* CPU implementation: [`./src/caffe/layers/memory_data_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/memory_data_layer.cpp)

The memory data layer reads data directly from memory, without copying it. In order to use it, one must call `MemoryDataLayer::Reset` (from C++) or `Net.set_input_arrays` (from Python) in order to specify a source of contiguous data (as 4D row major array), which is read one batch-sized chunk at a time.

# Parameters

* Parameters (`MemoryDataParameter memory_data_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/MemoryDataParameter.txt %}
{% endhighlight %}

* Parameters
    - Required
        - `batch_size`, `channels`, `height`, `width`: specify the size of input chunks to read from memory
---
title: Parameter Layer
---

# Parameter Layer

* Layer type: `Parameter`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ParameterLayer.html)
* Header: [`./include/caffe/layers/parameter_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/parameter_layer.hpp)
* CPU implementation: [`./src/caffe/layers/parameter_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/parameter_layer.cpp)

See [https://github.com/BVLC/caffe/pull/2079](https://github.com/BVLC/caffe/pull/2079).

## Parameters

* Parameters (`ParameterParameter parameter_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/ParameterParameter.txt %}
{% endhighlight %}
---
title: Recurrent Layer
---

# Recurrent Layer

* Layer type: `Recurrent`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1RecurrentLayer.html)
* Header: [`./include/caffe/layers/recurrent_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/recurrent_layer.hpp)
* CPU implementation: [`./src/caffe/layers/recurrent_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/recurrent_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/recurrent_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/recurrent_layer.cu)

## Parameters

* Parameters (`RecurrentParameter recurrent_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/RecurrentParameter.txt %}
{% endhighlight %}
---
title: Sigmoid Layer
---

# Sigmoid Layer

* Layer type: `Sigmoid`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1SigmoidLayer.html)
* Header: [`./include/caffe/layers/sigmoid_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/sigmoid_layer.hpp)
* CPU implementation: [`./src/caffe/layers/sigmoid_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/sigmoid_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/sigmoid_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/sigmoid_layer.cu)
* Example (from [`./examples/mnist/mnist_autoencoder.prototxt`](https://github.com/BVLC/caffe/blob/master/examples/mnist/mnist_autoencoder.prototxt)):

      layer {
        name: "encode1neuron"
        bottom: "encode1"
        top: "encode1neuron"
        type: "Sigmoid"
      }

The `Sigmoid` layer computes `sigmoid(x)` for each element `x` in the bottom blob.

## Parameters

* Parameters (`SigmoidParameter sigmoid_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/SigmoidParameter.txt %}
{% endhighlight %}
---
title: Filter Layer
---

# Filter Layer

* Layer type: `Filter`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1FilterLayer.html)
* Header: [`./include/caffe/layers/filter_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/filter_layer.hpp)
* CPU implementation: [`./src/caffe/layers/filter_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/filter_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/filter_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/filter_layer.cu)

## Parameters

Does not take any parameters.
---
title: Absolute Value Layer
---

# Absolute Value Layer

* Layer type: `AbsVal`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1AbsValLayer.html)
* Header: [`./include/caffe/layers/absval_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/absval_layer.hpp)
* CPU implementation: [`./src/caffe/layers/absval_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/absval_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/absval_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/absval_layer.cu)

* Sample

      layer {
        name: "layer"
        bottom: "in"
        top: "out"
        type: "AbsVal"
      }

The `AbsVal` layer computes the output as abs(x) for each input element x.
---
title: ImageData Layer
---

# ImageData Layer

* Layer type: `ImageData`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ImageDataLayer.html)
* Header: [`./include/caffe/layers/image_data_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/image_data_layer.hpp)
* CPU implementation: [`./src/caffe/layers/image_data_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/image_data_layer.cpp)

## Parameters

* Parameters (`ImageDataParameter image_data_parameter`)
    - Required
        - `source`: name of a text file, with each line giving an image filename and label
        - `batch_size`: number of images to batch together
    - Optional
        - `rand_skip`
        - `shuffle` [default false]
        - `new_height`, `new_width`: if provided, resize all images to this size

* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/ImageDataParameter.txt %}
{% endhighlight %}
---
title: Sigmoid Cross-Entropy Loss Layer
---

# Sigmoid Cross-Entropy Loss Layer

* Layer type: `SigmoidCrossEntropyLoss`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1SigmoidCrossEntropyLossLayer.html)
* Header: [`./include/caffe/layers/sigmoid_cross_entropy_loss_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/sigmoid_cross_entropy_loss_layer.hpp)
* CPU implementation: [`./src/caffe/layers/sigmoid_cross_entropy_loss_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/sigmoid_cross_entropy_loss_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/sigmoid_cross_entropy_loss_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/sigmoid_cross_entropy_loss_layer.cu)

To-do.
---
title: Contrastive Loss Layer
---

# Contrastive Loss Layer

* Layer type: `ContrastiveLoss`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ContrastiveLossLayer.html)
* Header: [`./include/caffe/layers/contrastive_loss_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/contrastive_loss_layer.hpp)
* CPU implementation: [`./src/caffe/layers/contrastive_loss_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/contrastive_loss_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/contrastive_loss_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/contrastive_loss_layer.cu)

## Parameters

* Parameters (`ContrastiveLossParameter contrastive_loss_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/ContrastiveLossParameter.txt %}
{% endhighlight %}
---
title: Python Layer
---

# Python Layer

* Layer type: `Python`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1PythonLayer.html)
* Header: [`./include/caffe/layers/python_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/python_layer.hpp)

The Python layer allows users to add customized layers without modifying the Caffe core code.

## Parameters

* Parameters (`PythonParameter python_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/PythonParameter.txt %}
{% endhighlight %}

## Examples and tutorials

* Simple Euclidean loss example
** [Python code](https://github.com/BVLC/caffe/blob/master/examples/pycaffe/layers/pyloss.py)
** [Prototxt](https://github.com/BVLC/caffe/blob/master/examples/pycaffe/linreg.prototxt)
* [Tutorial for writing Python layers with DIGITS](https://github.com/NVIDIA/DIGITS/tree/master/examples/python-layer)
---
title: Silence Layer
---

# Silence Layer

* Layer type: `Silence`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1SilenceLayer.html)
* Header: [`./include/caffe/layers/silence_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/silence_layer.hpp)
* CPU implementation: [`./src/caffe/layers/silence_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/silence_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/silence_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/silence_layer.cu)

Silences a blob, so that it is not printed.

## Parameters

No parameters.
---
title: TanH Layer
---

# TanH Layer

* Header: [`./include/caffe/layers/tanh_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/tanh_layer.hpp)
* CPU implementation: [`./src/caffe/layers/tanh_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/tanh_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/tanh_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/tanh_layer.cu)

## Parameters

* Parameters (`TanHParameter tanh_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/TanHParameter.txt %}
{% endhighlight %}
---
title: Inner Product / Fully Connected Layer
---

# Inner Product / Fully Connected Layer

* Layer type: `InnerProduct`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1InnerProductLayer.html)
* Header: [`./include/caffe/layers/inner_product_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/inner_product_layer.hpp)
* CPU implementation: [`./src/caffe/layers/inner_product_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/inner_product_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/inner_product_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/inner_product_layer.cu)

* Input
    - `n * c_i * h_i * w_i`
* Output
    - `n * c_o * 1 * 1`
* Sample

      layer {
        name: "fc8"
        type: "InnerProduct"
        # learning rate and decay multipliers for the weights
        param { lr_mult: 1 decay_mult: 1 }
        # learning rate and decay multipliers for the biases
        param { lr_mult: 2 decay_mult: 0 }
        inner_product_param {
          num_output: 1000
          weight_filler {
            type: "gaussian"
            std: 0.01
          }
          bias_filler {
            type: "constant"
            value: 0
          }
        }
        bottom: "fc7"
        top: "fc8"
      }

The `InnerProduct` layer (also usually referred to as the fully connected layer) treats the input as a simple vector and produces an output in the form of a single vector (with the blob's height and width set to 1).


## Parameters

* Parameters (`InnerProductParameter inner_product_param`)
    - Required
        - `num_output` (`c_o`): the number of filters
    - Strongly recommended
        - `weight_filler` [default `type: 'constant' value: 0`]
    - Optional
        - `bias_filler` [default `type: 'constant' value: 0`]
        - `bias_term` [default `true`]: specifies whether to learn and apply a set of additive biases to the filter outputs
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/InnerProductParameter.txt %}
{% endhighlight %}
 
---
title: Pooling Layer
---
# Pooling

* Layer type: `Pooling`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1PoolingLayer.html)
* Header: [`./include/caffe/layers/pooling_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/pooling_layer.hpp)
* CPU implementation: [`./src/caffe/layers/pooling_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/pooling_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/pooling_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/pooling_layer.cu)

* Input
    - `n * c * h_i * w_i`
* Output
    - `n * c * h_o * w_o`, where h_o and w_o are computed in the same way as convolution.

## Parameters

* Parameters (`PoolingParameter pooling_param`)
    - Required
        - `kernel_size` (or `kernel_h` and `kernel_w`): specifies height and width of each filter
    - Optional
        - `pool` [default MAX]: the pooling method. Currently MAX, AVE, or STOCHASTIC
        - `pad` (or `pad_h` and `pad_w`) [default 0]: specifies the number of pixels to (implicitly) add to each side of the input
        - `stride` (or `stride_h` and `stride_w`) [default 1]: specifies the intervals at which to apply the filters to the input


* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/PoolingParameter.txt %}
{% endhighlight %}

## Sample
* Sample (as seen in [`./models/bvlc_reference_caffenet/train_val.prototxt`](https://github.com/BVLC/caffe/blob/master/models/bvlc_reference_caffenet/train_val.prototxt))

      layer {
        name: "pool1"
        type: "Pooling"
        bottom: "conv1"
        top: "pool1"
        pooling_param {
          pool: MAX
          kernel_size: 3 # pool over a 3x3 region
          stride: 2      # step two pixels (in the bottom blob) between pooling regions
        }
      }
---
title: Scale Layer
---

# Scale Layer

* Layer type: `Scale`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ScaleLayer.html)
* Header: [`./include/caffe/layers/scale_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/scale_layer.hpp)
* CPU implementation: [`./src/caffe/layers/scale_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/scale_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/scale_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/scale_layer.cu)

## Parameters

* Parameters (`ScaleParameter scale_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/ScaleParameter.txt %}
{% endhighlight %}
---
title: Batch Norm Layer
---

# Batch Norm Layer

* Layer type: `BatchNorm`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1BatchNormLayer.html)
* Header: [`./include/caffe/layers/batch_norm_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/batch_norm_layer.hpp)
* CPU implementation: [`./src/caffe/layers/batch_norm_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/batch_norm_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/batch_norm_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/batch_norm_layer.cu)

## Parameters

* Parameters (`BatchNormParameter batch_norm_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/BatchNormParameter.txt %}
{% endhighlight %}
---
title: Database Layer
---

# Database Layer

* Layer type: `Data`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1DataLayer.html)
* Header: [`./include/caffe/layers/data_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/data_layer.hpp)
* CPU implementation: [`./src/caffe/layers/data_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/data_layer.cpp)


## Parameters

* Parameters (`DataParameter data_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/DataParameter.txt %}
{% endhighlight %}

* Parameters
    - Required
        - `source`: the name of the directory containing the database
        - `batch_size`: the number of inputs to process at one time
    - Optional
        - `rand_skip`: skip up to this number of inputs at the beginning; useful for asynchronous sgd
        - `backend` [default `LEVELDB`]: choose whether to use a `LEVELDB` or `LMDB`

---
title: Dummy Data Layer
---

# Dummy Data Layer

* Layer type: `DummyData`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1DummyDataLayer.html)
* Header: [`./include/caffe/layers/dummy_data_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/dummy_data_layer.hpp)
* CPU implementation: [`./src/caffe/layers/dummy_data_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/dummy_data_layer.cpp)


## Parameters

* Parameters (`DummyDataParameter dummy_data_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/DummyDataParameter.txt %}
{% endhighlight %}
---
title: ArgMax Layer
---

# ArgMax Layer

* Layer type: `ArgMax`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ArgMaxLayer.html)
* Header: [`./include/caffe/layers/argmax_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/argmax_layer.hpp)
* CPU implementation: [`./src/caffe/layers/argmax_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/argmax_layer.cpp)

## Parameters
* Parameters (`ArgMaxParameter argmax_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/ArgMaxParameter.txt %}
{% endhighlight %}
---
title: HDF5 Data Layer
---

# HDF5 Data Layer

* Layer type: `HDF5Data`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1HDF5DataLayer.html)
* Header: [`./include/caffe/layers/hdf5_data_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/hdf5_data_layer.hpp)
* CPU implementation: [`./src/caffe/layers/hdf5_data_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/hdf5_data_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/hdf5_data_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/hdf5_data_layer.cu)

## Parameters

* Parameters (`HDF5DataParameter hdf5_data_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/HDF5DataParameter.txt %}
{% endhighlight %}
---
title: Euclidean Loss Layer
---
# Sum-of-Squares / Euclidean Loss Layer

* Layer type: `EuclideanLoss`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1EuclideanLossLayer.html)
* Header: [`./include/caffe/layers/euclidean_loss_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/euclidean_loss_layer.hpp)
* CPU implementation: [`./src/caffe/layers/euclidean_loss_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/euclidean_loss_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/euclidean_loss_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/euclidean_loss_layer.cu)

The Euclidean loss layer computes the sum of squares of differences of its two inputs, $$\frac 1 {2N} \sum_{i=1}^N \| x^1_i - x^2_i \|_2^2$$.

## Parameters

Does not take any parameters.
---
title: Deconvolution Layer
---

# Deconvolution Layer

* Layer type: `Deconvolution`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1DeconvolutionLayer.html)
* Header: [`./include/caffe/layers/deconv_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/deconv_layer.hpp)
* CPU implementation: [`./src/caffe/layers/deconv_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/deconv_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/deconv_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/deconv_layer.cu)

## Parameters

Uses the same parameters as the Convolution layer.

* Parameters (`ConvolutionParameter convolution_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/ConvolutionParameter.txt %}
{% endhighlight %}
---
title: Power Layer
---

# Power Layer

* Layer type: `Power`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1PowerLayer.html)
* Header: [`./include/caffe/layers/power_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/power_layer.hpp)
* CPU implementation: [`./src/caffe/layers/power_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/power_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/power_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/power_layer.cu)

The `Power` layer computes the output as (shift + scale * x) ^ power for each input element x.

## Parameters
* Parameters (`PowerParameter power_param`)
    - Optional
        - `power` [default 1]
        - `scale` [default 1]
        - `shift` [default 0]

* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/PowerParameter.txt %}
{% endhighlight %}
 
 
 
## Sample

      layer {
        name: "layer"
        bottom: "in"
        top: "out"
        type: "Power"
        power_param {
          power: 1
          scale: 1
          shift: 0
        }
      }

## See also

* [Exponential layer](exp.html)
---
title: Spatial Pyramid Pooling Layer
---

# Spatial Pyramid Pooling Layer

* Layer type: `SPP`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1SPPLayer.html)
* Header: [`./include/caffe/layers/spp_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/spp_layer.hpp)
* CPU implementation: [`./src/caffe/layers/spp_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/spp_layer.cpp)


## Parameters

* Parameters (`SPPParameter spp_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/SPPParameter.txt %}
{% endhighlight %}
---
title: Flatten Layer
---

# Flatten Layer

* Layer type: `Flatten`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1FlattenLayer.html)
* Header: [`./include/caffe/layers/flatten_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/flatten_layer.hpp)
* CPU implementation: [`./src/caffe/layers/flatten_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/flatten_layer.cpp)

The `Flatten` layer is a utility layer that flattens an input of shape `n * c * h * w` to a simple vector output of shape `n * (c*h*w)`.

## Parameters

* Parameters (`FlattenParameter flatten_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/FlattenParameter.txt %}
{% endhighlight %}
---
title: Slice Layer
---

# Slice Layer

* Layer type: `Slice`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1SliceLayer.html)
* Header: [`./include/caffe/layers/slice_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/slice_layer.hpp)
* CPU implementation: [`./src/caffe/layers/slice_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/slice_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/slice_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/slice_layer.cu)

The `Slice` layer is a utility layer that slices an input layer to multiple output layers along a given dimension (currently num or channel only) with given slice indices.

* Sample

      layer {
        name: "slicer_label"
        type: "Slice"
        bottom: "label"
        ## Example of label with a shape N x 3 x 1 x 1
        top: "label1"
        top: "label2"
        top: "label3"
        slice_param {
          axis: 1
          slice_point: 1
          slice_point: 2
        }
      }

`axis` indicates the target axis; `slice_point` indicates indexes in the selected dimension (the number of indices must be equal to the number of top blobs minus one).

## Parameters

* Parameters (`SliceParameter slice_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/SliceParameter.txt %}
{% endhighlight %}

---
title: Infogain Loss Layer
---

# Infogain Loss Layer

* Layer type: `InfogainLoss`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1InfogainLossLayer.html)
* Header: [`./include/caffe/layers/infogain_loss_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/infogain_loss_layer.hpp)
* CPU implementation: [`./src/caffe/layers/infogain_loss_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/infogain_loss_layer.cpp)

A generalization of [MultinomialLogisticLossLayer](multinomiallogisticloss.html) that takes an "information gain" (infogain) matrix specifying the "value" of all label pairs.

Equivalent to the [MultinomialLogisticLossLayer](multinomiallogisticloss.html) if the infogain matrix is the identity.

## Parameters

* Parameters (`Parameter infogain_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/InfogainLossParameter.txt %}
{% endhighlight %}
---
title: Batch Reindex Layer
---

# Batch Reindex Layer

* Layer type: `BatchReindex`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1BatchReindexLayer.html)
* Header: [`./include/caffe/layers/batch_reindex_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/batch_reindex_layer.hpp)
* CPU implementation: [`./src/caffe/layers/batch_reindex_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/batch_reindex_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/batch_reindex_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/batch_reindex_layer.cu)


## Parameters

No parameters.
---
title: Embed Layer
---

# Embed Layer

* Layer type: `Embed`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1EmbedLayer.html)
* Header: [`./include/caffe/layers/embed_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/embed_layer.hpp)
* CPU implementation: [`./src/caffe/layers/embed_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/embed_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/embed_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/embed_layer.cu)

## Parameters

* Parameters (`EmbedParameter embed_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/EmbedParameter.txt %}
{% endhighlight %}
---
title: Threshold Layer
---

# Threshold Layer

* Header: [`./include/caffe/layers/threshold_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/threshold_layer.hpp)
* CPU implementation: [`./src/caffe/layers/threshold_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/threshold_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/threshold_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/threshold_layer.cu)

## Parameters

* Parameters (`ThresholdParameter threshold_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/ThresholdParameter.txt %}
{% endhighlight %}
---
title: Crop Layer
---

# Crop Layer

* Layer type: `Crop`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1CropLayer.html)
* Header: [`./include/caffe/layers/crop_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/crop_layer.hpp)
* CPU implementation: [`./src/caffe/layers/crop_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/crop_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/crop_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/crop_layer.cu)

## Parameters

* Parameters (`CropParameter crop_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/CropParameter.txt %}
{% endhighlight %}
---
title: Im2col Layer
---

# im2col

* File type: `Im2col`
* Header: [`./include/caffe/layers/im2col_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/im2col_layer.hpp)
* CPU implementation: [`./src/caffe/layers/im2col_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/im2col_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/im2col_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/im2col_layer.cu)

`Im2col` is a helper for doing the image-to-column transformation that you most
likely do not need to know about. This is used in Caffe's original convolution
to do matrix multiplication by laying out all patches into a matrix.


---
title: Local Response Normalization (LRN)
---

# Local Response Normalization (LRN)

* Layer type: `LRN`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1LRNLayer.html)
* Header: [`./include/caffe/layers/lrn_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/lrn_layer.hpp)
* CPU Implementation: [`./src/caffe/layers/lrn_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/lrn_layer.cpp)
* CUDA GPU Implementation: [`./src/caffe/layers/lrn_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/lrn_layer.cu)
* Parameters (`LRNParameter lrn_param`)
    - Optional
        - `local_size` [default 5]: the number of channels to sum over (for cross channel LRN) or the side length of the square region to sum over (for within channel LRN)
        - `alpha` [default 1]: the scaling parameter (see below)
        - `beta` [default 5]: the exponent (see below)
        - `norm_region` [default `ACROSS_CHANNELS`]: whether to sum over adjacent channels (`ACROSS_CHANNELS`) or nearby spatial locations (`WITHIN_CHANNEL`)

The local response normalization layer performs a kind of "lateral inhibition" by normalizing over local input regions. In `ACROSS_CHANNELS` mode, the local regions extend across nearby channels, but have no spatial extent (i.e., they have shape `local_size x 1 x 1`). In `WITHIN_CHANNEL` mode, the local regions extend spatially, but are in separate channels (i.e., they have shape `1 x local_size x local_size`). Each input value is divided by $$(1 + (\alpha/n) \sum_i x_i^2)^\beta$$, where $$n$$ is the size of each local region, and the sum is taken over the region centered at that value (zero padding is added where necessary).

## Parameters

* Parameters (`LRNParameter lrn_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/LRNParameter.txt %}
{% endhighlight %}
---
title: PReLU Layer
---

# PReLU Layer

* Layer type: `PReLU`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1PReLULayer.html)
* Header: [`./include/caffe/layers/prelu_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/prelu_layer.hpp)
* CPU implementation: [`./src/caffe/layers/prelu_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/prelu_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/prelu_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/prelu_layer.cu)

## Parameters

* Parameters (`PReLUParameter prelu_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/PReLUParameter.txt %}
{% endhighlight %}
---
title: Eltwise Layer
---

# Eltwise Layer

* Layer type: `Eltwise`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1EltwiseLayer.html)
* Header: [`./include/caffe/layers/eltwise_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/eltwise_layer.hpp)
* CPU implementation: [`./src/caffe/layers/eltwise_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/eltwise_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/eltwise_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/eltwise_layer.cu)

## Parameters

* Parameters (`EltwiseParameter eltwise_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/EltwiseParameter.txt %}
{% endhighlight %}
---
title: WindowData Layer
---

# WindowData Layer

* Layer type: `WindowData`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1WindowDataLayer.html)
* Header: [`./include/caffe/layers/window_data_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/window_data_layer.hpp)
* CPU implementation: [`./src/caffe/layers/window_data_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/window_data_layer.cpp)

## Parameters

* Parameters (`WindowDataParameter`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/WindowDataParameter.txt %}
{% endhighlight %}
---
title: Hinge Loss Layer
---

# Hinge (L1, L2) Loss Layer

* Layer type: `HingeLoss`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1HingeLossLayer.html)
* Header: [`./include/caffe/layers/hinge_loss_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/hinge_loss_layer.hpp)
* CPU implementation: [`./src/caffe/layers/hinge_loss_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/hinge_loss_layer.cpp)

## Parameters

* Parameters (`HingeLossParameter hinge_loss_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/HingeLossParameter.txt %}
{% endhighlight %}
---
title: Log Layer
---

# Log Layer

* Layer type: `Log`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1LogLayer.html)
* Header: [`./include/caffe/layers/log_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/log_layer.hpp)
* CPU implementation: [`./src/caffe/layers/log_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/log_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/log_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/log_layer.cu)

## Parameters

* Parameters (`Parameter log_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/LogParameter.txt %}
{% endhighlight %}
---
title: Reshape Layer
---

# Reshape Layer
* Layer type: `Reshape`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ReshapeLayer.html)
* Header: [`./include/caffe/layers/reshape_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/reshape_layer.hpp)
* Implementation: [`./src/caffe/layers/reshape_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/reshape_layer.cpp)

* Input
    - a single blob with arbitrary dimensions
* Output
    - the same blob, with modified dimensions, as specified by `reshape_param`

* Sample

        layer {
          name: "reshape"
          type: "Reshape"
          bottom: "input"
          top: "output"
          reshape_param {
            shape {
              dim: 0  # copy the dimension from below
              dim: 2
              dim: 3
              dim: -1 # infer it from the other dimensions
            }
          }
        }

The `Reshape` layer can be used to change the dimensions of its input, without changing its data. Just like the `Flatten` layer, only the dimensions are changed; no data is copied in the process.

Output dimensions are specified by the `ReshapeParam` proto. Positive numbers are used directly, setting the corresponding dimension of the output blob. In addition, two special values are accepted for any of the target dimension values:

* **0** means "copy the respective dimension of the bottom layer". That is, if the bottom has 2 as its 1st dimension, the top will have 2 as its 1st dimension as well, given `dim: 0` as the 1st target dimension.
* **-1** stands for "infer this from the other dimensions". This behavior is similar to that of -1 in *numpy*'s or `[]` for *MATLAB*'s reshape: this dimension is calculated to keep the overall element count the same as in the bottom layer. At most one -1 can be used in a reshape operation.

As another example, specifying `reshape_param { shape { dim: 0 dim: -1 } }` makes the layer behave in exactly the same way as the `Flatten` layer.
 
## Parameters

* Parameters (`ReshapeParameter reshape_param`)
    - Optional: (also see detailed description below)
        - `shape`
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/ReshapeParameter.txt %}
{% endhighlight %}
---
title: BNLL Layer
---

# BNLL Layer

* Layer type: `BNLL`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1BNLLLayer.html)
* Header: [`./include/caffe/layers/bnll_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/bnll_layer.hpp)
* CPU implementation: [`./src/caffe/layers/bnll_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/bnll_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/bnll_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/bnll_layer.cu)

The `BNLL` (binomial normal log likelihood) layer computes the output as log(1 + exp(x)) for each input element x.

## Parameters
No parameters.

## Sample

      layer {
        name: "layer"
        bottom: "in"
        top: "out"
        type: BNLL
      }
---
title: Exponential Layer
---

# Exponential Layer

* Layer type: `Exp`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ExpLayer.html)
* Header: [`./include/caffe/layers/exp_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/exp_layer.hpp)
* CPU implementation: [`./src/caffe/layers/exp_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/exp_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/exp_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/exp_layer.cu)

## Parameters

* Parameters (`Parameter exp_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/ExpParameter.txt %}
{% endhighlight %}

## See also

* [Power layer](power.html)
---
title: Concat Layer
---

# Concat Layer

* Layer type: `Concat`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ConcatLayer.html)
* Header: [`./include/caffe/layers/concat_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/concat_layer.hpp)
* CPU implementation: [`./src/caffe/layers/concat_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/concat_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/concat_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/concat_layer.cu)
* Input
    - `n_i * c_i * h * w` for each input blob i from 1 to K.
* Output
    - if `axis = 0`: `(n_1 + n_2 + ... + n_K) * c_1 * h * w`, and all input `c_i` should be the same.
    - if `axis = 1`: `n_1 * (c_1 + c_2 + ... + c_K) * h * w`, and all input `n_i` should be the same.
* Sample

      layer {
        name: "concat"
        bottom: "in1"
        bottom: "in2"
        top: "out"
        type: "Concat"
        concat_param {
          axis: 1
        }
      }

The `Concat` layer is a utility layer that concatenates its multiple input blobs to one single output blob.

## Parameters
* Parameters (`ConcatParameter concat_param`)
    - Optional
        - `axis` [default 1]: 0 for concatenation along num and 1 for channels.
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/ConcatParameter.txt %}
{% endhighlight %}
---
title: Multinomial Logistic Loss Layer
---

# Multinomial Logistic Loss Layer

* Layer type: `MultinomialLogisticLoss`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1MultinomialLogisticLossLayer.html)
* Header: [`./include/caffe/layers/multinomial_logistic_loss_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/multinomial_logistic_loss_layer.hpp)
* CPU implementation: [`./src/caffe/layers/multinomial_logistic_loss_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/multinomial_logistic_loss_layer.cpp)

## Parameters

* Parameters (`LossParameter loss_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/LossParameter.txt %}
{% endhighlight %}
---
title: Convolution Layer
---

# Convolution Layer

* Layer type: `Convolution`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1ConvolutionLayer.html)
* Header: [`./include/caffe/layers/conv_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/conv_layer.hpp)
* CPU implementation: [`./src/caffe/layers/conv_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/conv_layer.cpp)
* CUDA GPU implementation: [`./src/caffe/layers/conv_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/conv_layer.cu)
* Input
    - `n * c_i * h_i * w_i`
* Output
    - `n * c_o * h_o * w_o`, where `h_o = (h_i + 2 * pad_h - kernel_h) / stride_h + 1` and `w_o` likewise.

The `Convolution` layer convolves the input image with a set of learnable filters, each producing one feature map in the output image.

## Sample

Sample (as seen in [`./models/bvlc_reference_caffenet/train_val.prototxt`](https://github.com/BVLC/caffe/blob/master/models/bvlc_reference_caffenet/train_val.prototxt)):

      layer {
        name: "conv1"
        type: "Convolution"
        bottom: "data"
        top: "conv1"
        # learning rate and decay multipliers for the filters
        param { lr_mult: 1 decay_mult: 1 }
        # learning rate and decay multipliers for the biases
        param { lr_mult: 2 decay_mult: 0 }
        convolution_param {
          num_output: 96     # learn 96 filters
          kernel_size: 11    # each filter is 11x11
          stride: 4          # step 4 pixels between each filter application
          weight_filler {
            type: "gaussian" # initialize the filters from a Gaussian
            std: 0.01        # distribution with stdev 0.01 (default mean: 0)
          }
          bias_filler {
            type: "constant" # initialize the biases to zero (0)
            value: 0
          }
        }
      }

## Parameters
* Parameters (`ConvolutionParameter convolution_param`)
    - Required
        - `num_output` (`c_o`): the number of filters
        - `kernel_size` (or `kernel_h` and `kernel_w`): specifies height and width of each filter
    - Strongly Recommended
        - `weight_filler` [default `type: 'constant' value: 0`]
    - Optional
        - `bias_term` [default `true`]: specifies whether to learn and apply a set of additive biases to the filter outputs
        - `pad` (or `pad_h` and `pad_w`) [default 0]: specifies the number of pixels to (implicitly) add to each side of the input
        - `stride` (or `stride_h` and `stride_w`) [default 1]: specifies the intervals at which to apply the filters to the input
        - `group` (g) [default 1]: If g > 1, we restrict the connectivity of each filter to a subset of the input. Specifically, the input and output channels are separated into g groups, and the $$i$$th output group channels will be only connected to the $$i$$th input group channels.
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/ConvolutionParameter.txt %}
{% endhighlight %}
---
title: LSTM Layer
---

# LSTM Layer

* Layer type: `LSTM`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1LSTMLayer.html)
* Header: [`./include/caffe/layers/lstm_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/lstm_layer.hpp)
* CPU implementation: [`./src/caffe/layers/lstm_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/lstm_layer.cpp)
* CPU implementation (helper): [`./src/caffe/layers/lstm_unit_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/lstm_unit_layer.cpp)
* CUDA GPU implementation (helper): [`./src/caffe/layers/lstm_unit_layer.cu`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/lstm_unit_layer.cu)

## Parameters

* Parameters (`Parameter recurrent_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto):

{% highlight Protobuf %}
{% include proto/RecurrentParameter.txt %}
{% endhighlight %}
---
title: Accuracy and Top-k
---

# Accuracy and Top-k

`Accuracy` scores the output as the accuracy of output with respect to target -- it is not actually a loss and has no backward step.

* Layer type: `Accuracy`
* [Doxygen Documentation](http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1AccuracyLayer.html)
* Header: [`./include/caffe/layers/accuracy_layer.hpp`](https://github.com/BVLC/caffe/blob/master/include/caffe/layers/accuracy_layer.hpp)
* CPU implementation: [`./src/caffe/layers/accuracy_layer.cpp`](https://github.com/BVLC/caffe/blob/master/src/caffe/layers/accuracy_layer.cpp)

## Parameters
* Parameters (`AccuracyParameter accuracy_param`)
* From [`./src/caffe/proto/caffe.proto`](https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto)):

{% highlight Protobuf %}
{% include proto/AccuracyParameter.txt %}
{% endhighlight %}
Cython>=0.19.2
numpy>=1.7.1
scipy>=0.13.2
scikit-image>=0.9.3
matplotlib>=1.3.1
ipython>=3.0.0
h5py>=2.2.0
leveldb>=0.191
networkx>=1.8.1
nose>=1.3.0
pandas>=0.12.0
python-dateutil>=1.4,<2
protobuf>=2.5.0
python-gflags>=2.0
pyyaml>=3.10
Pillow>=2.3.0
six>=1.1.0if(NOT HAVE_PYTHON)
  message(STATUS "Python interface is disabled or not all required dependencies found. Building without it...")
  return()
endif()

file(GLOB_RECURSE python_srcs ${PROJECT_SOURCE_DIR}/python/*.cpp)

add_library(pycaffe SHARED ${python_srcs})
caffe_default_properties(pycaffe)
set_target_properties(pycaffe PROPERTIES PREFIX "" OUTPUT_NAME "_caffe")
target_include_directories(pycaffe PUBLIC ${PYTHON_INCLUDE_DIRS} ${NUMPY_INCLUDE_DIR})
target_link_libraries(pycaffe PUBLIC ${Caffe_LINK} ${PYTHON_LIBRARIES})

if(UNIX OR APPLE)
    set(__linkname "${PROJECT_SOURCE_DIR}/python/caffe/_caffe.so")
    add_custom_command(TARGET pycaffe POST_BUILD
                       COMMAND ln -sf $<TARGET_LINKER_FILE:pycaffe> "${__linkname}"
                       COMMAND ${CMAKE_COMMAND} -E make_directory ${PROJECT_SOURCE_DIR}/python/caffe/proto
                       COMMAND touch ${PROJECT_SOURCE_DIR}/python/caffe/proto/__init__.py
                       COMMAND cp ${proto_gen_folder}/*.py ${PROJECT_SOURCE_DIR}/python/caffe/proto/
                       COMMENT "Creating symlink ${__linkname} -> ${PROJECT_BINARY_DIR}/lib/_caffe${Caffe_POSTFIX}.so")
endif()

# ---[ Install
# scripts
file(GLOB python_files *.py requirements.txt)
install(FILES ${python_files} DESTINATION python)

# module
install(DIRECTORY caffe
    DESTINATION python
    FILES_MATCHING
    PATTERN "*.py"
    PATTERN "ilsvrc_2012_mean.npy"
    PATTERN "test" EXCLUDE
    )

# _caffe.so
install(TARGETS pycaffe  DESTINATION python/caffe)

add_library(gtest STATIC EXCLUDE_FROM_ALL gtest.h gtest-all.cpp)
caffe_default_properties(gtest)
target_include_directories(gtest PUBLIC ${Caffe_SRC_DIR})
target_compile_definitions(gtest PUBLIC -DGTEST_USE_OWN_TR1_TUPLE)


#add_library(gtest_main gtest_main.cc)
#target_link_libraries(gtest_main gtest)
# generate protobuf sources
file(GLOB proto_files proto/*.proto)
caffe_protobuf_generate_cpp_py(${proto_gen_folder} proto_srcs proto_hdrs proto_python ${proto_files})

# include python files either to force generation
add_library(caffeproto STATIC ${proto_hdrs} ${proto_srcs} ${proto_python})
caffe_default_properties(caffeproto)
target_link_libraries(caffeproto PUBLIC ${PROTOBUF_LIBRARIES})
target_include_directories(caffeproto PUBLIC ${PROTOBUF_INCLUDE_DIR})

list(INSERT Caffe_LINKER_LIBS 0 PUBLIC caffeproto) # note, crucial to prepend!

# --[ Caffe library

# creates 'test_srcs', 'srcs', 'test_cuda', 'cuda' lists
caffe_pickup_caffe_sources(${PROJECT_SOURCE_DIR})

if(HAVE_CUDA)
  caffe_cuda_compile(cuda_objs ${cuda})
  list(APPEND srcs ${cuda_objs} ${cuda})
endif()

add_library(caffe ${srcs})
caffe_default_properties(caffe)
target_link_libraries(caffe ${Caffe_LINKER_LIBS})
target_include_directories(caffe ${Caffe_INCLUDE_DIRS}
                                 PUBLIC
                                 $<BUILD_INTERFACE:${Caffe_INCLUDE_DIR}>
                                 $<INSTALL_INTERFACE:include>)
target_compile_definitions(caffe ${Caffe_DEFINITIONS})
if(Caffe_COMPILE_OPTIONS)
  target_compile_options(caffe ${Caffe_COMPILE_OPTIONS})
endif()
set_target_properties(caffe PROPERTIES
    VERSION   ${CAFFE_TARGET_VERSION}
    SOVERSION ${CAFFE_TARGET_SOVERSION}
    )

# ---[ Tests
 add_subdirectory(test)

# ---[ Install
install(DIRECTORY ${Caffe_INCLUDE_DIR}/caffe DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(FILES ${proto_hdrs} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/caffe/proto)
install(TARGETS caffe caffeproto EXPORT CaffeTargets DESTINATION ${CMAKE_INSTALL_LIBDIR})

file(WRITE ${PROJECT_BINARY_DIR}/__init__.py)
list(APPEND proto_python ${PROJECT_BINARY_DIR}/__init__.py)
install(PROGRAMS ${proto_python} DESTINATION python/caffe/proto)

# The option allows to include in build only selected test files and exclude all others
# Usage example:
#  cmake -DBUILD_only_tests="common,net,blob,im2col_kernel"
set(BUILD_only_tests "" CACHE STRING "Blank or comma-separated list of test files to build without 'test_' prefix and extension")
caffe_leave_only_selected_tests(test_srcs ${BUILD_only_tests})
caffe_leave_only_selected_tests(test_cuda ${BUILD_only_tests})

# For 'make runtest' target we don't need to embed test data paths to
# source files, because test target is executed in source directory
# That's why the lines below are commented. TODO: remove them

# definition needed to include CMake generated files
#add_definitions(-DCMAKE_BUILD)

# generates test_data/sample_data_list.txt.gen.cmake
#caffe_configure_testdatafile(test_data/sample_data_list.txt)

set(the_target test.testbin)
set(test_args --gtest_shuffle)

if(HAVE_CUDA)
  caffe_cuda_compile(test_cuda_objs ${test_cuda})
  list(APPEND test_srcs ${test_cuda_objs} ${test_cuda})
else()
  list(APPEND test_args --gtest_filter="-*GPU*")
endif()

# ---[ Adding test target
add_executable(${the_target} EXCLUDE_FROM_ALL ${test_srcs})
target_link_libraries(${the_target} gtest ${Caffe_LINK})
caffe_default_properties(${the_target})
caffe_set_runtime_directory(${the_target} "${PROJECT_BINARY_DIR}/test")

# ---[ Adding runtest
add_custom_target(runtest COMMAND ${the_target} ${test_args}
                          WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})
src/caffe/test/test_data/sample_data.h5
src/caffe/test/test_data/sample_data_2_gzip.h5
src/caffe/test/test_data/solver_data.h5
file(GLOB_RECURSE examples_srcs "${PROJECT_SOURCE_DIR}/examples/*.cpp")

foreach(source_file ${examples_srcs})
  # get file name
  get_filename_component(name ${source_file} NAME_WE)
    
  # get folder name
  get_filename_component(path ${source_file} PATH)
  get_filename_component(folder ${path} NAME_WE)
    
  add_executable(${name} ${source_file})
  target_link_libraries(${name} ${Caffe_LINK})
  caffe_default_properties(${name})

  # set back RUNTIME_OUTPUT_DIRECTORY
  set_target_properties(${name} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/examples/${folder}")

  caffe_set_solution_folder(${name} examples)

  # install
  install(TARGETS ${name} DESTINATION ${CMAKE_INSTALL_BINDIR})


  if(UNIX OR APPLE)
    # Funny command to make tutorials work
    # TODO: remove in future as soon as naming is standardized everywhere
    set(__outname ${PROJECT_BINARY_DIR}/examples/${folder}/${name}${Caffe_POSTFIX})
    add_custom_command(TARGET ${name} POST_BUILD
                       COMMAND ln -sf "${__outname}" "${__outname}.bin")
  endif()
endforeach()
---
title: CaffeNet C++ Classification example
description: A simple example performing image classification using the low-level C++ API.
category: example
include_in_docs: true
priority: 10
---

# Classifying ImageNet: using the C++ API

Caffe, at its core, is written in C++. It is possible to use the C++
API of Caffe to implement an image classification application similar
to the Python code presented in one of the Notebook examples. To look
at a more general-purpose example of the Caffe C++ API, you should
study the source code of the command line tool `caffe` in `tools/caffe.cpp`.

## Presentation

A simple C++ code is proposed in
`examples/cpp_classification/classification.cpp`. For the sake of
simplicity, this example does not support oversampling of a single
sample nor batching of multiple independent samples. This example is
not trying to reach the maximum possible classification throughput on
a system, but special care was given to avoid unnecessary
pessimization while keeping the code readable.

## Compiling

The C++ example is built automatically when compiling Caffe. To
compile Caffe you should follow the documented instructions. The
classification example will be built as `examples/classification.bin`
in your build directory.

## Usage

To use the pre-trained CaffeNet model with the classification example,
you need to download it from the "Model Zoo" using the following
script:
```
./scripts/download_model_binary.py models/bvlc_reference_caffenet
```
The ImageNet labels file (also called the *synset file*) is also
required in order to map a prediction to the name of the class:
```
./data/ilsvrc12/get_ilsvrc_aux.sh
```
Using the files that were downloaded, we can classify the provided cat
image (`examples/images/cat.jpg`) using this command:
```
./build/examples/cpp_classification/classification.bin \
  models/bvlc_reference_caffenet/deploy.prototxt \
  models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel \
  data/ilsvrc12/imagenet_mean.binaryproto \
  data/ilsvrc12/synset_words.txt \
  examples/images/cat.jpg
```
The output should look like this:
```
---------- Prediction for examples/images/cat.jpg ----------
0.3134 - "n02123045 tabby, tabby cat"
0.2380 - "n02123159 tiger cat"
0.1235 - "n02124075 Egyptian cat"
0.1003 - "n02119022 red fox, Vulpes vulpes"
0.0715 - "n02127052 lynx, catamount"
```

## Improving Performance

To further improve performance, you will need to leverage the GPU
more, here are some guidelines:

* Move the data on the GPU early and perform all preprocessing
operations there.
* If you have many images to classify simultaneously, you should use
batching (independent images are classified in a single forward pass).
* Use multiple classification threads to ensure the GPU is always fully
utilized and not waiting for an I/O blocked CPU thread.
---
title: CIFAR-10 tutorial
category: example
description: Train and test Caffe on CIFAR-10 data.
include_in_docs: true
priority: 5
---

Alex's CIFAR-10 tutorial, Caffe style
=====================================

Alex Krizhevsky's [cuda-convnet](https://code.google.com/p/cuda-convnet/) details the model definitions, parameters, and training procedure for good performance on CIFAR-10. This example reproduces his results in Caffe.

We will assume that you have Caffe successfully compiled. If not, please refer to the [Installation page](/installation.html). In this tutorial, we will assume that your caffe installation is located at `CAFFE_ROOT`.

We thank @chyojn for the pull request that defined the model schemas and solver configurations.

*This example is a work-in-progress. It would be nice to further explain details of the network and training choices and benchmark the full training.*

Prepare the Dataset
-------------------

You will first need to download and convert the data format from the [CIFAR-10 website](http://www.cs.toronto.edu/~kriz/cifar.html). To do this, simply run the following commands:

    cd $CAFFE_ROOT
    ./data/cifar10/get_cifar10.sh
    ./examples/cifar10/create_cifar10.sh

If it complains that `wget` or `gunzip` are not installed, you need to install them respectively. After running the script there should be the dataset, `./cifar10-leveldb`, and the data set image mean `./mean.binaryproto`.

The Model
---------

The CIFAR-10 model is a CNN that composes layers of convolution, pooling, rectified linear unit (ReLU) nonlinearities, and local contrast normalization with a linear classifier on top of it all. We have defined the model in the `CAFFE_ROOT/examples/cifar10` directory's `cifar10_quick_train_test.prototxt`.

Training and Testing the "Quick" Model
--------------------------------------

Training the model is simple after you have written the network definition protobuf and solver protobuf files (refer to [MNIST Tutorial](../examples/mnist.html)). Simply run `train_quick.sh`, or the following command directly:

    cd $CAFFE_ROOT
    ./examples/cifar10/train_quick.sh

`train_quick.sh` is a simple script, so have a look inside. The main tool for training is `caffe` with the `train` action, and the solver protobuf text file as its argument.

When you run the code, you will see a lot of messages flying by like this:

    I0317 21:52:48.945710 2008298256 net.cpp:74] Creating Layer conv1
    I0317 21:52:48.945716 2008298256 net.cpp:84] conv1 <- data
    I0317 21:52:48.945725 2008298256 net.cpp:110] conv1 -> conv1
    I0317 21:52:49.298691 2008298256 net.cpp:125] Top shape: 100 32 32 32 (3276800)
    I0317 21:52:49.298719 2008298256 net.cpp:151] conv1 needs backward computation.

These messages tell you the details about each layer, its connections and its output shape, which may be helpful in debugging. After the initialization, the training will start:

    I0317 21:52:49.309370 2008298256 net.cpp:166] Network initialization done.
    I0317 21:52:49.309376 2008298256 net.cpp:167] Memory required for Data 23790808
    I0317 21:52:49.309422 2008298256 solver.cpp:36] Solver scaffolding done.
    I0317 21:52:49.309447 2008298256 solver.cpp:47] Solving CIFAR10_quick_train

Based on the solver setting, we will print the training loss function every 100 iterations, and test the network every 500 iterations. You will see messages like this:

    I0317 21:53:12.179772 2008298256 solver.cpp:208] Iteration 100, lr = 0.001
    I0317 21:53:12.185698 2008298256 solver.cpp:65] Iteration 100, loss = 1.73643
    ...
    I0317 21:54:41.150030 2008298256 solver.cpp:87] Iteration 500, Testing net
    I0317 21:54:47.129461 2008298256 solver.cpp:114] Test score #0: 0.5504
    I0317 21:54:47.129500 2008298256 solver.cpp:114] Test score #1: 1.27805

For each training iteration, `lr` is the learning rate of that iteration, and `loss` is the training function. For the output of the testing phase, **score 0 is the accuracy**, and **score 1 is the testing loss function**.

And after making yourself a cup of coffee, you are done!

    I0317 22:12:19.666914 2008298256 solver.cpp:87] Iteration 5000, Testing net
    I0317 22:12:25.580330 2008298256 solver.cpp:114] Test score #0: 0.7533
    I0317 22:12:25.580379 2008298256 solver.cpp:114] Test score #1: 0.739837
    I0317 22:12:25.587262 2008298256 solver.cpp:130] Snapshotting to cifar10_quick_iter_5000
    I0317 22:12:25.590215 2008298256 solver.cpp:137] Snapshotting solver state to cifar10_quick_iter_5000.solverstate
    I0317 22:12:25.592813 2008298256 solver.cpp:81] Optimization Done.

Our model achieved ~75% test accuracy. The model parameters are stored in binary protobuf format in

    cifar10_quick_iter_5000

which is ready-to-deploy in CPU or GPU mode! Refer to the `CAFFE_ROOT/examples/cifar10/cifar10_quick.prototxt` for the deployment model definition that can be called on new data.

Why train on a GPU?
-------------------

CIFAR-10, while still small, has enough data to make GPU training attractive.

To compare CPU vs. GPU training speed, simply change one line in all the `cifar*solver.prototxt`:

    # solver mode: CPU or GPU
    solver_mode: CPU

and you will be using CPU for training.
---
title: Siamese Network Tutorial
description: Train and test a siamese network on MNIST data.
category: example
include_in_docs: true
layout: default
priority: 100
---

# Siamese Network Training with Caffe
This example shows how you can use weight sharing and a contrastive loss
function to learn a model using a siamese network in Caffe.

We will assume that you have caffe successfully compiled. If not, please refer
to the [Installation page](../../installation.html). This example builds on the
[MNIST tutorial](mnist.html) so it would be a good idea to read that before
continuing.

*The guide specifies all paths and assumes all commands are executed from the
root caffe directory*

## Prepare Datasets

You will first need to download and convert the data from the MNIST
website. To do this, simply run the following commands:

    ./data/mnist/get_mnist.sh
    ./examples/siamese/create_mnist_siamese.sh

After running the script there should be two datasets,
`./examples/siamese/mnist_siamese_train_leveldb`, and
`./examples/siamese/mnist_siamese_test_leveldb`.

## The Model
First, we will define the model that we want to train using the siamese network.
We will use the convolutional net defined in
`./examples/siamese/mnist_siamese.prototxt`. This model is almost
exactly the same as the [LeNet model](mnist.html), the only difference is that
we have replaced the top layers that produced probabilities over the 10 digit
classes with a linear "feature" layer that produces a 2 dimensional vector.

    layer {
      name: "feat"
      type: "InnerProduct"
      bottom: "ip2"
      top: "feat"
      param {
        name: "feat_w"
        lr_mult: 1
      }
      param {
        name: "feat_b"
        lr_mult: 2
      }
      inner_product_param {
        num_output: 2
      }
    }

## Define the Siamese Network

In this section we will define the siamese network used for training. The
resulting network is defined in
`./examples/siamese/mnist_siamese_train_test.prototxt`.

### Reading in the Pair Data

We start with a data layer that reads from the LevelDB database we created
earlier. Each entry in this database contains the image data for a pair of
images (`pair_data`) and a binary label saying if they belong to the same class
or different classes (`sim`).

    layer {
      name: "pair_data"
      type: "Data"
      top: "pair_data"
      top: "sim"
      include { phase: TRAIN }
      transform_param {
        scale: 0.00390625
      }
      data_param {
        source: "examples/siamese/mnist_siamese_train_leveldb"
        batch_size: 64
      }
    }

In order to pack a pair of images into the same blob in the database we pack one
image per channel. We want to be able to work with these two images separately,
so we add a slice layer after the data layer. This takes the `pair_data` and
slices it along the channel dimension so that we have a single image in `data`
and its paired image in `data_p.`

    layer {
      name: "slice_pair"
      type: "Slice"
      bottom: "pair_data"
      top: "data"
      top: "data_p"
      slice_param {
        slice_dim: 1
        slice_point: 1
      }
    }

### Building the First Side of the Siamese Net

Now we can specify the first side of the siamese net. This side operates on
`data` and produces `feat`. Starting from the net in
`./examples/siamese/mnist_siamese.prototxt` we add default weight fillers. Then
we name the parameters of the convolutional and inner product layers. Naming the
parameters allows Caffe to share the parameters between layers on both sides of
the siamese net. In the definition this looks like:

    ...
    param { name: "conv1_w" ...  }
    param { name: "conv1_b" ...  }
    ...
    param { name: "conv2_w" ...  }
    param { name: "conv2_b" ...  }
    ...
    param { name: "ip1_w" ...  }
    param { name: "ip1_b" ...  }
    ...
    param { name: "ip2_w" ...  }
    param { name: "ip2_b" ...  }
    ...

### Building the Second Side of the Siamese Net

Now we need to create the second path that operates on `data_p` and produces
`feat_p`. This path is exactly the same as the first. So we can just copy and
paste it. Then we change the name of each layer, input, and output by appending
`_p` to differentiate the "paired" layers from the originals.

### Adding the Contrastive Loss Function

To train the network we will optimize a contrastive loss function proposed in:
Raia Hadsell, Sumit Chopra, and Yann LeCun "Dimensionality Reduction by Learning
an Invariant Mapping". This loss function encourages matching pairs to be close
together in feature space while pushing non-matching pairs apart. This cost
function is implemented with the `CONTRASTIVE_LOSS` layer:

    layer {
        name: "loss"
        type: "ContrastiveLoss"
        contrastive_loss_param {
            margin: 1.0
        }
        bottom: "feat"
        bottom: "feat_p"
        bottom: "sim"
        top: "loss"
    }

## Define the Solver

Nothing special needs to be done to the solver besides pointing it at the
correct model file. The solver is defined in
`./examples/siamese/mnist_siamese_solver.prototxt`.

## Training and Testing the Model

Training the model is simple after you have written the network definition
protobuf and solver protobuf files. Simply run
`./examples/siamese/train_mnist_siamese.sh`:

    ./examples/siamese/train_mnist_siamese.sh

# Plotting the results

First, we can draw the model and siamese networks by running the following
commands that draw the DAGs defined in the .prototxt files:

    ./python/draw_net.py \
        ./examples/siamese/mnist_siamese.prototxt \
        ./examples/siamese/mnist_siamese.png

    ./python/draw_net.py \
        ./examples/siamese/mnist_siamese_train_test.prototxt \
        ./examples/siamese/mnist_siamese_train_test.png

Second, we can load the learned model and plot the features using the iPython
notebook:

    ipython notebook ./examples/siamese/mnist_siamese.ipynb

Detailed
Pastel
Melancholy
Noir
HDR
Vintage
Long Exposure
Horror
Sunny
Bright
Hazy
Bokeh
Serene
Texture
Ethereal
Macro
Depth of Field
Geometric Composition
Minimal
Romantic
---
title: Fine-tuning for style recognition
description: Fine-tune the ImageNet-trained CaffeNet on the "Flickr Style" dataset.
category: example
include_in_docs: true
priority: 5
---

# Fine-tuning CaffeNet for Style Recognition on "Flickr Style" Data

Fine-tuning takes an already learned model, adapts the architecture, and resumes training from the already learned model weights.
Let's fine-tune the BAIR-distributed CaffeNet model on a different dataset, [Flickr Style](http://sergeykarayev.com/files/1311.3715v3.pdf), to predict image style instead of object category.

## Explanation

The Flickr-sourced images of the Style dataset are visually very similar to the ImageNet dataset, on which the `bvlc_reference_caffenet` was trained.
Since that model works well for object category classification, we'd like to use this architecture for our style classifier.
We also only have 80,000 images to train on, so we'd like to start with the parameters learned on the 1,000,000 ImageNet images, and fine-tune as needed.
If we provide the `weights` argument to the `caffe train` command, the pretrained weights will be loaded into our model, matching layers by name.

Because we are predicting 20 classes instead of a 1,000, we do need to change the last layer in the model.
Therefore, we change the name of the last layer from `fc8` to `fc8_flickr` in our prototxt.
Since there is no layer named that in the `bvlc_reference_caffenet`, that layer will begin training with random weights.

We will also decrease the overall learning rate `base_lr` in the solver prototxt, but boost the `lr_mult` on the newly introduced layer.
The idea is to have the rest of the model change very slowly with new data, but let the new layer learn fast.
Additionally, we set `stepsize` in the solver to a lower value than if we were training from scratch, since we're virtually far along in training and therefore want the learning rate to go down faster.
Note that we could also entirely prevent fine-tuning of all layers other than `fc8_flickr` by setting their `lr_mult` to 0.

## Procedure

All steps are to be done from the caffe root directory.

The dataset is distributed as a list of URLs with corresponding labels.
Using a script, we will download a small subset of the data and split it into train and val sets.

    caffe % ./examples/finetune_flickr_style/assemble_data.py -h
    usage: assemble_data.py [-h] [-s SEED] [-i IMAGES] [-w WORKERS]

    Download a subset of Flickr Style to a directory

    optional arguments:
      -h, --help            show this help message and exit
      -s SEED, --seed SEED  random seed
      -i IMAGES, --images IMAGES
                            number of images to use (-1 for all)
      -w WORKERS, --workers WORKERS
                            num workers used to download images. -x uses (all - x)
                            cores.

    caffe % python examples/finetune_flickr_style/assemble_data.py --workers=-1 --images=2000 --seed 831486
    Downloading 2000 images with 7 workers...
    Writing train/val for 1939 successfully downloaded images.

This script downloads images and writes train/val file lists into `data/flickr_style`.
The prototxts in this example assume this, and also assume the presence of the ImageNet mean file (run `get_ilsvrc_aux.sh` from `data/ilsvrc12` to obtain this if you haven't yet).

We'll also need the ImageNet-trained model, which you can obtain by running `./scripts/download_model_binary.py models/bvlc_reference_caffenet`.

Now we can train! The key to fine-tuning is the `-weights` argument in the
command below, which tells Caffe that we want to load weights from a pre-trained
Caffe model.

(You can fine-tune in CPU mode by leaving out the `-gpu` flag.)

    caffe % ./build/tools/caffe train -solver models/finetune_flickr_style/solver.prototxt -weights models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel -gpu 0

    [...]

    I0828 22:10:04.025378  9718 solver.cpp:46] Solver scaffolding done.
    I0828 22:10:04.025388  9718 caffe.cpp:95] Use GPU with device ID 0
    I0828 22:10:04.192004  9718 caffe.cpp:107] Finetuning from models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel

    [...]

    I0828 22:17:48.338963 11510 solver.cpp:165] Solving FlickrStyleCaffeNet
    I0828 22:17:48.339010 11510 solver.cpp:251] Iteration 0, Testing net (#0)
    I0828 22:18:14.313817 11510 solver.cpp:302]     Test net output #0: accuracy = 0.0308
    I0828 22:18:14.476822 11510 solver.cpp:195] Iteration 0, loss = 3.78589
    I0828 22:18:14.476878 11510 solver.cpp:397] Iteration 0, lr = 0.001
    I0828 22:18:19.700408 11510 solver.cpp:195] Iteration 20, loss = 3.25728
    I0828 22:18:19.700461 11510 solver.cpp:397] Iteration 20, lr = 0.001
    I0828 22:18:24.924685 11510 solver.cpp:195] Iteration 40, loss = 2.18531
    I0828 22:18:24.924741 11510 solver.cpp:397] Iteration 40, lr = 0.001
    I0828 22:18:30.114858 11510 solver.cpp:195] Iteration 60, loss = 2.4915
    I0828 22:18:30.114910 11510 solver.cpp:397] Iteration 60, lr = 0.001
    I0828 22:18:35.328071 11510 solver.cpp:195] Iteration 80, loss = 2.04539
    I0828 22:18:35.328127 11510 solver.cpp:397] Iteration 80, lr = 0.001
    I0828 22:18:40.588317 11510 solver.cpp:195] Iteration 100, loss = 2.1924
    I0828 22:18:40.588373 11510 solver.cpp:397] Iteration 100, lr = 0.001
    I0828 22:18:46.171576 11510 solver.cpp:195] Iteration 120, loss = 2.25107
    I0828 22:18:46.171669 11510 solver.cpp:397] Iteration 120, lr = 0.001
    I0828 22:18:51.757809 11510 solver.cpp:195] Iteration 140, loss = 1.355
    I0828 22:18:51.757863 11510 solver.cpp:397] Iteration 140, lr = 0.001
    I0828 22:18:57.345080 11510 solver.cpp:195] Iteration 160, loss = 1.40815
    I0828 22:18:57.345135 11510 solver.cpp:397] Iteration 160, lr = 0.001
    I0828 22:19:02.928794 11510 solver.cpp:195] Iteration 180, loss = 1.6558
    I0828 22:19:02.928850 11510 solver.cpp:397] Iteration 180, lr = 0.001
    I0828 22:19:08.514497 11510 solver.cpp:195] Iteration 200, loss = 0.88126
    I0828 22:19:08.514552 11510 solver.cpp:397] Iteration 200, lr = 0.001

    [...]

    I0828 22:22:40.789010 11510 solver.cpp:195] Iteration 960, loss = 0.112586
    I0828 22:22:40.789175 11510 solver.cpp:397] Iteration 960, lr = 0.001
    I0828 22:22:46.376626 11510 solver.cpp:195] Iteration 980, loss = 0.0959077
    I0828 22:22:46.376682 11510 solver.cpp:397] Iteration 980, lr = 0.001
    I0828 22:22:51.687258 11510 solver.cpp:251] Iteration 1000, Testing net (#0)
    I0828 22:23:17.438894 11510 solver.cpp:302]     Test net output #0: accuracy = 0.2356

Note how rapidly the loss went down. Although the 23.5% accuracy is only modest, it was achieved in only 1000, and evidence that the model is starting to learn quickly and well.
Once the model is fully fine-tuned on the whole training set over 100,000 iterations the final validation accuracy is 39.16%.
This takes ~7 hours in Caffe on a K40 GPU.

For comparison, here is how the loss goes down when we do not start with a pre-trained model:

    I0828 22:24:18.624004 12919 solver.cpp:165] Solving FlickrStyleCaffeNet
    I0828 22:24:18.624099 12919 solver.cpp:251] Iteration 0, Testing net (#0)
    I0828 22:24:44.520992 12919 solver.cpp:302]     Test net output #0: accuracy = 0.0366
    I0828 22:24:44.676905 12919 solver.cpp:195] Iteration 0, loss = 3.47942
    I0828 22:24:44.677120 12919 solver.cpp:397] Iteration 0, lr = 0.001
    I0828 22:24:50.152454 12919 solver.cpp:195] Iteration 20, loss = 2.99694
    I0828 22:24:50.152509 12919 solver.cpp:397] Iteration 20, lr = 0.001
    I0828 22:24:55.736256 12919 solver.cpp:195] Iteration 40, loss = 3.0498
    I0828 22:24:55.736311 12919 solver.cpp:397] Iteration 40, lr = 0.001
    I0828 22:25:01.316514 12919 solver.cpp:195] Iteration 60, loss = 2.99549
    I0828 22:25:01.316567 12919 solver.cpp:397] Iteration 60, lr = 0.001
    I0828 22:25:06.899554 12919 solver.cpp:195] Iteration 80, loss = 3.00573
    I0828 22:25:06.899610 12919 solver.cpp:397] Iteration 80, lr = 0.001
    I0828 22:25:12.484624 12919 solver.cpp:195] Iteration 100, loss = 2.99094
    I0828 22:25:12.484678 12919 solver.cpp:397] Iteration 100, lr = 0.001
    I0828 22:25:18.069056 12919 solver.cpp:195] Iteration 120, loss = 3.01616
    I0828 22:25:18.069149 12919 solver.cpp:397] Iteration 120, lr = 0.001
    I0828 22:25:23.650928 12919 solver.cpp:195] Iteration 140, loss = 2.98786
    I0828 22:25:23.650984 12919 solver.cpp:397] Iteration 140, lr = 0.001
    I0828 22:25:29.235535 12919 solver.cpp:195] Iteration 160, loss = 3.00724
    I0828 22:25:29.235589 12919 solver.cpp:397] Iteration 160, lr = 0.001
    I0828 22:25:34.816898 12919 solver.cpp:195] Iteration 180, loss = 3.00099
    I0828 22:25:34.816953 12919 solver.cpp:397] Iteration 180, lr = 0.001
    I0828 22:25:40.396656 12919 solver.cpp:195] Iteration 200, loss = 2.99848
    I0828 22:25:40.396711 12919 solver.cpp:397] Iteration 200, lr = 0.001

    [...]

    I0828 22:29:12.539094 12919 solver.cpp:195] Iteration 960, loss = 2.99203
    I0828 22:29:12.539258 12919 solver.cpp:397] Iteration 960, lr = 0.001
    I0828 22:29:18.123092 12919 solver.cpp:195] Iteration 980, loss = 2.99345
    I0828 22:29:18.123147 12919 solver.cpp:397] Iteration 980, lr = 0.001
    I0828 22:29:23.432059 12919 solver.cpp:251] Iteration 1000, Testing net (#0)
    I0828 22:29:49.409044 12919 solver.cpp:302]     Test net output #0: accuracy = 0.0572

This model is only beginning to learn.

Fine-tuning can be feasible when training from scratch would not be for lack of time or data.
Even in CPU mode each pass through the training set takes ~100 s. GPU fine-tuning is of course faster still and can learn a useful model in minutes or hours instead of days or weeks.
Furthermore, note that the model has only trained on < 2,000 instances. Transfer learning a new task like style recognition from the ImageNet pretraining can require much less data than training from scratch.

Now try fine-tuning to your own tasks and data!

## Trained model

We provide a model trained on all 80K images, with final accuracy of 39%.
Simply do `./scripts/download_model_binary.py models/finetune_flickr_style` to obtain it.

## License

The Flickr Style dataset as distributed here contains only URLs to images.
Some of the images may have copyright.
Training a category-recognition model for research/non-commercial use may constitute fair use of this data, but the result should not be used for commercial purposes.
---
title: Feature extraction with Caffe C++ code.
description: Extract CaffeNet / AlexNet features using the Caffe utility.
category: example
include_in_docs: true
priority: 10
---

Extracting Features
===================

In this tutorial, we will extract features using a pre-trained model with the included C++ utility.
Note that we recommend using the Python interface for this task, as for example in the [filter visualization example](http://nbviewer.ipython.org/github/BVLC/caffe/blob/master/examples/00-classification.ipynb).

Follow instructions for [installing Caffe](../../installation.html) and run `scripts/download_model_binary.py models/bvlc_reference_caffenet` from caffe root directory.
If you need detailed information about the tools below, please consult their source code, in which additional documentation is usually provided.

Select data to run on
---------------------

We'll make a temporary folder to store things into.

    mkdir examples/_temp

Generate a list of the files to process.
We're going to use the images that ship with caffe.

    find `pwd`/examples/images -type f -exec echo {} \; > examples/_temp/temp.txt

The `ImageDataLayer` we'll use expects labels after each filenames, so let's add a 0 to the end of each line

    sed "s/$/ 0/" examples/_temp/temp.txt > examples/_temp/file_list.txt

Define the Feature Extraction Network Architecture
--------------------------------------------------

In practice, subtracting the mean image from a dataset significantly improves classification accuracies.
Download the mean image of the ILSVRC dataset.

    ./data/ilsvrc12/get_ilsvrc_aux.sh

We will use `data/ilsvrc212/imagenet_mean.binaryproto` in the network definition prototxt.

Let's copy and modify the network definition.
We'll be using the `ImageDataLayer`, which will load and resize images for us.

    cp examples/feature_extraction/imagenet_val.prototxt examples/_temp

Extract Features
----------------

Now everything necessary is in place.

    ./build/tools/extract_features.bin models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel examples/_temp/imagenet_val.prototxt fc7 examples/_temp/features 10 leveldb

The name of feature blob that you extract is `fc7`, which represents the highest level feature of the reference model.
We can use any other layer, as well, such as `conv5` or `pool3`.

The last parameter above is the number of data mini-batches.

The features are stored to LevelDB `examples/_temp/features`, ready for access by some other code.

If you meet with the error "Check failed: status.ok() Failed to open leveldb examples/_temp/features", it is because the directory examples/_temp/features has been created the last time you run the command. Remove it and run again.

    rm -rf examples/_temp/features/

If you'd like to use the Python wrapper for extracting features, check out the [filter visualization notebook](http://nbviewer.ipython.org/github/BVLC/caffe/blob/master/examples/00-classification.ipynb).

Clean Up
--------

Let's remove the temporary directory now.

    rm -r examples/_temp
---
title: ImageNet tutorial
description: Train and test "CaffeNet" on ImageNet data.
category: example
include_in_docs: true
priority: 1
---

Brewing ImageNet
================

This guide is meant to get you ready to train your own model on your own data.
If you just want an ImageNet-trained network, then note that since training takes a lot of energy and we hate global warming, we provide the CaffeNet model trained as described below in the [model zoo](/model_zoo.html).

Data Preparation
----------------

*The guide specifies all paths and assumes all commands are executed from the root caffe directory.*

*By "ImageNet" we here mean the ILSVRC12 challenge, but you can easily train on the whole of ImageNet as well, just with more disk space, and a little longer training time.*

We assume that you already have downloaded the ImageNet training data and validation data, and they are stored on your disk like:

    /path/to/imagenet/train/n01440764/n01440764_10026.JPEG
    /path/to/imagenet/val/ILSVRC2012_val_00000001.JPEG

You will first need to prepare some auxiliary data for training. This data can be downloaded by:

    ./data/ilsvrc12/get_ilsvrc_aux.sh

The training and validation input are described in `train.txt` and `val.txt` as text listing all the files and their labels. Note that we use a different indexing for labels than the ILSVRC devkit: we sort the synset names in their ASCII order, and then label them from 0 to 999. See `synset_words.txt` for the synset/name mapping.

You may want to resize the images to 256x256 in advance. By default, we do not explicitly do this because in a cluster environment, one may benefit from resizing images in a parallel fashion, using mapreduce. For example, Yangqing used his lightweight [mincepie](https://github.com/Yangqing/mincepie) package. If you prefer things to be simpler, you can also use shell commands, something like:

    for name in /path/to/imagenet/val/*.JPEG; do
        convert -resize 256x256\! $name $name
    done

Take a look at `examples/imagenet/create_imagenet.sh`. Set the paths to the train and val dirs as needed, and set "RESIZE=true" to resize all images to 256x256 if you haven't resized the images in advance.
Now simply create the leveldbs with `examples/imagenet/create_imagenet.sh`. Note that `examples/imagenet/ilsvrc12_train_leveldb` and `examples/imagenet/ilsvrc12_val_leveldb` should not exist before this execution. It will be created by the script. `GLOG_logtostderr=1` simply dumps more information for you to inspect, and you can safely ignore it.

Compute Image Mean
------------------

The model requires us to subtract the image mean from each image, so we have to compute the mean. `tools/compute_image_mean.cpp` implements that - it is also a good example to familiarize yourself on how to manipulate the multiple components, such as protocol buffers, leveldbs, and logging, if you are not familiar with them. Anyway, the mean computation can be carried out as:

    ./examples/imagenet/make_imagenet_mean.sh

which will make `data/ilsvrc12/imagenet_mean.binaryproto`.

Model Definition
----------------

We are going to describe a reference implementation for the approach first proposed by Krizhevsky, Sutskever, and Hinton in their [NIPS 2012 paper](http://books.nips.cc/papers/files/nips25/NIPS2012_0534.pdf).

The network definition (`models/bvlc_reference_caffenet/train_val.prototxt`) follows the one in Krizhevsky et al.
Note that if you deviated from file paths suggested in this guide, you'll need to adjust the relevant paths in the `.prototxt` files.

If you look carefully at `models/bvlc_reference_caffenet/train_val.prototxt`, you will notice several `include` sections specifying either `phase: TRAIN` or `phase: TEST`. These sections allow us to define two closely related networks in one file: the network used for training and the network used for testing. These two networks are almost identical, sharing all layers except for those marked with `include { phase: TRAIN }` or `include { phase: TEST }`. In this case, only the input layers and one output layer are different.

**Input layer differences:** The training network's `data` input layer draws its data from `examples/imagenet/ilsvrc12_train_leveldb` and randomly mirrors the input image. The testing network's `data` layer takes data from `examples/imagenet/ilsvrc12_val_leveldb` and does not perform random mirroring.

**Output layer differences:** Both networks output the `softmax_loss` layer, which in training is used to compute the loss function and to initialize the backpropagation, while in validation this loss is simply reported. The testing network also has a second output layer, `accuracy`, which is used to report the accuracy on the test set. In the process of training, the test network will occasionally be instantiated and tested on the test set, producing lines like `Test score #0: xxx` and `Test score #1: xxx`. In this case score 0 is the accuracy (which will start around 1/1000 = 0.001 for an untrained network) and score 1 is the loss (which will start around 7 for an untrained network).

We will also lay out a protocol buffer for running the solver. Let's make a few plans:

* We will run in batches of 256, and run a total of 450,000 iterations (about 90 epochs).
* For every 1,000 iterations, we test the learned net on the validation data.
* We set the initial learning rate to 0.01, and decrease it every 100,000 iterations (about 20 epochs).
* Information will be displayed every 20 iterations.
* The network will be trained with momentum 0.9 and a weight decay of 0.0005.
* For every 10,000 iterations, we will take a snapshot of the current status.

Sound good? This is implemented in `models/bvlc_reference_caffenet/solver.prototxt`.

Training ImageNet
-----------------

Ready? Let's train.

    ./build/tools/caffe train --solver=models/bvlc_reference_caffenet/solver.prototxt

Sit back and enjoy!

On a K40 machine, every 20 iterations take about 26.5 seconds to run (while a on a K20 this takes 36 seconds), so effectively about 5.2 ms per image for the full forward-backward pass. About 2 ms of this is on forward, and the rest is backward. If you are interested in dissecting the computation time, you can run

    ./build/tools/caffe time --model=models/bvlc_reference_caffenet/train_val.prototxt

Resume Training?
----------------

We all experience times when the power goes out, or we feel like rewarding ourself a little by playing Battlefield (does anyone still remember Quake?). Since we are snapshotting intermediate results during training, we will be able to resume from snapshots. This can be done as easy as:

    ./build/tools/caffe train --solver=models/bvlc_reference_caffenet/solver.prototxt --snapshot=models/bvlc_reference_caffenet/caffenet_train_iter_10000.solverstate

where in the script `caffenet_train_iter_10000.solverstate` is the solver state snapshot that stores all necessary information to recover the exact solver state (including the parameters, momentum history, etc).

Parting Words
-------------

Hope you liked this recipe!
Many researchers have gone further since the ILSVRC 2012 challenge, changing the network architecture and/or fine-tuning the various parameters in the network to address new data and tasks.
**Caffe lets you explore different network choices more easily by simply writing different prototxt files** - isn't that exciting?

And since now you have a trained network, check out how to use it with the Python interface for [classifying ImageNet](http://nbviewer.ipython.org/github/BVLC/caffe/blob/master/examples/00-classification.ipynb).
---
title: LeNet MNIST Tutorial
description: Train and test "LeNet" on the MNIST handwritten digit data.
category: example
include_in_docs: true
priority: 1
---

# Training LeNet on MNIST with Caffe

We will assume that you have Caffe successfully compiled. If not, please refer to the [Installation page](/installation.html). In this tutorial, we will assume that your Caffe installation is located at `CAFFE_ROOT`.

## Prepare Datasets

You will first need to download and convert the data format from the MNIST website. To do this, simply run the following commands:

    cd $CAFFE_ROOT
    ./data/mnist/get_mnist.sh
    ./examples/mnist/create_mnist.sh

If it complains that `wget` or `gunzip` are not installed, you need to install them respectively. After running the script there should be two datasets, `mnist_train_lmdb`, and `mnist_test_lmdb`.

## LeNet: the MNIST Classification Model

Before we actually run the training program, let's explain what will happen. We will use the [LeNet](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) network, which is known to work well on digit classification tasks. We will use a slightly different version from the original LeNet implementation, replacing the sigmoid activations with Rectified Linear Unit (ReLU) activations for the neurons.

The design of LeNet contains the essence of CNNs that are still used in larger models such as the ones in ImageNet. In general, it consists of a convolutional layer followed by a pooling layer, another convolution layer followed by a pooling layer, and then two fully connected layers similar to the conventional multilayer perceptrons. We have defined the layers in `$CAFFE_ROOT/examples/mnist/lenet_train_test.prototxt`.

## Define the MNIST Network

This section explains the `lenet_train_test.prototxt` model definition that specifies the LeNet model for MNIST handwritten digit classification. We assume that you are familiar with [Google Protobuf](https://developers.google.com/protocol-buffers/docs/overview), and assume that you have read the protobuf definitions used by Caffe, which can be found at `$CAFFE_ROOT/src/caffe/proto/caffe.proto`.

Specifically, we will write a `caffe::NetParameter` (or in python, `caffe.proto.caffe_pb2.NetParameter`) protobuf. We will start by giving the network a name:

    name: "LeNet"

### Writing the Data Layer

Currently, we will read the MNIST data from the lmdb we created earlier in the demo. This is defined by a data layer:

    layer {
      name: "mnist"
      type: "Data"
      transform_param {
        scale: 0.00390625
      }
      data_param {
        source: "mnist_train_lmdb"
        backend: LMDB
        batch_size: 64
      }
      top: "data"
      top: "label"
    }

Specifically, this layer has name `mnist`, type `data`, and it reads the data from the given lmdb source. We will use a batch size of 64, and scale the incoming pixels so that they are in the range \[0,1\). Why 0.00390625? It is 1 divided by 256. And finally, this layer produces two blobs, one is the `data` blob, and one is the `label` blob.

### Writing the Convolution Layer

Let's define the first convolution layer:

    layer {
      name: "conv1"
      type: "Convolution"
      param { lr_mult: 1 }
      param { lr_mult: 2 }
      convolution_param {
        num_output: 20
        kernel_size: 5
        stride: 1
        weight_filler {
          type: "xavier"
        }
        bias_filler {
          type: "constant"
        }
      }
      bottom: "data"
      top: "conv1"
    }

This layer takes the `data` blob (it is provided by the data layer), and produces the `conv1` layer. It produces outputs of 20 channels, with the convolutional kernel size 5 and carried out with stride 1.

The fillers allow us to randomly initialize the value of the weights and bias. For the weight filler, we will use the `xavier` algorithm that automatically determines the scale of initialization based on the number of input and output neurons. For the bias filler, we will simply initialize it as constant, with the default filling value 0.

`lr_mult`s are the learning rate adjustments for the layer's learnable parameters. In this case, we will set the weight learning rate to be the same as the learning rate given by the solver during runtime, and the bias learning rate to be twice as large as that - this usually leads to better convergence rates.

### Writing the Pooling Layer

Phew. Pooling layers are actually much easier to define:

    layer {
      name: "pool1"
      type: "Pooling"
      pooling_param {
        kernel_size: 2
        stride: 2
        pool: MAX
      }
      bottom: "conv1"
      top: "pool1"
    }

This says we will perform max pooling with a pool kernel size 2 and a stride of 2 (so no overlapping between neighboring pooling regions).

Similarly, you can write up the second convolution and pooling layers. Check `$CAFFE_ROOT/examples/mnist/lenet_train_test.prototxt` for details.

### Writing the Fully Connected Layer

Writing a fully connected layer is also simple:

    layer {
      name: "ip1"
      type: "InnerProduct"
      param { lr_mult: 1 }
      param { lr_mult: 2 }
      inner_product_param {
        num_output: 500
        weight_filler {
          type: "xavier"
        }
        bias_filler {
          type: "constant"
        }
      }
      bottom: "pool2"
      top: "ip1"
    }

This defines a fully connected layer (known in Caffe as an `InnerProduct` layer) with 500 outputs. All other lines look familiar, right?

### Writing the ReLU Layer

A ReLU Layer is also simple:

    layer {
      name: "relu1"
      type: "ReLU"
      bottom: "ip1"
      top: "ip1"
    }

Since ReLU is an element-wise operation, we can do *in-place* operations to save some memory. This is achieved by simply giving the same name to the bottom and top blobs. Of course, do NOT use duplicated blob names for other layer types!

After the ReLU layer, we will write another innerproduct layer:

    layer {
      name: "ip2"
      type: "InnerProduct"
      param { lr_mult: 1 }
      param { lr_mult: 2 }
      inner_product_param {
        num_output: 10
        weight_filler {
          type: "xavier"
        }
        bias_filler {
          type: "constant"
        }
      }
      bottom: "ip1"
      top: "ip2"
    }

### Writing the Loss Layer

Finally, we will write the loss!

    layer {
      name: "loss"
      type: "SoftmaxWithLoss"
      bottom: "ip2"
      bottom: "label"
    }

The `softmax_loss` layer implements both the softmax and the multinomial logistic loss (that saves time and improves numerical stability). It takes two blobs, the first one being the prediction and the second one being the `label` provided by the data layer (remember it?). It does not produce any outputs - all it does is to compute the loss function value, report it when backpropagation starts, and initiates the gradient with respect to `ip2`. This is where all magic starts.


### Additional Notes: Writing Layer Rules

Layer definitions can include rules for whether and when they are included in the network definition, like the one below:

    layer {
      // ...layer definition...
      include: { phase: TRAIN }
    }

This is a rule, which controls layer inclusion in the network, based on current network's state.
You can refer to `$CAFFE_ROOT/src/caffe/proto/caffe.proto` for more information about layer rules and model schema.

In the above example, this layer will be included only in `TRAIN` phase.
If we change `TRAIN` with `TEST`, then this layer will be used only in test phase.
By default, that is without layer rules, a layer is always included in the network.
Thus, `lenet_train_test.prototxt` has two `DATA` layers defined (with different `batch_size`), one for the training phase and one for the testing phase.
Also, there is an `Accuracy` layer which is included only in `TEST` phase for reporting the model accuracy every 100 iteration, as defined in `lenet_solver.prototxt`.

## Define the MNIST Solver

Check out the comments explaining each line in the prototxt `$CAFFE_ROOT/examples/mnist/lenet_solver.prototxt`:

    # The train/test net protocol buffer definition
    net: "examples/mnist/lenet_train_test.prototxt"
    # test_iter specifies how many forward passes the test should carry out.
    # In the case of MNIST, we have test batch size 100 and 100 test iterations,
    # covering the full 10,000 testing images.
    test_iter: 100
    # Carry out testing every 500 training iterations.
    test_interval: 500
    # The base learning rate, momentum and the weight decay of the network.
    base_lr: 0.01
    momentum: 0.9
    weight_decay: 0.0005
    # The learning rate policy
    lr_policy: "inv"
    gamma: 0.0001
    power: 0.75
    # Display every 100 iterations
    display: 100
    # The maximum number of iterations
    max_iter: 10000
    # snapshot intermediate results
    snapshot: 5000
    snapshot_prefix: "examples/mnist/lenet"
    # solver mode: CPU or GPU
    solver_mode: GPU


## Training and Testing the Model

Training the model is simple after you have written the network definition protobuf and solver protobuf files. Simply run `train_lenet.sh`, or the following command directly:

    cd $CAFFE_ROOT
    ./examples/mnist/train_lenet.sh

`train_lenet.sh` is a simple script, but here is a quick explanation: the main tool for training is `caffe` with action `train` and the solver protobuf text file as its argument.

When you run the code, you will see a lot of messages flying by like this:

    I1203 net.cpp:66] Creating Layer conv1
    I1203 net.cpp:76] conv1 <- data
    I1203 net.cpp:101] conv1 -> conv1
    I1203 net.cpp:116] Top shape: 20 24 24
    I1203 net.cpp:127] conv1 needs backward computation.

These messages tell you the details about each layer, its connections and its output shape, which may be helpful in debugging. After the initialization, the training will start:

    I1203 net.cpp:142] Network initialization done.
    I1203 solver.cpp:36] Solver scaffolding done.
    I1203 solver.cpp:44] Solving LeNet

Based on the solver setting, we will print the training loss function every 100 iterations, and test the network every 500 iterations. You will see messages like this:

    I1203 solver.cpp:204] Iteration 100, lr = 0.00992565
    I1203 solver.cpp:66] Iteration 100, loss = 0.26044
    ...
    I1203 solver.cpp:84] Testing net
    I1203 solver.cpp:111] Test score #0: 0.9785
    I1203 solver.cpp:111] Test score #1: 0.0606671

For each training iteration, `lr` is the learning rate of that iteration, and `loss` is the training function. For the output of the testing phase, score 0 is the accuracy, and score 1 is the testing loss function.

And after a few minutes, you are done!

    I1203 solver.cpp:84] Testing net
    I1203 solver.cpp:111] Test score #0: 0.9897
    I1203 solver.cpp:111] Test score #1: 0.0324599
    I1203 solver.cpp:126] Snapshotting to lenet_iter_10000
    I1203 solver.cpp:133] Snapshotting solver state to lenet_iter_10000.solverstate
    I1203 solver.cpp:78] Optimization Done.

The final model, stored as a binary protobuf file, is stored at

    lenet_iter_10000

which you can deploy as a trained model in your application, if you are training on a real-world application dataset.

### Um... How about GPU training?

You just did! All the training was carried out on the GPU. In fact, if you would like to do training on CPU, you can simply change one line in `lenet_solver.prototxt`:

    # solver mode: CPU or GPU
    solver_mode: CPU

and you will be using CPU for training. Isn't that easy?

MNIST is a small dataset, so training with GPU does not really introduce too much benefit due to communication overheads. On larger datasets with more complex models, such as ImageNet, the computation speed difference will be more significant.

### How to reduce the learning rate at fixed steps?
Look at lenet_multistep_solver.prototxt
werkzeug
flask
tornado
numpy
pandas
pillow
pyyaml
---
title: Web demo
description: Image classification demo running as a Flask web server.
category: example
include_in_docs: true
priority: 10
---

# Web Demo

## Requirements

The demo server requires Python with some dependencies.
To make sure you have the dependencies, please run `pip install -r examples/web_demo/requirements.txt`, and also make sure that you've compiled the Python Caffe interface and that it is on your `PYTHONPATH` (see [installation instructions](/installation.html)).

Make sure that you have obtained the Reference CaffeNet Model and the ImageNet Auxiliary Data:

    ./scripts/download_model_binary.py models/bvlc_reference_caffenet
    ./data/ilsvrc12/get_ilsvrc_aux.sh

NOTE: if you run into trouble, try re-downloading the auxiliary files.

## Run

Running `python examples/web_demo/app.py` will bring up the demo server, accessible at `http://0.0.0.0:5000`.
You can enable debug mode of the web server, or switch to a different port:

    % python examples/web_demo/app.py -h
    Usage: app.py [options]

    Options:
      -h, --help            show this help message and exit
      -d, --debug           enable debug mode
      -p PORT, --port=PORT  which port to serve content on

## How are the "maximally accurate" results generated?

In a nutshell: ImageNet predictions are made at the leaf nodes, but the organization of the project allows leaf nodes to be united via more general parent nodes, with 'entity' at the very top.
To give "maximally accurate" results, we "back off" from maximally specific predictions to maintain a high accuracy.
The `bet_file` that is loaded in the demo provides the graph structure and names of all relevant ImageNet nodes as well as measures of information gain between them.
Please see the "Hedging your bets" paper from [CVPR 2012](http://www.image-net.org/projects/hedging/) for further information.
