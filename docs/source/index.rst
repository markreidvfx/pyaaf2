..

Welcome to PyAAF's documentation!
=================================

Python module for the reading and writing Advanced Authoring Format (AAF) files.

Basic Demo
----------

::

    import aaf2

    f = aaf2.open("path/to/file.aaf", "r")

    # get the main composition
    main_compostion = next(f.content.toplevel())

    # print the name of the composition
    print(main_compostion.name)

    # AAFObjects have properties that can be accessed like a dictionary
    # print out the creation time
    print(main_compostion['CreationTime'].value)

    # video, audio and other track types are stored in slots
    # on a mob object.
    for slot in main_compostion.slots:
        segment = slot.segment
        print(segment)


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
