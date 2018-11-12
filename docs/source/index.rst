..

Welcome to pyaaf2 Documentation!
===================================

A python module for the reading and writing Advanced Authoring Format (AAF) files.

About the AAF File Format
=========================

AAF is a file format use for professional multimedia creation and authoring.
The file specification is managed by the `Advanced Media Workflow Association
(AMWA) <https://www.amwa.tv/>`_.

AAF uses a object-oriented data model. The data model has a single inheritance
class hierarchy and classes have properties that store metadata.  Classes, properties,
and types uses 16-byte unique identifiers, known as Authoring Unique Identifiers (AUID).
AAF and MXF are closely related, the AAF data model is the basis for the MXF data model.

The Compound File Binary Format (CFBF) is what AAF uses for binary storage.  CFBF,
also called Structured Storage or Object Linking and Embedding (OLE), is a file format developed
by Microsoft for storing hierarchical data.  CFBF is basically a FAT32 filesystem
in a file and AAF uses "directories" as classes and "files" to store property metadata.

Further Reading
---------------

- `aafobjectspec-v1.1.pdf <https://sourceforge.net/p/aaf/code2/ci/master/tree/doc/aafobjectspec-v1.1.pdf?format=raw>`_
- `aafeditprotocol.pdf <https://sourceforge.net/p/aaf/code2/ci/master/tree/doc/aafeditprotocol.pdf?format=raw>`_
- `aafstoredformatspec-v1.0.1.pdf <https://sourceforge.net/p/aaf/code2/ci/master/tree/doc/aafstoredformatspec-v1.0.1.pdf?format=raw>`_
- `aafcontainerspec-v1.0.1.pdf <https://sourceforge.net/p/aaf/code2/ci/master/tree/doc/aafcontainerspec-v1.0.1.pdf?format=raw>`_
- `AAF SDK <http://aaf.sourceforge.net>`_
- `Media Authoring with Java API (MAJ) <https://github.com/AMWA-TV/maj>`_
- `Advanced Authoring Format Wikipedia <https://en.wikipedia.org/wiki/Advanced_Authoring_Format>`_
- `Compound File Binary Format Wikipedia <https://en.wikipedia.org/wiki/Compound_File_Binary_Format>`_
- `COM Structured Storage Wikipedia <https://en.wikipedia.org/wiki/COM_Structured_Storage>`_

Quick Start
===========

Reading Example
---------------

::

    import aaf2

    with aaf2.open("path/to/file.aaf", "r") as f:

        # get the main composition
        main_compostion = next(f.content.toplevel())

        # print the name of the composition
        print(main_compostion.name)

        # AAFObjects have properties that can be
        # accessed just like a dictionary
        print(main_compostion['CreationTime'].value)

        # video, audio and other track types are
        # stored in slots on a mob object.
        for slot in main_compostion.slots:
            segment = slot.segment
            print(segment)

Embedding Footage Example
-------------------------

First lets generate some DNxHR media with ffmpeg::

    ffmpeg -f lavfi -i testsrc=size=960x540 -frames:v 24 -vcodec dnxhd -pix_fmt yuv422p -profile:v dnxhr_lb sample.dnxhd

Now lets generate some audio media::

    ffmpeg -f lavfi -i aevalsrc="sin(420*2*PI*t):s=48000:d=1.0" -acodec pcm_s16le sample.wav

Finally import the footage::

    import aaf2

    with aaf2.open("example2.aaf", 'w') as f:

        # objects are create with a factory
        # on the AAFFile Object
        mob = f.create.MasterMob("Demo2")

        # add the mob to the file
        f.content.mobs.append(mob)

        edit_rate = 25

        # lets also create a tape so we can add timecode (optional)
        tape_mob = f.create.SourceMob()
        f.content.mobs.append(tape_mob)

        timecode_rate = 25
        start_time = timecode_rate * 60 * 60 # 1 hour
        tape_name = "Demo Tape"

        # add tape slots to tape mob
        tape_mob.create_tape_slots(tape_name, edit_rate,
                                   timecode_rate, media_kind='picture')

        # create sourceclip that references timecode
        tape_clip = tape_mob.create_source_clip(1, start_time)

        # now finally import the generated media
        mob.import_dnxhd_essence("sample.dnxhd", edit_rate, tape_clip)
        mob.import_audio_essence("sample.wav", edit_rate)

API Reference
=============

.. toctree::
   :maxdepth: 5
   :caption: Contents:

   api/aaf2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
